from __future__ import annotations

import pandas as pd

from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

INPUT_PATH: Final[Path] = PROJECT_ROOT / "data" / "raw" / "data.csv"
PROCESSED_DIR: Final[Path] = PROJECT_ROOT / "data" / "processed"

def make_output_path(folder_name: str, file_name: str) -> Path:

    return PROCESSED_DIR / folder_name / f"{file_name}.csv"

def load_data(input_path: Path) -> pd.DataFrame:

    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} does not exist")

    return pd.read_csv(input_path)

def filter_spender_segments(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    median_spending = df["history"].median()

    high_spenders = df[df["history"] > median_spending].copy()
    low_spenders = df[df["history"] < median_spending].copy()

    return high_spenders, low_spenders

def filter_customer_offer(df: pd.DataFrame) -> dict[str, pd.DataFrame]:

    offer_segments = {
        "no_offer": df[df["offer"] == "No Offer"].copy(),
        "discount_offer": df[df["offer"] == "Discount"].copy(),
        "bogo_offer": df[df["offer"] == "Buy One Get One"].copy()
    }

    return offer_segments

def filter_zip_code_segments(df: pd.DataFrame) -> dict[str, pd.DataFrame]:

    zip_code_segments = {
        "rural": df[df["zip_code"] == "Rural"].copy(),
        "urban": df[df["zip_code"] == "Urban"].copy(),
        "suburban": df[df["zip_code"] == "Surburban"].copy()
    }

    return zip_code_segments

def save_data(df: pd.DataFrame, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def main() -> None:

    customer_data = load_data(INPUT_PATH)
    high_spenders, low_spenders = filter_spender_segments(customer_data)

    low_spender_offer_segments = filter_customer_offer(low_spenders)
    high_spender_offer_segments = filter_customer_offer(high_spenders)

    for offer_name, offer_df in high_spender_offer_segments.items():
        save_data(offer_df, make_output_path("high_spender_offers_segment", f"high_spender_{offer_name}_customers"))

    for offer_name, offer_df in low_spender_offer_segments.items():
        save_data(offer_df, make_output_path("low_spender_offers_segment", f"low_spender_{offer_name}_customers"))

    low_spender_no_offer_zip_code_segments = filter_zip_code_segments(low_spender_offer_segments["no_offer"])
    low_spender_bogo_offer_zip_code_segments = filter_zip_code_segments(low_spender_offer_segments["bogo_offer"])
    low_spender_discount_offer_zip_code_segments = filter_zip_code_segments(low_spender_offer_segments["discount_offer"])

    for zip_code_name, zip_code_df in low_spender_no_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"low_spender_{zip_code_name}_customers",f"low_spender_{zip_code_name}_no_offer_customers"))

    for zip_code_name, zip_code_df in low_spender_bogo_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"low_spender_{zip_code_name}_customers",f"low_spender_{zip_code_name}_bogo_offer_customers"))

    for zip_code_name, zip_code_df in low_spender_discount_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"low_spender_{zip_code_name}_customers",f"low_spender_{zip_code_name}_discount_offer_customers"))

    high_spender_no_offer_zip_code_segments = filter_zip_code_segments(high_spender_offer_segments["no_offer"])
    high_spender_bogo_offer_zip_code_segments = filter_zip_code_segments(high_spender_offer_segments["bogo_offer"])
    high_spender_discount_offer_zip_code_segments = filter_zip_code_segments(high_spender_offer_segments["discount_offer"])

    for zip_code_name, zip_code_df in high_spender_no_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"high_spender_{zip_code_name}_customers",f"high_spender_{zip_code_name}_no_offer_customers"))

    for zip_code_name, zip_code_df in high_spender_bogo_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"high_spender_{zip_code_name}_customers",f"high_spender_{zip_code_name}_bogo_offer_customers"))

    for zip_code_name, zip_code_df in high_spender_discount_offer_zip_code_segments.items():
        save_data(zip_code_df, make_output_path(f"high_spender_{zip_code_name}_customers", f"high_spender_{zip_code_name}_discount_offer_customers"))

if __name__ == "__main__":
    main()