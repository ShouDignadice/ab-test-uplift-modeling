from __future__ import annotations

import pandas as pd

from pathlib import Path
from typing import Final

from src.ab_test_segment_analysis_functions import analyze_comparison

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

HIGH_SPENDER_RURAL_BOGO_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_rural_customers" / "high_spender_rural_bogo_offer_customers.csv"
HIGH_SPENDER_RURAL_DISCOUNT_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_rural_customers" / "high_spender_rural_discount_offer_customers.csv"
HIGH_SPENDER_RURAL_NO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_rural_customers" / "high_spender_rural_no_offer_customers.csv"

HIGH_SPENDER_SUBURBAN_BOGO_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_suburban_customers" / "high_spender_suburban_bogo_offer_customers.csv"
HIGH_SPENDER_SUBURBAN_DISCOUNT_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_suburban_customers" / "high_spender_suburban_discount_offer_customers.csv"
HIGH_SPENDER_SUBURBAN_NO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_suburban_customers" / "high_spender_suburban_no_offer_customers.csv"

HIGH_SPENDER_URBAN_BOGO_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_urban_customers" / "high_spender_urban_bogo_offer_customers.csv"
HIGH_SPENDER_URBAN_DISCOUNT_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_urban_customers" / "high_spender_urban_discount_offer_customers.csv"
HIGH_SPENDER_URBAN_NO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_urban_customers" / "high_spender_urban_no_offer_customers.csv"

OUTPUT_PATH_HIGH_SPENDER_ZIP_SEGMENTS: Final[Path] = PROJECT_ROOT / "outputs" / "tables" / "high_spender_zip_ab_test_analysis_summary.csv"


def load_data (input_path: Path) -> pd.DataFrame:

    if not input_path.exists():
        raise FileNotFoundError(f'{input_path} does not exist')

    return pd.read_csv(input_path)

def save_data(df: pd.DataFrame, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def main() -> None:

    high_spender_rural_bogo_offer = load_data(HIGH_SPENDER_RURAL_BOGO_PATH)
    high_spender_rural_discount_offer =  load_data(HIGH_SPENDER_RURAL_DISCOUNT_PATH)
    high_spender_rural_no_offer = load_data(HIGH_SPENDER_RURAL_NO_OFFER_PATH)

    results_rural = [
        analyze_comparison(
            segment_info={
            "spender_segment": "High Spender",
            "zip_code_segment": "Rural",
            },
            treatment_name="BOGO",
            no_offer_df=high_spender_rural_no_offer,
            treatment_df=high_spender_rural_bogo_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
                "zip_code_segment": "Rural",
            },
            treatment_name="Discount",
            no_offer_df=high_spender_rural_no_offer,
            treatment_df=high_spender_rural_discount_offer,
        )
    ]

    high_spender_suburban_bogo_offer = load_data(HIGH_SPENDER_SUBURBAN_BOGO_PATH)
    high_spender_suburban_discount_offer = load_data(HIGH_SPENDER_SUBURBAN_DISCOUNT_PATH)
    high_spender_suburban_no_offer = load_data(HIGH_SPENDER_SUBURBAN_NO_OFFER_PATH)

    results_suburban = [
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
                "zip_code_segment": "Suburban",
            },
            treatment_name="BOGO",
            no_offer_df=high_spender_suburban_no_offer,
            treatment_df=high_spender_suburban_bogo_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
                "zip_code_segment": "Suburban",
            },
            treatment_name="Discount",
            no_offer_df=high_spender_suburban_no_offer,
            treatment_df=high_spender_suburban_discount_offer,
        )
    ]

    high_spender_urban_bogo_offer = load_data(HIGH_SPENDER_URBAN_BOGO_PATH)
    high_spender_urban_discount_offer = load_data(HIGH_SPENDER_URBAN_DISCOUNT_PATH)
    high_spender_urban_no_offer = load_data(HIGH_SPENDER_URBAN_NO_OFFER_PATH)

    results_urban = [
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
                "zip_code_segment": "Urban",
            },
            treatment_name="BOGO",
            no_offer_df=high_spender_urban_no_offer,
            treatment_df=high_spender_urban_bogo_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
                "zip_code_segment": "Urban",
            },
            treatment_name="Discount",
            no_offer_df=high_spender_urban_no_offer,
            treatment_df=high_spender_urban_discount_offer,
        )
    ]

    all_results = results_rural + results_suburban + results_urban

    all_results_df = pd.DataFrame(all_results)
    save_data(all_results_df, OUTPUT_PATH_HIGH_SPENDER_ZIP_SEGMENTS)

if __name__ == "__main__":
    main()