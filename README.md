
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

---

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

### 4. Run the notebook

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
---

##  Predictive Modeling

The supervised learning objective is to estimate the likelihood of term-deposit subscription before a marketing call is made.

### Models Evaluated

Four classification models were compared:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

The data was divided using an 80/20 stratified train-test split.

Rather than creating a separate fixed validation dataset, 5-fold stratified cross-validation was performed within the training data for model comparison and hyperparameter tuning. The 20% test set remained untouched until final evaluation.

### Primary Evaluation Metric

Because only approximately 11% of contacts subscribed, the target is imbalanced.

Therefore, **PR-AUC (Precision-Recall Area Under the Curve)** was used as the primary model-comparison metric.

PR-AUC is useful because it evaluates the balance between:

- **Precision:** How many predicted subscribers actually subscribed?
- **Recall:** How many actual subscribers did the model identify?

---

##  Model Results

### Cross-Validation Performance

| Model | CV PR-AUC |
|---|---:|
| Logistic Regression | 0.4500 |
| Decision Tree | 0.4207 |
| Random Forest | 0.4684 |
| XGBoost | **0.4697** |

Random Forest and XGBoost showed very similar performance.

### Holdout Test Performance

| Model | ROC-AUC | PR-AUC |
|---|---:|---:|
| Logistic Regression | 0.8003 | 0.4540 |
| Decision Tree | 0.8038 | 0.4441 |
| **Random Forest** | **0.8127** | **0.4902** |
| XGBoost | 0.8126 | 0.4847 |

Random Forest was retained for the final customer-ranking and business analysis because it provided strong holdout ranking performance, slightly higher test PR-AUC, and interpretable feature importance.

---

##  Customer Ranking Strategy

Rather than relying only on a yes/no classification, the final model was used to **rank contacts from higher to lower predicted subscription potential**.

This allows the bank to decide how deeply it wants to work through the ranked contact list.

### Contact-Depth Analysis

| Contact Depth | Contacts | Subscribers Captured | Capture Rate | Lift |
|---:|---:|---:|---:|---:|
| 10% | 823 | 434 | 46.77% | 4.68× |
| **20%** | **1,647** | **614** | **66.16%** | **3.31×** |
| 30% | 2,470 | 689 | 74.25% | 2.48× |
| 50% | 4,118 | 779 | 83.94% | 1.68× |
| 100% | 8,236 | 928 | 100% | 1.00× |

---

## Lift & Cumulative Gains

Lift analysis compares model-based targeting with random targeting.

At the **Top 20% contact depth**:

- **1,647** contacts are prioritized
- **614 of 928** historical subscribers are captured
- **66.16%** of subscribers are reached
- **3.31× lift** is achieved over random targeting
- Approximately **6,589 calls are avoided** compared with contacting the full evaluation population

Increasing the contact depth from **20% to 30%** requires approximately **823 additional calls** while historically capturing only **75 additional subscribers**.

This demonstrates diminishing returns as the bank moves further down the ranked contact list.

---

## Resource Allocation Recommendation

### Recommended Starting Strategy: Top 20%

The analysis recommends the **Top 20% of model-ranked contacts as a practical starting point**.

This strategy:

- Concentrates potential subscribers near the top of the contact list
- Captures approximately **66% of historical subscribers**
- Requires only **20% of the evaluation calls**
- Produces approximately **3.31× lift**
- Avoids approximately **80% of calls** compared with contacting everyone

> **Important:** The Top 20% should be interpreted as a practical, resource-efficient starting point rather than a financially optimal cutoff.

Actual campaign call costs and the financial value of a successful term-deposit subscription were not available in the dataset.

---

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
