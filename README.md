# A/B Test & Uplift Modeling

This project analyzes a public synthetic marketing promotion dataset to understand how different CRM campaign offers impact customer conversion. The goal is to go beyond basic campaign performance and eventually identify which customers should receive an offer, which customers do not need one, and which customers may respond negatively.

## Project Goals

* Perform a deep-dive A/B test analysis comparing:

  * No Offer vs Discount
  * No Offer vs BOGO

* Analyze customer segments such as:

  * High spenders vs low spenders
  * Channel: Web, Phone, and Multi-channel customers
  * Zip code type: Urban, Suburban, and Rural customers

* Estimate incremental lift to understand whether each offer created additional conversions compared to no offer.

* Build an uplift modeling workflow to classify customers into groups such as:

  * Persuadables: customers who need a small nudge to convert
  * Sure Things: customers likely to convert without an offer
  * Lost Causes: customers unlikely to convert even with an offer
  * Sleeping Dogs: customers who may respond negatively to receiving an offer

## Business Question

Should the promotion be sent to everyone, or only to selected customers?

## Current Phase

The current phase focuses on A/B test analysis and customer segmentation. Instead of treating the campaign as one A/B/C test, each offer is compared separately against the control group:

* No Offer vs BOGO
* No Offer vs Discount

This makes the analysis easier to interpret and keeps each treatment comparison focused.

After the overall A/B test, the analysis segments customers into High Spenders and Low Spenders to understand whether campaign performance differs by historical customer value.

## A/B Test Results

| Test                 | No Offer Conversion Rate | Treatment Conversion Rate | Absolute Lift | Relative Lift | Result                    |
| -------------------- | -----------------------: | ------------------------: | ------------: | ------------: | ------------------------- |
| BOGO vs No Offer     |                   10.62% |                    15.14% |         4.52% |        42.61% | Statistically significant |
| Discount vs No Offer |                   10.62% |                    18.28% |         7.66% |        72.14% | Statistically significant |

## Key Findings

Both promotional offers outperformed No Offer.

BOGO increased conversion from **10.62% to 15.14%**, producing a **4.52 percentage point lift** and a **42.61% relative lift**.

Discount increased conversion from **10.62% to 18.28%**, producing a **7.66 percentage point lift** and a **72.14% relative lift**.

Based on conversion lift alone, **Discount was the stronger offer**. It outperformed BOGO by approximately **3.14 percentage points** in conversion rate.

## High Spender vs Low Spender Segment Analysis

Customers were segmented using the `history` column as a proxy for customer value. The `history` column represents the dollar value of historical purchases.

In the current analysis:

* **High Spenders** are customers with `history` greater than the median historical purchase value.
* **Low Spenders** are customers with `history` less than the median historical purchase value.

Customers exactly equal to the median were excluded from this version of the segment analysis because the segmentation logic used `>` for High Spenders and `<` for Low Spenders.

### Spender Segment Distribution

| Segment      | Definition         | Customers | Customer Share |
| ------------ | ------------------ | --------: | -------------: |
| High Spender | `history > median` |    31,999 |         50.00% |
| Low Spender  | `history < median` |    31,999 |         50.00% |

This median-based segmentation creates two nearly equal-sized customer groups, making it easier to compare campaign performance between higher-value and lower-value customers.

### Segment A/B Test Results

| Segment      | Test                 | No Offer Conversion Rate | Treatment Conversion Rate | Absolute Lift | Relative Lift | Z-Score | P-Value | Result                                  |
| ------------ | -------------------- | -----------------------: | ------------------------: | ------------: | ------------: | ------: | ------: | --------------------------------------- |
| High Spender | No Offer vs Discount |                   12.83% |                    21.19% |         8.36% |        65.14% |   16.20 |    0.00 | Statistically significant positive lift |
| High Spender | No Offer vs BOGO     |                   12.83% |                    17.27% |         4.43% |        34.56% |    9.06 |    0.00 | Statistically significant positive lift |
| Low Spender  | No Offer vs Discount |                    8.43% |                    15.38% |         6.95% |        82.50% |   15.71 |    0.00 | Statistically significant positive lift |
| Low Spender  | No Offer vs BOGO     |                    8.43% |                    12.98% |         4.55% |        53.95% |   10.74 |    0.00 | Statistically significant positive lift |

The p-values are displayed as **0.00** because they were rounded to two decimal places. This does not mean the p-values are literally zero; it means they are extremely small after rounding.

### Segment Key Findings

Discount produced the strongest conversion lift in both customer value segments.

For **High Spenders**, Discount increased conversion from **12.83% to 21.19%**, producing an **8.36 percentage point lift** and a **65.14% relative lift**.

For **Low Spenders**, Discount increased conversion from **8.43% to 15.38%**, producing a **6.95 percentage point lift** and an **82.50% relative lift**.

BOGO also improved conversion in both segments, but the lift was smaller than Discount.

For **High Spenders**, BOGO increased conversion from **12.83% to 17.27%**, producing a **4.43 percentage point lift** and a **34.56% relative lift**.

For **Low Spenders**, BOGO increased conversion from **8.43% to 12.98%**, producing a **4.55 percentage point lift** and a **53.95% relative lift**.

Another important finding is that **High Spenders had a higher No Offer conversion rate than Low Spenders**. High Spenders converted at **12.83%** without an offer, while Low Spenders converted at **8.43%** without an offer. This suggests that High Spenders are more likely to convert naturally, even without receiving a promotion.

Overall, the segment analysis shows:

* Discount was the strongest offer for both High Spenders and Low Spenders.
* High Spenders had higher baseline conversion without an offer.
* Low Spenders had lower baseline conversion, but showed strong relative lift from Discount.
* BOGO created positive lift in both segments, but did not outperform Discount.

These findings support a targeted CRM strategy instead of sending the same promotion to every customer.

## Business Interpretation

The results show that both BOGO and Discount were effective at increasing customer conversion compared to No Offer. However, a higher conversion rate does not automatically mean the promotion should be sent to every customer.

A full rollout may create unnecessary promotion costs by sending offers to customers who would have converted anyway. This is especially important because High Spenders already showed a stronger baseline conversion rate without any offer.

Discount produced the strongest overall conversion lift and was effective for both High Spenders and Low Spenders. Low Spenders had a lower natural conversion rate, but they responded strongly to Discount in relative lift terms. This suggests that Discount may be useful for customers who need a stronger incentive to convert.

These findings suggest that the business should move toward a more targeted CRM strategy. Instead of sending every customer the same offer, the company should evaluate which customer segments are most likely to be influenced by each promotion.

## Decision Framework

The project evaluates whether a broad campaign rollout would create unnecessary promotion costs by sending incentives to customers who do not need them.

The final recommendation will prioritize a targeted CRM rollout by sending offers only to customers with positive estimated uplift, while suppressing offers for customers likely to convert without incentives or customers who may respond negatively.

Based on the analysis so far:

* Discount appears to be the strongest overall offer.
* Discount produced the highest conversion rate in both High Spender and Low Spender segments.
* High Spenders converted at a higher rate even without an offer, suggesting some may be likely to purchase naturally.
* Low Spenders had a lower No Offer conversion rate but showed strong lift from Discount.
* BOGO also created meaningful positive lift, but it was weaker than Discount in both spender segments.
* Customer-level and segment-level differences should be considered before deciding on a full rollout.

## Next Steps

The next phase will continue customer segmentation to understand whether campaign performance differs across:

* Channel: Web, Phone, and Multi-channel customers
* Zip code type: Urban, Suburban, and Rural customers

After segmentation, the project will move into uplift modeling to estimate which customers are most likely to be influenced by each offer.

The uplift modeling phase will focus on identifying:

* Persuadables: customers who are likely to convert because of the offer
* Sure Things: customers likely to convert without an offer
* Lost Causes: customers unlikely to convert even with an offer
* Sleeping Dogs: customers who may respond negatively to receiving an offer

## Tools Used

Python, Pandas, NumPy, scikit-learn, A/B Testing, Customer Segmentation, Uplift Modeling, Data Visualization

## Key Takeaway

A promotion should not be judged only by total conversion rate. The better CRM decision is to identify which customers are actually influenced by an offer, then target promotions toward customers with positive incremental lift.

The analysis so far shows that both Discount and BOGO increase conversion, but Discount is the stronger offer across both High Spender and Low Spender segments. High Spenders also show stronger natural conversion without an offer, which supports the need for more targeted promotion decisions rather than sending offers to every customer.
