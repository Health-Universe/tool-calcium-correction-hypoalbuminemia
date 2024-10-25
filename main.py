"""FastAPI application for calculating Corrected Calcium in Hypoalbuminemia with Normal Albumin field."""
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Corrected Ca - Hypoalbuminemia Tool",
    description="API for calculating corrected calcium levels in patients with hypoalbuminemia. Allows customization of the normal albumin value.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalciumCorrectionInput(BaseModel):
    """Form-based input schema for calculating Corrected Calcium."""

    measured_calcium: float = Field(
        title="Measured Total Calcium (mg/dL)",
        ge=4.0,
        le=14.0,
        examples=[9.5],
        description="Enter the measured total calcium level in mg/dL. Typical range: 4.0 - 14.0 mg/dL.",
    )
    serum_albumin: float = Field(
        title="Serum Albumin (g/dL)",
        ge=2.0,
        le=5.5,
        examples=[3.5],
        description="Enter the serum albumin level in g/dL. Typical range: 2.0 - 5.5 g/dL.",
    )
    normal_albumin: float = Field(
        title="Normal Albumin (g/dL)",
        ge=3.0,
        le=5.0,
        default=4.0,
        examples=[4.0],
        description="Enter the normal albumin level in g/dL used for correction. Default is 4.0 g/dL.",
    )


class CalciumCorrectionOutput(BaseModel):
    """Form-based output schema for Corrected Calcium."""

    corrected_calcium: float = Field(
        title="Corrected Calcium (mg/dL)",
        examples=[10.1],
        description="Your calculated Corrected Calcium level in mg/dL.",
    )


@app.post(
    "/calculate",
    description="Calculate Corrected Calcium based on Measured Total Calcium, Serum Albumin, and Normal Albumin.",
    response_model=CalciumCorrectionOutput,
)
async def calculate_corrected_calcium(
    data: Annotated[CalciumCorrectionInput, Form()],
) -> CalciumCorrectionOutput:
    """Calculate Corrected Calcium for Hypoalbuminemia.

    Args:
        data (CalciumCorrectionInput): The input data containing measured calcium, serum albumin, and normal albumin levels.

    Returns:
        CalciumCorrectionOutput: The calculated Corrected Calcium level.
    """
    # Calculate Corrected Calcium using the formula:
    # Corrected Calcium = Measured Calcium + 0.8 * (Normal Albumin - Serum Albumin)
    corrected_calcium = data.measured_calcium + 0.8 * (data.normal_albumin - data.serum_albumin)

    corrected_calcium = round(corrected_calcium, 1)

    return CalciumCorrectionOutput(corrected_calcium=corrected_calcium)
