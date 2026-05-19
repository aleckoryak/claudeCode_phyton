# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Package manager is `uv`. Python >= 3.10.

```bash
# Install in development mode (after `uv venv` + activation)
uv pip install -e .

# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test class or method
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is a **FastMCP server** that exposes Python functions as tools to AI assistants. The wiring pattern is intentionally minimal:

- `tools/*.py` — each module defines plain Python functions. Functions stay framework-agnostic (no MCP imports); they use `pydantic.Field` for parameter metadata and rely on docstrings for tool documentation.
- `main.py` — constructs the `FastMCP("docs")` instance and registers tools via `mcp.tool()(function)`. **A function in `tools/` is only exposed to clients if `main.py` registers it.** For example, `tools/document.py::binary_document_to_markdown` exists but is not currently registered.
- `tests/` — pytest tests import directly from `tools.*` and exercise functions as ordinary Python (bypassing MCP). Binary fixtures live in `tests/fixtures/`.

When adding a new tool: write the function in `tools/<module>.py` using `Field(description=...)` for each parameter and a docstring that follows the README's structure (one-line summary, details, "When to use", examples), then register it in `main.py`.

## Document conversion

`tools/document.py` uses `markitdown` (with `[docx,pdf]` extras) to convert binary documents to markdown. Callers pass raw `bytes` plus a `file_type` extension string (e.g. `"docx"`, `"pdf"`); the function wraps the bytes in `BytesIO` and a `StreamInfo` for markitdown.