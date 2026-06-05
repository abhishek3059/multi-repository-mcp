# Semantic-Release Commit Tool

## Overview

The `commit_semantic_release_repo` tool automates commits for repositories that enforce semantic-release style commit conventions with Husky, Commitizen, or similar hooks.

It is useful when a repository normally opens an interactive commit prompt, but an MCP client needs to create the commit non-interactively while still respecting the repository's release and linting rules.

## What the Tool Does

1. Stages the current changes
2. Runs `npm run lint-staged:fix`
3. Reads the latest semantic version tag
4. Builds a conventional commit message
5. Commits with `--no-verify` to bypass the interactive prompt
6. Optionally pushes the branch

## Tool Name

`commit_semantic_release_repo`

## Parameters

- `repo_name` (required)
- `commit_type` (required): `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, or `revert`
- `scope` (required)
- `subject` (required)
- `body` (optional)
- `breaking_changes` (optional)
- `issues_closed` (optional)
- `push` (optional, default `false`)

## Example

```json
{
  "repo_name": "example-release-ui",
  "commit_type": "feat",
  "scope": "dashboard",
  "subject": "add analytics widget",
  "push": false
}
```

Generated commit message:

```text
feat(dashboard): add analytics widget
```

## When to Use It

Use `commit_semantic_release_repo` when:

- the repository enforces conventional commit formatting
- a normal `git commit` would trigger an interactive Commitizen-style flow
- you want the MCP client to lint and commit automatically

Prefer `stage_and_commit_repo` for standard repositories that do not need this workflow.

## Notes

- Linting must pass before the commit is created
- `push` is disabled by default for safety
- the tool is intended for repositories with semantic-release style automation, not for one specific organization

## Verification

After running the tool, verify:

1. the commit message uses the expected conventional format
2. linting completed successfully
3. the repository history shows the new commit
4. push only happens when explicitly requested
