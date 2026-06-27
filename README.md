# A/B Test & Uplift Modeling

This project analyzes a public synthetic marketing promotion dataset to understand how different CRM campaign offers impact customer conversion. The goal is to go beyond basic campaign performance and identify which customers should receive an offer, which customers do not need one, and which customers may respond negatively.

## Project Goals

* Perform a deep-dive A/B test analysis comparing:

  * No Offer vs Discount
  * No Offer vs BOGO

* Analyze customer segments such as:

  * High spenders vs low spenders
  * Channel: Web, Phone, and Multi-channel customers
  * Zip code type: Urban, Suburban, and Rural customers

* Estimate incremental lift to understand whether each offer truly caused additional conversions.

* Build an uplift modeling workflow to classify customers into groups such as:

  * Persuadables: customers who need a small nudge to convert
  * Sure Things: customers likely to convert without an offer
  * Lost Causes: customers unlikely to convert even with an offer
  * Sleeping Dogs: customers who may respond negatively to receiving an offer

## Business Question

Should the promotion be sent to everyone, or only to selected customers?

## Decision Framework

The project evaluates whether a full campaign rollout would create unnecessary promotion costs by sending discounts to customers who would have converted anyway.

The final recommendation is to prioritize a targeted CRM rollout by sending offers only to customers with positive estimated uplift, while suppressing offers for customers likely to convert without incentives or customers who may respond negatively.

## Tools Used

Python, Pandas, NumPy, scikit-learn, A/B Testing, Customer Segmentation, Uplift Modeling, Data Visualization

## Key Takeaway

A promotion should not be judged only by total conversion rate. The better CRM decision is to identify which customers are influenced by the offer and use that insight to support more targeted, efficient, and personalized campaign decisions.
