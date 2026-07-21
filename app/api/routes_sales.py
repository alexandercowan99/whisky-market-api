from fastapi import APIRouter

from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from typing import Literal

from app.db.database import get_db
from app.db.repository import get_auction_lots, get_sales_summary, insert_auction_lots, get_top_auction_lots, get_auction_house_summary, get_monthly_sales_summary
from app.services.validation import validate_required_columns
from app.services.cleaning import add_cleaned_columns
from app.services.analytics import build_upload_summary
from app.api.serializers import serialize_auction_lot
from app.api.schemas import AuctionLotsResponse

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/test")
def test_sales_route():
    return {
        "message": "Sales routes are connected",
        "next_step": "CSV upload endpoint"
    }

@router.get("/summary")
def sales_summary(db: Session = Depends(get_db)):
    return get_sales_summary(db)


@router.get("/top-lots", response_model=AuctionLotsResponse)
def top_sales_lots(limit: int = Query(default=10, ge=1, le=50),db: Session = Depends(get_db),):

    auction_lots = get_top_auction_lots(db, limit=limit)

    lots_response = [
        serialize_auction_lot(lot)
        for lot in auction_lots
    ]

    return {
        "count": len(lots_response),
        "lots": lots_response,
    }

@router.post("/upload")
async def upload_sales_file(file: UploadFile = File(...), db: Session = Depends(get_db),):
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

    cleaned_df = add_cleaned_columns(df)
    upload_summary = build_upload_summary(cleaned_df)
    rows_inserted = insert_auction_lots(db, cleaned_df)

    cleaned_preview = cleaned_df[
        [
            "Auction_Name",
            "Auction_Date_String",
            "auction_date",
            "Lot_Title",
            "Lot_Result_String",
            "result_price",
            "result_currency",
            "sale_status",
            "Lot_Estimate_String",
            "estimate_low",
            "estimate_high",
            "estimate_currency",
            "size_ml",
            "quantity",
        ]
    ].head(5).to_dict(orient="records")

    return {
        "filename": file.filename,
        "rows_received": len(df),
        "columns_received": len(df.columns),
        "columns": received_columns,
        "validation": validation_result,
        "upload_summary": upload_summary,
        "rows_inserted": rows_inserted,
        "cleaned_preview": cleaned_preview,
    }

@router.get("/lots", response_model=AuctionLotsResponse)
def list_sales_lots(limit: int = Query(default=100, ge=1, le=500), 
                    sale_status: Literal["sold", "unsold", "unknown"] | None = None, 
                    auction_name: str | None = None,
                    lot_category: str | None = None,
                    min_price: int = Query(default=None, ge=0),
                    max_price: int = Query(default=None, ge=0),
                    db: Session = Depends(get_db)):        
    
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail={"message": "min_price cannot be greater than max_price."},
        )

    auction_lots = get_auction_lots(db, limit=limit, sale_status = sale_status, auction_name=auction_name,
                                    lot_category=lot_category,min_price=min_price,max_price=max_price)

    lots_response = [
        serialize_auction_lot(lot)
        for lot in auction_lots
    ]

    return {
        "count": len(lots_response),
        "lots": lots_response,
    }

@router.get("/auction-houses")
def auction_house_summary(db: Session = Depends(get_db)):
    auction_houses = get_auction_house_summary(db)

    return {
        "count": len(auction_houses),
        "auction_houses": auction_houses,
    }

@router.get("/monthly-summary")
def monthly_sales_summary(db: Session = Depends(get_db)):
    monthly_summary = get_monthly_sales_summary(db)

    return {
        "count": len(monthly_summary),
        "monthly_summary": monthly_summary,
    }