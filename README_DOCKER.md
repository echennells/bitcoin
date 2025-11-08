# Bitcoin Demo Tools - Docker Setup

This directory contains educational Bitcoin tools that run in a Docker container, keeping your host machine clean.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the demo
docker-compose run --rm bitcoin-demo

# Run specific scripts
docker-compose run --rm bitcoin-demo python quick_bitcoin_tools.py
docker-compose run --rm bitcoin-demo python p2pkh_stack_demo.py

# Get an interactive shell
docker-compose run --rm bitcoin-demo bash
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t bitcoin-demo .

# Run the comprehensive demo
docker run --rm bitcoin-demo

# Run the quick tools
docker run --rm bitcoin-demo python quick_bitcoin_tools.py

# Get an interactive shell to play around
docker run --rm -it bitcoin-demo bash
```

## What's Included

- **bitcoin_address_demo.py** - Comprehensive demo showing:
  - Legacy P2PKH addresses (1...)
  - Native SegWit addresses (bc1q...)
  - Bitcoin hashing (SHA256, Double-SHA256, RIPEMD160)
  - OP_RETURN data embedding

- **quick_bitcoin_tools.py** - Quick utility functions you can import:
  ```python
  from quick_bitcoin_tools import generate_address, sha256, double_sha256, hash160
  ```

- **p2pkh_stack_demo.py** - Interactive stack-based execution demo:
  - Step-by-step P2PKH transaction validation
  - Visual stack operations (OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG)
  - Shows how Bitcoin Script validates transactions
  - Includes opcode reference

- **bitcoin_visualization.html** - Interactive HTML visualization (open in browser)

## Interactive Python Session

To use the tools interactively:

```bash
# Start Python in the container
docker-compose run --rm bitcoin-demo python

# Then in Python:
>>> from quick_bitcoin_tools import generate_address, sha256
>>> addr = generate_address()
>>> print(addr['address'])
>>> print(sha256('Hello Bitcoin'))
```

## Serving the HTML Visualization

```bash
# Run a simple HTTP server
docker-compose run --rm -p 8000:8000 bitcoin-demo python -m http.server 8000

# Then open: http://localhost:8000/bitcoin_visualization.html
```

## Notes

- All scripts generate random keys for educational purposes only
- **Never use these keys for real funds!**
- The container is ephemeral - nothing persists unless you modify the mounted volume
