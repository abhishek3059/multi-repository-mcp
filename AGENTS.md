# Codex Operating Instructions — Multi-Repo MCP Workflow

You are working in an environment with a **Multi-Repo MCP server**. For every user task, follow this workflow **before** making changes.

Before following the rest of this workflow, always read `agent.md` when it is present. In this repo, `agent.md` points back to `AGENTS.md`, which remains the canonical instruction file.

Documentation index for humans and agents:
- read [docs/README.md](docs/README.md) for the high-level doc map
- use [docs/guides/EFFECTIVE_MCP_SERVER_USAGE.md](docs/guides/EFFECTIVE_MCP_SERVER_USAGE.md) for the recommended end-to-end workflow

## Golden workflow (always follow)

### Workspace-first workflow (highest priority when applicable)
If the user provides repositories for a new workspace:
1. Call `ensure_workspace`.
   - Clone operations default to background jobs to avoid MCP client timeouts.
   - If a clone `job_id` is returned, call `get_clone_job_status` until it reports ready; do not call `get_workspace_info` merely to check clone/context readiness.
2. Call `start_workflow` with the user request as the objective.
   - If `ensure_workspace` already returned a bootstrapped `workflow_id`, reuse it instead of creating a duplicate workflow.
3. Call `prepare_context_bundle`.
4. If a Linear ticket is provided, call `analyze_ticket` with the `workflow_id`.
5. Use `locate_candidates` or `workspace_locate` before broad search.
6. Subagents now auto-run at workflow milestones:
   - `searcher` after `context_prepared`
   - `trace` and `fix_plan` after `ticket_analyzed`
   - `verifier` during verification planning/execution
   - `reviewer` after applied changes
7. For additional complex or exploratory work, use subagents manually:
   - `prepare_subagent_packet`
   - `run_subagent`
   - `merge_subagent_results`

### 0) Establish the correct workspace
1. Call `list_workspaces`.
2. If the user mentions a workspace name:
   - Call `switch_workspace` to set it active.
3. If no workspace is mentioned:
   - Use the currently active one shown by `list_workspaces`.
   - If none is active, ask the user for the workspace name or create one via `setup_workspace`.

### 1) Refresh workspace understanding (mandatory)
Run this step in all of these cases:
- the first Multi-Repo MCP call in a new chat
- immediately after workspace initialization/creation
- immediately after switching to a different workspace
- immediately after adding a repository to an existing workspace

After a workspace is active (or immediately after `setup_workspace` / repo-addition / workspace switch):
1. Call `refresh_workspace_context`.
   - This generates/refreshes the workspace context plus MCP metadata artifacts, including:
     - `context.md` (alias of `WORKSPACE_CONTEXT.md`)
     - `.mcp/digests.json`
     - `.mcp/repo_index.json`
     - `.mcp/retrieval/chunks.json`
     - `.mcp/retrieval/logic_chunks.json`
     - `.mcp/architecture_map.json`
     - `.clinerules`
2. **Must do:** read `context.md` / `WORKSPACE_CONTEXT.md` in the workspace root the first time a workspace is initialized or switched to in a chat, and always before analysis or code edits.

### 2) Locate logic with minimal searching
1. Use `workspace_locate` with the user’s query/ticket title to jump to likely files/symbols/routes.
2. Only if needed, use `search_repos` with targeted keywords.
3. Prefer opening specific files with `get_file` rather than wide repeated searches.

### 3) If a Linear ticket is provided
1. Use `analyze_ticket` and pass the active `workflow_id` when available.
2. Treat the ticket as signal; ground decisions in the codebase using generated workspace context first, then `workspace_locate` + `context.md`.

### 4) Make changes (minimal-diff contract)
- Make the **smallest change** that satisfies the request.
- Do **not** refactor, reformat, rename, or optimize unrelated code unless explicitly asked.
- If changes grow beyond ~3 files or ~80 lines, stop and explain why.

### 5) After completing the task
1. Update `context.md` (and/or `WORKSPACE_CONTEXT.md`) “Recent task log” section:
   - What changed (files)
   - Why
   - How to verify (commands/tests)
2. If pushing changes, prefer `push_with_review` where appropriate.

## Quick commands
- Configure workspace storage outside the MCP repo:
  - `set_workspace_root({"workspace_root": "D:\\workspaces", "persist": true})`
- Start generic workflow:
  - `ensure_workspace({"workspace_name": "<name>", "repos": ["org/repo"]})`
  - `start_workflow({"objective": "fix <issue or task>"})`
  - `prepare_context_bundle({"workflow_id": "<id>", "query": "<what to find>"})`
- Automatic milestone subagents:
  - `start_workflow`/`prepare_context_bundle` auto-run `searcher`
  - `analyze_ticket` auto-runs `trace` and `fix_plan`
  - `build_verification_plan`/`verify_repos` auto-run `verifier`
  - `apply_fix(apply=true)` auto-runs `reviewer`
- Run a focused advisory subagent:
  - `run_subagent({"workflow_id": "<id>", "role": "searcher", "query": "<narrow task>"})`
- Refresh workspace context:
  - `refresh_workspace_context({"workspace_name": "<optional>", "generate_code_workspace_file": false})`
- Locate logic:
  - `workspace_locate({"query": "<what to find>", "limit": 8})`
