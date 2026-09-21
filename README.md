# ADS 505 Final Project

## Predictive Banking Marketing Intelligence

Our project uses bank marketing data to predict whether a customer will subscribe to a term deposit. The goal is to help the bank prioritize who to contact and use its marketing resources more effectively.

**Team 5:** Mason Delan, Sheshma Jaganathan, and Yubi Joy Quinzon.

## Data

We are using the [Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing) from the UCI Machine Learning Repository, specifically `bank-additional-full.csv`.

- 41,188 records and 20 predictors
- Target: `y` (whether the customer subscribed, yes or no)
- The CSV uses a semicolon separator (`sep=";"` in pandas).

## Project structure

```text
01_preprocessing/        Data cleaning and quality checks
02_eda_1/                Initial exploration and visualizations
03_feature_engineering/  Create and prepare features
04_eda_2/                Review the engineered features
05_train_test_split/     Training and test sets, validation setup
06_modeling/             Model comparison, clustering, and targeting analysis
```

Add Jupyter notebooks to the folder for each stage as the project progresses.

## Approach

We plan to compare logistic regression, decision tree, random forest, and XGBoost models. We will use precision, recall, F1, ROC-AUC, and PR-AUC to evaluate performance, then use lift and cumulative gains to support a targeting recommendation.

The `duration` variable will be excluded because it is only known after a call. Encoding, scaling, and any class balancing will be fitted on training data only.
