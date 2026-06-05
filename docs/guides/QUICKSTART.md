# Quick Start Guide - Multi-Repo MCP Server

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (30 seconds)

```bash
cd multi-repo-mcp
pip install -e .
```

### Step 2: Configure SSH Key (1 minute)

Open `config/default_config.json` and update the SSH key path:

```json
{
  "ssh_key_path": "C:\\Users\\<you>\\.ssh\\id_ed25519"
}
```

Replace `<you>` with your actual username.

### Step 3: Add to Cline (2 minutes)

1. Open VSCode
2. Click Cline icon → Settings (⚙️) → MCP Servers
3. Add this configuration:

```json
{
  "mcpServers": {
    "multi-repo": {
      "command": "python",
      "args": ["-m", "multi_repo_mcp.server"],
      "env": {
        "HOME": "C:\\Users\\<you>"
      }
    }
  }
}
```

### Step 4: Restart VSCode (1 minute)

Close and reopen VSCode.

### Step 5: Test It! (1 minute)

In Cline, type:

```
Setup a workspace with these repos:
- git@github.com:yourusername/repo1.git
- git@github.com:yourusername/repo2.git
Name it "test-workspace"
```

## ✅ That's It!

You can now:
- Search across multiple repos
- Get files from any repo
- Find files by name
- Update all repos at once

## 📖 Full Documentation

See [../../README.md](../../README.md) for complete documentation.

## 🆘 Problems?

**MCP server not showing up?**
1. Check Python version: `python --version` (must be 3.10+)
2. Reinstall: `pip install -e .`
3. Restart VSCode

**SSH errors?**
1. Test SSH: `ssh -T git@github.com`
2. Check key path in `config/default_config.json`
3. Ensure key is added to GitHub

## 💡 First Commands to Try

```
List all my workspaces
```

```
Show workspace info
```

```
Search for "UserService" in all repos
```

```
Find all pom.xml files
```

---

**Ready to work across multiple repos!** 🎉
