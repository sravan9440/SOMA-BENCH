import numpy as np

def evaluate(df, decisions, tti_cfg=None, overlay_profile=\"classical\"):
    y = df[\"is_fraud\"].to_numpy()
    dec = np.array(decisions)
    fraud_blocked = ((y == True) & ((dec == \"challenge\") | (dec == \"deny\"))).sum() / max(1, (y==True).sum())
    legit_friction = ((y == False) & ((dec == \"challenge\") | (dec == \"deny\"))).sum() / max(1, (y==False).sum())
    base = np.where(dec == \"allow\", 80, np.where(dec == \"challenge\", 120, 140))
    p95 = float(np.percentile(base, 95))
    tti = None
    if tti_cfg:
        import random
        a,b = tti_cfg.get(\"challenge_ms\", (800,2200))
        mr_a,mr_b = tti_cfg.get(\"manual_review_ms\", (4000,6500))
        tti_samples = []
        for d in dec:
            if d == \"challenge\":
                tti_samples.append(random.randint(a,b))
        if tti_samples:
            tti = float(np.median(tti_samples))
    return dict(
        fraud_blocked_pct=100.0 * fraud_blocked,
        legit_friction_pct=100.0 * legit_friction,
        p95_latency_ms=p95,
        tti_ms=tti if tti is not None else np.nan
    )
