def get_model_prediction(
    model,
    text_vector
):
    prediction = model.predict(
        text_vector
    )[0]

    class_scores = {}

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            text_vector
        )[0]

        class_scores = {
            class_name: float(score)
            for class_name, score in zip(
                model.classes_,
                probabilities
            )
        }

        score = class_scores[prediction]
        score_type = "probability"

    elif hasattr(model, "decision_function"):

        decision_scores = model.decision_function(
            text_vector
        )

        if decision_scores.ndim == 1:
            decision_scores = decision_scores.reshape(
                1, -1
            )

        decision_scores = decision_scores[0]

        class_scores = {
            class_name: float(score)
            for class_name, score in zip(
                model.classes_,
                decision_scores
            )
        }

        score = class_scores[prediction]
        score_type = "decision_score"

    else:

        score = None
        score_type = None
        class_scores = {}

    return {
        "prediction": prediction,
        "score": score,
        "score_type": score_type,
        "class_scores": class_scores
    }