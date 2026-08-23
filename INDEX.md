# x402 Weather API — Index

## Quick Links
- 🌐 **Live Endpoint:** http://forex2026.mooo.com:5010
- 📂 **GitHub:** https://github.com/tronnew/x402-weather
- 🔗 **Payment Address:** `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
- ⛓️ **Chain:** Base L2 (chainId 8453)

## Endpoints

| Method | Path | Price | Description |
|---|---|---|---|
| GET | `/` | Free (10/day) | API docs |
| GET | `/forecast?city=puentealto` | $0.05 | 5-day ensemble |
| POST | `/scrape` | $0.10 | Headless browser |
| GET | `/addr?address=0x...` | $0.05 | Address report |
| GET | `/ens?name=vitalik.eth` | $0.02 | ENS lookup |
| GET | `/tx?hash=0x...` | $0.02 | Tx decoder |

## Libraries
- `x402_client.py` — Simple Python client
- `examples_advanced.py` — Full EIP-712 signing example

## Deployment
- `docker/` — Docker + docker-compose
- `DEPLOY.md` — Full deployment guide
