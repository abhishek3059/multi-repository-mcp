# Current Context: multi-repo-mcp

This file is a sanitized, repo-level context artifact for the local `multi-repo-mcp` project.

## Project Purpose

`multi-repo-mcp` is a Python MCP server that lets an MCP client manage and work across multiple Git repositories through a shared workspace model.

## Repo Identity

- Root: `multi-repo-mcp`
- Python package: `src/multi_repo_mcp`
- Entry point: `multi_repo_mcp.server:main`
- Python requirement: `>=3.10`

## Key Modules

- `src/multi_repo_mcp/server.py` — MCP server entry point, tool registration, workspace orchestration, and clone job handling.
- `src/multi_repo_mcp/workflow_tools.py` — workflow helpers such as `ensure_workspace`, `start_workflow`, and context preparation.
- `src/multi_repo_mcp/workspace_manager.py` — workspace metadata persistence.
- `src/multi_repo_mcp/git_manager.py` — clone/fetch/branch/commit helpers.
- `src/multi_repo_mcp/workspace_ai.py` — workspace artifact generation (`context.md`, repo index, retrieval chunks, logic chunks, architecture map).

## Publish Safety Notes

The public repo should not contain:
- local workspace clones or test workspaces
- generated local-only folders such as `.codex`, `.tmp-smoke`, `data`, or `__pycache__`
- user-specific absolute paths or private organization examples in committed docs/config
- real credentials or access tokens

## Recent Task Log

- 2026-06-05: Sanitized the repository for public upload. Removed local/generated artifacts, deleted archived restart notes, replaced user-specific paths with placeholders, removed private organization examples from configs/docs/source comments, generalized semantic-release tooling/docs for public collaboration, and added ignore rules for non-publishable files. Verify with `python -m compileall src\multi_repo_mcp` plus a text scan for placeholder org names and local home paths.
