from __future__ import annotations

import pandas as pd

from pathlib import Path
from typing import Final

from src.ab_test_segment_analysis_functions import analyze_comparison

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

HIGH_NO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_offers_segment" / "high_spender_no_offer_customers.csv"
HIGH_DISCOUNT_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_offers_segment" / "high_spender_discount_offer_customers.csv"
HIGH_BOGO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "high_spender_offers_segment" / "high_spender_bogo_offer_customers.csv"

LOW_NO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "low_spender_offers_segment" / "low_spender_no_offer_customers.csv"
LOW_DISCOUNT_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "low_spender_offers_segment" / "low_spender_discount_offer_customers.csv"
LOW_BOGO_OFFER_PATH: Final[Path] = PROJECT_ROOT / "data" / "processed" / "low_spender_offers_segment" / "low_spender_bogo_offer_customers.csv"

OUTPUT_PATH: Final[Path] = PROJECT_ROOT / "outputs" / "tables" / "high_spender_and_low_spender_ab_test_analysis_summary.csv"

def load_data (input_path: Path) -> pd.DataFrame:

    if not input_path.exists():
        raise FileNotFoundError(f'{input_path} does not exist')

    return pd.read_csv(input_path)

def save_data(df: pd.DataFrame, output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def main() -> None:

    high_spender_no_offer = load_data(HIGH_NO_OFFER_PATH)
    high_spender_discount_offer = load_data(HIGH_DISCOUNT_OFFER_PATH)
    high_spender_bogo_offer = load_data(HIGH_BOGO_OFFER_PATH)

    low_spender_no_offer = load_data(LOW_NO_OFFER_PATH)
    low_spender_discount_offer = load_data(LOW_DISCOUNT_OFFER_PATH)
    low_spender_bogo_offer = load_data(LOW_BOGO_OFFER_PATH)

    results = [
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
            },
            treatment_name="Discount",
            no_offer_df=high_spender_no_offer,
            treatment_df=high_spender_discount_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "High Spender",
            },
            treatment_name="BOGO",
            no_offer_df=high_spender_no_offer,
            treatment_df=high_spender_bogo_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "Low Spender",
            },
            treatment_name="Discount",
            no_offer_df=low_spender_no_offer,
            treatment_df=low_spender_discount_offer,
        ),
        analyze_comparison(
            segment_info={
                "spender_segment": "Low Spender",
            },
            treatment_name="BOGO",
            no_offer_df=low_spender_no_offer,
            treatment_df=low_spender_bogo_offer,
        ),
    ]

    results_df = pd.DataFrame(results)
    save_data(results_df, OUTPUT_PATH)

if __name__ == "__main__":
    main()

