FROM python:3.13-alpine@sha256:9ba6d8cbebf0fb6546ae71f2a1c14f6ffd2fdab83af7fa5669734ef30ad48844
LABEL org.opencontainers.image.source="https://github.com/Septimus4/Chronogen"

RUN apk add --no-cache gcc python3-dev

RUN pip install --no-cache-dir build

WORKDIR /app
COPY . .
RUN python -m build --wheel


FROM python:3.13-alpine@sha256:9ba6d8cbebf0fb6546ae71f2a1c14f6ffd2fdab83af7fa5669734ef30ad48844

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN adduser -D chronogen
USER chronogen
ENV PATH="/home/chronogen/.local/bin:$PATH"

COPY --from=0 --chown=chronogen:chronogen /app/dist/*.whl /tmp/
RUN pip install --no-cache-dir --user /tmp/*.whl && \
    rm -f /tmp/*.whl && \
    rm -rf /home/chronogen/.cache/pip

ENTRYPOINT ["chronogen"]
