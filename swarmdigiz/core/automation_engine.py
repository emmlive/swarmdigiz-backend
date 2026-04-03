def should_trigger_marketing(inspection_result):
    """
    Determines whether an inspection should trigger
    an automated marketing swarm.
    """

    job_score = inspection_result.get("job_score", 0)
    estimated_total = inspection_result.get("estimated_total", 0)
    tier = inspection_result.get("value_tier", "low")

    # High-value opportunities
    if tier in ["premium", "high"]:
        return True

    # Strong service signals
    if job_score >= 70:
        return True

    # High revenue potential
    if estimated_total >= 500:
        return True

    return False