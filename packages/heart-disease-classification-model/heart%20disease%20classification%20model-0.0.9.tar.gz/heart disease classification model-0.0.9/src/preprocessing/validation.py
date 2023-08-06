from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, ValidationError


class inputSchema(BaseModel):

    # Survive: str
    Gender: Optional[str]
    Smoke: Optional[str]
    Diabetes: Optional[str]
    Age: Optional[int]
    Ejection_Fraction: Optional[str]  # renamed
    Sodium: Optional[int]
    Creatinine: Optional[float]
    Pletelets: Optional[int]
    CK: Optional[int]  # renamed
    BP: Optional[int]  # renamed
    Hemoglobin: Optional[float]
    Height: Optional[int]
    Weight: Optional[int]
    BMI: Optional[float]  # new feature


class multiple_inputSchema(BaseModel):
    inputs: List[inputSchema]


def api_input_validation(input_data: pd.DataFrame) -> [pd.DataFrame, Optional[dict]]:
    print('Entering api input validation')

    errors = None

    input_data_copy = input_data.copy()

    print(input_data_copy.to_dict(orient="records"))

    try:
        multiple_inputSchema(inputs=input_data_copy.to_dict(orient="records"))

    except ValidationError as error:
        errors = error.json()

    return input_data, errors
