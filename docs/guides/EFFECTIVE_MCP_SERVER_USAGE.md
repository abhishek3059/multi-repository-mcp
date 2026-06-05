# Effective MCP Server Usage

This guide is the recommended end-to-end workflow for developers and Codex agents using the Multi-Repo MCP server in real work. It assumes the server is already installed and available to your MCP client.

## 1. Configure the Runtime Once

1. Install the package in editable mode from the repo root.
   ```bash
   pip install -e .
   ```
2. Configure the MCP client to run `python -m multi_repo_mcp.server`.
3. Set a workspace root outside the MCP repo.
   Recommended examples:
   - `D:\your-workspaces`
   - `C:\Users\<you>\Workspaces`
4. Persist that path so future sessions reuse it.
   ```json
   set_workspace_root({"workspace_root": "D:\\Workspaces", "persist": true})
   ```
5. Make sure the required credentials are available through environment variables when needed:
   - `GITHUB_TOKEN` or `MULTI_REPO_GITHUB_TOKEN`
   - `LINEAR_API_KEY` or `MULTI_REPO_LINEAR_API_KEY`
   - `OPENAI_API_KEY` for ticket analysis and AI review flows

## 2. Create or Reuse a Workspace

1. If the workspace already exists, activate or reuse it.
2. If it does not exist, create it with `ensure_workspace`.
   ```json
   ensure_workspace({
     "workspace_name": "workspace-demo",
     "repos": ["example-org/example-repo", "example-org/example-repo"]
   })
   ```
3. Clone operations default to background jobs to avoid MCP client timeouts. When a job finishes, the server refreshes `context.md`, repo indexes, retrieval chunks, logic chunks, and architecture artifacts automatically.
4. If `ensure_workspace` returns a clone `job_id`, call `get_clone_job_status` for readiness. A ready status includes context/workflow bootstrap details, so do **not** call `get_workspace_info` unless you specifically need detailed Git status.

## 3. Start a Workflow, Not a One-Off Search

1. Start every non-trivial task with `start_workflow`.
2. Provide a clear objective and, when relevant, a ticket identifier.
   ```json
   start_workflow({
     "workspace_name": "workspace-demo",
     "objective": "Work ENG-123 and identify the smallest checklist URL logic change",
     "workflow_type": "linear_ticket",
     "issue_id": "ENG-123",
     "auto_continue": true
   })
   ```
3. `auto_continue` should usually be `true`.
4. The workflow will persist state under `.mcp/workflows/<workflow_id>.json`.

## 4. Let the Server Build Cached Context

When the workflow starts, the server prepares reusable workspace context instead of re-reading the full repo every time.

Artifacts worth knowing:
- `.mcp/repo_index.json`
- `.mcp/architecture_map.json`
- `.mcp/digests.json`
- `.mcp/retrieval/chunks.json`
- `.mcp/retrieval/logic_chunks.json`
- `.mcp/summaries/workspace_digest.md`

Why this matters:
- later runs are cheaper
- the agent can search architecture and logic summaries first
- token-heavy full-repo reads become the fallback, not the default

## 5. Use the Built-In Workflow Milestones

These subagents now run automatically:

1. `searcher` after `context_prepared`
2. `trace` and `fix_plan` after `ticket_analyzed`
3. `verifier` during verification planning or verification execution
4. `reviewer` after applied changes

You do not need to ask for these explicitly for standard workflows. Use manual `run_subagent` only when you want an extra focused pass.

## 6. For Ticket Work, Let the Workflow Continue

1. If a Linear ticket is part of the task, pass the `issue_id` into `start_workflow` or call `analyze_ticket` with the active `workflow_id`.
2. The server will:
   - fetch the ticket
   - persist `linear_ticket.json`
   - run search and retrieval
   - persist `ticket_analysis.json`
   - write `developer_handoff.md`
3. After ticket analysis, inspect:
   - workflow stage
   - subagent results
   - likely starting files

Useful follow-up tools:
- `get_workflow_status`
- `merge_subagent_results`
- `workspace_locate`
- `locate_candidates`

## 7. Inspect Before Editing

Before making code changes:

1. Read the `developer_handoff.md` when a ticket exists.
2. Read merged subagent outputs to see:
   - candidate files
   - logic trace
   - change plan
   - verification plan
3. Use `workspace_locate` or `get_file` for only the narrow files involved.
4. Avoid broad repeated repo searches if the cached artifacts already identify the path.

## 8. Apply the Smallest Possible Change

1. Use `apply_fix` with a `workflow_id` when the change should become part of the tracked workflow.
2. Keep the diff minimal.
3. After `apply_fix(apply=true)` the server will:
   - persist the latest diff
   - refresh workspace context in delta mode
   - create a review request artifact
   - auto-run the `reviewer` subagent

## 9. Verify the Change

1. Build a verification plan first.
   ```json
   build_verification_plan({
     "workflow_id": "<workflow_id>",
     "mode": "minimal"
   })
   ```
2. Review the generated commands and expectations.
3. Run verification only after the plan is grounded.
   ```json
   verify_repos({
     "workflow_id": "<workflow_id>",
     "mode": "minimal"
   })
   ```
4. The workflow will auto-run the `verifier` subagent around these steps.

## 10. Review, Commit, and Push Carefully

If the change should proceed:

1. Inspect:
   - `latest_change.diff`
   - `review_request.json`
   - `code_review.json` or `push_review.json` when generated
2. Use:
   - `stage_and_commit_repo`
   - `push_with_review`
3. Keep the workflow id attached so artifacts stay linked to the same task.

## 11. Use Manual Subagents Only for Extra Depth

The manual subagent tools are still useful for focused follow-up work:

1. `prepare_subagent_packet`
2. `run_subagent`
3. `store_subagent_result`
4. `merge_subagent_results`

Use them when:
- the built-in auto pass was too shallow
- you want a second independent search/trace pass
- you want extra review on a narrow code area

## 12. Recommended Daily Workflow

For a normal ticket, the shortest effective sequence is:

1. `ensure_workspace`
2. `start_workflow(..., auto_continue=true, issue_id=...)`
3. `get_workflow_status`
4. `merge_subagent_results`
5. inspect narrow files only
6. `apply_fix`
7. `build_verification_plan`
8. `verify_repos`
9. `stage_and_commit_repo` or `push_with_review`

## 13. What Other Codex Agents Should Read First

If another developer or Codex agent opens this repo, the recommended order is:

1. [../../README.md](../../README.md)
2. [../README.md](../README.md)
3. [../../AGENTS.md](../../AGENTS.md)
4. [../../context.md](../../context.md)
5. this guide

That order gives product context, current local rules, recent implementation history, and the workflow that should be followed now.
