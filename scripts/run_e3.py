from soma_bench.protocol import run_e3
if __name__ == "__main__":
    run_e3("configs/e3.yaml")
    print("E3 done → results/e3_drift_dropout_timelines.csv, figs/fig4a_drift_fraud.png, figs/fig4b_drift_friction.png")
