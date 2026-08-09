from src.main import build_model_input, get_risk_level, load_model, predict_churn


def test_prediction_input_matches_model_schema():
    model = load_model()

    model_input = build_model_input(
        model=model,
        age=35,
        monthly_charges=50.0,
        contract_length="Monthly",
        support_calls=3,
    )

    assert list(model_input.columns) == list(model.feature_names_in_)
    assert model_input.shape == (1, model.n_features_in_)


def test_prediction_returns_binary_label_and_probability():
    model = load_model()
    model_input = build_model_input(
        model=model,
        age=35,
        monthly_charges=50.0,
        contract_length="Monthly",
        support_calls=3,
    )

    prediction, probability = predict_churn(model, model_input)

    assert prediction in {0, 1}
    assert 0.0 <= probability <= 1.0


def test_optional_inputs_override_model_features():
    model = load_model()

    model_input = build_model_input(
        model=model,
        age=41,
        monthly_charges=80.0,
        contract_length="Quarterly",
        support_calls=5,
        tenure_months=10,
        usage_frequency=22,
        payment_delay=7,
        last_interaction=4,
        gender="Male",
        subscription_type="Premium",
    )

    row = model_input.iloc[0]
    assert row["Age"] == 41.0
    assert row["Support Calls"] == 5.0
    assert row["Tenure"] == 10.0
    assert row["Total Spend"] == 800.0
    assert row["Usage Frequency"] == 22.0
    assert row["Payment Delay"] == 7.0
    assert row["Last Interaction"] == 4.0
    assert row["Gender_Male"] == 1.0
    assert row["Subscription Type_Premium"] == 1.0
    assert row["Contract Length_Quarterly"] == 1.0


def test_risk_level_uses_probability_ranges():
    assert get_risk_level(0.2) == "Low risk"
    assert get_risk_level(0.5) == "Medium risk"
    assert get_risk_level(0.8) == "High risk"
