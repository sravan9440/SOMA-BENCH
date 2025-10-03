import pandas as pd
from .utils import make_rng

def _sample_bool(rngp, p):
    return rngp.random() < p

def generate_events(n, seed=42, fraud_prevalence=0.05,
                    dropout=None, split="flat",
                    window_size=None, n_windows=None):
    rng = make_rng(seed)
    rows = []
    if split == "windows":
        assert window_size and n_windows
        total = window_size * n_windows
    else:
        total = n

    for i in range(total):
        evt_type = "recovery" if (i % 5 == 0) else "signin"  # ~20% recovery
        is_fraud = _sample_bool(rng.py, fraud_prevalence)
        asn_rep = max(0.0, min(1.0, rng.np.normal(0.7, 0.15)))
        new_device = _sample_bool(rng.py, 0.15)
        geo_vel = _sample_bool(rng.py, 0.05)
        rpwc = _sample_bool(rng.py, 0.03)
        rmfac = _sample_bool(rng.py, 0.02)
        d = dropout or {}
        if d.get("ip_asn_reputation", 0) and rng.py.random() < d["ip_asn_reputation"]:
            asn_rep = None
        def drop(b, key): return None if (d.get(key,0) and rng.py.random() < d[key]) else b
        new_device = drop(new_device, "new_device")
        geo_vel = drop(geo_vel, "geo_velocity_flag")
        rpwc = drop(rpwc, "recent_pw_change")
        rmfac = drop(rmfac, "recent_mfa_change")

        rows.append(dict(
            event_id=f\"e{i}\",
            ts=f\"t{i}\",
            event_type=evt_type,
            is_fraud=is_fraud,
            device_hash=f\"d{i%2000}\",
            new_device=new_device if new_device is not None else False,
            ip_asn_reputation=asn_rep if asn_rep is not None else 0.5,
            geo_velocity_flag=geo_vel if geo_vel is not None else False,
            recent_pw_change=rpwc if rpwc is not None else False,
            recent_mfa_change=rmfac if rmfac is not None else False,
            service_id=f\"s{i%200}\",
            S=1 + (i % 3),
            C=\"G\"
        ))
    return pd.DataFrame(rows)
