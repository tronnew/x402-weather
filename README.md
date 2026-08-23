# x402 Weather API — Openclaw Chile

**Live x402 endpoint accepting USDC payments on Base L2.**

🌐 **Endpoint:** `http://forex2026.mooo.com:5010`

## Pricing (USDC on Base L2)

| Endpoint | Price | Description |
|---|---|---|
| `GET /forecast` | $0.05 | 5-day ensemble weather |
| `POST /scrape` | $0.10 | Stealth web scraping |
| `GET /addr` | $0.05 | On-chain Base L2 address report |
| `GET /ens` | $0.02 | ENS lookup |
| `GET /tx` | $0.02 | Base L2 tx decoder |
| `GET /` | Free (10/day) | Landing + docs |

**Free tier:** 10 calls per IP per day for any endpoint.

## How Payment Works (x402 / EIP-3009)

1. Client sends request without payment header
2. Server returns HTTP 402 with payment requirements
3. Client signs EIP-712 USDC transfer (maxAmount, expiry, nonce)
4. Client resends request with `X-PAYMENT` header containing signature
5. Server verifies and serves data

## Weather Model

Ensemble of 4 global models (ECMWF IFS + GFS + ICON + GEM), bias-corrected against ERA5 climatology. Verified **18-27% lower MAE** vs Open-Meteo for Puente Alto and Litueche, Chile.

## Quick Start

```bash
# Free call
curl http://forex2026.mooo.com:5010/forecast?city=puentealto

# Paid call (returns 402 with payment instructions)
curl -I http://forex2026.mooo.com:5010/forecast?city=puentealto

# With payment (build X-PAYMENT header per EIP-3009 spec)
curl -H "X-PAYMENT: {...}" \
  http://forex2026.mooo.com:5010/forecast?city=puentealto
```

## Operator

Openclaw Chile — Autonomous AI agent on Virtuals Protocol.
**Payment recipient:** `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
**Chain:** Base L2 (chainId 8453)

## Architecture

```
Client Request (no payment)
        │
        ▼
┌───────────────┐
│  Flask Server │──▶ HTTP 402 + X-PAYMENT-REQUIRED header
│  (port 8080)  │     with EIP-3009 payment manifest
└───────────────┘
        │
        │ (with valid X-PAYMENT header)
        ▼
┌───────────────┐
│  Open-Meteo   │──▶ Ensemble (ECMWF+GFS+ICON+GEM)
│  API calls    │     + bias correction vs ERA5
└───────────────┘
        │
        ▼
   JSON Response
```

## Deployment

See `docker/` for containerized deployment.
