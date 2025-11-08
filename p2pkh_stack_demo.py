#!/usr/bin/env python3
"""
Bitcoin P2PKH Script Stack Execution Demo

This demonstrates how Bitcoin validates a Pay-to-Public-Key-Hash (P2PKH)
transaction using a stack-based scripting system.
"""

import hashlib
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core import b2x
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
import bitcoin

bitcoin.SelectParams('mainnet')

class StackVisualizer:
    """Visualizes the Bitcoin script stack execution"""

    def __init__(self):
        self.stack = []
        self.step_number = 0

    def show_stack(self, operation="", description=""):
        """Display current stack state"""
        self.step_number += 1

        print(f"\n{'='*70}")
        print(f"Step {self.step_number}: {operation}")
        if description:
            print(f"Description: {description}")
        print(f"{'='*70}")

        if not self.stack:
            print("Stack: [EMPTY]")
        else:
            print("Stack (top -> bottom):")
            for i, item in enumerate(reversed(self.stack)):
                prefix = "  ↑ TOP" if i == 0 else "  ↓"
                # Truncate long items for display
                display_item = str(item)[:60] + "..." if len(str(item)) > 60 else str(item)
                print(f"{prefix}  {display_item}")

    def push(self, item, label=""):
        """Push item onto stack"""
        self.stack.append(item)
        return item

    def pop(self):
        """Pop item from stack"""
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self):
        """Look at top of stack without removing"""
        if self.stack:
            return self.stack[-1]
        return None

    def duplicate_top(self):
        """Duplicate top stack item"""
        if self.stack:
            self.stack.append(self.stack[-1])

    def is_true(self):
        """Check if top of stack is true"""
        return len(self.stack) > 0 and self.stack[-1] not in [0, b'', False]


def demonstrate_p2pkh_script():
    """Demonstrate P2PKH script execution step by step"""

    print("="*70)
    print("BITCOIN P2PKH TRANSACTION VALIDATION DEMO")
    print("="*70)
    print("\nThis shows how Bitcoin validates a standard P2PKH transaction")
    print("using a stack-based scripting language.\n")

    # Generate a key pair and address
    print("\n" + "="*70)
    print("SETUP: Generate Key Pair and Address")
    print("="*70)

    secret = CBitcoinSecret.from_secret_bytes(b'\x01' * 32)  # Fixed key for consistent demo
    pub_key = secret.pub
    address = P2PKHBitcoinAddress.from_pubkey(pub_key)

    # Calculate pubKeyHash (what goes in the locking script)
    pub_key_hash = hashlib.new('ripemd160', hashlib.sha256(pub_key).digest()).digest()

    print(f"\nPrivate Key: {secret}")
    print(f"Public Key:  {b2x(pub_key)}")
    print(f"PubKeyHash:  {b2x(pub_key_hash)}")
    print(f"Address:     {address}")

    # Show the scripts
    print("\n" + "="*70)
    print("SCRIPT COMPONENTS")
    print("="*70)

    print("\nLocking Script (scriptPubKey) - Created when receiving funds:")
    print("  OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG")
    print(f"  └─ pubKeyHash: {b2x(pub_key_hash)[:40]}...")

    print("\nUnlocking Script (scriptSig) - Created when spending funds:")
    print("  <signature> <pubKey>")
    print(f"  ├─ signature: <DER-encoded-signature> (simulated)")
    print(f"  └─ pubKey:    {b2x(pub_key)[:40]}...")

    # Simulate the stack execution
    print("\n" + "="*70)
    print("STACK EXECUTION WALKTHROUGH")
    print("="*70)
    print("\nThe unlocking script runs first, then the locking script.")
    print("If the stack ends with TRUE, the transaction is valid.\n")

    input("Press Enter to start execution...")

    stack = StackVisualizer()

    # Simulated signature (in reality this would be a real ECDSA signature)
    signature = b"<ECDSA_SIGNATURE>"

    # Step 1: Push signature
    stack.push(signature, "signature")
    stack.show_stack(
        "Push <signature>",
        "First element of scriptSig (unlocking script)"
    )

    # Step 2: Push public key
    stack.push(pub_key, "pubKey")
    stack.show_stack(
        "Push <pubKey>",
        "Second element of scriptSig (unlocking script)"
    )

    print("\n" + "-"*70)
    print("Unlocking script complete. Now executing locking script...")
    print("-"*70)
    input("Press Enter to continue...")

    # Step 3: OP_DUP
    stack.duplicate_top()
    stack.show_stack(
        "OP_DUP",
        "Duplicates the top stack item (pubKey)"
    )

    # Step 4: OP_HASH160
    top = stack.pop()
    hashed = hashlib.new('ripemd160', hashlib.sha256(top).digest()).digest()
    stack.push(hashed, "hash160(pubKey)")
    stack.show_stack(
        "OP_HASH160",
        "Hash the top item: SHA256 then RIPEMD160"
    )

    # Step 5: Push pubKeyHash from locking script
    stack.push(pub_key_hash, "pubKeyHash (from script)")
    stack.show_stack(
        "Push <pubKeyHash>",
        "Push the expected pubKeyHash from locking script"
    )

    # Step 6: OP_EQUALVERIFY
    a = stack.pop()
    b = stack.pop()
    equal = (a == b)
    stack.show_stack(
        "OP_EQUALVERIFY",
        f"Compare top two items: {equal}. If false, transaction fails!"
    )

    if not equal:
        print("\n❌ TRANSACTION INVALID: PubKeyHash mismatch!")
        return False

    print(f"\n✓ Hash verification passed: {b2x(a)[:40]}... == {b2x(b)[:40]}...")

    # Step 7: OP_CHECKSIG
    # In reality, this verifies the signature against the public key
    # and the transaction data
    sig = stack.pop()
    pubkey = stack.pop()

    stack.show_stack(
        "OP_CHECKSIG (preparing)",
        "Pop signature and pubKey for verification"
    )

    print("\nVerifying signature...")
    print(f"  - Signature: {str(sig)[:40]}...")
    print(f"  - Public Key: {b2x(pubkey)[:40]}...")
    print(f"  - Transaction data: <tx_hash> (simulated)")

    # Simulate successful signature verification
    sig_valid = True  # In reality: verify_signature(sig, pubkey, tx_hash)
    stack.push(sig_valid)

    stack.show_stack(
        "OP_CHECKSIG (result)",
        "Push TRUE if signature is valid, FALSE otherwise"
    )

    # Final result
    print("\n" + "="*70)
    if stack.is_true():
        print("✅ TRANSACTION VALID!")
        print("="*70)
        print("\nThe stack ends with TRUE, so this transaction is accepted.")
        print("The spender proved they have the private key corresponding to")
        print(f"the address: {address}")
    else:
        print("❌ TRANSACTION INVALID!")
        print("="*70)
        print("\nThe stack does not end with TRUE.")

    return stack.is_true()


def show_script_opcodes():
    """Show the actual Bitcoin script opcodes"""

    print("\n" + "="*70)
    print("BITCOIN SCRIPT OPCODES REFERENCE")
    print("="*70)

    opcodes = [
        ("OP_DUP", "0x76", "Duplicates the top stack item"),
        ("OP_HASH160", "0xa9", "Hash top item with SHA256 then RIPEMD160"),
        ("OP_EQUALVERIFY", "0x88", "Check top two items are equal, fail if not"),
        ("OP_CHECKSIG", "0xac", "Verify signature against public key"),
    ]

    print("\nCommon P2PKH Opcodes:")
    for name, code, desc in opcodes:
        print(f"\n{name:20} ({code})")
        print(f"  └─ {desc}")

    print("\n" + "="*70)
    print("\nA complete P2PKH locking script in hex:")

    # Create actual script
    pub_key_hash = b'\x00' * 20  # Example hash
    script = CScript([OP_DUP, OP_HASH160, pub_key_hash, OP_EQUALVERIFY, OP_CHECKSIG])

    print(f"{b2x(script)}")
    print("\nBreakdown:")
    print(f"  76           = OP_DUP")
    print(f"  a9           = OP_HASH160")
    print(f"  14           = Push 20 bytes")
    print(f"  {b2x(pub_key_hash)} = pubKeyHash (20 bytes)")
    print(f"  88           = OP_EQUALVERIFY")
    print(f"  ac           = OP_CHECKSIG")


def main():
    """Main demo function"""

    # Run the P2PKH demonstration
    demonstrate_p2pkh_script()

    # Show opcodes reference
    input("\n\nPress Enter to see opcodes reference...")
    show_script_opcodes()

    print("\n" + "="*70)
    print("Demo complete! This is how Bitcoin validates every P2PKH transaction.")
    print("="*70)


if __name__ == "__main__":
    main()
