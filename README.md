# ChurnSense

AI-powered customer churn prediction dashboard built with Python,
Machine Learning, and Streamlit.

## Overview

ChurnSense predicts whether a customer is likely to leave a service
based on customer behavior and subscription information.

The application uses a trained Decision Tree classification model
to analyze customer characteristics and generate churn predictions.

## Features

- Customer churn prediction
- Interactive Streamlit dashboard
- Customer risk indicators
- Recommended retention actions
- Prediction history
- Session statistics
- Customer summary
- Machine learning model information

## Machine Learning

The final model is a Decision Tree classifier.

Model accuracy:

99.97%

### Input Features

- Age
- Gender
- Tenure
- Usage Frequency
- Support Calls
- Payment Delay
- Subscription Type
- Contract Length
- Total Spend
- Last Interaction

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit
- Git & GitHub

## Project Structure

```text
ChurnSense/
│
├── app.py
├── churn_model.pkl
├── requirements.txt
├── README.md
└── .gitignore