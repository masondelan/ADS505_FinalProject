
# **Predictive Banking Marketing Intelligence**

**ADS-505 Team Project – Team 5**  

## **Project Purpose**

This project uses historical bank marketing data to predict whether a contact will subscribe to a term deposit. The goal is to help the bank prioritize higher-potential contacts and use its marketing resources more efficiently.

## **Business Problem**

Only about 11.27% of historical marketing contacts resulted in a term-deposit subscription. Calling the entire contact list can use significant staff time and resources, while reducing calls without a targeting strategy may miss potential subscribers.

The project addresses the following business question:

*How can historical customer and campaign information be used to identify who should be contacted first?*

To support this decision, the project ranks contacts by predicted subscription potential and evaluates different contact levels using lift and cumulative gains.

## **Data**

The project uses the Bank Marketing dataset from the UCI Machine Learning Repository, specifically `bank-additional-full.csv`.

The dataset includes:

- Customer demographics
- Financial characteristics
- Current campaign information
- Previous campaign history
- Contact timing
- Economic indicators
- Term-deposit subscription outcome

*Data Source*

Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing* [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306



## **Project Structure**

```text
ADS505_FinalProject/
├── 01_preprocessing_eda/        Data cleaning and initial EDA
├── 02_feature_engineering_eda/ Feature engineering and additional EDA
├── 03_modeling/                Clustering, model training, evaluation, and targeting analysis
├── data/                       Raw dataset (bank-additional-full.csv)
├── dashboard/                  Streamlit dashboard and supporting CSV files
├── README.md                   Project documentation
└── requirements.txt            Required Python packages
```

## **Setup and How to Run**

### 1. Clone the repository

```bash
git clone https://github.com/masondelan/ADS505_FinalProject.git
cd ADS505_FinalProject
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the notebook

Open the technical Jupyter Notebook and run the cells from top to bottom.
Run the Jupyter notebook `03_modeling/modeling.ipynb`
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

### 4. Run the dashboard

From the repository root:

```bash
streamlit run dashboard/app.py
```

## **Interactive Dashboard**

The Streamlit dashboard allows users to explore contact levels, subscribers reached, calls avoided, and illustrative campaign-value assumptions.

*Live Dashboard:*

https://predictive-banking-marketing-intelligence.streamlit.app/

The financial values shown in the dashboard are illustrative because actual bank call costs and subscription values were not included in the dataset.



## **Data Preparation & Feature Engineering**

Several preprocessing decisions were made to create a modeling-ready dataset.

*Key Strategies*

- Removed exact duplicate records
- Preserved meaningful `"unknown"` categories
- Converted `pdays = 999` into a more interpretable previous-contact representation
- Created `previously_contacted`
- Created `days_since_previous_contact`
- Created customer `age_group`
- Created `campaign_capped` to reduce the influence of extreme campaign-contact values
- Encoded categorical variables
- Standardized numerical variables where appropriate


*The variable `duration` was excluded from predictive modeling.Although call duration is highly associated with subscription, it is only known after the marketing call occurs. Since the goal is to decide who should be contacted before making the call, including this variable would introduce data leakage.*



## **Exploratory Data Analysis**

EDA identified several patterns related to term-deposit subscription:

- Only about 11% of contacts subscribed, showing a class imbalance.
- Previous campaign success was strongly associated with subscription (~65%).
- Subscription rates were higher among customers under 25 and age 60+.
- Subscription rates generally decreased as the number of campaign contacts increased.
- Economic conditions also showed meaningful relationships with subscription.

These findings helped guide feature engineering, model evaluation, and the final customer-targeting strategy.

## **Customer Segmentation**

K-Means clustering was used to explore whether contacts formed meaningful groups based on customer characteristics and previous campaign history. 

| Cluster | Share | Subscription Rate | Main Pattern |
|---|---:|---:|---|
| Cluster 0 | 86.34% | 8.83% | No previous campaign outcome |
| Cluster 1 | 13.66% | 26.65% | Previous failure or success |

The clusters mainly reflected previous campaign history, so clustering was used as descriptive analysis rather than the final prediction method.

##  **Predictive Modeling**

The objective is to estimate the likelihood of term-deposit subscription before a marketing call is made.Four classification models were evaluated: Logistic Regression, Decision Tree, Random Forest, and XGBoost. Models were tuned using 5-fold stratified cross-validation on the training data, with PR-AUC as the primary metric because only about 11% of contacts subscribed.

| Model | CV PR-AUC | Test PR-AUC | Test ROC-AUC |
|---|---:|---:|---:|
| Logistic Regression | 0.4500 | 0.4540 | 0.8003 |
| Decision Tree | 0.4207 | 0.4441 | 0.8038 |
| Random Forest | 0.4684 | **0.4902** | **0.8127** |
| XGBoost | **0.4697** | 0.4847 | 0.8126 |

Random Forest and XGBoost performed very similarly. Random Forest was retained for the final customer-ranking and business analysis because of its strong ranking performance and straightforward feature-importance interpretation.



## **Lift & Cumulative Gains**

Lift analysis compares model-based targeting with random targeting.

At the **Top 20% contact depth**:

- 1,647 contacts are prioritized
- 614 of 928 historical subscribers are captured
- 66.16% of subscribers are reached
- 3.31× lift is achieved over random targeting
- Approximately 6,589 calls are avoided compared with contacting the full evaluation population

Increasing the contact depth from 20% to 30% requires approximately 823 additional calls while historically capturing only 75 additional subscribers.

This shows diminishing returns as the bank moves further down the ranked contact list.


## **Limitations and Future Work**

The analysis is based on historical campaign data, so customer behavior and economic conditions may change over time. Actual call costs and subscription values were unavailable, and the Top 20% strategy does not capture every potential subscriber.

The holdout test set also informed final model, threshold, and contact-depth decisions, so reported performance may be somewhat optimistic.

Future work could include:

- Time-based validation
- Model monitoring and retraining
- Prospective testing of the Top 20% strategy
- Actual bank call-cost and subscription-value data
- Additional model explainability and calibration analysis

---

## **Team Contributions**

**Yubi Joy Quinzon:**  
Data preprocessing and EDA

**Mason Delan:**  
Feature Engineering and EDA

**Sheshma Jaganathan:**  
Modeling and Dashboard

