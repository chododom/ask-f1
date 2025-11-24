FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# UV_COMPILE_BYTECODE: Compiles Python to .pyc files for faster startup
# UV_LINK_MODE: Copy files instead of hardlinking (safer for Docker layers)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml ./
COPY . .

RUN uv sync --no-install-project
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "ask_f1_agent.main:app", "--host", "0.0.0.0", "--port", "8080"]