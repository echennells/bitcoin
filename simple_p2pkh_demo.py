#!/usr/bin/env python3
"""
Simple Bitcoin P2PKH Transaction Demo

A beginner-friendly explanation of how Bitcoin validates transactions
"""

import hashlib
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x
import bitcoin

bitcoin.SelectParams('mainnet')

def print_box(title, content, width=70):
    """Print content in a nice box"""
    print("┌" + "─" * (width - 2) + "┐")
    print("│ " + title.center(width - 4) + " │")
    print("├" + "─" * (width - 2) + "┤")
    for line in content:
        # Truncate if too long
        display_line = line[:width-4] if len(line) > width-4 else line
        padding = width - 4 - len(display_line)
        print("│ " + display_line + " " * padding + " │")
    print("└" + "─" * (width - 2) + "┘")

def simple_demo():
    """Simple P2PKH demonstration"""

    print("\n" + "="*70)
    print("BITCOIN TRANSACTION VALIDATION - THE SIMPLE VERSION")
    print("="*70)

    print("\n🎯 THE GOAL: Prove you own a Bitcoin address without revealing your")
    print("   private key (the secret password)\n")

    # Generate keys
    secret = CBitcoinSecret.from_secret_bytes(b'\x01' * 32)
    pub_key = secret.pub
    pub_key_hash = hashlib.new('ripemd160', hashlib.sha256(pub_key).digest()).digest()
    address = P2PKHBitcoinAddress.from_pubkey(pub_key)

    # Show the basics
    print_box("THE SETUP", [
        "",
        "Alice has:",
        f"  🔐 Private Key (SECRET!)  = {str(secret)[:20]}...",
        f"  🔑 Public Key             = {b2x(pub_key)[:20]}...",
        f"  📫 Bitcoin Address        = {address}",
        "",
        "Alice received 1 BTC at this address.",
        "Now she wants to spend it.",
        ""
    ])

    input("\nPress Enter to continue...\n")

    # The Challenge
    print_box("THE CHALLENGE", [
        "",
        "Alice needs to prove:",
        "  ✓ She knows the private key for this address",
        "  ✓ WITHOUT revealing the private key itself",
        "",
        "How? With a DIGITAL SIGNATURE!",
        ""
    ])

    input("\nPress Enter to see how validation works...\n")

    # Simple visualization
    print("\n" + "="*70)
    print("HOW BITCOIN VALIDATES THE TRANSACTION")
    print("="*70 + "\n")

    print("Think of it like a 3-step verification process:\n")

    # Step 1
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  STEP 1: Alice provides two things                         │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("   📝 Signature (proves she has the private key)")
    print("   🔑 Public Key")
    print()

    input("Press Enter for Step 2...\n")

    # Step 2
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  STEP 2: Bitcoin checks - does the Public Key match?       │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()
    print("   Bitcoin takes Alice's Public Key and hashes it:")
    print(f"   🔑 Public Key → [HASH] → {b2x(pub_key_hash)[:20]}...")
    print()
    print("   Then compares to the address that received the coins:")
    print(f"   📫 Address contains     → {b2x(pub_key_hash)[:20]}...")
    print()
    print("   ✅ They MATCH! Alice is using the right public key.")
    print()

    input("Press Enter for Step 3...\n")

    # Step 3
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│  STEP 3: Bitcoin verifies the signature                    │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()
    print("   Bitcoin checks:")
    print("   📝 Is this signature valid for this transaction?")
    print("   🔑 Was it created by the private key matching this public key?")
    print()
    print("   This uses ECDSA (Elliptic Curve Digital Signature Algorithm)")
    print("   Math magic that proves Alice has the private key")
    print("   WITHOUT revealing it!")
    print()
    print("   ✅ Signature is VALID!")
    print()

    input("Press Enter to see the result...\n")

    # Result
    print("\n" + "="*70)
    print("TRANSACTION VALIDATED! ✅")
    print("="*70)
    print()
    print_box("WHAT JUST HAPPENED?", [
        "",
        "Bitcoin verified:",
        "  1. The public key matches the receiving address ✓",
        "  2. The signature proves Alice has the private key ✓",
        "",
        "Alice can spend the coins WITHOUT revealing her private key!",
        "",
        "This is the magic of public key cryptography!",
        ""
    ])

    print("\n" + "="*70)
    print("VISUAL SUMMARY")
    print("="*70 + "\n")

    print("         Alice's Wallet                Bitcoin Network")
    print("         ─────────────                ───────────────")
    print()
    print("      🔐 Private Key")
    print("           │")
    print("           ├──→ Creates Signature ──→ 📝 Signature")
    print("           │                              ↓")
    print("           └──→ Derives ──→ 🔑 Public Key → Hash → 📫 Address")
    print("                                          ↓")
    print("                                    Verify Match? ✓")
    print("                                          ↓")
    print("                                    Check Signature? ✓")
    print("                                          ↓")
    print("                                   ✅ APPROVED!")
    print()

def show_simple_script():
    """Show the script in plain English"""
    print("\n" + "="*70)
    print("THE BITCOIN SCRIPT (In Plain English)")
    print("="*70 + "\n")

    print("When someone sends coins to Alice's address, they create a LOCK:")
    print()
    print_box("THE LOCK (scriptPubKey)", [
        "",
        "To spend these coins, you must:",
        "  1. Provide a public key",
        "  2. That hashes to: " + "79b0...5983",
        "  3. And provide a valid signature from the matching private key",
        ""
    ])

    print("\nWhen Alice spends the coins, she creates the KEY:")
    print()
    print_box("THE KEY (scriptSig)", [
        "",
        "Here is:",
        "  1. My signature",
        "  2. My public key",
        ""
    ])

    print("\nBitcoin tries the key in the lock:")
    print("  → Does the public key hash match? ✓")
    print("  → Is the signature valid? ✓")
    print("  → UNLOCKED! Transaction approved ✅")

def main():
    simple_demo()

    input("\n\nPress Enter to see the technical version...\n")

    show_simple_script()

    print("\n" + "="*70)
    print("That's P2PKH in a nutshell!")
    print("="*70)
    print("\n💡 Key Takeaway: Bitcoin uses cryptography to let you prove")
    print("   ownership without revealing your secret password!\n")

if __name__ == "__main__":
    main()
