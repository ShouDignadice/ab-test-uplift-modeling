from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

HIGH_SPENDER_SUMMARY_PATH: Final[Path] = PROJECT_ROOT / "outputs" / "tables" / "high_spender_zip_ab_test_analysis_summary.csv"
LOW_SPENDER_SUMMARY_PATH: Final[Path] = PROJECT_ROOT / "outputs" / "tables" / "low_spender_zip_ab_test_analysis_summary.csv"

OUTPUT_DIR: Final[Path] = PROJECT_ROOT / "outputs" / "figures"

CONVERSION_RATE_OUTPUT_PATH: Final[Path] = OUTPUT_DIR / "zip_segment_conversion_rates.png"
ABSOLUTE_LIFT_OUTPUT_PATH: Final[Path] = OUTPUT_DIR / "zip_segment_absolute_lift.png"

def load_data(input_path: Path) -> pd.DataFrame:

    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} does not exist")

    return pd.read_csv(input_path)

def save_plot(output_path: Path) -> None:

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

def add_segment_label(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df["segment_label"] = df["spender_segment"] + " - " + df["zip_code_segment"]

    return df

def plot_conversion_rates(df: pd.DataFrame) -> None:

    control_conversion_rates = (
        df.drop_duplicates(subset=["segment_label"])
        .set_index("segment_label")["control_conversion_rate"]
        .rename("No Offer")
    )

    treatment_conversion_rates = df.pivot_table(
        index="segment_label",
        columns="treatment_group",
        values="treatment_conversion_rate",
    )

    conversion_rate_summary = pd.concat(
        [control_conversion_rates, treatment_conversion_rates],
        axis=1,
    )

    conversion_rate_summary = conversion_rate_summary[["No Offer", "BOGO", "Discount"]]

    ax = conversion_rate_summary.plot(
        kind="bar",
        figsize=(12, 6),
    )

    ax.set_title("Conversion Rate by Customer Segment and Offer")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Conversion Rate (%)")
    ax.legend(title="Offer Type")

    plt.xticks(rotation=30, ha="right")

    save_plot(CONVERSION_RATE_OUTPUT_PATH)

def plot_absolute_lift(df: pd.DataFrame) -> None:

    absolute_lift_summary = df.pivot_table(
        index="segment_label",
        columns="treatment_group",
        values="absolute_lift",
    )

    absolute_lift_summary = absolute_lift_summary[["BOGO", "Discount"]]

    ax = absolute_lift_summary.plot(
        kind="bar",
        figsize=(12, 6),
    )

    ax.set_title("Absolute Lift by Customer Segment and Offer")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Absolute Lift (Percentage Points)")
    ax.axhline(0, linewidth=0.8)
    ax.legend(title="Offer Type")

    plt.xticks(rotation=30, ha="right")

    save_plot(ABSOLUTE_LIFT_OUTPUT_PATH)

def main() -> None:

    high_spender_summary = load_data(HIGH_SPENDER_SUMMARY_PATH)
    low_spender_summary = load_data(LOW_SPENDER_SUMMARY_PATH)

    combined_summary = pd.concat(
        [high_spender_summary, low_spender_summary],
        ignore_index=True,
    )

    combined_summary = add_segment_label(combined_summary)

    plot_conversion_rates(combined_summary)
    plot_absolute_lift(combined_summary)

if __name__ == "__main__":
    main()