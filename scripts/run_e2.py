from soma_bench.protocol import run_e2
if __name__ == "__main__":
    run_e2("configs/e2.yaml")
    print("E2 done → results/e2_overlay_costs.csv, results/table1b_latency_extension.csv, figs/fig3_overlay_p95.png")
