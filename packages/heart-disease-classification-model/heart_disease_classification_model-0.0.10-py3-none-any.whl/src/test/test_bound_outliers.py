"""test the bound outliers function."""
import pandas as pd

from src.config.settings import SAMPLE_DATA_PATH, config
from src.preprocessing.datamanager import bound_outliers, preprocess_data

sample_data = pd.read_csv(SAMPLE_DATA_PATH)
processed_sample_data = preprocess_data(sample_data)


def test_bound_outliers():
    """
    Test if the outliers have been cap to the min or max.

    :return: None
    """
    arbitary_value = 1
    for col in config.modelConfig.original_num_features:
        ori_min = processed_sample_data[col].min()
        ori_max = processed_sample_data[col].max()

        bound_outliers(processed_sample_data, col)

        current_min = processed_sample_data[col].min()
        current_max = processed_sample_data[col].max()

        assert ori_min - arbitary_value <= current_min
        assert ori_max + arbitary_value >= current_max
