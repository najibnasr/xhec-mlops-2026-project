FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
COPY bin ./bin

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8001 4201

CMD ["bash", "bin/run_services.sh"]
