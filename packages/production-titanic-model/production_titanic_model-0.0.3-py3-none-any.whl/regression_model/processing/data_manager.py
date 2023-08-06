import joblib
import pandas as pd

from regression_model import __version__ as _version
from regression_model.config.core import TRAINED_MODEL_DIR


def load_dataset(url_path: str) -> pd.DataFrame:
    df = pd.read_csv(url_path)
    return df


def save_model(model) -> None:

    # Prepare versioned save file name
    save_file_name = f"model_{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    joblib.dump(model, save_path)


def load_model(file_name):
    return joblib.load(file_name)
