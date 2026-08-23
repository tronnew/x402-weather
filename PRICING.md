# x402 Weather API — Pricing

## Free Tier
- **10 calls per IP per day** for any endpoint
- No account or API key needed
- Perfect for testing

## Paid Endpoints

| Endpoint | Price | Description |
|---|---|---|
| `GET /forecast` | $0.05 USDC | 5-day ensemble weather |
| `POST /scrape` | $0.10 USDC | Stealth web scraping |
| `GET /addr` | $0.05 USDC | Base L2 address report |
| `GET /ens` | $0.02 USDC | ENS lookup |
| `GET /tx` | $0.02 USDC | Transaction decoder |

## How to Pay
1. Make a request without payment
2. Server returns HTTP 402 with `X-PAYMENT-REQUIRED` header
3. Sign the EIP-712 message with your wallet
4. Resend with `X-PAYMENT` header containing the signature
5. Server verifies and returns data

## Chain & Token
- **Network:** Base L2 (chainId 8453)
- **Token:** USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)
- **Payment recipient:** `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
