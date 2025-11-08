#!/usr/bin/env python3
"""
Quick Bitcoin Tools - Simple utilities for Bitcoin lessons
"""

import hashlib
import os
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x
import bitcoin

bitcoin.SelectParams('mainnet')

def generate_address():
    """Generate a simple Bitcoin address"""
    secret = CBitcoinSecret.from_secret_bytes(os.urandom(32))
    pub = secret.pub
    address = P2PKHBitcoinAddress.from_pubkey(pub)
    return {
        'private_key': str(secret),
        'public_key': b2x(pub),
        'address': str(address)
    }

def sha256(data):
    """Single SHA256 hash"""
    if isinstance(data, str):
        data = data.encode()
    return b2x(hashlib.sha256(data).digest())

def double_sha256(data):
    """Double SHA256 (Bitcoin standard)"""
    if isinstance(data, str):
        data = data.encode()
    return b2x(hashlib.sha256(hashlib.sha256(data).digest()).digest())

def hash160(data):
    """Hash160: SHA256 then RIPEMD160 (used in addresses)"""
    if isinstance(data, str):
        data = data.encode()
    sha = hashlib.sha256(data).digest()
    ripemd = hashlib.new('ripemd160', sha).digest()
    return b2x(ripemd)

# Example usage
if __name__ == "__main__":
    print("Quick Bitcoin Tools Demo\n")

    # Generate an address
    addr_info = generate_address()
    print("Generated Bitcoin Address:")
    print(f"  Address: {addr_info['address']}")
    print(f"  Private: {addr_info['private_key']}")
    print(f"  Public:  {addr_info['public_key'][:66]}...\n")

    # Hash examples
    message = "Bitcoin Lesson Example"
    print(f"Hashing: '{message}'")
    print(f"  SHA256:        {sha256(message)}")
    print(f"  Double-SHA256: {double_sha256(message)}")
    print(f"  Hash160:       {hash160(message)}")
