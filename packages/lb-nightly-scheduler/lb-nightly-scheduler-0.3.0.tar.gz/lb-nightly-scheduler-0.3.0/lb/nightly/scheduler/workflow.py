###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
import logging
import os
from tempfile import TemporaryFile

import luigi
from lb.nightly.configuration import DataProject
from lb.nightly.db import connect
from lb.nightly.utils import make_slot_deployment_dir, trigger_deployment

from ._types import ArtifactTarget, DeploymentTarget, ProjectParameter, SlotParameter

logger = logging.getLogger("luigi-interface")


class Checkout(luigi.Task):
    project = ProjectParameter()

    def output(self):
        return ArtifactTarget(self.project, stage="checkout")

    def run(self):
        from lb.nightly.rpc import checkout

        out = self.output()
        with out.acquire_lock():
            if out.artifact_ready():
                if not out.summary_ready():
                    # if we are here it means that artifact is present, but the summary
                    # is not available in the database
                    db = connect()
                    summary = db.get_artifact_summary(
                        self.project.artifacts("checkout")
                    )

                    if summary:

                        def update_summary(doc):
                            if "checkout" not in doc:
                                doc["checkout"] = {}
                            if "projects" not in doc["checkout"]:
                                doc["checkout"]["projects"] = {}
                            doc["checkout"]["projects"][self.project.name] = summary
                            for project in doc["config"]["projects"]:
                                if project["name"] == self.project.name:
                                    project["dependencies"] = summary["dependencies"]
                                    break

                        db = connect()
                        db.apply(update_summary, db[self.project.slot])

            else:
                checkout(
                    self.project.id(),
                )

        assert out.artifact_ready(), f"problem with {self.project.id()} checkout"


class DeploySources(luigi.Task):
    project = ProjectParameter()

    def output(self):
        return DeploymentTarget(self.project, stage="checkout")

    def requires(self):
        return Checkout(project=self.project)

    def run(self):
        install_id = trigger_deployment(self.project)
        logger.info(
            f"Triggered deployment of sources for {self.project.id()}. See the status on: https://lhcb-core-tasks.web.cern.ch/tasks/status/{install_id}"
        )
        self.output().wait_for_deployment()


class DeployDataProject(luigi.WrapperTask):
    project = ProjectParameter()

    def requires(self):
        for package in self.project.packages:
            yield DeploySources(project=package)


class Build(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return ArtifactTarget(self.project, stage="build", platform=self.platform)

    def requires(self):
        return Checkout(project=self.project)

    def run(self):
        out = self.output()
        with out.acquire_lock():
            # at this point we should be able to get the dependencies from
            # CouchDB
            from ._types import _get

            slot = _get(self.project.slot.id())
            for dep in slot.projects[self.project.name].dependencies():
                if dep in slot.projects and self.project.slot.projects[dep].enabled:
                    if isinstance(self.project.slot.projects[dep], DataProject):
                        yield DeployDataProject(project=self.project.slot.projects[dep])
                    else:
                        yield DeployBinaries(
                            project=self.project.slot.projects[dep],
                            platform=self.platform,
                        )

            if out.artifact_ready():
                if not out.summary_ready():
                    # if we are here it means that artifact is present, but the summary
                    # is not available in the database
                    db = connect()
                    summary = db.get_artifact_summary(
                        self.project.artifacts(self.project.name, self.platform)
                    )

                    if summary:

                        def update_summary(doc):
                            if "builds" not in doc:
                                doc["builds"] = {}
                            if self.platform not in doc["builds"]:
                                doc["builds"][self.platform] = {}
                            doc["builds"][self.platform][self.project.name] = summary

                        db = connect()
                        db.apply(update_summary, db[self.project.slot])
            else:
                from lb.nightly.rpc import build

                build(
                    self.project.id(),
                    self.platform,
                )

        assert (
            out.artifact_ready()
        ), f"problem with {self.project.id()} build for {self.platform}"


class DeployBinaries(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return DeploymentTarget(self.project, stage="build", platform=self.platform)

    def requires(self):
        return Build(project=self.project, platform=self.platform)

    def run(self):
        install_id = trigger_deployment(self.project, self.platform)
        logger.info(
            f"Triggered deployment of binaries for {self.project.id()} and {self.platform}. See the status on: https://lhcb-core-tasks.web.cern.ch/tasks/status/{install_id}"
        )
        self.output().wait_for_deployment()


class Test(luigi.Task):
    project = ProjectParameter()
    platform = luigi.Parameter()

    def output(self):
        return ArtifactTarget(self.project, stage="test", platform=self.platform)

    def requires(self):
        return (
            Checkout(project=self.project),
            Build(project=self.project, platform=self.platform),
        )

    def run(self):
        from lb.nightly.rpc import test

        test(
            self.project.id(),
            self.platform,
        )


class DeploymentDir(luigi.Task):
    slot = SlotParameter()

    def output(self):
        return DeploymentTarget(self.slot, stage="deployment_dir")

    def run(self):
        out = self.output()

        if not out.repo.exist(out.artifact_name):
            with TemporaryFile() as tmpfile:
                make_slot_deployment_dir(self.slot, tmpfile)
                assert out.repo.push(
                    tmpfile, out.artifact_name
                ), "failed to upload artifacts"

            install_id = trigger_deployment(self.slot)
            logger.info(
                f"Triggered deployment of deployment directory for {self.slot.id()}. See the status on: https://lhcb-core-tasks.web.cern.ch/tasks/status/{install_id}"
            )

        out.wait_for_deployment()


class Slot(luigi.WrapperTask):
    slot = SlotParameter()

    def requires(self):
        def update_scheduler_task_id(doc):
            doc["scheduler_task_id"] = self.task_id

        db = connect()
        db.apply(update_scheduler_task_id, db[self.slot])

        yield DeploymentDir(slot=self.slot)

        for project in self.slot.activeProjects:
            if isinstance(project, DataProject):
                yield DeployDataProject(project=project)
            else:
                yield DeploySources(project=project)
                for platform in self.slot.platforms:
                    if not project.platform_independent:
                        yield DeployBinaries(project=project, platform=platform)
                        if not (self.slot.no_test or project.no_test):
                            yield Test(project=project, platform=platform)


class SlotList(luigi.Task):
    slots = luigi.ListParameter(
        default=[],
        description="Name of the slots to start, leave empty to run all enabled ones",
    )
    flavour = luigi.ChoiceParameter(
        choices=["nightly", "testing", "release"], default="nightly"
    )
    config_repository = luigi.Parameter(
        default="https://gitlab.cern.ch/lhcb-core/LHCbNightlyConf.git"
    )
    config_version = luigi.Parameter(default="master")

    def output(self):
        return luigi.LocalTarget("meta/slots_to_run.json")

    def run(self):
        from subprocess import check_call
        from tempfile import TemporaryDirectory

        from git import Repo

        # if 1:
        #     tmp = "/home/marco/Devel/workspace/lb-nightly-scheduler/tmp"
        with TemporaryDirectory() as tmp:
            if not os.path.exists(os.path.join(tmp, "configs")):
                Repo.clone_from(
                    self.config_repository,
                    os.path.join(tmp, "configs"),
                    branch=self.config_version,
                )
            cmd = [
                "lbn-enabled-slots",
                # "--debug",
                # "--submit",
                # "--resolve-mrs",
                f"--flavour={self.flavour}",
                "--output={name}.params.txt",
            ]
            if self.slots:
                cmd.append("--slots={}".format(" ".join(self.slots)))
            check_call(cmd, cwd=tmp)
            required = []
            for paramfile in [f for f in os.listdir(tmp) if f.endswith(".params.txt")]:
                params = dict(
                    l.strip().split("=", 1) for l in open(os.path.join(tmp, paramfile))
                )
                try:
                    required.append(
                        f"{self.flavour}/{params['slot']}.{int(params['slot_build_id'])-1}"
                    )
                except KeyError:
                    pass
            with self.output().open("w") as out:
                json.dump(required[:2], out, indent=2)


class Main(luigi.Task):
    slots = luigi.ListParameter(
        default=[],
        description="Name of the slots to start, leave empty to run all enabled ones",
    )
    flavour = luigi.ChoiceParameter(
        choices=["nightly", "testing", "release"], default="nightly"
    )
    config_repository = luigi.Parameter(
        default="https://gitlab.cern.ch/lhcb-core/LHCbNightlyConf.git"
    )
    config_version = luigi.Parameter(default="master")

    def requires(self):
        return SlotList(
            slots=self.slots,
            flavour=self.flavour,
            config_repository=self.config_repository,
            config_version=self.config_version,
        )

    def output(self):
        return luigi.LocalTarget("dummy")

    def run(self):
        from ._types import _getSlot

        yield [Slot(_getSlot(slot)) for slot in json.load(self.input().open("r"))]
