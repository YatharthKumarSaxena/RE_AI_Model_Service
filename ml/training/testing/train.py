import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# ============================================================
# CONFIG
# ============================================================

INPUT_CSV = "entity_classifier_data.csv"
RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_CSV)

print("=" * 70)
print("ENTITY CLASSIFIER - BASELINE MODEL")
print("=" * 70)

print(f"\nTotal rows: {len(df)}")


# ============================================================
# BUILD INPUT TEXT
# ============================================================
# Model ke 8 input fields use honge.
# rowId aur entityType input mein nahi jayenge.

INPUT_COLUMNS = [
    "projectTitle",
    "projectDescription",
    "problemStatement",
    "projectGoal",
    "projectType",
    "productVision",
    "entityTitle",
    "entityDescription",
]


def combine_fields(row):
    parts = []

    for column in INPUT_COLUMNS:
        value = str(row[column]).strip()

        if value and value.lower() != "nan":
            parts.append(f"{column}: {value}")

    return " ".join(parts)


X = df.apply(combine_fields, axis=1)
y = df["entityType"]


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\nClass distribution:")
print(y.value_counts())


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================
# 70% train
# 15% validation
# 15% test

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=RANDOM_STATE,
    stratify=y,
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=y_temp,
)

print("\nDataset split:")
print(f"Train      : {len(X_train)}")
print(f"Validation : {len(X_val)}")
print(f"Test       : {len(X_test)}")


# ============================================================
# BASELINE MODEL
# ============================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
        )
    ),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )
    ),
])


# ============================================================
# TRAIN
# ============================================================

print("\nTraining baseline model...")

model.fit(X_train, y_train)

print("Training complete.")


# ============================================================
# VALIDATION
# ============================================================

val_predictions = model.predict(X_val)

val_accuracy = accuracy_score(
    y_val,
    val_predictions
)

print("\n" + "=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)

print(f"\nValidation Accuracy: {val_accuracy:.4f}")


# ============================================================
# FINAL TEST
# ============================================================

test_predictions = model.predict(X_test)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

print("\n" + "=" * 70)
print("TEST RESULTS")
print("=" * 70)

print(f"\nTest Accuracy: {test_accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        test_predictions,
        digits=4,
        zero_division=0,
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    test_predictions,
    labels=labels,
)

print("\nConfusion Matrix:")
print("Labels:")
print(labels)
print()

print(cm)


# ============================================================
# MISCLASSIFIED EXAMPLES
# ============================================================

results = pd.DataFrame({
    "actual": y_test.values,
    "predicted": test_predictions,
    "text": X_test.values,
})

errors = results[
    results["actual"] != results["predicted"]
]

print("\n" + "=" * 70)
print("MISCLASSIFIED EXAMPLES")
print("=" * 70)

print(f"\nTotal errors: {len(errors)}")

for _, row in errors.head(20).iterrows():

    print("\n----------------------------------------")
    print(f"Actual    : {row['actual']}")
    print(f"Predicted : {row['predicted']}")
    print(f"Text      : {row['text'][:700]}")


# ============================================================
# SAVE ERROR ANALYSIS
# ============================================================

errors.to_csv(
    "baseline_errors.csv",
    index=False,
)

print("\nSaved:")
print("baseline_errors.csv")

print("\nDone.")