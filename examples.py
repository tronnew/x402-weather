#!/usr/bin/env python3
"""Example usage of x402 Weather API."""
import requests, json, subprocess, time

BASE = "http://forex2026.mooo.com:5010"

def call_forecast(city="puentealto"):
    r = requests.get(f"{BASE}/forecast", params={"city": city})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 402:
        req = json.loads(r.headers["X-PAYMENT-REQUIRED"])
        print(f"💸 Payment required: {int(req['maxAmountRequired'])/1e6:.2f} USDC")
        print(f"📍 Pay to: {req['payTo']}")
        print(f"⏱️  Valid for: {req['maxTimeoutSeconds']}s")
        # Build EIP-3009 payment and call with it
        print("\n📋 Payment instructions:")
        print(json.dumps(req, indent=2))
        return None
    return r.text

if __name__ == "__main__":
    result = call_forecast("puentealto")
    if result:
        print(json.dumps(result, indent=2)[:500])
