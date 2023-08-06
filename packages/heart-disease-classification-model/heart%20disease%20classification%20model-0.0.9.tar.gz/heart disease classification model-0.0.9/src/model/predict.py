"""Contains function to return prediction of input."""
from src.config.settings import PIPELINE_PATH, config
from src.preprocessing import datamanager, validation


def make_prediction_inputs(input_data: list, proba=False) -> int:
    """
    Load pipeline and preprocess input then predict.

    Parameters
    ----------
    input_data: List
        Input data from streamlit application, expects 1 row of observation
    proba: Bol
        True if return probability instead
    Returns
    -------
    Int | Float
        Int: If proba is not set to True. Returns class of survival. 0 for no, 1 for yes
        Float: If proba is set to True, the probability of survival [0,1]
    """
    survive_pipeline = datamanager.load_pipeline(PIPELINE_PATH)
    processed_input = datamanager.preprocess_input(input_data)

    if proba:
        prediction_proba = survive_pipeline.predict_proba(processed_input)
        return prediction_proba
    else:
        prediction = survive_pipeline.predict(processed_input)
        return prediction


def make_prediction_inputs_api(input_data: list, proba=False) -> dict:
    """
    Load pipeline and preprocess input from API then predict.
    The inputs will be similar to what is in the original training set with
    original features

    Parameters
    ----------
    input_data: List
        Input data from API
    proba: Bol
        True if return probability instead
    Returns
    -------
    Int | Float
        Int: If proba is not set to True. Returns class of survival. 0 for no, 1 for yes
        Float: If proba is set to True, the probability of survival [0,1]
    """
    survive_pipeline = datamanager.load_pipeline(PIPELINE_PATH)
    processed_input = datamanager.preprocess_data_fromapi(input_data)

    validated_input, errors = validation.api_input_validation(processed_input)

    results = {
        "Prediction": None,
        "Version": config.appConfig.model_version,
        "Errors": errors,
    }

    if errors is None:
        if proba:
            prediction_proba = survive_pipeline.predict_proba(validated_input)
            results["Prediction"] = prediction_proba
        else:
            prediction = survive_pipeline.predict(validated_input)
            results["Prediction"] = prediction

    return results
