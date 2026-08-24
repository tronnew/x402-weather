# x402 Weather API 🌤️

**Autonomous weather API earning USDC on Base L2 via x402 protocol.**

- 🌡️ Ensemble model: ECMWF IFS + GFS + ICON + GEM, bias-corrected vs ERA5 climatology
- 📍 Cities: Puente Alto, Litueche (Chile)
- 🧠 **Accuracy: 18–27% lower MAE vs Open-Meteo on 2025 observed data**
  - Puente Alto: **3.65°C MAE** vs Open-Meteo 4.97°C (**27% better**)
  - Litueche: **3.59°C MAE** vs Open-Meteo 4.38°C (**18% better**)
- 💰 Free tier: 1 call/day per IP
- 💵 Paid: 0.05 USDC/call via EIP-3009 (Base L2)
- 🔗 Payment address: `0x6dDCd5CC6f0614A291954daf2fF1B41DA44363DE`
- 🔗 Endpoint: `http://forex2026.mooo.com:5010`

## Quick Start

```bash
# Free call (1/day per IP)
curl "http://forex2026.mooo.com:5010/forecast?city=puentealto"

# Paid call — see API.md for EIP-3009 integration
```

## Performance

| City | Our MAE | Open-Meteo MAE | Improvement |
|------|---------|----------------|-------------|
| Puente Alto | 3.65°C | 4.97°C | **27%** |
| Litueche | 3.59°C | 4.38°C | **18%** |

*Based on same-calendar observations, August 2025. MAE = Mean Absolute Error vs official station data.*

## Tech Stack

Python 3 · Flask · Gunicorn · nginx · x402 protocol · Base L2 (Chain ID: 8453) · EIP-3009

## License

MIT — github.com/tronnew/x402-weather
