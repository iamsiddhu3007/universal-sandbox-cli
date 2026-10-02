FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-full \
    nodejs \
    npm \
    golang \
    build-essential \
    git \
    bash \
    curl \
    ca-certificates \
    openjdk-17-jdk \
    rustc \
    cargo \
    ruby \
    php \
    && rm -rf /var/lib/apt/lists/*


RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH:/root/go/bin"


RUN npm install -g @anthropic-ai/claude-code && \
    curl -fsSL https://chatgpt.com/codex/install.sh | sh && \
    curl -fsSL https://antigravity.google/cli/install.sh | bash && \
    curl -fsSL https://opencode.ai/v2/install | bash


# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

WORKDIR /workspace

# ENTRYPOINT ["/entrypoint.sh"]