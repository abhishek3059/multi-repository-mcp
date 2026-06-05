# Flexible Repository Input Guide

The multi-repo MCP server now supports multiple repository input formats, making it easier to set up workspaces without typing full URLs.

## Supported Input Formats

### 1. Full HTTPS URL
```
https://github.com/example-org/example-repo.git
https://github.com/sample-org/example-data-platform.git
```

### 2. Full SSH URL
```
git@github.com:example-org/example-repo.git
git@github.com:sample-org/example-data-platform.git
```

### 3. Organization/Repository Format
```
example-org/example-repo
sample-org/example-data-platform
```

### 4. Repository Name Only (requires default org in config)
```
example-repo
example-repo
example-data-platform
```

## Configuration

Add your GitHub token and default organization to `config/default_config.json`:

```json
{
  "github_token": "<github-token>",
  "github_org": "example-org",
  "github_orgs": ["example-org", "sample-org"]
}
```

## Usage Examples

### Example 1: Mixed Input Formats
```
Setup a workspace with these repos:
- https://github.com/example-org/example-repo.git
- example-org/example-repo
- example-repo
Name it "my-workspace"
```

The system will automatically:
1. Use HTTPS URL as-is
2. Convert `example-org/example-repo` to HTTPS URL
3. Use default org for `example-repo` → `example-org/example-repo`
4. Inject GitHub token for authentication

### Example 2: Just Repository Names
```
Setup a workspace with these repos:
- example-repo
- example-repo
- example-repo
Name it "kar-workspace"
```

All repos will use the default organization `example-org`.

### Example 3: Multiple Organizations
```
Setup a workspace with these repos:
- example-org/example-repo
- sample-org/example-data-platform
- example-org/example-repo
Name it "cross-org-workspace"
```

Mix repos from different organizations seamlessly.

### Example 4: SSH URLs (Converted to HTTPS)
```
Setup a workspace with these repos:
- git@github.com:example-org/example-repo.git
- git@github.com:sample-org/example-data-platform.git
Name it "ssh-workspace"
```

SSH URLs are automatically converted to HTTPS with token authentication.

## How It Works

1. **Input Parsing**: Each repo input is analyzed to determine its format
2. **Normalization**: All inputs are converted to HTTPS URLs
3. **Token Injection**: GitHub token is automatically added for authentication
4. **Validation**: Errors are caught and reported before cloning
5. **Cloning**: Normalized URLs are used to clone repositories

## Output Example

When you set up a workspace, you'll see:

```
Workspace 'my-workspace' created and activated!

Repository Input Summary:
  • example-org/example-repo
    URL: https://github.com/example-org/example-repo.git
  • example-org/example-repo
    URL: https://github.com/example-org/example-repo.git
  • example-org/example-repo
    URL: https://github.com/example-org/example-repo.git

✓ Cloned: example-repo
✓ Cloned: example-repo
✓ Cloned: example-repo
```

## Error Handling

If a repository input is invalid, you'll get a clear error message:

```
Error parsing repositories:
✗ invalid-format: Invalid org/repo format. Expected 'org/repo'
✗ just-repo: Cannot parse 'just-repo' without a default organization
```

## Benefits

1. **Faster Setup**: Type less, work more
2. **Flexible**: Use whatever format is convenient
3. **Consistent**: All formats work the same way
4. **Safe**: GitHub token never exposed in commands
5. **Clear**: See exactly what will be cloned before it happens

## Requirements

- GitHub Personal Access Token with `repo` scope
- Token configured in `config/default_config.json`
- Default organization set (optional, for short names)

## Troubleshooting

### "Cannot parse without default organization"
- Solution: Set `github_org` in config or use `org/repo` format

### "Authentication failed"
- Solution: Check that `github_token` is valid and has `repo` scope

### "Invalid format"
- Solution: Use one of the supported formats above

## Advanced: Multi-Organization Support

The config supports multiple organizations:

```json
{
  "github_org": "example-org",
  "github_orgs": ["example-org", "sample-org"]
}
```

This helps document which organizations you commonly use, though the primary org (`github_org`) is used for short repo names.
