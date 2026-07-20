from fastapi import APIRouter

from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.validation import validate_required_columns

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/test")
def test_sales_route():
    return {
        "message": "Sales routes are connected",
        "next_step": "CSV upload endpoint"
    }


@router.post("/upload")
async def upload_sales_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Only CSV files are supported."
            },
        )

    contents = await file.read()

    try:
        df = pd.read_csv(BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Uploaded file could not be read as a CSV."
            },
        )

    received_columns = list(df.columns)
    validation_result = validate_required_columns(received_columns)

    if not validation_result["is_valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Uploaded CSV is missing required columns.",
                "missing_columns": validation_result["missing_columns"],
                "extra_columns": validation_result["extra_columns"],
            },
        )

    return {
        "filename": file.filename,
        "rows_received": len(df),
        "columns_received": len(df.columns),
        "columns": received_columns,
        "validation": validation_result,
    }
