import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import (
    LogisticRegression,
    SGDClassifier,
    RidgeClassifier,
)

from sklearn.svm import LinearSVC

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
)

from sklearn.naive_bayes import (
    MultinomialNB,
    ComplementNB,
    BernoulliNB,
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


# ============================================================
# CONFIG
# ============================================================

DATASET = "entity_classifier_data.csv"

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

TARGET_COLUMN = "entityType"

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("ENTITY CLASSIFIER - MODEL COMPARISON")
print("=" * 70)

df = pd.read_csv(DATASET)

print(f"\nTotal rows: {len(df)}")

print("\nClass distribution:")
print(df[TARGET_COLUMN].value_counts())


# ============================================================
# COMBINE TEXT FIELDS
# ============================================================

def combine_fields(row):
    parts = []

    for column in INPUT_COLUMNS:
        value = row[column]

        if pd.isna(value):
            value = ""

        value = str(value).strip()

        if value:
            parts.append(f"{column}: {value}")

    return " ".join(parts)


X = df.apply(combine_fields, axis=1)
y = df[TARGET_COLUMN]


# ============================================================
# TRAIN / VALIDATION / TEST SPLIT
# ============================================================

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
# TF-IDF
# ============================================================

def create_pipeline(classifier):

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                sublinear_tf=True,
            ),
        ),
        (
            "classifier",
            classifier,
        ),
    ])


# ============================================================
# MODELS
# ============================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
        ),

    "Linear SVM":
        LinearSVC(
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=RANDOM_STATE,
            class_weight="balanced",
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1,
        ),

    "Extra Trees":
        ExtraTreesClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1,
        ),

    "Multinomial Naive Bayes":
        MultinomialNB(),

    "Complement Naive Bayes":
        ComplementNB(),

    "Bernoulli Naive Bayes":
        BernoulliNB(),

    "SGD Classifier":
        SGDClassifier(
            loss="hinge",
            max_iter=2000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),

    "Ridge Classifier":
        RidgeClassifier(
            class_weight="balanced",
        ),
}


# ============================================================
# TRAIN + EVALUATE
# ============================================================

results = []


for name, classifier in models.items():

    print("\n")
    print("=" * 70)
    print(f"MODEL: {name}")
    print("=" * 70)

    model = create_pipeline(classifier)

    print("\nTraining...")

    model.fit(X_train, y_train)

    print("Training complete.")

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    val_predictions = model.predict(X_val)

    val_accuracy = accuracy_score(
        y_val,
        val_predictions,
    )

    print("\nValidation Accuracy:")
    print(f"{val_accuracy:.4f}")

    # --------------------------------------------------------
    # Test
    # --------------------------------------------------------

    test_predictions = model.predict(X_test)

    test_accuracy = accuracy_score(
        y_test,
        test_predictions,
    )

    print("\nTest Accuracy:")
    print(f"{test_accuracy:.4f}")

    # --------------------------------------------------------
    # Classification Report
    # --------------------------------------------------------

    report = classification_report(
        y_test,
        test_predictions,
        output_dict=True,
        zero_division=0,
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            test_predictions,
            zero_division=0,
        )
    )

    # --------------------------------------------------------
    # Confusion Matrix
    # --------------------------------------------------------

    labels = sorted(y.unique())

    cm = confusion_matrix(
        y_test,
        test_predictions,
        labels=labels,
    )

    print("\nConfusion Matrix:")
    print("Labels:")
    print(labels)
    print(cm)

    # --------------------------------------------------------
    # Errors
    # --------------------------------------------------------

    errors = []

    for index, actual, predicted in zip(
        X_test.index,
        y_test,
        test_predictions,
    ):

        if actual != predicted:

            errors.append({
                "index": index,
                "actual": actual,
                "predicted": predicted,
                "text": X_test.loc[index],
            })

    print(f"\nTotal errors: {len(errors)}")

    if errors:

        for error in errors:

            print("\n----------------------------------------")
            print(f"Actual    : {error['actual']}")
            print(f"Predicted : {error['predicted']}")
            print(f"Text      : {error['text']}")

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    results.append({
        "Model": name,
        "Validation Accuracy": val_accuracy,
        "Test Accuracy": test_accuracy,
        "Macro Precision": report["macro avg"]["precision"],
        "Macro Recall": report["macro avg"]["recall"],
        "Macro F1": report["macro avg"]["f1-score"],
        "Weighted F1": report["weighted avg"]["f1-score"],
        "Errors": len(errors),
    })


# ============================================================
# FINAL COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Test Accuracy",
    ascending=False,
)


print("\n\n")
print("=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


# ============================================================
# SAVE RESULTS
# ============================================================

results_df.to_csv(
    "model_comparison_results.csv",
    index=False,
)

print("\nSaved:")
print("model_comparison_results.csv")

print("\nDone.")