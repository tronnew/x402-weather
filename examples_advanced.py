#!/usr/bin/env python3
"""
Advanced x402 Weather API client examples.
Shows how to handle EIP-712 payment signing for x402 endpoints.
"""
import os, json, time, eth_account, web3
from eth_account import Account
from eth_account.messages import encode_structured_data
from web3 import Web3
import requests

BASE_URL = "http://forex2026.mooo.com:5010"

def get_wallet():
    """Load wallet from PRIVATE_KEY env var."""
    key = os.environ.get('PRIVATE_KEY')
    if not key:
        raise ValueError("Set PRIVATE_KEY environment variable")
    return Account.from_key(key)

def request_with_payment(path, wallet, method='GET', params=None):
    """Make request, handling 402 payment flow automatically."""
    url = BASE_URL + path
    headers = {}
    
    # First attempt without payment
    if method == 'GET':
        r = requests.get(url, params=params, headers=headers, timeout=30)
    else:
        r = requests.post(url, json=params, headers=headers, timeout=30)
    
    if r.status_code != 402:
        return r.json() if r.content else {}
    
    # Parse payment requirements
    req = json.loads(r.headers['X-PAYMENT-REQUIRED'])
    
    # Build EIP-712 signature
    domain = {
        "name": "USDC",
        "version": "1",
        "chainId": 8453,
        "verifyingContract": req['asset']
    }
    
    msg = {
        "from": wallet.address,
        "to": req['payTo'],
        "value": int(req['maxAmountRequired']),
        "validAfter": int(req['validAfter']),
        "validBefore": int(req['validBefore']),
        "nonce": req['nonce']
    }
    
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"}
        ],
        "TransferWithAuthorization": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "validAfter", "type": "uint256"},
            {"name": "validBefore", "type": "uint256"},
            {"name": "nonce", "type": "bytes32"}
        ]
    }
    
    msg_encoded = encode_structured_data(domain=domain, message=msg)
    signed = wallet.sign_message(msg_encoded)
    
    payment = {
        "payload": {
            "authorization": {
                "from": wallet.address,
                "to": req['payTo'],
                "value": str(msg['value']),
                "validAfter": str(msg['validAfter']),
                "validBefore": str(msg['validBefore']),
                "nonce": msg['nonce']
            },
            "signature": signed.signature.hex()
        }
    }
    
    headers['X-PAYMENT'] = json.dumps(payment)
    
    if method == 'GET':
        r = requests.get(url, params=params, headers=headers, timeout=30)
    else:
        r = requests.post(url, json=params, headers=headers, timeout=30)
    
    return r.json() if r.content else {}

if __name__ == "__main__":
    wallet = get_wallet()
    print(f"Wallet: {wallet.address}")
    
    # Free call (within free tier)
    result = request_with_payment('/forecast', wallet, params={'city': 'puentealto'})
    print(json.dumps(result, indent=2)[:300])
