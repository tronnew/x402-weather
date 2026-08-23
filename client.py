#!/usr/bin/env python3
"""Example x402 client for weather API."""
import requests, json, time

BASE = "http://forex2026.mooo.com:5010"
WALLET = "0xYourWalletAddress"

def get_forecast(city="puentealto", days=5):
    r = requests.get(f"{BASE}/forecast", params={"city": city, "days": days})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 402:
        req = json.loads(r.headers["X-PAYMENT-REQUIRED"])
        print(f"Payment required: {req['maxAmountRequired']} USDC to {req['payTo']}")
        print(f"Valid for {req['maxTimeoutSeconds']}s")
        return None
    return r.text

if __name__ == "__main__":
    result = get_forecast("puentealto")
    if result:
        print(json.dumps(result, indent=2)[:500])
