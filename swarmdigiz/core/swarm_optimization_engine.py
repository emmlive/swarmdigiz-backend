# -*- coding: utf-8 -*-

"""
SwarmDigiz Campaign Optimization Engine
Analyzes performance and improves campaigns automatically.
"""


def analyze_campaign_performance(metrics):

    ctr = metrics.get("ctr", 0)
    conversions = metrics.get("conversions", 0)

    recommendations = []

    if ctr < 1.5:
        recommendations.append("Rewrite ad headline")

    if conversions < 2:
        recommendations.append("Increase ad targeting radius")

    if ctr > 4:
        recommendations.append("Increase campaign budget")

    return recommendations


def optimize_campaign(metrics):

    recommendations = analyze_campaign_performance(metrics)

    return {
        "status": "optimized",
        "recommendations": recommendations
    }