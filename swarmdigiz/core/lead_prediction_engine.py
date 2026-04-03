# -*- coding: utf-8 -*-

"""
SwarmDigiz AI Lead Prediction Engine
Predicts probability of conversion.
"""


def predict_lead_outcome(result):

    score = result.get("lead_score", 0)

    severity = result.get("ai_severity", 0)

    # Simple scoring model
    prediction_score = score + severity

    if prediction_score >= 120:

        tier = "High Probability"
        action = "Prioritize booking + upsell"

    elif prediction_score >= 70:

        tier = "Medium Probability"
        action = "Send follow-up + remarketing"

    else:

        tier = "Low Probability"
        action = "Trigger discount campaign"

    return {
        "prediction_score": prediction_score,
        "prediction_tier": tier,
        "recommended_action": action,
    }