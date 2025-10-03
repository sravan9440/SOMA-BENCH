OVERLAYS = {
    \"classical\": {\"payload_bytes\": 128,  \"p50\": 1.0, \"p95\": 5.0},
    \"hybrid\":    {\"payload_bytes\": 1024, \"p50\": 2.0, \"p95\": 7.5},
    \"pqc\":       {\"payload_bytes\": 2400, \"p50\": 3.0, \"p95\": 10.0},
}

def add_latency(base_ms, profile, tail=False):
    add = OVERLAYS[profile][\"p95\"] if tail else OVERLAYS[profile][\"p50\"]
    return base_ms + add
