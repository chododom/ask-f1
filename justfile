_default:
    just --list


### Recipes ###


fix:
    uv run ruff check --fix src/ask_f1_agent/ask_f1_agent src/f1_mcp/main.py

format:
    uv run ruff format src/ask_f1_agent/ask_f1_agent src/f1_mcp/main.py

ingest:
    uv run python scripts/chroma_ingest.py