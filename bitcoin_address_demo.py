#!/usr/bin/env python3
"""
Bitcoin Address Generation Demo
Educational script for generating various types of Bitcoin addresses and hashes
"""

import hashlib
import os
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2WPKHBitcoinAddress
from bitcoin.core import b2x, lx, x, b2lx
from bitcoin.core.script import CScript, OP_RETURN
import bitcoin

# Set to mainnet for real addresses, or testnet for testing
bitcoin.SelectParams('mainnet')

def generate_legacy_address():
    """Generate a legacy P2PKH address (starts with 1)"""
    # Generate a random private key
    secret = CBitcoinSecret.from_secret_bytes(os.urandom(32))

    # Get the public key
    pub = secret.pub

    # Create P2PKH address
    address = P2PKHBitcoinAddress.from_pubkey(pub)

    print("=== Legacy P2PKH Address (1...) ===")
    print(f"Private Key (WIF): {secret}")
    print(f"Public Key (hex): {b2x(pub)}")
    print(f"Address: {address}")
    print()

def generate_segwit_address():
    """Generate a native SegWit address (starts with bc1q)"""
    # Generate a random private key
    secret = CBitcoinSecret.from_secret_bytes(os.urandom(32))

    # Get the public key
    pub = secret.pub

    # Create P2WPKH address
    address = P2WPKHBitcoinAddress.from_scriptPubKey(
        CScript([0, hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()])
    )

    print("=== Native SegWit P2WPKH Address (bc1q...) ===")
    print(f"Private Key (WIF): {secret}")
    print(f"Public Key (hex): {b2x(pub)}")
    print(f"Address: {address}")
    print()

def demonstrate_hashing():
    """Demonstrate common Bitcoin hashing operations"""
    print("=== Bitcoin Hashing Examples ===")

    # Example data
    data = b"Hello Bitcoin!"

    # SHA256
    sha256_hash = hashlib.sha256(data).digest()
    print(f"Data: {data.decode()}")
    print(f"SHA256: {b2x(sha256_hash)}")

    # Double SHA256 (used in Bitcoin)
    double_sha256 = hashlib.sha256(sha256_hash).digest()
    print(f"Double SHA256: {b2x(double_sha256)}")

    # RIPEMD160 (SHA256 then RIPEMD160 - used for addresses)
    ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()
    print(f"RIPEMD160(SHA256): {b2x(ripemd160)}")
    print()

def demonstrate_op_return():
    """Create an OP_RETURN script (for embedding data)"""
    print("=== OP_RETURN Data Embedding ===")

    message = b"Educational Bitcoin Demo"
    script = CScript([OP_RETURN, message])

    print(f"Message: {message.decode()}")
    print(f"OP_RETURN Script: {b2x(script)}")
    print()

def main():
    print("Bitcoin Address & Hash Generation Demo")
    print("=" * 50)
    print()

    # Generate addresses
    generate_legacy_address()
    generate_segwit_address()

    # Demonstrate hashing
    demonstrate_hashing()

    # Demonstrate OP_RETURN
    demonstrate_op_return()

    print("=" * 50)
    print("Note: These are randomly generated examples for educational purposes.")
    print("Never use these keys for real funds!")

if __name__ == "__main__":
    main()
