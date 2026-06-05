# 🔑 Authentication Setup for Multi-Repo MCP

## Current Issue

The MCP server subprocess doesn't inherit SSH agent credentials on Windows, causing authentication failures when auto-cloning repos.

**Error:** `SSH authentication failed for git@github.com:example-org/example-repo.git`

---

## ✅ Solution: Use HTTPS URLs (Recommended)

HTTPS URLs work more reliably with Git credential managers on Windows.

### For Public Repositories

```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
- https://github.com/example-org/example-repo.git
Name it "workspace-demo"
```

### For Private Repositories

You need a GitHub Personal Access Token (PAT).

#### Step 1: Generate GitHub Token

1. Go to GitHub: **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Give it a name: `Multi-Repo MCP`
4. Select scopes: ✅ **repo** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

#### Step 2: Use Token in URLs

**Method A - Embed in URL:**
```
Setup a workspace with these repos:
- https://<github-token>@github.com/example-org/example-repo.git
- https://<github-token>@github.com/example-org/example-repo.git
Name it "workspace-demo"
```

**Method B - Use Git Credential Manager (Better):**

1. Configure Git to use Windows Credential Manager:
   ```bash
   git config --global credential.helper wincred
   ```

2. Use regular HTTPS URLs:
   ```
   Setup a workspace with these repos:
   - https://github.com/example-org/example-repo.git
   - https://github.com/example-org/example-repo.git
   Name it "workspace-demo"
   ```

3. Git will prompt for credentials **once**, then cache them
   - Username: Your GitHub username
   - Password: Your Personal Access Token (NOT your GitHub password!)

---

## Alternative: Fix SSH Agent on Windows

If you prefer SSH URLs, here's how to make it work:

### Option 1: Start SSH Agent Before VSCode

```powershell
# In PowerShell (as Administrator)
# Enable SSH Agent service
Set-Service -Name ssh-agent -StartupType Automatic
Start-Service ssh-agent

# Add your key
ssh-add C:\Users\<you>\.ssh\id_ed25519
```

Then close VSCode completely and reopen it.

### Option 2: Use Git Bash SSH

Git Bash includes its own SSH agent that works better with subprocesses:

1. Open Git Bash (not PowerShell)
2. Run:
   ```bash
   eval $(ssh-agent)
   ssh-add ~/.ssh/id_ed25519
   ```
3. From the same Git Bash window, launch VSCode:
   ```bash
   code
   ```

---

## 🎯 Recommended Approach for Your Team

### For Team Setup

**Create a team configuration guide:**

#### Configuration 1: HTTPS with Token (Easiest)

**Best for:** Everyone, especially Windows users

**Setup:**
1. Generate GitHub Personal Access Token
2. Configure Git credential helper:
   ```bash
   git config --global credential.helper wincred
   ```
3. Use HTTPS URLs when creating workspaces
4. Enter token once when prompted

#### Configuration 2: SSH (Advanced Users)

**Best for:** Users comfortable with SSH

**Setup:**
1. Generate SSH key if needed
2. Add to GitHub
3. Start SSH agent service:
   ```powershell
   Set-Service -Name ssh-agent -StartupType Automatic
   Start-Service ssh-agent
   ssh-add path\to\key
   ```
4. Restart VSCode
5. Use SSH URLs when creating workspaces

---

## 🔧 Testing Authentication

### Test HTTPS:

```bash
git ls-remote https://github.com/example-org/example-repo.git HEAD
```

If prompted, enter:
- Username: your GitHub username
- Password: your PAT token

### Test SSH:

```bash
ssh -T git@github.com
```

Should show: `Hi username! You've successfully authenticated...`

---

## 📝 Current Workaround (Until Fixed)

**You can still use the MCP server by cloning manually:**

```bash
# Navigate to workspace
cd C:\Users\<you>\.multi-repo-mcp\workspaces\workspace-demo

# Clone using your method (SSH works for you manually)
git clone git@github.com:example-org/example-repo.git
git clone git@github.com:example-org/example-repo.git
```

Then all MCP tools work perfectly:
- Search across repos
- Read files from any repo
- Find files everywhere
- Update all repos

---

## 🚀 Quick Fix for You Right Now

Since SSH works for you manually, just try with HTTPS:

```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
- https://github.com/example-org/example-repo.git
Name it "workspace-demo-https"
```

If private, use token:
```
Setup a workspace with these repos:
- https://YOUR_TOKEN@github.com/example-org/example-repo.git
- https://YOUR_TOKEN@github.com/example-org/example-repo.git
Name it "workspace-demo-https"
```

---

## 💡 Why This Happens

**SSH Agent Inheritance Issue:**
- Your terminal has SSH agent running
- VSCode starts the MCP server as a subprocess
- Subprocess doesn't inherit SSH_AUTH_SOCK environment variable
- Git can't find SSH agent → authentication fails

**HTTPS Solution:**
- Uses Windows Credential Manager
- Credentials are system-wide
- Subprocesses can access them
- More reliable on Windows

---

## ✅ Best Practice

**For production use with your team:**

1. **Document both methods** (HTTPS + SSH)
2. **Recommend HTTPS** for ease of use
3. **Provide token generation guide**
4. **Show how to test authentication**
5. **Keep token secure** (never commit it!)

---

## 📞 Next Steps

1. **Try HTTPS URLs** with the MCP server
2. **Generate GitHub PAT** if repo is private
3. **Configure Git credential helper** for caching
4. **Test workspace creation** with HTTPS URLs
5. **Document for your team** which method to use

The MCP server is fully working - this is just about which authentication method Git uses! 🚀
