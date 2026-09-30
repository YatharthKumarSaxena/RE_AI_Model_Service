import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import (
    ComplementNB,
    BernoulliNB,
    MultinomialNB
)

from sklearn.ensemble import (
    ExtraTreesClassifier,
    RandomForestClassifier
)

from sklearn.tree import DecisionTreeClassifier


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "data",
    "entity_classifier_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "entityType"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# DATASET COLUMNS
# ============================================================

TEXT_COLUMNS = [
    "projectTitle",
    "projectDescription",
    "problemStatement",
    "projectGoal",
    "projectType",
    "productVision",
    "entityTitle",
    "entityDescription"
]

TARGET_COLUMN = "entityType"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("ENTITY CLASSIFIER - MODEL TRAINING")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(
    DATA_PATH
)

print(
    f"Total rows: {len(df)}"
)


# ============================================================
# VALIDATION
# ============================================================

required_columns = (
    TEXT_COLUMNS +
    [TARGET_COLUMN]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )


# ============================================================
# REMOVE ROWS WITHOUT TARGET
# ============================================================

df = df.dropna(
    subset=[TARGET_COLUMN]
).copy()


# ============================================================
# BUILD MODEL INPUT
# ============================================================

print("\nBuilding model input...")

for column in TEXT_COLUMNS:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
    )


def build_text(row):
    return " ".join([
        row["projectTitle"],
        row["projectDescription"],
        row["problemStatement"],
        row["projectGoal"],
        row["projectType"],
        row["productVision"],
        row["entityTitle"],
        row["entityDescription"]
    ])


df["model_text"] = df.apply(
    build_text,
    axis=1
)

X = df["model_text"]
y = df[TARGET_COLUMN]


# ============================================================
# CLASS DISTRIBUTION
# ============================================================

print("\nClass distribution:")

print(
    y.value_counts()
)


# ============================================================
# TF-IDF
# ============================================================

print("\nTraining TF-IDF...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_tfidf = vectorizer.fit_transform(
    X
)

print(
    f"TF-IDF matrix: {X_tfidf.shape}"
)


# ============================================================
# SAVE TF-IDF
# ============================================================

vectorizer_path = os.path.join(
    MODEL_DIR,
    "entity_tfidf.joblib"
)

joblib.dump(
    vectorizer,
    vectorizer_path
)

print(
    f"\nTF-IDF saved at:\n{vectorizer_path}"
)


# ============================================================
# MODELS
# ============================================================

models = {

    "linear_svm": LinearSVC(
        C=1.0
    ),

    "sgd_classifier": SGDClassifier(
        loss="hinge",
        random_state=42
    ),

    "ridge_classifier": RidgeClassifier(
        alpha=1.0
    ),

    "logistic_regression": LogisticRegression(
        max_iter=2000,
        random_state=42
    ),

    "complement_naive_bayes": ComplementNB(),

    "bernoulli_naive_bayes": BernoulliNB(),

    "multinomial_naive_bayes": MultinomialNB(),

    "extra_trees": ExtraTreesClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "random_forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "decision_tree": DecisionTreeClassifier(
        random_state=42
    )
}


# ============================================================
# TRAIN MODELS
# ============================================================

print("\n" + "=" * 70)
print("TRAINING MODELS")
print("=" * 70)

for model_name, model in models.items():

    print(
        f"\nTraining: {model_name}"
    )

    model.fit(
        X_tfidf,
        y
    )

    model_path = os.path.join(
        MODEL_DIR,
        f"entity_{model_name}.joblib"
    )

    joblib.dump(
        model,
        model_path
    )

    print(
        f"Saved: {model_path}"
    )


# ============================================================
# DONE
# ============================================================

print("\n" + "=" * 70)
print("ALL MODEL TRAINING COMPLETED")
print("=" * 70)

print("\nModels:")

for model_name in models:
    print(
        f"✓ {model_name}"
    )

print("\nClasses:")
print(
    models["linear_svm"].classes_
)

print("\nModel directory:")
print(
    MODEL_DIR
)

print("\n✅ All production models are ready.")