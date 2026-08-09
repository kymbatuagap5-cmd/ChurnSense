# Educational Practice Mini-Project

## Team Information

Academic group: Pending confirmation

Team name: StarTrio

Project track: Machine Learning

Project topic: Customer Churn Prediction

## Team Members

| No. | Full Name | Role / Contribution |
|---|---|---|
| 1 | Kymbat Uagap | Team Leader / Machine Learning Engineer. Organized the workflow and repository, performed preprocessing, trained and evaluated Logistic Regression, Decision Tree, and Random Forest models, selected and saved the final model, and prepared ML screenshots and report materials. |
| 2 | Zhansaya Yerkenova | Data Analyst. Prepared the dataset, performed EDA, analyzed churn patterns, created charts, interpreted dataset characteristics, and provided screenshots and findings for the report. |
| 3 | Saltanat Tlegen | Documentation & Project Integration. Organized documentation, compiled and formatted the report, prepared the contribution table, assisted with GitHub maintenance, and collected screenshots. |

## Project Description

This project predicts customer churn using a machine learning model trained on a customer churn dataset. The workflow includes data cleaning, categorical feature encoding, model training, model comparison, evaluation, and deployment through a Streamlit application.

The final application accepts customer profile values and returns:

- churn prediction;
- probability score;
- risk level;
- summary of the input values used for prediction.

## Dataset and Model

The dataset contains 440,833 customer records before cleaning and includes customer profile, service usage, support, payment, subscription, and churn fields.

Main preprocessing steps:

- removed rows with missing values;
- removed `CustomerID` because it is an identifier;
- encoded `Gender`, `Subscription Type`, and `Contract Length` with one-hot encoding;
- split the data into training and testing subsets.

Models compared:

- Logistic Regression;
- Decision Tree Classifier;
- Random Forest Classifier.

The Decision Tree model achieved the highest accuracy and was saved as:

```text
models/churn_model.pkl
```

## Application Features

The Streamlit app provides required inputs:

- `Age`
- `Monthly Charges`
- `Contract Length`
- `Support Calls`

Optional details:

- `Tenure Months`
- `Usage Frequency`
- `Payment Delay`
- `Last Interaction`
- `Gender`
- `Subscription Type`

The saved model was trained with more features than the four required app inputs. For missing model features, the app uses medians for numeric columns and modes for categorical columns from the training dataset. `Monthly Charges` is converted into the model's `Total Spend` field using the selected or default customer tenure.

## Project Structure

```text
data/                         Dataset
models/                       Saved trained model
notebooks/                    EDA and model training materials
screenshots/app/              Streamlit application screenshots
screenshots/ml/               ML workflow, EDA, and evaluation screenshots
report/                       Report, contribution table, and PDF materials
src/main.py                   Streamlit application
tests/                        Project and prediction tests
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run src/main.py
```

Run tests:

```bash
python -m pytest -q
```

## Evaluation Results

| Model | Accuracy |
|---|---:|
| Logistic Regression | 89.65% |
| Decision Tree | 99.97% |
| Random Forest | 99.96% |

Selected model: Decision Tree Classifier.

Key important features:

- Support Calls
- Total Spend
- Contract Length
- Age
- Payment Delay

## Screenshots and Report Materials

Screenshots are organized in:

```text
screenshots/app/
screenshots/ml/
```

Report materials are organized in:

```text
report/
```

## Final Submission Checklist

According to the Educational Practice task description, the team leader must submit:

- private GitHub repository link;
- report PDF;
- contribution table.

The instructor GitHub account `@bakhtiyar-k` must be added as a collaborator to the private repository.

## Links

GitHub repository link: https://github.com/aitu-educational-practice-2026/educational-practice-project-startrio
