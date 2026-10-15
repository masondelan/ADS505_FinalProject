# ADS 505 Final Project

# Predictive Banking Marketing Intelligence

**ADS-505 Team Project – Team 5**  

## Project Purpose

This project uses historical bank marketing data to predict whether a contact will subscribe to a term deposit. The goal is to help the bank prioritize higher-potential contacts and use its marketing resources more efficiently.

## Business Problem

Only about 11.27% of historical marketing contacts resulted in a term-deposit subscription. Calling the entire contact list can use significant staff time and resources, while reducing calls without a targeting strategy may miss potential subscribers.

The project addresses the following business question:

**Which contacts should the bank prioritize, and how many should it contact before additional calls provide limited value?**

To support this decision, the project ranks contacts by predicted subscription potential and evaluates different contact levels using lift and cumulative gains.

## Data

The project uses the **Bank Marketing dataset** from the UCI Machine Learning Repository, specifically `bank-additional-full.csv`.

- Original records: **41,188**
- Cleaned records: **41,176**
- Target: `y` (term-deposit subscription: yes/no)
- Unit of analysis: one recorded marketing contact, not necessarily a unique customer
- CSV separator: semicolon (`;`)

### Key Data Preparation

- Removed 12 exact duplicate records.
- Retained `unknown` values as categories.
- Treated `pdays = 999` as indicating that no usable previous-contact date is available.
- Created previous-contact features.
- Capped `campaign` to reduce the influence of extreme values.
- Encoded categorical variables and scaled numerical variables.
- Reviewed highly correlated economic variables and retained them for prediction.
- Removed `duration` because it is only known after a call and would create data leakage.

## Analysis and Modeling

The project includes exploratory data analysis, K-Means clustering, and supervised classification.

Four classification models were compared:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

The data was split into **80% training and 20% holdout test data**. Five-fold stratified cross-validation within the training data served as the validation stage for hyperparameter tuning.

GridSearchCV and RandomizedSearchCV were used for hyperparameter tuning. Because the target is imbalanced, **PR-AUC** was the primary model-comparison metric. ROC-AUC, precision, recall, and F1-score were also evaluated.

Random Forest and XGBoost produced very similar results. **Random Forest was retained for the final analysis** because it provided strong ranking performance and straightforward feature-importance interpretation.

K-Means clustering was also used for exploratory customer segmentation. The final two-cluster solution was mainly associated with previous campaign history, so clustering was treated as supporting analysis rather than the primary targeting method.

## Key Results

The final model was used to rank contacts from higher to lower subscription potential.

The **Top 20%** was selected as a practical starting point for resource allocation.

In the historical holdout evaluation:

- **1,647** of 8,236 contacts were prioritized.
- **614 of 928 subscribers** were reached.
- About **66% of subscribers** were captured using only 20% of the calls.
- The strategy produced approximately **3.31× lift** compared with random targeting.
- **6,589 calls** were avoided compared with calling the entire evaluation list.

The Top 20% is a practical starting point rather than a financially optimal cutoff because actual call costs and the financial value of a subscription were not available.


## Project Structure

```text
ADS505_FinalProject/
├── 01_preprocessing_eda/        Data cleaning and initial EDA
├── 02_feature_engineering_eda/ Feature engineering and additional EDA
├── 03_modeling/                Clustering, model training, evaluation, and targeting       analysis
├── dashboard/                  Streamlit dashboard and supporting CSV files
├── README.md                   Project documentation
└── requirements.txt            Required Python packages

## Setup and How to Run

### 1. Clone the repository

```bash
git clone https://github.com/masondelan/ADS505_FinalProject.git
cd ADS505_FinalProject
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the dataset

Download `bank-additional-full.csv` from the UCI Bank Marketing dataset and place it in the location expected by the notebook.

The file is read using a semicolon separator:

```python
pd.read_csv("bank-additional-full.csv", sep=";")
```

### 4. Run the analysis

Open the technical Jupyter Notebook and run the cells from top to bottom.
Run the Jupyter notebook `03_modeling.ipynb`
The notebook performs:

- Data cleaning and feature engineering
- EDA
- K-Means clustering
- Model training and tuning
- Model evaluation
- Threshold analysis
- Customer ranking
- Lift and cumulative gains analysis
- Dashboard-data preparation

### 5. Run the dashboard

From the repository root:

```bash
streamlit run dashboard/app.py
```

## Interactive Dashboard

The Streamlit dashboard allows users to explore contact levels, subscribers reached, calls avoided, and illustrative campaign-value assumptions.

**Live Dashboard:**  
https://predictive-banking-marketing-intelligence.streamlit.app/

The financial values shown in the dashboard are illustrative because actual bank call costs and subscription values were not included in the dataset.

## Reproducibility

Random seeds were set where applicable for data splitting, cross-validation, clustering, model training, and hyperparameter tuning.

Preprocessing and model-training steps were designed so that transformations used for supervised modeling were fitted using the training data.

Running the notebook from top to bottom with the required dataset and dependencies reproduces the analysis and dashboard output files.

## Limitations and Future Work

The analysis is based on historical campaign data, so customer behavior and economic conditions may change over time. Actual call costs and subscription values were unavailable, and the Top 20% strategy does not capture every potential subscriber.

The holdout test set also informed final model, threshold, and contact-depth decisions, so reported performance may be somewhat optimistic.

Future work could include:

- Time-based validation
- Model monitoring and retraining
- Prospective testing of the Top 20% strategy
- Actual bank call-cost and subscription-value data
- Additional model explainability and calibration analysis

## Team Contributions

**Yubi Joy Quinzon:**  
Data preprocessing and EDA

**Mason Delan:**  
Feature Engineering and EDA

**Sheshma Jaganathan:**  
Modeling and Dashboard

## Data Source

Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306
