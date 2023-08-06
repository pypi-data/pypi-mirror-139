"""[summary]
"""
import json
import os
from typing import TYPE_CHECKING, Any, Dict
from unittest.mock import DEFAULT  # noqa TYP001

import azureml
from azureml.core import Experiment, Run

from energinetml.azure.datasets import (
    DownloadedAzureMLDataStore,
    MountedAzureMLDataStore,
)
from energinetml.azure.logger import AzureMlLogger
from energinetml.core.logger import ConsoleLogger
from energinetml.core.training import AbstractTrainingContext
from energinetml.settings import DEFAULT_RELATIVE_ARTIFACT_PATH

if TYPE_CHECKING:
    from energinetml.azure.backend import AzureBackend
    from energinetml.core.model import Model, TrainedModel


class AzureLocalTrainingContext(AbstractTrainingContext):
    """[summary]"""

    def __init__(self, backend: "AzureBackend", force_download: bool):
        """[summary]

        Args:
            backend (AzureBackend): [description]
            force_download (bool): [description]
        """
        self.backend = backend
        self.force_download = force_download
        self.az_run = None

    def train_model(
        self, model: "Model", tags: Dict[str, Any], **kwargs
    ) -> "TrainedModel":
        """[summary]

        Args:
            model (Model): [description]
            tags (Dict[str, Any]): [description]

        Raises:
            AbstractBackend.BackendException: [description]
            AbstractBackend.BackendException: [description]

        Returns:
            TrainedModel: [description]
        """
        az_workspace = self.backend.get_workspace(
            name=model.project.workspace_name,
            subscription_id=model.project.subscription_id,
            resource_group=model.project.resource_group,
        )

        az_experiment = Experiment(workspace=az_workspace, name=model.experiment)

        datasets = DownloadedAzureMLDataStore.from_model(
            model=model,
            datasets=model.datasets_parsed.local,
            workspace=az_workspace,
            force_download=self.force_download,
        )

        with model.temporary_folder() as temp_path:
            # The "outputs" parameter is provided here with a non-existing
            # folder path to avoid having azureml upload files. We will do
            # this manually somewhere else.

            try:
                self.az_run = az_experiment.start_logging(
                    snapshot_directory=temp_path,
                    outputs=os.path.join(temp_path, "a-folder-that-does-not-exists"),
                )
            except azureml._common.exceptions.AzureMLException as ex:
                raise self.backend.parse_azureml_exception(ex)

            self.az_run.set_tags(tags)
            try:
                return model.train(
                    datasets=datasets, logger=AzureMlLogger(self.az_run), **kwargs
                )
            finally:
                try:
                    self.az_run.complete()
                except azureml._common.exceptions.AzureMLException as ex:
                    raise self.backend.parse_azureml_exception(ex)

    def save_artifacts(self, model: "Model"):
        """[summary]

        Args:
            model (Model): [description]

        Raises:
            AbstractBackend.BackendException: [description]
        """
        try:
            self.az_run.upload_folder(
                DEFAULT_RELATIVE_ARTIFACT_PATH, model.artifact_path
            )
        except azureml._common.exceptions.AzureMLException as ex:
            raise self.backend.parse_azureml_exception(ex)

    def save_meta_data(self, meta_data: dict, meta_file_path):
        """Create a meta.json file with the name of the module

        Args:
            file_path (_type_): _description_
            folder_name (_type_): _description_
        """
        json_object = json.dumps(meta_data, indent=4)
        with open(meta_file_path, "w") as outfile:
            outfile.write(json_object)

    def save_log_file(self, clog: ConsoleLogger) -> None:
        """This function takes the log file generated from clog and
        pushes the log into the azure ml expiremnt tab called output.

        Args:
            clog (ConsoleLogger): This argument is an object of our logger function

        Raises:
            AbstractBackend.BackendException: [description]
        """
        try:
            clog.flush()
            self.az_run.upload_file(clog.filename, clog.filepath)
        except azureml._common.exceptions.AzureMLException as ex:
            raise self.backend.parse_azureml_exception(ex)

    def save_logs(self, *cloggers):
        try:
            for clogger in cloggers:
                clogger.flush()
                self.az_run.upload_file(clogger.filename, clogger.filepath)
        except azureml._common.exceptions.AzureMLException as ex:
            raise self.backend.parse_azureml_exception(ex)

    def get_portal_url(self) -> str:
        """[summary]

        Raises:
            AbstractBackend.BackendException: [description]

        Returns:
            str: [description]
        """
        try:
            return self.az_run.get_portal_url()
        except azureml._common.exceptions.AzureMLException as ex:
            raise self.backend.parse_azureml_exception(ex)

    def get_parameters(self, model: "Model") -> Dict:
        """[summary]

        Args:
            model (Model): [description]

        Returns:
            Dict: [description]
        """
        params = {}
        params.update(model.parameters)
        params.update(model.parameters_local)
        return params

    def get_tags(self, model: "Model") -> Dict:
        """[summary]

        Args:
            model (Model): [description]

        Returns:
            Dict: [description]
        """
        return {"datasets": ", ".join(model.datasets + model.datasets_local)}


class AzureCloudTrainingContext(AbstractTrainingContext):
    """[summary]"""

    def __init__(self):
        self.az_run = None

    def train_model(
        self, model: "Model", tags: Dict[str, Any], **kwargs
    ) -> "TrainedModel":
        """[summary]

        Args:
            model (Model): [description]
            tags (Dict[str, Any]): [description]

        Returns:
            TrainedModel: [description]
        """
        self.az_run = Run.get_context(allow_offline=False)
        self.az_run.set_tags(tags)

        datasets = MountedAzureMLDataStore.from_model(
            model=model,
            datasets=model.datasets_parsed.cloud,
            workspace=self.az_run.experiment.workspace,
        )

        try:
            return model.train(
                datasets=datasets, logger=AzureMlLogger(self.az_run), **kwargs
            )
        finally:
            self.az_run.complete()

    def get_portal_url(self) -> str:
        """[summary]

        Returns:
            str: [description]
        """
        return self.az_run.get_portal_url()

    def get_parameters(self, model: "Model") -> Dict:
        """[summary]

        Args:
            model (Model): [description]

        Returns:
            Dict: [description]
        """
        params = {}
        params.update(model.parameters)
        params.update(model.parameters_cloud)
        return params

    def get_tags(self, model: "Model") -> Dict:
        """[summary]

        Args:
            model (Model): [description]

        Returns:
            Dict: [description]
        """
        return {"datasets": ", ".join(model.datasets + model.datasets_cloud)}

    def save_log_file(self, clog: ConsoleLogger) -> None:
        """This function takes the log file generated from clog and
        pushes the log into the azure ml expiremnt tab called output.

        Args:
            clog (ConsoleLogger): This argument is an object of our logger function.

        Raises:
            AbstractBackend.BackendException: [description]
        """
        try:
            clog.flush()
            self.az_run.upload_file(clog.filename, clog.filepath)
        except azureml._common.exceptions.AzureMLException as ex:
            raise self.backend.parse_azureml_exception(ex)
