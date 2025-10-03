def static_mfa(evt):
    if evt[\"event_type\"] == \"recovery\":
        return \"challenge\"
    return \"challenge\"

def trivial_risk(evt, asn_bad_threshold=0.20):
    risky = (
        evt[\"new_device\"] or
        evt[\"geo_velocity_flag\"] or
        evt[\"recent_pw_change\"] or
        evt[\"recent_mfa_change\"] or
        (evt[\"ip_asn_reputation\"] < asn_bad_threshold)
    )
    if evt[\"event_type\"] == \"recovery\":
        return \"deny\" if risky else \"challenge\"
    return \"challenge\" if risky else \"allow\"
