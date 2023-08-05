import argparse
import os
import tempfile
import typing
from collections.abc import Mapping

import mlflow

from mlfoundry.exceptions import MlflowException, MlFoundryException


def download_artifact(mlflow_client, run_id, artifact_name, dest_path):
    try:
        return mlflow_client.download_artifacts(run_id, artifact_name, dest_path)
    except MlflowException as e:
        raise MlFoundryException(e.message).with_traceback(e.__traceback__) from None


ParamsType = typing.Union[typing.Mapping[str, typing.Any], argparse.Namespace]


def process_params(params: ParamsType) -> typing.Dict[str, typing.Any]:
    if isinstance(params, Mapping):
        return params
    if isinstance(params, argparse.Namespace):
        return vars(params)
    # TODO: add absl support if required
    # move to a different file then
    raise MlFoundryException(
        "params should be either argparse.Namespace or a Mapping (dict) type"
    )


def log_artifact_blob(
    mlflow_client: mlflow.tracking.MlflowClient,
    run_id: str,
    blob: typing.Union[str, bytes],
    file_name: str,
    artifact_path: typing.Optional[str] = None,
):
    with tempfile.TemporaryDirectory(prefix=run_id) as tmpdirname:
        local_path = os.path.join(tmpdirname, file_name)
        mode = "wb" if isinstance(blob, bytes) else "w"
        with open(local_path, mode) as local_file:
            local_file.write(blob)
        mlflow_client.log_artifact(run_id, local_path, artifact_path=artifact_path)
