import pandas as pd


def build_upload_summary(cleaned_df: pd.DataFrame) -> dict:
    sold_lots = int((cleaned_df["sale_status"] == "sold").sum())
    unsold_lots = int((cleaned_df["sale_status"] == "unsold").sum())

    rows_with_result_price = int(cleaned_df["result_price"].notna().sum())
    rows_with_auction_date = int(cleaned_df["auction_date"].notna().sum())

    average_result_price = cleaned_df["result_price"].mean()

    return {
        "total_rows": int(len(cleaned_df)),
        "sold_lots": sold_lots,
        "unsold_lots": unsold_lots,
        "rows_with_result_price": rows_with_result_price,
        "rows_with_auction_date": rows_with_auction_date,
        "average_result_price": (
            round(float(average_result_price), 2)
            if pd.notna(average_result_price)
            else None
        ),
    }