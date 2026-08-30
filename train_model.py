import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/historical_flood_events.csv"
)

print("\n========== FIRST 5 ROWS ==========\n")
print(df.head())


# ==========================================
# FEATURE ENGINEERING
# ==========================================

from utils.encoders import DISTRICTS, RIVERS

unknown_districts = set(df["district"].dropna()) - set(DISTRICTS)
unknown_rivers = set(df["river"].dropna()) - set(RIVERS)

if unknown_districts:
    raise ValueError(f"Unknown districts: {unknown_districts}")

if unknown_rivers:
    raise ValueError(f"Unknown rivers: {unknown_rivers}")

df["district"] = df["district"].map(DISTRICTS)
df["river"] = df["river"].map(RIVERS)

# ==========================================
# FEATURES & TARGET
# ==========================================

X = df[[
    "district",
    "river",
    "rainfall_mm",
    "river_level_m",
    "dmc_alert",
    "temperature",
    "humidity"
]]

y = df["flood_occurred"]


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)


# ==========================================
# TRAIN MODEL
# ==========================================

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=10,

    random_state=42

)

model.fit(

    X_train,
    y_train

)


# ==========================================
# EVALUATION
# ==========================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n========== RESULTS ==========\n")

print(
    f"Accuracy: {accuracy:.4f}"
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

with open("models/sri_flood_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model Saved Successfully!")

