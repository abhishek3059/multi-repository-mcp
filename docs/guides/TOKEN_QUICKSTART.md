# 🚀 Quick Start: GitHub Token Authentication

## ✅ What's New

The MCP server now **automatically injects your GitHub token** into HTTPS URLs!

**You just need to:**
1. Generate a GitHub token
2. Add it to the config file
3. Restart VSCode
4. Use HTTPS URLs - token injection happens automatically!

---

## Step 1: Generate GitHub Token (2 minutes)

### Go to GitHub:
1. **Login:** https://github.com
2. **Click:** Your profile picture (top right)
3. **Click:** Settings
4. **Scroll down:** Click "Developer settings"
5. **Click:** Personal access tokens → Tokens (classic)
6. **Click:** "Generate new token (classic)"

### Configure Token:
1. **Note:** `Multi-Repo MCP`
2. **Expiration:** 90 days (or No expiration)
3. **Scopes:** Check ✅ **repo** (full repository access)
4. **Generate:** Click green "Generate token" button
5. **Copy:** Copy the token (starts with `ghp_...`)

---

## Step 2: Add Token to Config (1 minute)

### Edit Config File:
**File:** `C:\Users\<you>\Desktop\multi-repo-mcp\config\default_config.json`

**Add your token:**
```json
{
  "storage_path": null,
  "ssh_key_path": "C:\\Users\\<you>\\.ssh\\id_ed25519",
  "github_token": "<github-token>",
  "default_excludes": [
    ...
  ],
  ...
}
```

Replace `"<github-token>"` with your actual token.

**Save the file!**

---

## Step 3: Restart VSCode (30 seconds)

1. **Close VSCode completely** (File → Exit or Alt+F4)
2. Wait 5 seconds
3. **Reopen VSCode**
4. The MCP server will load with token support!

---

## Step 4: Test It! (Create Workspace)

Now use **HTTPS URLs** (not SSH) and the token will be injected automatically:

```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
- https://github.com/example-org/example-repo.git
Name it "kar-test"
```

### Expected Result:
```
Workspace 'kar-test' created and activated!

✓ Using GitHub token for authentication
✓ Cloned: example-repo
✓ Using GitHub token for authentication
✓ Cloned: example-repo
```

**Success!** Repos are now cloned automatically with token authentication! 🎉

---

## How It Works

### Before (Manual Token):
```
❌ Setup workspace with: https://TOKEN@github.com/example-org/example-repo.git
```
You had to manually add token to URL.

### Now (Automatic):
```
✅ Setup workspace with: https://github.com/example-org/example-repo.git
```
Server automatically injects token! Just use regular HTTPS URLs.

---

## What URLs to Use

### ✅ Use HTTPS URLs:
```
https://github.com/example-org/example-repo.git
https://github.com/example-org/example-repo.git
```

### ❌ Don't use SSH URLs (unless SSH is configured):
```
git@github.com:example-org/example-repo.git  ← Will fail without SSH agent
```

---

## Environment Variable (Alternative)

Instead of config file, you can use environment variable:

**PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', '<github-token>', 'User')
```

Then restart VSCode. Server will use `GITHUB_TOKEN` automatically.

---

## For Your Team

### Team Setup Instructions:

**Option A: Each user configures their own token**
1. Each developer generates their own GitHub PAT
2. Adds to their local `config/default_config.json`
3. File is in `.gitignore` so token stays private

**Option B: Environment variable**
1. Each developer sets `GITHUB_TOKEN` environment variable
2. No config file changes needed
3. More secure (not in files)

---

## Security

### ✅ Safe:
- Token in `config/default_config.json` (it's in `.gitignore`)
- Token in environment variable
- Token is only used locally

### ❌ Never:
- Commit token to git
- Share token publicly
- Use same token in CI/CD (use GitHub Actions tokens)

---

## Testing Your Setup

### 1. Check token is configured:
Edit `config/default_config.json` - should see `"github_token": "ghp_..."`

### 2. Restart VSCode
Close completely and reopen.

### 3. Create test workspace:
```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
Name it "test"
```

### 4. Look for this message:
```
✓ Using GitHub token for authentication
✓ Cloned: example-repo
```

If you see this, **token authentication is working!** 🎉

---

## Troubleshooting

### Token not working?

**Check 1:** Is token in config file?
- Open `config/default_config.json`
- Verify `"github_token": "ghp_..."`

**Check 2:** Did you restart VSCode?
- Must close completely (not just reload window)

**Check 3:** Is token valid?
- Test: `git ls-remote https://YOUR_TOKEN@github.com/example-org/example-repo.git`
- If fails: Generate new token

**Check 4:** Are you using HTTPS URLs?
- Use `https://github.com/...`
- Not `git@github.com:...`

---

## Quick Reference

### Generate Token:
GitHub → Settings → Developer settings → PAT → Generate → Check "repo" → Copy

### Add to Config:
Edit: `config/default_config.json`
Add: `"github_token": "<github-token>"`

### Restart:
Close VSCode → Wait → Reopen

### Test:
Create workspace with HTTPS URLs

---

## ⏱️ Total Time: ~5 Minutes

1. Generate token: 2 minutes
2. Add to config: 1 minute  
3. Restart VSCode: 30 seconds
4. Test workspace: 1 minute

**Then you're set for automatic authentication!** 🚀

---

## Next Steps

After token is working:

1. **Create your real workspaces** with actual repos
2. **Use cross-repo search** to find code patterns
3. **Update all repos** with one command
4. **Share setup with your team** (each person needs their own token)

**See README.md for full documentation on all features!**
