# x402 Weather API — Documentation

## Base URL
```
http://forex2026.mooo.com:5010
```

## Authentication
This API uses x402 (EIP-3009) protocol. No API key needed — payments are self-contained in the request headers.

## Endpoints

### GET /
Health check and API documentation.

**Free:** 10 calls per IP per day.

### GET /forecast
Get 5-day weather forecast for Puente Alto or Litueche, Chile.

| Parameter | Type | Description |
|---|---|---|
| `city` | string | `puentealto` or `litueche` (default: puentealto) |

**Paid:** $0.05 USDC (via x402/EIP-3009)

**Response:**
```json
{
  "city": "puentealto",
  "days": [
    {
      "day": 1,
      "date": "2026-08-24",
      "tmax_max_c": 18.5,
      "tmin_min_c": 7.2,
      "precip_mean_mm": 0.0,
      "precip_prob_max_pct": 12,
      "wind_max_kmh": 15,
      "condition": "sunny"
    }
  ]
}
```

### POST /scrape
Stealth web scraping with headless browser (Obscura).

| Parameter | Type | Description |
|---|---|---|
| `url` | string | URL to scrape |
| `prompt` | string | What to extract |

**Paid:** $0.10 USDC

### GET /addr?address=0x...
On-chain Base L2 address report — balance, tokens, recent txs.

**Paid:** $0.05 USDC

### GET /ens?name=vitalik.eth
ENS lookup on Base L2.

**Paid:** $0.02 USDC

### GET /tx?hash=0x...
Base L2 transaction decoder.

**Paid:** $0.02 USDC

## Payment Flow

1. Client sends request **without** payment
2. Server returns **HTTP 402** with `X-PAYMENT-REQUIRED` header containing:
   ```json
   {
     "x402Version": 1,
     "scheme": "exact",
     "network": "base",
     "payTo": "0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE",
     "maxAmountRequired": "10000",
     "maxTimeoutSeconds": 600,
     "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
     "validAfter": 1787524452,
     "validBefore": 1787525052,
     "nonce": "0x..."
   }
   ```
3. Client signs EIP-712 `TransferWithAuthorization` message
4. Client resends request with `X-PAYMENT` header containing the signature
5. Server verifies and serves the data

## Pricing Summary

| Endpoint | Price | Notes |
|---|---|---|
| `/` | Free | 10/day per IP |
| `/forecast` | $0.05 | 5-day ensemble |
| `/scrape` | $0.10 | Headless browser |
| `/addr` | $0.05 | On-chain report |
| `/ens` | $0.02 | ENS lookup |
| `/tx` | $0.02 | Tx decoder |

**Chain:** Base L2 (chainId 8453)
**Payment recipient:** `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
**USDC contract:** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
