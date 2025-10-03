import matplotlib.pyplot as plt

def fraud_friction_curve(points, static_point=None, path=\"figs/fig2_fraud_friction_curve.png\"):
    xs = [p[\"legit\"] for p in points]
    ys = [p[\"fraud\"] for p in points]
    labels = [p[\"label\"] for p in points]
    plt.figure()
    plt.plot(xs, ys, marker=\"o\")
    for x,y,l in zip(xs,ys,labels):
        plt.text(x,y,l)
    if static_point:
        plt.scatter([static_point[\"legit\"]],[static_point[\"fraud\"]], marker=\"s\")
        plt.text(static_point[\"legit\"], static_point[\"fraud\"], static_point[\"label\"], ha=\"right\", va=\"bottom\")
    plt.xlabel(\"Legitimate friction (%)\")
    plt.ylabel(\"Fraud blocked (%)\")
    plt.title(\"Figure 2. Fraud–Friction Trade-Off\")
    plt.savefig(path, dpi=220, bbox_inches=\"tight\")
    plt.close()

def bar_overlay(p95_map, path=\"figs/fig3_overlay_p95.png\"):
    labels = list(p95_map.keys())
    vals = [p95_map[k] for k in labels]
    plt.figure()
    plt.bar(labels, vals)
    plt.xlabel(\"Overlay profile\")
    plt.ylabel(\"CPU p95 add (ms)\")
    plt.title(\"Figure 3. PQC Overlay Impact (p95 adders)\")
    plt.savefig(path, dpi=220, bbox_inches=\"tight\")
    plt.close()

def timeline(windows, tr_vals, smfa_vals, ylabel, title, path):
    plt.figure()
    plt.plot(windows, tr_vals, marker=\"o\", label=\"Trivial Risk\")
    plt.plot(windows, smfa_vals, marker=\"s\", label=\"Static MFA\")
    plt.xlabel(\"Time window\")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(path, dpi=220, bbox_inches=\"tight\")
    plt.close()
