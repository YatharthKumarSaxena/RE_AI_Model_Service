import csv
from collections import Counter

import numpy as np

from sklearn.model_selection import GroupShuffleSplit
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
    f1_score,
    precision_score,
    recall_score,
)


# ==========================================================
# CONFIG
# ==========================================================

INPUT_CSV = "entity_classifier_data.csv"

RANDOM_STATE = 42

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


# ==========================================================
# LOAD DATA
# ==========================================================

def load_dataset():

    texts = []
    labels = []
    groups = []

    with open(
        INPUT_CSV,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            text_parts = []

            for column in INPUT_COLUMNS:
                value = row[column].strip()

                if value:
                    text_parts.append(value)

            combined_text = " ".join(text_parts)

            texts.append(combined_text)
            labels.append(row["entityType"].strip())

            # IMPORTANT:
            # All rows belonging to the same project
            # will remain in the same split.
            groups.append(row["projectTitle"].strip())

    return (
        np.array(texts),
        np.array(labels),
        np.array(groups),
    )


# ==========================================================
# GROUP SPLIT
# ==========================================================

def project_level_split(texts, labels, groups):

    print("\n" + "=" * 70)
    print("PROJECT-LEVEL DATA SPLIT")
    print("=" * 70)

    unique_projects = np.unique(groups)

    print(f"\nTotal rows     : {len(texts)}")
    print(f"Unique projects: {len(unique_projects)}")

    # ------------------------------------------------------
    # First split:
    # 85% development (train + validation)
    # 15% test
    # ------------------------------------------------------

    gss_test = GroupShuffleSplit(
        n_splits=1,
        test_size=0.15,
        random_state=RANDOM_STATE,
    )

    train_val_idx, test_idx = next(
        gss_test.split(
            texts,
            labels,
            groups=groups,
        )
    )

    # ------------------------------------------------------
    # Second split:
    # 15% of train_val -> validation
    #
    # This gives approximately:
    # Train      ~70%
    # Validation ~15%
    # Test       ~15%
    # ------------------------------------------------------

    gss_val = GroupShuffleSplit(
        n_splits=1,
        test_size=0.1765,
        random_state=RANDOM_STATE,
    )

    train_idx, val_idx = next(
        gss_val.split(
            texts[train_val_idx],
            labels[train_val_idx],
            groups=groups[train_val_idx],
        )
    )

    train_idx = train_val_idx[train_idx]
    val_idx = train_val_idx[val_idx]

    # ------------------------------------------------------
    # Safety check:
    # No project can exist in multiple splits.
    # ------------------------------------------------------

    train_projects = set(groups[train_idx])
    val_projects = set(groups[val_idx])
    test_projects = set(groups[test_idx])

    train_val_overlap = train_projects & val_projects
    train_test_overlap = train_projects & test_projects
    val_test_overlap = val_projects & test_projects

    print("\nPROJECT OVERLAP CHECK")

    print(
        f"Train ∩ Validation: {len(train_val_overlap)}"
    )

    print(
        f"Train ∩ Test      : {len(train_test_overlap)}"
    )

    print(
        f"Validation ∩ Test : {len(val_test_overlap)}"
    )

    if (
        train_val_overlap
        or train_test_overlap
        or val_test_overlap
    ):
        raise RuntimeError(
            "ERROR: Project leakage detected!"
        )

    print("PASS: No project leakage.")

    # ------------------------------------------------------
    # Distribution
    # ------------------------------------------------------

    print("\nROW DISTRIBUTION")

    print(
        f"Train      : {len(train_idx)} "
        f"({len(train_idx) / len(texts):.2%})"
    )

    print(
        f"Validation : {len(val_idx)} "
        f"({len(val_idx) / len(texts):.2%})"
    )

    print(
        f"Test       : {len(test_idx)} "
        f"({len(test_idx) / len(texts):.2%})"
    )

    print("\nPROJECT DISTRIBUTION")

    print(f"Train      : {len(train_projects)}")
    print(f"Validation : {len(val_projects)}")
    print(f"Test       : {len(test_projects)}")

    return (
        train_idx,
        val_idx,
        test_idx,
    )


# ==========================================================
# MODEL DEFINITIONS
# ==========================================================

def get_models():

    return {

        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
        ),

        "Linear SVM": LinearSVC(
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),

        "Decision Tree": DecisionTreeClassifier(
            random_state=RANDOM_STATE,
            class_weight="balanced",
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1,
        ),

        "Extra Trees": ExtraTreesClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            class_weight="balanced",
            n_jobs=-1,
        ),

        "Multinomial Naive Bayes": MultinomialNB(),

        "Complement Naive Bayes": ComplementNB(),

        "Bernoulli Naive Bayes": BernoulliNB(),

        "SGD Classifier": SGDClassifier(
            random_state=RANDOM_STATE,
            class_weight="balanced",
            max_iter=2000,
            tol=1e-3,
        ),

        "Ridge Classifier": RidgeClassifier(
            class_weight="balanced",
        ),
    }


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("ENTITY CLASSIFIER - PROJECT LEVEL MODEL COMPARISON")
    print("=" * 70)

    # ------------------------------------------------------
    # Load
    # ------------------------------------------------------

    texts, labels, groups = load_dataset()

    # ------------------------------------------------------
    # Split by project
    # ------------------------------------------------------

    (
        train_idx,
        val_idx,
        test_idx,
    ) = project_level_split(
        texts,
        labels,
        groups,
    )

    X_train_text = texts[train_idx]
    X_val_text = texts[val_idx]
    X_test_text = texts[test_idx]

    y_train = labels[train_idx]
    y_val = labels[val_idx]
    y_test = labels[test_idx]

    # ------------------------------------------------------
    # TF-IDF
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("TF-IDF")
    print("=" * 70)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
    )

    X_train = vectorizer.fit_transform(X_train_text)

    X_val = vectorizer.transform(X_val_text)

    X_test = vectorizer.transform(X_test_text)

    print(f"\nTrain matrix: {X_train.shape}")
    print(f"Validation matrix: {X_val.shape}")
    print(f"Test matrix: {X_test.shape}")

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------

    models = get_models()

    results = []

    # ======================================================
    # TRAIN EACH MODEL
    # ======================================================

    for model_name, model in models.items():

        print("\n")
        print("=" * 70)
        print(f"MODEL: {model_name}")
        print("=" * 70)

        print("\nTraining...")

        model.fit(
            X_train,
            y_train,
        )

        print("Training complete.")

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        val_predictions = model.predict(X_val)

        val_accuracy = accuracy_score(
            y_val,
            val_predictions,
        )

        # --------------------------------------------------
        # Test
        # --------------------------------------------------

        test_predictions = model.predict(X_test)

        test_accuracy = accuracy_score(
            y_test,
            test_predictions,
        )

        macro_precision = precision_score(
            y_test,
            test_predictions,
            average="macro",
            zero_division=0,
        )

        macro_recall = recall_score(
            y_test,
            test_predictions,
            average="macro",
            zero_division=0,
        )

        macro_f1 = f1_score(
            y_test,
            test_predictions,
            average="macro",
            zero_division=0,
        )

        weighted_f1 = f1_score(
            y_test,
            test_predictions,
            average="weighted",
            zero_division=0,
        )

        # --------------------------------------------------
        # Print metrics
        # --------------------------------------------------

        print("\nValidation Accuracy:")
        print(f"{val_accuracy:.4f}")

        print("\nTest Accuracy:")
        print(f"{test_accuracy:.4f}")

        print("\nClassification Report:")

        print(
            classification_report(
                y_test,
                test_predictions,
                zero_division=0,
            )
        )

        # --------------------------------------------------
        # Confusion Matrix
        # --------------------------------------------------

        labels_sorted = sorted(
            np.unique(labels)
        )

        cm = confusion_matrix(
            y_test,
            test_predictions,
            labels=labels_sorted,
        )

        print("Confusion Matrix:")

        print("Labels:")
        print(labels_sorted)

        print(cm)

        # --------------------------------------------------
        # Errors
        # --------------------------------------------------

        error_indices = np.where(
            test_predictions != y_test
        )[0]

        print(
            f"\nTotal errors: "
            f"{len(error_indices)}"
        )

        for index in error_indices:

            print("\n" + "-" * 40)

            print(
                f"Actual    : "
                f"{y_test[index]}"
            )

            print(
                f"Predicted : "
                f"{test_predictions[index]}"
            )

            print(
                f"Project   : "
                f"{groups[test_idx[index]]}"
            )

            print(
                f"Text      : "
                f"{X_test_text[index]}"
            )

        # --------------------------------------------------
        # Save result
        # --------------------------------------------------

        results.append({

            "Model": model_name,

            "Validation Accuracy":
                round(val_accuracy, 4),

            "Test Accuracy":
                round(test_accuracy, 4),

            "Macro Precision":
                round(macro_precision, 4),

            "Macro Recall":
                round(macro_recall, 4),

            "Macro F1":
                round(macro_f1, 4),

            "Weighted F1":
                round(weighted_f1, 4),

            "Errors":
                len(error_indices),
        })

    # ======================================================
    # FINAL COMPARISON
    # ======================================================

    print("\n")
    print("=" * 70)
    print("FINAL PROJECT-LEVEL MODEL COMPARISON")
    print("=" * 70)

    header = (
        f"{'Model':30}"
        f"{'Val Acc':>10}"
        f"{'Test Acc':>10}"
        f"{'Macro F1':>10}"
        f"{'Errors':>8}"
    )

    print(header)
    print("-" * len(header))

    for result in sorted(
        results,
        key=lambda x: x["Test Accuracy"],
        reverse=True,
    ):

        print(
            f"{result['Model']:30}"
            f"{result['Validation Accuracy']:>10.4f}"
            f"{result['Test Accuracy']:>10.4f}"
            f"{result['Macro F1']:>10.4f}"
            f"{result['Errors']:>8}"
        )

    # ======================================================
    # SAVE CSV
    # ======================================================

    output_file = "project_level_model_comparison_results.csv"

    with open(
        output_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n")
    print("Saved:")
    print(output_file)

    print("\nDone.")


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    main()