from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, ValidationError


class inputSchema(BaseModel):

    Survive: str
    Gender: str
    Smoke: str
    Diabetes: str
    Age: int
    Ejection_Fraction: str  # renamed
    Sodium: int
    Creatinine: float
    Pletelets: int
    CK: int  # renamed
    BP: int  # renamed
    Hemoglobin: float
    Height: int
    Weight: int
    BMI: float  # new feature


class multiple_inputSchema(BaseModel):
    inputs: List[inputSchema]


def api_input_validation(input_data: pd.DataFrame) -> [pd.DataFrame, Optional[dict]]:
    try:
        multiple_inputSchema(inputs=input_data)

    except ValidationError as error:
        errors = error.json()

    return input_data, errors
