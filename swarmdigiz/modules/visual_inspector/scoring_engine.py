# swarmdigiz/modules/visual_inspector/scoring_engine.py


def score_service(service_name, pricing_result, inspection_result):
    """
    Returns score contribution (0–100 scale normalized per service)
    """

    total_price = pricing_result.get("total", 0)
    complexity = inspection_result.get("complexity", "standard")

    score = 0

    # Base score from price (value weight)
    if total_price < 200:
        score += 20
    elif total_price < 500:
        score += 40
    elif total_price < 1000:
        score += 60
    else:
        score += 80

    # Complexity weight
    if complexity in ["large", "extended", "medium"]:
        score += 10
    elif complexity in ["high", "high_risk"]:
        score += 20
    elif complexity == "emergency":
        score += 30

    # HVAC multiplier (higher lifetime value)
    if service_name == "hvac_service":
        score += 15

    return min(score, 100)


def aggregate_job_score(service_scores):
    """
    Combine multiple services into unified job score.
    We weight by highest value service primarily.
    """

    if not service_scores:
        return 0

    highest = max(service_scores)
    average = sum(service_scores) / len(service_scores)

    # Bias toward highest-value service
    final_score = int((highest * 0.6) + (average * 0.4))

    return min(final_score, 100)


def determine_value_tier(score):
    if score <= 40:
        return "low"
    elif score <= 70:
        return "standard"
    elif score <= 85:
        return "high"
    else:
        return "premium"