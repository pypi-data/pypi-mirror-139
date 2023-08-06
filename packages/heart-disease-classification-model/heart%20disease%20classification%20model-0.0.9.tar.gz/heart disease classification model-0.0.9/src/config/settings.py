"""Contains all of the constant variables used."""
import os
from pathlib import Path
from typing import List

from pydantic import BaseModel
from strictyaml import YAML, load

# main folders
CONFIG_PATH = os.path.dirname(__file__)  # aiap/src/config
SRC_ROOT = Path(CONFIG_PATH).parent  # aiap/src
ROOT = Path(SRC_ROOT).parent  # aiap

DATA_PATH = os.path.join(SRC_ROOT, "data")  # aiap/data
MODEL_PATH = os.path.join(SRC_ROOT, "model")  # aiap/src/model
PREPROCESSING_PATH = os.path.join(SRC_ROOT, "preprocessing")  # aiap/src/preprocessing
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, "config.yml")  # aiap/src/configconfig.yml

# Objects
DATABASE_PATH = os.path.join(DATA_PATH, "survive.db")  # aiap/data/survive.db
SAMPLE_DATA_PATH = os.path.join(DATA_PATH, "sample_df.csv")  # data/sample_df.csv
PIPELINE_NAME = "pipeline.pkl"
PIPELINE_PATH = os.path.join(MODEL_PATH, PIPELINE_NAME)  # aiap/src/model/pipeline.pkl
LOG_OUTPUT_NAME = "log_file.txt"
LOG_OUTPUT_PATH = os.path.join(
    MODEL_PATH, LOG_OUTPUT_NAME
)  # aiap/src/model/log_file.txt

# model specific objects
PARAMS = {}  # insert params configuration here


class AppConfig(BaseModel):
    """
    Application-level config
    """

    package_name: str
    pipeline_save_file: str
    model_version: str


class ModelConfig(BaseModel):
    """
    Model-level config
    """

    # features....
    target: str
    features: List[str]
    original_features: List[str]
    renamed_features: List[str]
    cat_features: List[str]
    original_num_features: List[str]
    total_features: list[str]
    total_num_features: list[str]
    total_features_with_target: List[str]

    # model...
    model_name: str
    test_size: float
    random_state: int
    cv: int
    random_state: int
    model_name: str


class StreamlitConfig(BaseModel):
    age: int
    sodium: int
    creatinine: float
    pletelets: int
    ck: int
    bp: int
    hemo: float
    height: int
    weight: int


class mainConfig(BaseModel):
    appConfig: AppConfig
    modelConfig: ModelConfig
    streamlitConfig: StreamlitConfig


def locate_config_file() -> Path:
    """
    locates the config.yml file. If its missing will raise an error
    :return: Path - Path of the config file
    """
    if Path(CONFIG_FILE_PATH).is_file():
        return CONFIG_FILE_PATH
    else:
        raise Exception(f"Config file is not found at {CONFIG_FILE_PATH}")


def load_config(cfg_path: Path = None) -> YAML:
    """
    Loads the config from the default path unless specified
    :param cfg_path: Path object that specifies path of config.yml file
    :return: YAML file
    """
    # default file
    if cfg_path is None:
        cfg_path = locate_config_file()

    # custom config.yml file specified
    if cfg_path:
        try:
            with open(cfg_path, "r") as f:
                parsed_config = load(f.read())
                return parsed_config
        except OSError:
            raise OSError(
                f"Did not manage to find the config.yml file specified at {cfg_path}"
            )


def create_and_validate_config(parsed_config: YAML = None) -> mainConfig:
    """
    using the YAML file it will instantiate a config file
    :param parsed_config: YAML file from config.yml
    :return: mainConfig object
    """
    if parsed_config is None:
        parsed_config = load_config()

    _config = mainConfig(
        appConfig=AppConfig(**parsed_config.data),
        modelConfig=ModelConfig(**parsed_config.data),
        streamlitConfig=StreamlitConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
