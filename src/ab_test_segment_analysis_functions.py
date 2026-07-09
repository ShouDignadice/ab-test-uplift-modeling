from __future__ import annotations

import math
import pandas as pd

from pathlib import Path
from typing import Final

SIGNIFICANCE_LEVEL: Final[float] = 0.05

def normal_cdf(z_score: float) -> float:

    return (1 + math.erf(z_score / math.sqrt(2))) / 2

def run_two_proportion_z_test(
        control_converted: int,
        control_total: int,
        treatment_converted: int,
        treatment_total: int,) -> tuple[float, float]:

    control_rate = control_converted / control_total
    treatment_rate = treatment_converted / treatment_total

    pooled_rate = (control_converted + treatment_converted) / (control_total + treatment_total)

    standard_error = math.sqrt(pooled_rate * (1 - pooled_rate) * ((1 / control_total) + (1 / treatment_total)))


    z_score = (treatment_rate - control_rate) / standard_error
    p_value = 2 * (1 - normal_cdf(abs(z_score)))

    return z_score, p_value

def analyze_comparison(
        segment_info: dict[str, str],
        treatment_name: str,
        no_offer_df: pd.DataFrame,
        treatment_df: pd.DataFrame,
        control_name: str = "No Offer") -> dict[str, int | float | str]:

    no_offer_total, no_offer_converted, no_offer_rate = calculate_conversion_stats(no_offer_df)
    treatment_total, treatment_converted, treatment_rate = calculate_conversion_stats(treatment_df)

    absolute_lift = treatment_rate - no_offer_rate
    relative_lift = absolute_lift / no_offer_rate

    z_score, p_value = run_two_proportion_z_test(
        control_converted=no_offer_converted,
        control_total=no_offer_total,
        treatment_converted=treatment_converted,
        treatment_total=treatment_total,
    )

    if p_value < SIGNIFICANCE_LEVEL and absolute_lift > 0:
        decision = "Statistically significant positive lift"

    elif p_value < SIGNIFICANCE_LEVEL and absolute_lift < 0:
        decision = "Statistically significant negative lift"

    else:
        decision = "No statistically significant lift"

    return {
        **segment_info,
        "comparison": f"{treatment_name} vs {control_name}",
        "control_group": control_name,
        "treatment_group": treatment_name,
        "control_total_customers": no_offer_total,
        "control_converted_customers": no_offer_converted,
        "control_conversion_rate": round(no_offer_rate * 100, 2),
        "treatment_total_customers": treatment_total,
        "treatment_converted_customers": treatment_converted,
        "treatment_conversion_rate": round(treatment_rate * 100, 2),
        "absolute_lift": round(absolute_lift * 100, 2),
        "relative_lift": round(relative_lift * 100, 2),
        "z_score": round(z_score, 4),
        "p_value": round(p_value, 4),
        "decision": decision,
    }

def calculate_conversion_stats(df: pd.DataFrame) -> tuple[int, int, float]:

    total_customers = len(df)
    converted_customers = int(df["conversion"].sum())

    conversion_rate = converted_customers / total_customers

    return total_customers, converted_customers, conversion_rate