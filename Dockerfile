FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Bitcoin demo scripts
COPY bitcoin_address_demo.py .
COPY quick_bitcoin_tools.py .
COPY p2pkh_stack_demo.py .
COPY simple_p2pkh_demo.py .
COPY bitcoin_visualization.html .

# Set executable permissions
RUN chmod +x bitcoin_address_demo.py quick_bitcoin_tools.py p2pkh_stack_demo.py simple_p2pkh_demo.py

# Default command runs the comprehensive demo
CMD ["python", "bitcoin_address_demo.py"]
