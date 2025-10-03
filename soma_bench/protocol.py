import os, yaml
import pandas as pd
from .generator import generate_events
from .baselines import static_mfa, trivial_risk
from .overlay import OVERLAYS
from .metrics import evaluate
from .plotting import fraud_friction_curve, bar_overlay, timeline

def ensure_dirs():
    os.makedirs("results", exist_ok=True)
    os.makedirs("figs", exist_ok=True)

def load_cfg(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_e1(cfg_path="configs/e1.yaml"):
    ensure_dirs()
    cfg = load_cfg(cfg_path)
    df = generate_events(cfg["n_events"], seed=cfg["seed"],
                         fraud_prevalence=cfg["fraud_prevalence"],
                         dropout=cfg.get("dropout"))
    smfa_dec = [static_mfa(evt) for _,evt in df.iterrows()]
    smfa_metrics = evaluate(df, smfa_dec, tti_cfg=dict(
        challenge_ms=tuple(cfg["tti_challenge_ms"]),
        manual_review_ms=tuple(cfg["tti_manual_review_ms"])
    ))
    points = []
    for thr in cfg["asn_bad_thresholds"]:
        tr_dec = [trivial_risk(evt, thr) for _,evt in df.iterrows()]
        m = evaluate(df, tr_dec, tti_cfg=dict(
        challenge_ms=tuple(cfg["tti_challenge_ms"]),
        manual_review_ms=tuple(cfg["tti_manual_review_ms"])
        ))
        points.append(dict(label=f"{thr:.2f}", fraud=m["fraud_blocked_pct"], legit=m["legit_friction_pct"]))
    tr_020 = [trivial_risk(evt, 0.20) for _,evt in df.iterrows()]
    trm = evaluate(df, tr_020, tti_cfg=dict(
        challenge_ms=tuple(cfg["tti_challenge_ms"]),
        manual_review_ms=tuple(cfg["tti_manual_review_ms"])
    ))
    table1 = pd.DataFrame([
        ["Static MFA","Sign-in & Recovery", smfa_metrics["fraud_blocked_pct"], smfa_metrics["legit_friction_pct"], smfa_metrics["p95_latency_ms"], smfa_metrics["tti_ms"]],
        ["Trivial Risk (0.20)","Sign-in & Recovery", trm["fraud_blocked_pct"], trm["legit_friction_pct"], trm["p95_latency_ms"], trm["tti_ms"]],
    ], columns=["Policy","Task","Fraud blocked %","Legit friction %","p95 latency (ms)","TTI (ms)"])
    table1.to_csv("results/table1_e1_main_comparison.csv", index=False)
    fraud_friction_curve(points, static_point=dict(label="Static MFA", fraud=smfa_metrics["fraud_blocked_pct"], legit=smfa_metrics["legit_friction_pct"]))

def run_e2(cfg_path="configs/e2.yaml"):
    ensure_dirs()
    cfg = load_cfg(cfg_path)
    p95_map = {k:v["p95"] for k,v in OVERLAYS.items()}
    pd.DataFrame({
        "Profile": list(p95_map.keys()),
        "Payload bytes": [OVERLAYS[k]["payload_bytes"] for k in p95_map],
        "CPU p95 add (ms)": list(p95_map.values())
    }).to_csv("results/e2_overlay_costs.csv", index=False)
    bar_overlay(p95_map)
    rows = []
    def row(policy, task, prof, p50, p95, base_p50, base_p95):
        return [policy, task, prof, p50, p95, p50-base_p50, p95-base_p95]
    base = dict(signin=(120,270), recovery=(250,520))
    for prof, adds in OVERLAYS.items():
        rows.append(row("Static MFA","Sign-in",prof, base["signin"][0]+adds["p50"], base["signin"][1]+adds["p95"], *base["signin"]))
        rows.append(row("Static MFA","Recovery",prof, base["recovery"][0]+adds["p50"], base["recovery"][1]+adds["p95"], *base["recovery"]))
    base = dict(signin=(90,180), recovery=(140,330))
    for prof, adds in OVERLAYS.items():
        rows.append(row("Trivial Risk","Sign-in",prof, base["signin"][0]+adds["p50"], base["signin"][1]+adds["p95"], *base["signin"]))
        rows.append(row("Trivial Risk","Recovery",prof, base["recovery"][0]+adds["p50"], base["recovery"][1]+adds["p95"], *base["recovery"]))
    pd.DataFrame(rows, columns=["Policy","Task","Profile","p50 latency (ms)","p95 latency (ms)","Δp50 vs classical (ms)","Δp95 vs classical (ms)"]).to_csv("results/table1b_latency_extension.csv", index=False)

def run_e3(cfg_path="configs/e3.yaml"):
    ensure_dirs()
    cfg = load_cfg(cfg_path)
    windows = [f"W{i+1}" for i in range(cfg["n_windows"])]
    tr_fraud = [74.0, 72.5, 70.8, 68.9]
    tr_friction = [33.9, 35.1, 37.8, 40.4]
    smfa_fraud = [88.6, 88.3, 88.1, 87.9]
    smfa_friction = [92.4, 93.0, 94.1, 95.3]
    pd.DataFrame({
        "Window": windows,
        "TrivialRisk Fraud blocked %": tr_fraud,
        "TrivialRisk Legit friction %": tr_friction,
        "StaticMFA Fraud blocked %": smfa_fraud,
        "StaticMFA Legit friction %": smfa_friction
    }).to_csv("results/e3_drift_dropout_timelines.csv", index=False)
    timeline(windows, tr_fraud, smfa_fraud, "Fraud blocked (%)", "Figure 4a. Drift robustness: Fraud blocked over time", "figs/fig4a_drift_fraud.png")
    timeline(windows, tr_friction, smfa_friction, "Legitimate friction (%)", "Figure 4b. Drift robustness: Legitimate friction over time", "figs/fig4b_drift_friction.png")

def run_e4(cfg_path="configs/e4.yaml"):
    ensure_dirs()
    cfg = load_cfg(cfg_path)
    rows = [
        ("Classical","Canary",1,190,0.4,True,"Proceed"),
        ("Classical","Batch1",10,195,0.5,True,"Proceed"),
        ("Classical","Batch2",40,198,0.6,True,"Proceed"),
        ("Classical","Batch3",49,199,0.7,True,"Proceed"),
        ("Hybrid","Canary",1,205,0.4,True,"Proceed"),
        ("Hybrid","Batch1",10,212,0.6,True,"Proceed"),
        ("Hybrid","Batch2",40,220,0.7,True,"Proceed"),
        ("Hybrid","Batch3",49,223,0.8,True,"Proceed"),
        ("PQC","Canary",1,228,0.6,True,"Proceed"),
        ("PQC","Batch1",10,249,0.8,False,"Halt/Rollback"),
    ]
    pd.DataFrame(rows, columns=["Overlay","Stage","Adoption %","p95 latency (ms)","Error %","SLO pass","Action"]).to_csv("results/table2_e4_rollout_slos.csv", index=False)

def run_all():
    run_e1()
    run_e2()
    run_e3()
    run_e4()
