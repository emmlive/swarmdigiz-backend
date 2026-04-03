# swarmdigiz/modules/visual_inspector/pricing_engine.py


def calculate_air_duct_price(data, config):
    base = config["base_price"]
    vents = data.get("vent_count", 0)

    extra_vents = max(0, vents - config["min_vents"])
    vent_cost = extra_vents * config["per_vent_price"]

    total = base + vent_cost

    return {
        "base": base,
        "adjustments": vent_cost,
        "total": total
    }


def calculate_dryer_vent_price(data, config):
    base = config["base_price"]
    return {
        "base": base,
        "adjustments": 0,
        "total": base
    }


def calculate_carpet_price(data, config):
    base = config["base_price"]
    rooms = data.get("room_count", 0)

    extra_rooms = max(0, rooms - config["base_rooms"])
    room_cost = extra_rooms * config["extra_room_price"]

    total = base + room_cost

    return {
        "base": base,
        "adjustments": room_cost,
        "total": total
    }


def calculate_tile_price(data, config):
    base = config["base_price"]
    sqft = data.get("square_feet", 0)

    extra_sqft = max(0, sqft - config["min_sqft"])
    sqft_cost = extra_sqft * config["per_sqft_price"]

    total = base + sqft_cost

    return {
        "base": base,
        "adjustments": sqft_cost,
        "total": total
    }


def calculate_pressure_washing_price(data, config):
    base = config["base_price"]
    sqft = data.get("square_feet", 0)

    extra_sqft = max(0, sqft - config["min_sqft"])
    sqft_cost = extra_sqft * config["per_sqft_price"]

    total = base + sqft_cost

    return {
        "base": base,
        "adjustments": sqft_cost,
        "total": total
    }


def calculate_window_cleaning_price(data, config):
    base = config["base_price"]
    windows = data.get("window_count", 0)

    extra_windows = max(0, windows - config["min_windows"])
    window_cost = extra_windows * config["per_window_price"]

    total = base + window_cost

    return {
        "base": base,
        "adjustments": window_cost,
        "total": total
    }


def calculate_hvac_price(data, config):
    base = config["base_diagnostic_fee"]

    service_type = data.get("service_type", "maintenance")
    emergency = data.get("emergency", False)

    service_cost = config["service_types"].get(service_type, 0)
    emergency_fee = config["emergency_fee"] if emergency else 0

    total = base + service_cost + emergency_fee

    return {
        "base": base,
        "adjustments": service_cost + emergency_fee,
        "total": total
    }