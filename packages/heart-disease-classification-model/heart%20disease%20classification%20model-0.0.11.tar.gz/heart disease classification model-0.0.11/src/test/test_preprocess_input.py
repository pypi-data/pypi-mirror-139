"""tests preprocess input from preprocessing datamanager function."""
import numpy as np
import pandas as pd

from src.config.settings import SAMPLE_DATA_PATH, config
from src.preprocessing.datamanager import preprocess_data, preprocess_input

sample_data = pd.read_csv(SAMPLE_DATA_PATH)
sample_data = sample_data.iloc[:,1:]
processed_sample_data = preprocess_data(sample_data)

sample_input = [
    "Male",
    "Yes",
    "Normal",
    21,
    "Low",
    120,
    0.2,
    266000,
    100,
    105,
    16.3,
    185,
    80,
    23.374726077428782,
]


def test_preprocess_input():
    """
    Test if the processed input has the correct cols, data types, shape.

    :return: None
    """
    processed_inputs = preprocess_input(sample_input)
    assert processed_inputs.columns.to_list() == config.modelConfig.total_features
    assert processed_inputs.shape[1] == len(config.modelConfig.total_features)
    for feature in config.modelConfig.cat_features:
        assert processed_inputs[feature].dtypes is np.dtype(object)

    for feature in config.modelConfig.total_num_features:
        assert processed_inputs[feature].dtypes is float or int
