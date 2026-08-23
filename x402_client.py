#!/usr/bin/env python3
"""
x402 client library for Python.
Handles EIP-712 payment signing for x402 endpoints on Base L2.
"""
import requests, json, time, eth_account, web3
from eth_account import Account
from eth_account.messages import encode_structured_data
from web3 import Web3

class X402Client:
    def __init__(self, wallet_private_key: str, base_url: str):
        self.key = wallet_private_key
        self.account = Account.from_key(wallet_private_key)
        self.base_url = base_url.rstrip('/')
        self.w3 = Web3()
    
    def request(self, path: str, method='GET', params=None, data=None, headers=None):
        """Make a request, handling x402 payment flow automatically."""
        url = f"{self.base_url}{path}"
        headers = headers or {}
        
        # First attempt without payment
        if method == 'GET':
            r = requests.get(url, params=params, headers=headers, timeout=30)
        else:
            r = requests.post(url, params=params, json=data, headers=headers, timeout=30)
        
        if r.status_code != 402:
            return r.json() if r.content else {}
        
        # Parse payment requirements
        req = json.loads(r.headers['X-PAYMENT-REQUIRED'])
        payment = self._build_payment(req)
        
        # Second attempt with payment
        headers['X-PAYMENT'] = json.dumps(payment)
        if method == 'GET':
            r = requests.get(url, params=params, headers=headers, timeout=30)
        else:
            r = requests.post(url, params=params, json=data, headers=headers, timeout=30)
        
        return r.json() if r.content else {}
    
    def _build_payment(self, req):
        domain = {
            "name": "USDC",
            "version": "1",
            "chainId": 8453,
            "verifyingContract": req['asset']
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
        
        msg = {
            "from": self.account.address,
            "to": req['payTo'],
            "value": int(req['maxAmountRequired']),
            "validAfter": int(req['validAfter']),
            "validBefore": int(req['validBefore']),
            "nonce": req['nonce']
        }
        
        msg_encoded = encode_structured_data(domain=domain, message=msg)
        signed = self.account.sign_message(msg_encoded)
        
        return {
            "payload": {
                "authorization": {
                    "from": self.account.address,
                    "to": req['payTo'],
                    "value": str(msg['value']),
                    "validAfter": str(msg['validAfter']),
                    "validBefore": str(msg['validBefore']),
                    "nonce": msg['nonce']
                },
                "signature": signed.signature.hex()
            }
        }


if __name__ == "__main__":
    # Example usage
    import os
    client = X402Client(
        wallet_private_key=os.environ.get('PRIVATE_KEY', '0x...'),
        base_url='http://forex2026.mooo.com:5010'
    )
    
    # Free tier call
    result = client.request('/forecast', params={'city': 'puentealto'})
    print(json.dumps(result, indent=2)[:500])
