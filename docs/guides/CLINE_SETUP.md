# 🔌 Connect Multi-Repo MCP to Cline

## ⚠️ Important: Cline is NOT Using the MCP Server Yet

When you say "setup workspace with repos", Cline is just cloning repos directly to your Desktop. This means **the MCP server is not connected**.

You need to **configure Cline to use the MCP server** first!

---

## 📋 Setup Steps

### Step 1: Locate Cline Settings

1. Open VSCode
2. Click the **Cline icon** in the left sidebar (it looks like a robot/AI icon)
3. Click the **settings/gear icon** (⚙️) at the top of the Cline panel
4. Look for **"MCP Settings"** or **"Model Context Protocol"** section

### Step 2: Find the MCP Configuration File

Cline's MCP settings are stored in a JSON file. The location depends on your OS:

**Windows:**
```
C:\Users\<you>\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

OR in VSCode settings:
- Press `Ctrl + Shift + P`
- Type "Open User Settings (JSON)"
- Look for `cline.mcpServers` section

### Step 3: Add This Configuration

Add the following to your Cline MCP settings:

```json
{
  "mcpServers": {
    "multi-repo": {
      "command": "python",
      "args": ["-m", "multi_repo_mcp.server"],
      "env": {
        "HOME": "C:\\Users\\<you>",
        "PYTHONPATH": "C:\\Users\\<you>\\Desktop\\multi-repo-mcp\\src"
      }
    }
  }
}
```

**IMPORTANT:** 
- Use double backslashes `\\` in Windows paths
- Make sure Python is in your PATH
- The `PYTHONPATH` helps Python find the modules

### Step 4: Restart Cline/VSCode

After adding the configuration:
1. Close VSCode completely
2. Reopen VSCode
3. Open Cline

### Step 5: Verify Connection

In Cline chat, type:

```
List available MCP tools
```

You should see tools like:
- ✅ setup_workspace
- ✅ search_repos
- ✅ get_file
- ✅ find_file
- ✅ list_workspaces
- ✅ etc.

If you DON'T see these tools, the MCP server is not connected!

---

## 🎯 Alternative: Use VSCode Settings UI

1. Open VSCode Settings: `Ctrl + ,`
2. Search for: `cline mcp`
3. Click "Edit in settings.json"
4. Add the configuration above

---

## ✅ How to Know It's Working

### Before (NOT working):
When you say: "Setup workspace with repos"

Cline responds:
```
✓ example-repo - Cloned to C:\Users\<you>\Desktop\example-repo
```
👆 This means Cline is just running git commands directly!

### After (WORKING):
When you say: "Setup workspace with repos"

Cline responds:
```
Workspace 'my-workspace' created and activated!
✓ Cloned: example-repo
✓ Cloned: example-repo

Workspace stored at: C:\Users\<you>\.multi-repo-mcp\workspaces\
```
👆 This means Cline is using the MCP server!

---

## 🧪 Test Commands Once Connected

### 1. Create a Workspace
```
Setup workspace with these repos:
- git@github.com:example-org/example-repo.git
- git@github.com:example-org/example-repo.git
Name it "workspace-demo"
```

**Expected output:**
```
Workspace 'workspace-demo' created and activated!

✓ Cloned: example-repo
✓ Cloned: example-repo
```

### 2. List Workspaces
```
List all my workspaces
```

**Expected output:**
```
Available Workspaces:

• workspace-demo (active)
  Repositories: 2
  Created: 2024-01-21T12:30:00
```

### 3. Search Across Repos
```
Search for "import" in all Java files
```

**Expected output:**
```
Found 150 matches for 'import':

1. example-repo:src/main/java/Service.java:5
-> import java.util.List;

2. example-repo:src/components/App.java:3
-> import org.springframework.boot.SpringApplication;
...
```

---

## 🐛 Troubleshooting

### Issue: "No MCP tools showing up"

**Solution 1: Check Python Path**
```bash
where python
```
Make sure Python is accessible from command line.

**Solution 2: Check Configuration**
Ensure the JSON is valid (no missing commas, brackets, etc.)

**Solution 3: Check Cline Logs**
Look at Cline's output panel for MCP connection errors.

### Issue: "Module not found error"

**Solution:**
Make sure you installed the package:
```bash
cd C:\Users\<you>\Desktop\multi-repo-mcp
pip install -e .
```

### Issue: "SSH key not found"

**Solution:**
Edit `config/default_config.json`:
```json
{
  "ssh_key_path": "C:\\Users\\<you>\\.ssh\\id_ed25519"
}
```

---

## 📸 Visual Guide

### Where to Find MCP Settings in Cline:

```
VSCode Sidebar
└── Cline Icon (🤖)
    └── Click Settings Icon (⚙️)
        └── Scroll to "MCP Settings"
            └── Add configuration
```

### What the Configuration Looks Like:

```json
{
  "mcpServers": {
    "multi-repo": {              ← Server name (can be anything)
      "command": "python",       ← Command to run
      "args": ["-m", "multi_repo_mcp.server"],  ← Python module
      "env": {                   ← Environment variables
        "HOME": "C:\\Users\\<you>"
      }
    }
  }
}
```

---

## 🎓 Understanding the Difference

### Without MCP Server (Current State):
```
You → Cline → Git commands directly → Clones to Desktop
```

### With MCP Server (Correct State):
```
You → Cline → MCP Server → Workspaces & Tools
                ↓
         Multi-repo operations
         Search across repos
         Coordinated changes
```

---

## 🚀 Next Steps After Setup

Once connected, you can:

1. **Create Workspaces:**
   ```
   Setup workspace with 5 auction repos
   ```

2. **Search Code:**
   ```
   Search for "UserService" in all Java files
   ```

3. **Find Files:**
   ```
   Find all pom.xml files
   ```

4. **Get Files:**
   ```
   Show me the application.properties from example-repo
   ```

5. **Update Repos:**
   ```
   Update all repos in workspace
   ```

---

## ✅ Checklist

- [ ] Located Cline MCP settings
- [ ] Added multi-repo configuration
- [ ] Restarted VSCode
- [ ] Verified tools show up with "List available MCP tools"
- [ ] Created first workspace
- [ ] Tested search functionality

---

## 📞 Still Not Working?

If after following all steps the MCP tools still don't show up:

1. Check Cline version (must support MCP)
2. Check Python version: `python --version` (must be 3.10+)
3. Check package is installed: `pip list | findstr multi-repo-mcp`
4. Try running server manually: `python -m multi_repo_mcp.server`
5. Check for errors in VSCode Developer Tools (Help → Toggle Developer Tools)

---

**Once connected, Cline will use the MCP server and you'll see the difference immediately!** 🎉
