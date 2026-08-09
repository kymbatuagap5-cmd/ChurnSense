from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
from streamlit.runtime import exists as streamlit_runtime_exists


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "customer_churn_dataset-training-master.csv"

CONTRACT_MONTHS = {
    "Monthly": 1,
    "Quarterly": 3,
    "Annual": 12,
}

RISK_LEVELS = (
    (0.7, "High risk"),
    (0.4, "Medium risk"),
    (0.0, "Low risk"),
)


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)


@lru_cache(maxsize=1)
def load_training_baseline():
    data = pd.read_csv(DATA_PATH).dropna()
    numeric_defaults = data.select_dtypes(include="number").median().to_dict()
    categorical_defaults = {
        column: data[column].mode().iloc[0]
        for column in data.select_dtypes(exclude="number").columns
    }
    return numeric_defaults, categorical_defaults


def build_model_input(
    model,
    age,
    monthly_charges,
    contract_length,
    support_calls,
    tenure_months=None,
    usage_frequency=None,
    payment_delay=None,
    last_interaction=None,
    gender=None,
    subscription_type=None,
):
    numeric_defaults, categorical_defaults = load_training_baseline()
    feature_names = list(model.feature_names_in_)
    row = {feature: 0.0 for feature in feature_names}

    for feature in feature_names:
        if feature in numeric_defaults:
            row[feature] = float(numeric_defaults[feature])

    row["Age"] = float(age)
    row["Support Calls"] = float(support_calls)

    tenure_value = tenure_months if tenure_months is not None else row.get("Tenure", 0.0)
    row["Tenure"] = float(tenure_value)
    if "Total Spend" in row:
        row["Total Spend"] = float(monthly_charges) * max(float(tenure_value), 1.0)
    if usage_frequency is not None:
        row["Usage Frequency"] = float(usage_frequency)
    if payment_delay is not None:
        row["Payment Delay"] = float(payment_delay)
    if last_interaction is not None:
        row["Last Interaction"] = float(last_interaction)

    gender_value = gender or categorical_defaults.get("Gender")
    subscription_value = subscription_type or categorical_defaults.get("Subscription Type")

    for feature in feature_names:
        if feature.startswith("Gender_"):
            row[feature] = float(feature == f"Gender_{gender_value}")
        elif feature.startswith("Subscription Type_"):
            row[feature] = float(feature == f"Subscription Type_{subscription_value}")
        elif feature.startswith("Contract Length_"):
            row[feature] = float(feature == f"Contract Length_{contract_length}")

    return pd.DataFrame([row], columns=feature_names)


def predict_churn(model, model_input):
    prediction = int(model.predict(model_input)[0])
    classes = list(model.classes_)
    positive_class = 1.0 if 1.0 in classes else classes[-1]
    probability = float(model.predict_proba(model_input)[0][classes.index(positive_class)])
    return prediction, probability


def get_risk_level(probability):
    for threshold, label in RISK_LEVELS:
        if probability >= threshold:
            return label
    return RISK_LEVELS[-1][1]


def format_prediction(prediction):
    return "Likely to churn" if prediction == 1 else "Not likely to churn"


def main():
    st.set_page_config(page_title="Churn Prediction", page_icon="bar_chart")

    st.title("Churn Prediction")

    model = load_model()
    numeric_defaults, categorical_defaults = load_training_baseline()

    input_panel, result_panel = st.columns([1, 1], gap="large")

    with input_panel:
        with st.form("prediction_form"):
            st.subheader("Customer profile")
            age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)
            monthly_charges = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                value=50.0,
                step=1.0,
                format="%.2f",
            )
            contract_length = st.selectbox("Contract Length", list(CONTRACT_MONTHS))
            support_calls = st.number_input(
                "Support Calls",
                min_value=0,
                max_value=100,
                value=3,
                step=1,
            )

            with st.expander("Optional details"):
                tenure_months = st.number_input(
                    "Tenure Months",
                    min_value=1,
                    max_value=120,
                    value=int(numeric_defaults.get("Tenure", 32)),
                    step=1,
                )
                usage_frequency = st.number_input(
                    "Usage Frequency",
                    min_value=0,
                    max_value=100,
                    value=int(numeric_defaults.get("Usage Frequency", 16)),
                    step=1,
                )
                payment_delay = st.number_input(
                    "Payment Delay",
                    min_value=0,
                    max_value=120,
                    value=int(numeric_defaults.get("Payment Delay", 12)),
                    step=1,
                )
                last_interaction = st.number_input(
                    "Last Interaction",
                    min_value=0,
                    max_value=365,
                    value=int(numeric_defaults.get("Last Interaction", 14)),
                    step=1,
                )
                gender = st.selectbox(
                    "Gender",
                    ["Female", "Male"],
                    index=0 if categorical_defaults.get("Gender") == "Female" else 1,
                )
                subscription_type = st.selectbox(
                    "Subscription Type",
                    ["Basic", "Standard", "Premium"],
                    index=["Basic", "Standard", "Premium"].index(
                        categorical_defaults.get("Subscription Type", "Standard")
                    ),
                )

            submitted = st.form_submit_button("Predict")

    with result_panel:
        st.subheader("Prediction")

        if not submitted:
            st.info("No prediction yet.")
            return

        model_input = build_model_input(
            model=model,
            age=age,
            monthly_charges=monthly_charges,
            contract_length=contract_length,
            support_calls=support_calls,
            tenure_months=tenure_months,
            usage_frequency=usage_frequency,
            payment_delay=payment_delay,
            last_interaction=last_interaction,
            gender=gender,
            subscription_type=subscription_type,
        )
        prediction, probability = predict_churn(model, model_input)
        risk_level = get_risk_level(probability)

        prediction_label = format_prediction(prediction)
        if prediction == 1:
            st.error(prediction_label)
        else:
            st.success(prediction_label)

        metric_a, metric_b = st.columns(2)
        metric_a.metric("Probability score", f"{probability:.2%}")
        metric_b.metric("Risk level", risk_level)

        st.progress(probability, text=risk_level)

        summary = pd.DataFrame(
            [
                ("Age", age),
                ("Monthly Charges", f"{monthly_charges:.2f}"),
                ("Contract Length", contract_length),
                ("Support Calls", support_calls),
                ("Tenure Months", tenure_months),
                ("Usage Frequency", usage_frequency),
                ("Payment Delay", payment_delay),
                ("Last Interaction", last_interaction),
                ("Gender", gender),
                ("Subscription Type", subscription_type),
            ],
            columns=["Input", "Value"],
        )
        summary["Value"] = summary["Value"].astype(str)
        st.dataframe(summary, hide_index=True, width="stretch")


if __name__ == "__main__":
    if streamlit_runtime_exists():
        main()
    else:
        print("Run the app with: streamlit run src/main.py")
