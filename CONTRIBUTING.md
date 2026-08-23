# Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a PR

## Development Setup

```bash
git clone https://github.com/tronnew/x402-weather.git
cd x402-weather
pip install -e .
```

## Running Tests

```bash
# Test endpoint
curl http://forex2026.mooo.com:5010/forecast?city=puentealto

# Test 402 response
curl -I http://forex2026.mooo.com:5010/forecast?city=puentealto
```
