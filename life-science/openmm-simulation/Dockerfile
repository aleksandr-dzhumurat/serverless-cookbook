# Use a base image with CUDA drivers
FROM nvidia/cuda:13.0.1-base-ubuntu24.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    wget \
    curl \
    build-essential \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

## Make directories
RUN mkdir -p /openmm/results
WORKDIR /openmm

# Copy project files
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY sim/ ./sim/

# Create Python virtual environment (3.12 for broad compatibility with scientific packages)
RUN uv python install 3.12 && uv venv /opt/venv --python 3.12
ENV PATH="/opt/venv/bin:/root/.local/bin:$PATH"

# Install Python dependencies with fallback for OpenMM
RUN uv pip install --python /opt/venv/bin/python . || \
    (echo "uv install failed, trying with OpenMM fallback..." && \
     uv pip install --python /opt/venv/bin/python openmm==8.4.0)

     
# Define the entrypoint using the modular approach
ENTRYPOINT ["python", "-m", "sim.run"]
