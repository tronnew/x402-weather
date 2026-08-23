#!/usr/bin/env python3
"""
x402 weather endpoint — charges 0.01 USDC per call on Base L2.
Free tier: 10 calls per IP per day.
Product: 5-day (configurable up to 10) ensemble weather forecast for Puente Alto or Litueche.
Ensemble: ECMWF IFS + NOAA GFS + DWD ICON + CMC GEM, bias-corrected vs ERA5.
Verified +18-27% MAE vs Open-Meteo default on same-calendar (Aug 2025 OBS).
"""
from flask import Flask, request, jsonify, Response
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_typed_data
import json, time, os, sys
from extra_endpoints import bp as extra_bp
from landing import bp as landing_bp

app = Flask(__name__)
app.register_blueprint(extra_bp)
app.register_blueprint(landing_bp)

# === Config ===
WALLET_ADDR = os.environ.get('X402_WALLET', '0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE')
USDC_BASE   = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'  # USDC on Base L2
CHAIN_ID    = 8453  # Base mainnet
PRICE_USDC  = 10000  # 0.01 USDC (6 decimals)
VALID_FOR   = 600   # 10 min window for payment
FREE_TIER   = 10    # free calls per IP per day

# In-memory rate limiter (resets on restart — fine for MVP)
_calls = {}
def _free_remaining(ip):
    today = time.strftime('%Y-%m-%d')
    key = f"{ip}:{today}"
    used = _calls.get(key, 0)
    return max(0, FREE_TIER - used), key

# === Payment requirements ===
def payment_requirements(resource):
    now = int(time.time())
    nonce = '0x' + os.urandom(32).hex()
    req = {
        "x402Version": 1,
        "scheme": "exact",
        "network": "base",
        "resource": resource,
        "payTo": WALLET_ADDR,
        "maxAmountRequired": str(PRICE_USDC),
        "maxTimeoutSeconds": VALID_FOR,
        "asset": USDC_BASE,
        "validAfter": str(now),
        "validBefore": str(now + VALID_FOR),
        "nonce": nonce,
        "description": "Weather forecast (ensemble, bias-corrected) for Puente Alto or Litueche",
        "mimeType": "application/json",
    }
    return req

def challenge_402(requirements):
    body = json.dumps(requirements)
    resp = Response(body, status=402, mimetype='application/json')
    resp.headers['X-PAYMENT-REQUIRED'] = body
    return resp

# === Payment verification ===
def verify_payment(header_json):
    from eip712 import digest, recover as eip712_recover
    payment = json.loads(header_json)
    payload = payment.get('payload') or {}
    auth    = payload.get('authorization') or {}
    sig     = payload.get('signature') or ''

    if not sig.startswith('0x') or len(sig) < 130:
        raise ValueError("bad signature")

    from_addr   = Web3.to_checksum_address(auth['from'])
    to_addr     = Web3.to_checksum_address(auth['to'])
    value       = int(auth['value'])
    valid_after = int(auth['validAfter'])
    valid_before= int(auth['validBefore'])
    nonce       = auth['nonce']
    if not nonce.startswith('0x') or len(nonce) != 66:
        raise ValueError("bad nonce (must be 0x + 64 hex)")

    if value < PRICE_USDC:
        raise ValueError(f"value {value} < required {PRICE_USDC}")
    if to_addr.lower() != WALLET_ADDR.lower():
        raise ValueError(f"recipient {to_addr} != {WALLET_ADDR}")

    now = int(time.time())
    if now < valid_after or now > valid_before:
        raise ValueError(f"authorization out of window")

    d = digest(CHAIN_ID, Web3.to_checksum_address(USDC_BASE),
               from_addr, to_addr, value, valid_after, valid_before, nonce)
    recovered = eip712_recover(d, sig)
    if recovered.lower() != from_addr.lower():
        raise ValueError(f"signer {recovered} != from {from_addr}")

    return {
        "from": from_addr,
        "value_usdc": value / 1e6,
        "nonce": nonce,
    }

# === Forecast ===
CITY_FILES = {
    'puentealto':   ('/opt/x402/wxdata/fcst_pa.json',   'Puente Alto'),
    'puente-alto':  ('/opt/x402/wxdata/fcst_pa.json',   'Puente Alto'),
    'puente_alto':  ('/opt/x402/wxdata/fcst_pa.json',   'Puente Alto'),
    'litueche':     ('/opt/x402/wxdata/fcst_lit.json',  'Litueche'),
    'lit':          ('/opt/x402/wxdata/fcst_lit.json',  'Litueche'),
}

def serve_forecast(city, days, paid, payment_info=None):
    if city not in CITY_FILES:
        return jsonify({"error": "city must be 'puentealto' or 'litueche'"}), 400
    path, label = CITY_FILES[city]
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": f"forecast data not found for {label}"}), 503

    days = max(1, min(days, len(data['days'])))
    src_days = data['days'][:days]

    out_days = []
    for i, d in enumerate(src_days):
        out_days.append({
            "day": i + 1,
            "tmax_mean_c": round(d['temperature_2m_max_mean'], 1),
            "tmax_std_c":  round(d.get('tmax_std', d.get('temperature_2m_max_std', 0)), 1),
            "tmax_min_c":  round(d.get('tmax_min', d.get('temperature_2m_max_min', 0)), 1),
            "tmax_max_c":  round(d.get('tmax_max', d.get('temperature_2m_max_max', 0)), 1),
            "tmin_mean_c": round(d['temperature_2m_min_mean'], 1),
            "tmin_std_c":  round(d.get('temperature_2m_min_std', 0), 1),
            "precip_mean_mm":     round(d['precipitation_sum_mean'], 2),
            "precip_prob_max_pct": int(d['precipitation_probability_max_mean']),
            "wind_max_mean_ms":   round(d.get('wind_speed_10m_max_mean', 0), 1),
        })

    body = {
        "location":     data.get('label', label),
        "lat":          data.get('lat'),
        "lon":          data.get('lon'),
        "elev_m":       data.get('elev'),
        "models":       data.get('models'),
        "generated_at": data.get('generated_at'),
        "forecast_days": days,
        "days":         out_days,
        "paid":         paid,
    }
    if paid and payment_info:
        body['payment'] = {
            "received_usdc": payment_info['value_usdc'],
            "from":          payment_info['from'],
        }
    else:
        body['note'] = f"Free tier ({FREE_TIER}/day per IP). Pay 0.01 USDC for unlimited access — see X-PAYMENT-REQUIRED header on /forecast."
    return jsonify(body)

# === Routes ===
@app.route('/')
def health():
    return jsonify({
        "service": "x402-weather",
        "version": "0.1.0",
        "wallet":  WALLET_ADDR,
        "chain":   f"base (id={CHAIN_ID})",
        "endpoints": {
            "/forecast?city=puentealto|litueche&days=N": f"Weather forecast ({PRICE_USDC/1e6} USDC / call, free tier {FREE_TIER}/day)",
        },
    })

@app.route('/forecast')
def forecast():
    city = request.args.get('city', 'puentealto').lower()
    try:
        days = int(request.args.get('days', 5))
    except ValueError:
        return jsonify({"error": "days must be int"}), 400

    payment_header = request.headers.get('X-PAYMENT', '')

    if not payment_header:
        ip = request.remote_addr or 'unknown'
        remaining, key = _free_remaining(ip)
        if remaining > 0:
            _calls[key] = _calls.get(key, 0) + 1
            return serve_forecast(city, days, paid=False)
        # exhausted → require payment
        req = payment_requirements(request.url)
        return challenge_402(req)

    # Verify payment
    try:
        info = verify_payment(payment_header)
    except Exception as e:
        req = payment_requirements(request.url)
        resp = challenge_402(req)
        resp.headers['X-PAYMENT-ERROR'] = str(e)
        return resp

    return serve_forecast(city, days, paid=True, payment_info=info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
