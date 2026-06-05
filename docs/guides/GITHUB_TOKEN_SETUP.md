# 🔑 How to Create a GitHub Personal Access Token

## Quick Steps (5 minutes)

### Step 1: Go to GitHub Settings
1. Log in to GitHub: https://github.com
2. Click your **profile picture** (top right)
3. Click **Settings**

### Step 2: Navigate to Developer Settings
1. Scroll down to the bottom of the left sidebar
2. Click **Developer settings**

### Step 3: Generate Token
1. Click **Personal access tokens**
2. Click **Tokens (classic)**
3. Click **Generate new token** → **Generate new token (classic)**

### Step 4: Configure Token
1. **Note:** Give it a name like `Multi-Repo MCP`
2. **Expiration:** Choose expiration (recommend: 90 days or No expiration for personal use)
3. **Select scopes:** Check ✅ **repo** (this gives full control of repositories)
   - This includes:
     - ✅ repo:status
     - ✅ repo_deployment
     - ✅ public_repo
     - ✅ repo:invite
     - ✅ security_events

### Step 5: Generate and Copy
1. Click **Generate token** (green button at bottom)
2. **IMPORTANT:** Copy the token immediately!
   - It looks like: `<github-token>`
   - You won't be able to see it again!
3. Save it somewhere safe temporarily

---

## Add Token to Multi-Repo MCP

### Method 1: Configuration File (Recommended)

Edit: `C:\Users\<you>\Desktop\multi-repo-mcp\config\default_config.json`

```json
{
  "storage_path": null,
  "ssh_key_path": "C:\\Users\\<you>\\.ssh\\id_ed25519",
  "github_token": "<github-token>",
  ...
}
```

Replace `"<github-token>"` with your actual token.

### Method 2: Environment Variable (More Secure)

Set environment variable:

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', '<github-token>', 'User')
```

**Or in System Settings:**
1. Search for "Environment Variables"
2. Click "Edit environment variables for your account"
3. Click "New"
4. Variable name: `GITHUB_TOKEN`
5. Variable value: `<github-token>`
6. Click OK
7. Restart VSCode

The MCP server will automatically use `GITHUB_TOKEN` if config file has `null`.

---

## Visual Guide

```
GitHub.com
  └─ Profile Picture (top right)
      └─ Settings
          └─ Developer settings (bottom left)
              └─ Personal access tokens
                  └─ Tokens (classic)
                      └─ Generate new token (classic)
                          ├─ Note: "Multi-Repo MCP"
                          ├─ Expiration: 90 days
                          └─ Scopes: [✓] repo
                              └─ Generate token
                                  └─ Copy token: <github-token>...
```

---

## Token Security

### ✅ DO:
- Store token in config file (it's in .gitignore)
- Or use environment variable
- Keep token private
- Regenerate if exposed

### ❌ DON'T:
- Commit token to git
- Share token publicly
- Use token in public repos

---

## Testing Your Token

Once you add the token to `default_config.json`, restart VSCode and try:

```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
- https://github.com/example-org/example-repo.git
Name it "kar-test"
```

The MCP server will automatically convert HTTPS URLs to include your token! 🎉

---

## Token Permissions Needed

For the multi-repo MCP server, you need the **`repo`** scope, which includes:

- ✅ Read/write access to code
- ✅ Read/write access to commit statuses
- ✅ Read/write access to deployments
- ✅ Read/write access to public and private repositories
- ✅ Read/write access to repository hooks and services
- ✅ Read/write access to repository projects
- ✅ Read access to user email addresses

This allows the server to:
- Clone private repositories
- Pull updates
- Push changes (future feature)
- Access all your org repositories

---

## If Token Expires

When your token expires:

1. Go back to GitHub → Settings → Developer settings → Personal access tokens
2. Find your token in the list
3. Click the token name
4. Click **Regenerate token**
5. Copy new token
6. Update `default_config.json` with new token
7. Restart VSCode

---

## Next Steps

After creating your token:

1. **Copy the token**
2. **Add to config:** Edit `config/default_config.json`
3. **Restart VSCode** (close and reopen completely)
4. **Test:** Create a workspace with HTTPS URLs
5. **Success!** Repos will clone automatically 🎉
