import datetime
import os
from pathlib import Path

# TODO (nikhil): This entire servicefoundry path needs to be changed to MLF folder
SERVICE_FOUNDRY_FOLDER = Path(os.path.abspath("./servicefoundry"))
RUN_TMP_FOLDER = Path(
    os.path.join(SERVICE_FOUNDRY_FOLDER, "logdirs")
)  # this is the log directory

RUN_PREDICTIONS_FOLDER = Path(
    os.path.join(RUN_TMP_FOLDER, "predictions")
)  # path to store predictions
RUN_DATASET_FOLDER = Path(
    os.path.join(RUN_TMP_FOLDER, "datasets")
)  # path to store datasets
# path to store dataset stats
RUN_STATS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, "stats"))
RUN_METRICS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, "metrics"))

GET_RUN_TMP_FOLDER = Path(
    os.path.join(SERVICE_FOUNDRY_FOLDER, "getdirs")
)  # this is the log directory
GET_RUN_PREDICTIONS_FOLDER = Path(
    os.path.join(GET_RUN_TMP_FOLDER, "predictions")
)  # path to store predictions
GET_RUN_DATASET_FOLDER = Path(
    os.path.join(GET_RUN_TMP_FOLDER, "datasets")
)  # path to store datasets
GET_RUN_WEBAPP_FOLDER = Path(
    os.path.join(GET_RUN_TMP_FOLDER, "webapp")
)  # path to store datasets

TIME_LIMIT_THRESHOLD = datetime.timedelta(minutes=1)
FILE_SIZE_LIMIT_THRESHOLD = pow(10, 7)  # 10MB

MLFLOW_HOST = "http://localhost:5000"


MULTI_DIMENSIONAL_METRICS = "multi_dimensional_metrics"  # multi dimensional metrics
NON_MULTI_DIMENSIONAL_METRICS = (
    "non_multi_dimensional_metrics"  # non-multi dimensional metrics
)
PROB_MULTI_DIMENSIONAL_METRICS = (
    "prob_multi_dimensional_metrics"  # multi dimensional metrics
)
PROB_NON_MULTI_DIMENSIONAL_METRICS = (
    "prob_non_multi_dimensional_metrics"  # non-multi dimensional metrics
)


ACTUAL_PREDICTION_COUNTS = "actuals_predictions_counts"
MLF_FOLDER_NAME = "mlf"
MLRUNS_FOLDER = "mlruns"
MLRUNS_FOLDER_NAME = Path(os.path.join(MLF_FOLDER_NAME, MLRUNS_FOLDER))


# Runs Name and DF constants
RUN_ID_COL_NAME = "run_id"
RUN_NAME_COL_NAME = "run_name"
RUN_NAME_PREFIX = "run"

TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


GIT_COMMIT_TAG_NAME = "mlfoundry.git.commit_sha"
GIT_BRANCH_TAG_NAME = "mlfoundry.git.branch_name"
GIT_REMOTE_URL_NAME = "mlfoundry.git.remote_url"
GIT_DIRTY_TAG_NAME = "mlfoundry.git.dirty"
PATCH_FILE_ARTIFACT_DIR = "mlfoundry/git"
# without .txt patch file does not load on UI
PATCH_FILE_NAME = "uncommitted_changes.patch.txt"
