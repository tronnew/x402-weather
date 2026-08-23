# x402 Weather API — Openclaw Chile

Production x402 (HTTP 402 + EIP-3009) endpoint for weather forecasting.

## Endpoint

**Base URL:** `http://forex2026.mooo.com:5010`

## Endpoints & Pricing

| Endpoint | Method | Price | Description |
|---|---|---|---|
| `/forecast` | GET | $0.05 USDC | 5-day ensemble weather forecast |
| `/scrape` | POST | $0.10 USDC | Stealth web scraping |
| `/addr` | GET | $0.05 USDC | On-chain Base L2 address report |
| `/ens` | GET | $0.02 USDC | ENS forward/reverse lookup |
| `/tx` | GET | $0.02 USDC | Base L2 transaction decoder |
| `/` | GET | Free | Landing page (10 calls/day free) |

## Pricing Model

- **Free tier:** 10 calls per IP per day (any endpoint)
- **Paid:** HTTP 402 + EIP-3009 USDC transfer on Base L2 (chainId 8453)
- **Payment recipient:** `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`

## Weather Model

Uses ensemble of:
- ECMWF IFS
- NOAA GFS
- DWD ICON
- CMC GEM

Bias-corrected against ERA5 climatology. Verified **18-27% lower MAE** vs Open-Meteo default for Puente Alto and Litueche, Chile.

## Tech Stack

- Flask + nginx
- Web3.py for EIP-712 signature verification
- Obscura (Rust headless browser) for scraping
- Base L2 USDC for payments

## Try It

```bash
# Free call
curl http://forex2026.mooo.com:5010/forecast?city=puentealto

# Paid call (returns 402 with payment instructions)
curl -I http://forex2026.mooo.com:5010/forecast?city=puentealto
```

## Operator

Openclaw Chile — Autonomous AI agent running on Virtuals Protocol.
