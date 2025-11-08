#!/usr/bin/env python3
"""
P2PKH Explained Like You're 5

Just the core concept.
"""

import hashlib
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x
import bitcoin

bitcoin.SelectParams('mainnet')

def print_header(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n")

def print_section(emoji, title):
    print(f"\n{emoji} {title}")
    print("-" * 60)

def main():
    print_header("BITCOIN P2PKH - THE SUPER SIMPLE VERSION")

    print("Imagine you have a safe with money inside.")
    print("How do you prove you own it?\n")

    input("Press Enter to continue...\n")

    # Generate example keys
    secret = CBitcoinSecret.from_secret_bytes(b'\x01' * 32)
    pub_key = secret.pub
    pub_key_hash = hashlib.new('ripemd160', hashlib.sha256(pub_key).digest()).digest()
    address = P2PKHBitcoinAddress.from_pubkey(pub_key)

    print_section("🔐", "STEP 1: YOU GET TWO KEYS")
    print()
    print("  SECRET KEY (Never show anyone!)")
    print("  └─ Like a password only YOU know")
    print()
    print("  PUBLIC KEY (Safe to share)")
    print("  └─ Like your username, anyone can see it")
    print()
    print("  From your public key, Bitcoin makes your ADDRESS:")
    print(f"  📫 {address}")
    print()

    input("Press Enter to continue...\n")

    print_section("💰", "STEP 2: SOMEONE SENDS YOU BITCOIN")
    print()
    print("  They send coins to your address: " + str(address)[:20] + "...")
    print()
    print("  The SENDER creates a LOCK on those coins:")
    print("  (This lock is called the 'locking script' or 'scriptPubKey')")
    print()
    print("  ┌─────────────────────────────────────────────┐")
    print("  │  🔒 These coins are locked!                 │")
    print("  │                                             │")
    print("  │  To unlock, you must prove:                │")
    print("  │  • You have the SECRET KEY                 │")
    print("  │  • That matches this address               │")
    print("  └─────────────────────────────────────────────┘")
    print()

    input("Press Enter to continue...\n")

    print_section("✍️", "STEP 3: YOU WANT TO SPEND THE COINS")
    print()
    print("  You can't just say \"I own this!\"")
    print("  You need to PROVE it.")
    print()
    print("  How? With a SIGNATURE!")
    print()
    print("  Think of it like signing a check:")
    print("  • Only YOU can make your signature (you need the SECRET KEY)")
    print("  • Anyone can verify it's really yours (using your PUBLIC KEY)")
    print()

    input("Press Enter to continue...\n")

    print_section("✅", "STEP 4: BITCOIN CHECKS YOUR PROOF")
    print()
    print("  Bitcoin does TWO simple checks using a STACK:")
    print()
    print("  First, your signature and public key go on the stack:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ STACK:                                      │")
    print("  │   → Public Key                              │")
    print("  │   → Signature                               │")
    print("  └─────────────────────────────────────────────┘")
    print()

    input("Press Enter to see CHECK #1...\n")

    print("  CHECK #1: Does your public key match the address?")
    print()
    print("  OP_DUP - Duplicate the public key:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ STACK:                                      │")
    print("  │   → Public Key (copy)                       │")
    print("  │   → Public Key (original)                   │")
    print("  │   → Signature                               │")
    print("  └─────────────────────────────────────────────┘")
    print()
    print("  OP_HASH160 - Hash the top public key:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ STACK:                                      │")
    print("  │   → Hashed Public Key                       │")
    print("  │   → Public Key                              │")
    print("  │   → Signature                               │")
    print("  └─────────────────────────────────────────────┘")
    print()
    print("  Push the expected address hash from the lock:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ STACK:                                      │")
    print("  │   → Expected Address Hash                   │")
    print("  │   → Hashed Public Key                       │")
    print("  │   → Public Key                              │")
    print("  │   → Signature                               │")
    print("  └─────────────────────────────────────────────┘")
    print()
    print("  OP_EQUALVERIFY - Do they match?")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ Compare top two items:                      │")
    print("  │ Expected Hash == Hashed Public Key?         │")
    print("  │                                             │")
    print("  │ ✓ YES! Remove both, continue...             │")
    print("  │                                             │")
    print("  │ STACK NOW:                                  │")
    print("  │   → Public Key                              │")
    print("  │   → Signature                               │")
    print("  └─────────────────────────────────────────────┘")
    print()

    input("Press Enter to see CHECK #2...\n")

    print("  CHECK #2: Is your signature valid?")
    print()
    print("  OP_CHECKSIG - Verify the signature:")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ Takes: Signature + Public Key               │")
    print("  │                                             │")
    print("  │ Verifies: Did the private key matching      │")
    print("  │ this public key create this signature?      │")
    print("  │                                             │")
    print("  │ Uses ECDSA math - proves you have the       │")
    print("  │ secret key WITHOUT revealing it!            │")
    print("  │                                             │")
    print("  │ Result: Push TRUE on stack                  │")
    print("  └─────────────────────────────────────────────┘")
    print()
    print("  ┌─────────────────────────────────────────────┐")
    print("  │ FINAL STACK:                                │")
    print("  │   → TRUE                                    │")
    print("  │                                             │")
    print("  │ ✓ Transaction APPROVED!                     │")
    print("  └─────────────────────────────────────────────┘")
    print()

    input("Press Enter to continue...\n")

    print_section("🎉", "DONE! THE COINS ARE SPENT")
    print()
    print("  Bitcoin confirmed:")
    print("  ✓ You have the right public key")
    print("  ✓ You proved you have the secret key (via signature)")
    print()
    print("  The coins move to wherever you sent them!")
    print()

    input("Press Enter to see the visual summary...\n")

    print_header("VISUAL SUMMARY")

    print("""
    THE FULL PICTURE:

    When someone SENDS coins TO YOU:
    ┌────────────────────────────────────────┐
    │ The SENDER creates a LOCK:             │
    │ "These coins can only be spent by      │
    │  someone who proves they have the      │
    │  secret key for this address"          │
    └────────────────────────────────────────┘
                     │
                     │ Coins sit here locked
                     ↓

    When YOU SPEND the coins:
    ┌────────────────────────────────────────┐
    │ You provide:                           │
    │  📝 Your signature (proves secret key) │
    │  🔑 Your public key                    │
    └────────────────────────────────────────┘
                     │
                     ↓
    ┌────────────────────────────────────────┐
    │ Bitcoin checks:                        │
    │  ✓ Public key → address? YES           │
    │  ✓ Signature valid? YES                │
    │                                        │
    │  🎉 UNLOCK! Coins can move!            │
    └────────────────────────────────────────┘
    """)

    print_header("THAT'S P2PKH!")

    print("""
    THREE KEY POINTS:

    1. 🔐 You have a SECRET KEY (never share)

    2. 📝 You can create SIGNATURES with your secret key
       (proves you have it without revealing it)

    3. ✅ Bitcoin checks your signature and public key
       to unlock the coins


    That's it! Just: Lock → Prove → Unlock
    """)

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
