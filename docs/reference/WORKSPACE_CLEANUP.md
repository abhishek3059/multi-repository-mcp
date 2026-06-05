# Workspace Cleanup Behavior

## Overview

The multi-repo MCP server now implements intelligent workspace cleanup to handle failed repository cloning scenarios.

## Three Scenarios

### Scenario 1: ✅ All Repositories Clone Successfully

**What Happens:**
```
✓ Workspace created
✓ All repos cloned
✓ Workspace activated
```

**Result:**
- Workspace is fully functional
- All repositories available
- Success message displayed

**Example Output:**
```
✅ Workspace 'my-workspace' created and activated successfully!

Repository Input Summary:
  • example-org/repo1
  • example-org/repo2

✓ Cloned: repo1
✓ Cloned: repo2
```

---

### Scenario 2: ❌ All Repositories Fail to Clone

**What Happens:**
```
✓ Workspace created temporarily
✗ All repos fail to clone
❌ AUTOMATIC CLEANUP:
   ├─ Delete workspace metadata
   ├─ Delete physical directory
   └─ Return error message
```

**Result:**
- NO workspace created
- NO folders left behind
- NO manual cleanup needed
- Clear error message

**Example Output:**
```
❌ Workspace creation failed! All 2 repositories failed to clone.

✗ Failed to clone repo1: Authentication failed
✗ Failed to clone repo2: Repository not found

Workspace 'my-workspace' was not created (automatic cleanup performed).
```

**Benefits:**
- Clean system - no orphaned workspaces
- No manual directory deletion needed
- Immediate feedback about what went wrong

---

### Scenario 3: ⚠️ Some Repositories Clone, Some Fail

**What Happens:**
```
✓ Workspace created
✓ Some repos cloned successfully
✗ Some repos failed
⚠️ KEEP WORKSPACE:
   ├─ Successful repos are functional
   ├─ Failed repos = no empty folders
   └─ Warning message displayed
```

**Result:**
- Workspace kept with successful repositories
- Can work with what succeeded
- Clear indication of what failed
- User can retry failed repos later

**Example Output:**
```
⚠️  Workspace 'my-workspace' created with partial success!

Repository Input Summary:
  • example-org/repo1
  • example-org/repo2
  • example-org/repo3

✓ Cloned: repo1
✗ Failed to clone repo2: Repository not found
✓ Cloned: repo3

⚠️  Warning: 1 of 3 repositories failed to clone.
✓ Successfully cloned: 2 repository(ies)

You can work with the successful repositories or delete this workspace and retry.
```

**Benefits:**
- Don't lose successful clones
- Can start working immediately with available repos
- Can retry failed repos later
- Clear visibility into what worked and what didn't

## Common Failure Reasons

### Authentication Failures
```
✗ Failed to clone repo: Authentication failed
```
**Cause:** Invalid or missing GitHub token
**Fix:** Check `github_token` in `config/default_config.json`

### Repository Not Found
```
✗ Failed to clone repo: Repository not found
```
**Cause:** Typo in repo name or lack of access permissions
**Fix:** Verify repo name and ensure you have access

### Network Issues
```
✗ Failed to clone repo: Could not connect
```
**Cause:** Network connectivity problems
**Fix:** Check internet connection and retry

## Manual Workspace Deletion

If you want to delete a workspace manually:

```
# Using file system (if needed)
C:\Users\<you>\.multi-repo-mcp\workspaces\workspace-name\
```

Or wait for a `delete_workspace` tool to be added to the MCP server.

## Key Improvements

1. **No Orphaned Workspaces:** Total failures automatically cleaned up
2. **No Empty Folders:** Failed repos don't leave empty directories
3. **Clear Feedback:** Know exactly what succeeded and what failed
4. **Flexible Recovery:** Can work with partial success or retry
5. **Automatic:** No manual intervention needed

## Testing the Cleanup

### Test Total Failure (with fake repo):
```
Setup a workspace with these repos:
- fake-repo-that-does-not-exist
- another-fake-repo
Name it "test-failure"
```
**Expected:** Workspace NOT created, automatic cleanup, error message

### Test Partial Failure:
```
Setup a workspace with these repos:
- example-repo (real repo)
- fake-repo-xyz (doesn't exist)
Name it "test-partial"
```
**Expected:** Workspace created with example-repo only, warning about failed repo

### Test Complete Success:
```
Setup a workspace with these repos:
- example-repo
- example-repo
Name it "test-success"
```
**Expected:** Workspace created with both repos, success message
