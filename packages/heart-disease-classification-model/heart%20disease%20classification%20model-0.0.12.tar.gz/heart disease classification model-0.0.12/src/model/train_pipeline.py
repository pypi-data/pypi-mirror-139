"""Contains functions regarding training of pipeline."""

from time import time

import joblib
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GridSearchCV, cross_validate, train_test_split

from src.config.settings import (
    DATABASE_PATH,
    LOG_OUTPUT_PATH,
    PARAMS,
    PIPELINE_PATH,
    config,
)
from src.model.pipeline import survive_pipe_rfc
from src.preprocessing import datamanager


def run_trainpipeline(gridsearch=False):
    """
    Trains then saves the pipeline and outputs training log with scoring metrics.Allows gridsearch to be done.

    :param gridsearch: Bol True to run gridsearch on pipeline
    :return: None
    """
    print("Entering run_trainpipeline function")
    df = datamanager.load_from_database(DATABASE_PATH)

    print("Entering split dataset")
    X_train, X_test, y_train, y_test = train_test_split(
        df[config.modelConfig.total_features],
        df[config.modelConfig.target],
        test_size=config.modelConfig.test_size,
        random_state=config.modelConfig.random_state,
    )

    if gridsearch:
        print("Gridsearch = True")
        try:
            model = GridSearchCV(survive_pipe_rfc, PARAMS, cv=config.modelConfig.cv)
            score_pipeline(model, X_train, y_train, X_test, y_test)
            joblib.dump(model, PIPELINE_PATH)
        except Exception:
            raise Exception("Unable to proceed, please check Parameters")

        joblib.dump(model, PIPELINE_PATH)
    else:
        print("Gridsearch = False")
        survive_pipe_rfc.fit(X_train, y_train)
        score_pipeline(survive_pipe_rfc, X_train, y_train, X_test, y_test)
        joblib.dump(survive_pipe_rfc, PIPELINE_PATH)


def score_pipeline(model, X_train, y_train, X_test, y_test):
    """
    Scores the pipeline  with F1, recall, precision, ROC-AUC and outputs.

    :param model: pipeline
    :param X_train: X Training set
    :param y_train: Y Training set
    :param X_test: X test set
    :param y_test: Y test set
    :return: None
    """
    now = time()
    y_pred = model.predict(X_test)

    model_cv_score = cross_validate(
        model,
        X_train,
        y_train,
        cv=config.modelConfig.cv,
        n_jobs=-1,
        return_train_score=True,
        scoring="accuracy",
    )
    then = time()
    diff = then - now
    output_logfile(model, model_cv_score, y_test, y_pred, diff)


def output_logfile(model, model_cv_score, y_test, y_pred, diff):
    """
    Ouput the training log on a output file with scoring metrics to LOG_OUTPUT_PATH.

    :param model: pipeline
    :param model_cv_score: Cross validation score
    :param y_test: y test set
    :param y_pred: prediction for y_test for scoring
    :param diff: How long it took the model to run
    :return:
    """
    with open(LOG_OUTPUT_PATH, "w") as log_file:
        log_file.write("Log file for model results\n")
        log_file.write("Model is " + config.modelConfig.model_name + "\n")
        log_file.write(
            f"Classifcation report :\n{classification_report(y_test, y_pred)}" + "\n"
        )
        log_file.write(
            f'Average CV train acc score : \n {model_cv_score["train_score"].mean()} '
            + "\n"
        )
        log_file.write(
            f'Average CV test acc score : \n {model_cv_score["test_score"].mean()} '
            + "\n"
        )
        log_file.write(f"ROC AUC score :\n {roc_auc_score(y_test, y_pred)}" + "\n")
        log_file.write(f"Seconds taken to run results is {diff}")


if __name__ == "__main__":
    run_trainpipeline()
