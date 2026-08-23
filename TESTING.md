# Testing the x402 Weather API

## Quick Test

```bash
# Test free tier (first 2 calls per IP per day return actual data)
curl http://forex2026.mooo.com:5010/forecast?city=puentealto

# After free tier exhausted, returns HTTP 402:
curl -I http://forex2026.mooo.com:5010/forecast?city=puentealto
```

## Expected Responses

### Free Tier Response (HTTP 200)
```json
{"days":[{"day":1,"precip_mean_mm":0.0,"precip_prob_max_pct":0,"tmax_max_c":20.0,...}]}
```

### Paid Tier Response (HTTP 402)
```json
{"error":"Payment required","payTo":"0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE","amount":"0.01 USDC"}
```

## Build Your Own x402 Client

See `x402_client.py` for a full Python implementation with EIP-712 signing.

## Verification

- x402 protocol: EIP-3009 (transferWithAuthorization)
- Chain: Base L2 (chainId 8453)
- Payment recipient: `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
- USDC contract: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
