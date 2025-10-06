FROM python:3.13-slim@sha256:5f55cdf0c5d9dc1a415637a5ccc4a9e18663ad203673173b8cda8f8dcacef689

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir build

WORKDIR /app
COPY . .

RUN python -m build --wheel


FROM python:3.13-slim@sha256:5f55cdf0c5d9dc1a415637a5ccc4a9e18663ad203673173b8cda8f8dcacef689

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN useradd -m chronogen
USER chronogen
ENV PATH="/home/chronogen/.local/bin:$PATH"

COPY --from=0 --chown=chronogen:chronogen /app/dist/*.whl /tmp/
RUN pip install --no-cache-dir --user /tmp/*.whl && \
    rm -f /tmp/*.whl

ENTRYPOINT ["chronogen"]
