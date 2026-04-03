# swarmdigiz/modules/visual_inspector/payload_builder.py

import uuid

from .services_config import SERVICES
from .inspection_engine import (
    evaluate_air_duct,
    evaluate_dryer_vent,
    evaluate_carpet,
    evaluate_hvac,
)
from .pricing_engine import (
    calculate_air_duct_price,
    calculate_dryer_vent_price,
    calculate_carpet_price,
    calculate_tile_price,
    calculate_pressure_washing_price,
    calculate_window_cleaning_price,
    calculate_hvac_price,
)
from .scoring_engine import score_service, aggregate_job_score, determine_value_tier
from .marketing_signal_engine import build_marketing_signals


def build_inspection_payload(input_data):
    """
    input_data structure example:

    {
        "services": {
            "air_duct_cleaning": {"vent_count": 14},
            "carpet_cleaning": {"room_count": 5},
            "hvac_service": {"service_type": "repair", "emergency": True}
        }
    }
    """

    services_requested = input_data.get("services", {})

    inspection_results = []
    pricing_results = []
    service_scores = []

    total_value = 0
    services_selected = []

    for service_name, service_data in services_requested.items():
        if service_name not in SERVICES:
            continue

        config = SERVICES[service_name]

        # -----------------------------
        # INSPECTION
        # -----------------------------
        if service_name == "air_duct_cleaning":
            inspection = evaluate_air_duct(service_data, config)
            pricing = calculate_air_duct_price(service_data, config)

        elif service_name == "dryer_vent_cleaning":
            inspection = evaluate_dryer_vent(service_data, config)
            pricing = calculate_dryer_vent_price(service_data, config)

        elif service_name == "carpet_cleaning":
            inspection = evaluate_carpet(service_data, config)
            pricing = calculate_carpet_price(service_data, config)

        elif service_name == "tile_and_grout_cleaning":
            inspection = {"service": service_name}
            pricing = calculate_tile_price(service_data, config)

        elif service_name == "pressure_washing":
            inspection = {"service": service_name}
            pricing = calculate_pressure_washing_price(service_data, config)

        elif service_name == "window_cleaning":
            inspection = {"service": service_name}
            pricing = calculate_window_cleaning_price(service_data, config)

        elif service_name == "hvac_service":
            inspection = evaluate_hvac(service_data, config)
            pricing = calculate_hvac_price(service_data, config)

        else:
            continue

        # -----------------------------
        # SCORING
        # -----------------------------
        score = score_service(service_name, pricing, inspection)

        inspection_results.append(inspection)
        pricing_results.append({
            "service": service_name,
            **pricing
        })
        service_scores.append(score)

        total_value += pricing.get("total", 0)
        services_selected.append(service_name)

    # -----------------------------
    # AGGREGATE SCORING
    # -----------------------------
    job_score = aggregate_job_score(service_scores)
    value_tier = determine_value_tier(job_score)

    # -----------------------------
    # MARKETING SIGNALS
    # -----------------------------
    marketing_signals = build_marketing_signals(
        total_value,
        job_score,
        value_tier,
        services_selected
    )

    # -----------------------------
    # CONFIDENCE LOGIC
    # -----------------------------
    requires_manual_confirmation = job_score >= 90
    confidence = "high" if job_score < 90 else "medium"

    # -----------------------------
    # FINAL PAYLOAD
    # -----------------------------
    payload = {
        "inspection_id": str(uuid.uuid4()),
        "services_selected": services_selected,
        "inspection_results": inspection_results,
        "pricing_breakdown": pricing_results,
        "estimated_total": total_value,
        "job_score": job_score,
        "value_tier": value_tier,
        "confidence": confidence,
        "requires_manual_confirmation": requires_manual_confirmation,
        "marketing_signals": marketing_signals,
        "qualification_status": "qualified" if total_value > 0 else "invalid"
    }

    return payload