"""Contains pipelines to transform input."""
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config.settings import config

num_pipe = Pipeline(
    [("num_impute_median", SimpleImputer(strategy="median")), ("ss", StandardScaler())]
)

cat_pipe = Pipeline([("ohe", OneHotEncoder(drop="first"))])

transform_pipe = ColumnTransformer(
    [
        ("num_transform", num_pipe, config.modelConfig.total_num_features),
        ("cat_transform", cat_pipe, config.modelConfig.cat_features),
    ]
)

survive_pipe_rfc = Pipeline(
    [
        ("transform", transform_pipe),
        ("rfc", RandomForestClassifier(random_state=config.modelConfig.random_state)),
    ]
)
