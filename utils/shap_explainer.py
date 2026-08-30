import pickle
import shap
import pandas as pd
import matplotlib.pyplot as plt


# ===================================
# LOAD MODEL
# ===================================

with open("models/sri_flood_model.pkl", "rb") as f:
    model = pickle.load(f)


# ===================================
# GENERATE SHAP PLOT
# ===================================

def generate_shap_plot(input_data):

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(input_data)

    # Handle different SHAP output formats
    if isinstance(shap_values, list):

        # Binary classification -> class 1 = Flood
        values = shap_values[1][0]
        base_value = explainer.expected_value[1]

    else:

        # New SHAP versions can return:
        # (samples, features, classes)
        if shap_values.ndim == 3:

            values = shap_values[0, :, 1]

            if hasattr(explainer.expected_value, "__len__"):
                base_value = explainer.expected_value[1]
            else:
                base_value = explainer.expected_value

        else:

            values = shap_values[0]

            if hasattr(explainer.expected_value, "__len__"):
                base_value = explainer.expected_value[1]
            else:
                base_value = explainer.expected_value

    explanation = shap.Explanation(
        values=values,
        base_values=base_value,
        data=input_data.iloc[0].values,
        feature_names=input_data.columns.tolist()
    )

    shap.plots.waterfall(
        explanation,
        max_display=7,
        show=False
    )

    fig = plt.gcf()

    fig.set_size_inches(9, 6)
    fig.tight_layout()

    return fig

def get_local_shap_explanation(input_data):

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(input_data)

    # Handle different SHAP output formats
    if isinstance(shap_values, list):
        values = shap_values[1][0]

    elif shap_values.ndim == 3:
        values = shap_values[0, :, 1]

    else:
        values = shap_values[0]

    feature_names = input_data.columns.tolist()

    # Find strongest feature for this prediction
    top_index = abs(values).argmax()

    top_feature = feature_names[top_index]
    top_value = input_data.iloc[0, top_index]
    contribution = float(values[top_index])

    direction = (
        "increased"
        if contribution > 0
        else "decreased"
    )

    return {
        "feature": top_feature,
        "value": top_value,
        "contribution": contribution,
        "direction": direction
    }

# ===================================
# FEATURE IMPORTANCE
# ===================================

def get_feature_importance():

    importance = model.feature_importances_

    features = [

        "District",
        "River",
        "Rainfall",
        "River Level",
        "DMC Alert",
        "Temperature",
        "Humidity"

    ]

    df = pd.DataFrame({

        "Feature": features,
        "Importance": importance

    })

    df = df.sort_values(

        by="Importance",
        ascending=False

    )

    return df