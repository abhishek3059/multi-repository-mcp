# 🔍 Multi-Repo MCP Server - Troubleshooting Guide

## Current Status: Server Not Connecting ⚠️

Your configuration is **correct**, but the MCP server isn't connecting to Cline.

---

## 🔎 Diagnostic Steps

### Step 1: Check Cline Output Logs

This is the **most important step** - it will show you exactly why the server isn't connecting.

1. In VSCode, open the **Output panel**:
   - Press `Ctrl + Shift + U`
   - OR go to `View` → `Output`

2. In the dropdown at the top right, select **"Cline"**

3. Look for messages about "multi-repo" or MCP server errors

**What to look for:**
- ✅ Success: `MCP server 'multi-repo' connected successfully`
- ❌ Error: `Failed to start MCP server 'multi-repo': ...`
- ❌ Error: `Python not found` or `Module not found`
- ❌ Error: `Permission denied` or `Access denied`

**Please share what you see in the Output panel!**

---

### Step 2: Manually Test the Server

Open a **new terminal** in VSCode and run:

```bash
cd C:\Users\<you>\Desktop\multi-repo-mcp
C:\Python313\python.exe -m multi_repo_mcp.server
```

**Expected output:**
```
✓ Using SSH key: C:\Users\<you>\.ssh\id_ed25519
```

If you see this, the server works! Press `Ctrl+C` to stop it.

**If you see errors:**
- Share the error message
- It will tell us what's wrong

---

### Step 3: Check Python and Package

```bash
# Check Python version
C:\Python313\python.exe --version

# Check if package is installed
C:\Python313\python.exe -m pip list | findstr multi-repo-mcp
```

**Expected:**
- Python 3.13.x
- `multi-repo-mcp 0.1.0`

---

### Step 4: Check Cline Version

The MCP feature requires a recent version of Cline.

1. Go to Extensions in VSCode
2. Find "Cline" extension
3. Check version number

**Required:** Cline should be version that supports MCP (v2.0+)

If your version is older, update it:
1. Right-click on Cline extension
2. Select "Update to..."

---

## 🐛 Common Issues & Solutions

### Issue 1: "Module 'mcp' not found"

**Solution:**
```bash
cd C:\Users\<you>\Desktop\multi-repo-mcp
pip install -e .
```

---

### Issue 2: "Module 'multi_repo_mcp' not found"

**Solution:** The PYTHONPATH might not be set correctly.

Try updating the configuration to use full paths:

```json
"multi-repo": {
  "command": "C:\\Python313\\python.exe",
  "args": [
    "-c",
    "import sys; sys.path.insert(0, 'C:\\\\Users\\\\<you>\\\\Desktop\\\\multi-repo-mcp\\\\src'); from multi_repo_mcp.server import main; main()"
  ],
  "env": {
    "HOME": "C:\\Users\\<you>"
  },
  "disabled": false,
  "autoApprove": []
}
```

---

### Issue 3: Python Permission Issues

**Solution:** Run VSCode as Administrator:
1. Close VSCode
2. Right-click VSCode icon
3. Select "Run as administrator"
4. Try again

---

### Issue 4: Other MCP Servers Also Not Connecting

**Check:** Are the figma and ado servers showing up in your MCP tools?

If **NO** MCP servers are connecting:
- Your Cline version might not support MCP yet
- Update Cline to the latest version

---

## 📋 Information Needed

To help you further, I need to know:

1. **What do you see in the Cline Output panel?**
   - Any errors?
   - Any messages about multi-repo?

2. **Does the server start manually?**
   - Run the command from Step 2 above
   - What output do you get?

3. **What's your Cline version?**
   - Check in Extensions panel

4. **Are other MCP servers (figma, ado) connected?**
   - Type `list mcp tools` in Cline
   - Do you see ANY tools?

---

## 🔧 Alternative: Direct Script Execution

If all else fails, we can change the server to run directly:

Create a file: `C:\Users\<you>\Desktop\multi-repo-mcp\run_server.bat`

```batch
@echo off
cd C:\Users\<you>\Desktop\multi-repo-mcp
set PYTHONPATH=C:\Users\<you>\Desktop\multi-repo-mcp\src
C:\Python313\python.exe -m multi_repo_mcp.server
```

Then update config to:
```json
"command": "C:\\Users\\<you>\\Desktop\\multi-repo-mcp\\run_server.bat"
```

---

## 📊 Your Current Configuration

```json
{
  "command": "C:\\Python313\\python.exe",
  "args": ["-m", "multi_repo_mcp.server"],
  "env": {
    "HOME": "C:\\Users\\<you>",
    "PYTHONPATH": "C:\\Users\\<you>\\Desktop\\multi-repo-mcp\\src"
  },
  "disabled": false,
  "autoApprove": []
}
```

This looks correct! ✅

---

## 🎯 Next Steps

**Please do this and report back:**

1. **Check Cline Output panel** (`Ctrl+Shift+U`, select "Cline")
2. **Tell me what errors you see** (if any)
3. **Run the manual test** (Step 2 above)
4. **Check your Cline version**

Once I know what errors you're seeing, I can provide a specific fix!

---

## 💡 Quick Diagnostic Command

Run this in terminal:

```bash
cd C:\Users\<you>\Desktop\multi-repo-mcp && C:\Python313\python.exe -m multi_repo_mcp.server
```

If it shows `✓ Using SSH key: ...` then the server works and the issue is with Cline's MCP loading.

Press Ctrl+C to stop after you see the output.
