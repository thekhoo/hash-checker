# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`hash-checker` is a Python 3.13 CLI tool (currently in early development). Entry point is `main.py:main()`.

## Commands

This project uses `uv` for dependency and environment management.

```bash
# Run the project
uv run python main.py

# Add a dependency
uv add <package>

# Install dependencies
uv sync
```
