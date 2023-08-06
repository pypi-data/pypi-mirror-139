"""Tests the predict api function in predict.py whether if it generates a prediction that is in
lined with expectations"""
import numpy as np
import pandas as pd

from src.model.predict import make_prediction_inputs_api_dict

sample_input = {
    "ID": "TIG1GE",
    "Gender": "Male",
    "Smoke": "Yes",
    "Diabetes": "Normal",
    "Age": 50,
    "Ejection Fraction": "Low",
    "Sodium": 141,
    "Creatinine": 0.7,
    "Pletelets": 266000,
    "Creatinine phosphokinase": 185,
    "Blood Pressure": 105,
    "Hemoglobin": 12.3,
    "Height": 180,
    "Weight": 93,
    "Favorite color": "Green",
}


def test_predict_api_dict():

    print("Entering test predict api dict")

    results = make_prediction_inputs_api_dict(sample_input)
    results_proba = make_prediction_inputs_api_dict(sample_input, True)

    print(results.items())
    print(results_proba.items())

    assert results["Errors"] is None
    assert len(results["Prediction"]) == 1
    assert type(results["Prediction"]) == np.ndarray
    assert type(results["Version"]) == str

    assert results_proba["Errors"] is None
    assert len(results_proba["Prediction"][0]) == 2
    assert type(results_proba["Prediction"]) == np.ndarray
    assert type(results_proba["Version"]) == str
