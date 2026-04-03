# swarmdigiz/modules/visual_inspector/services_config.py

SERVICES = {
    # -----------------------------
    # AIR QUALITY SERVICES
    # -----------------------------
    "air_duct_cleaning": {
        "base_price": 299,
        "per_vent_price": 25,
        "min_vents": 8,
        "large_threshold": 15,
        "upsells": {
            "sanitizer": 49,
            "dryer_vent_addon": 99
        }
    },
    "dryer_vent_cleaning": {
        "base_price": 149,
        "upsells": {}
    },
    "hvac_service": {
        "base_diagnostic_fee": 129,
        "emergency_fee": 89,
        "service_types": {
            "maintenance": 0,
            "repair": 75,
            "installation": 250
        },
        "upsells": {
            "air_filter_replacement": 39,
            "coil_cleaning": 99,
            "system_tuneup": 149
        }
    },

    # -----------------------------
    # FLOOR CARE SERVICES
    # -----------------------------
    "carpet_cleaning": {
        "base_price": 180,
        "base_rooms": 3,
        "extra_room_price": 45,
        "upsells": {
            "pet_treatment": 39,
            "deep_scrub": 59
        }
    },
    "tile_and_grout_cleaning": {
        "base_price": 199,
        "per_sqft_price": 1.25,
        "min_sqft": 150,
        "upsells": {
            "sealant": 79
        }
    },

    # -----------------------------
    # GENERAL HOME SERVICES
    # -----------------------------
    "pressure_washing": {
        "base_price": 249,
        "per_sqft_price": 0.35,
        "min_sqft": 500,
        "upsells": {
            "driveway_seal": 129
        }
    },
    "window_cleaning": {
        "base_price": 199,
        "per_window_price": 8,
        "min_windows": 15,
        "upsells": {
            "screen_cleaning": 49
        }
    }
}