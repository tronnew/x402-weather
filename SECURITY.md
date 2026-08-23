# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | ✅ Currently supported |

## Reporting a Vulnerability

Report security issues to the maintainer directly.

## Smart Contract Security

This API uses:
- **EIP-712** for typed data signing
- **EIP-3009** for USDC transfers on Base L2
- No private keys ever leave the client
- All transactions are signed locally

## Payment Security

- Server never has access to client private keys
- Payments are authorization-based (approve + call pattern)
- Max amount and timeout prevent overcharging
