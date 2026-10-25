def analyze_route(
    route_name,
    distance,
    crime_risk,
    lighting,
    cctv,
    traffic,
    police_proximity
):

    safety_score = (
        (100 - crime_risk) * 0.30
        + lighting * 0.20
        + cctv * 0.20
        + traffic * 0.10
        + police_proximity * 0.20
    )

    if safety_score >= 70:

        risk_level = "Low Risk"

    elif safety_score >= 40:

        risk_level = "Medium Risk"

    else:

        risk_level = "High Risk"

    return {
        "route_name": route_name,
        "distance": distance,
        "safety_score": round(safety_score),
        "risk_level": risk_level
    }