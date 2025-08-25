# ── Build stage ───────────────────────────────────────────────────
FROM python:{{cookiecutter.python_version}}-slim AS builder
ENV PEX_ROOT=/pex
WORKDIR /build

# Copy source + Pants config
COPY . /build
RUN pip install --no-cache-dir pip==23.3.1 setuptools wheel \
 && ./pants package services/main:main

# ── Runtime stage ─────────────────────────────────────────────────
FROM python:{{cookiecutter.python_version}}-slim
ENV PEX_ROOT=/pex
WORKDIR /app

# Copy the PEX created by Pants
COPY --from=builder /build/dist/*.pex /app/app.pex

EXPOSE 8000
ENTRYPOINT ["python", "app.pex"]
