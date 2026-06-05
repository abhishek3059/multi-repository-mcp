# AI Code Review Integration

## Overview

The Multi-Repo MCP server now includes AI-powered code review using OpenAI's GPT-4. This feature reviews your code changes before pushing to ensure quality, security, and best practices.

## Setup Instructions

### 1. Install OpenAI Package

```bash
pip install openai
```

### 2. Add OpenAI API Key to Config

Edit `config/default_config.json`:

```json
{
  "code_review": {
    "enabled": true,
    "openai_api_key": "<openai-api-key>",
    "model": "gpt-4",
    "auto_push_threshold": 8.0,
    "default_review_depth": "standard"
  }
}
```

### 3. Restart MCP Server

After adding the API key, restart the MCP server in Cline settings or reload VS Code.

---

## Tool: push_with_review

### Description

Performs AI code review on uncommitted or unpushed changes before pushing to remote. Catches bugs, security issues, and code quality problems early.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| repo_name | string | ✅ Yes | - | Repository name |
| branch | string | ❌ No | current | Branch to push |
| set_upstream | boolean | ❌ No | false | Set upstream tracking |
| review_depth | string | ❌ No | "standard" | "quick", "standard", or "thorough" |
| auto_push_on_pass | boolean | ❌ No | false | Auto-push if review passes |

---

## Usage Examples

### Example 1: Review Before Manual Push

```json
{
  "repo_name": "example-repo"
}
```

**What Happens:**
1. Gets diff of unpushed changes
2. AI reviews the code
3. Shows review report with score and issues
4. Waits for manual approval to push

**Output:**
```
🤖 AI Code Review for 'example-repo'

📊 Overall Score: 8.5/10.0 🟢
🎯 Recommendation: ✅ SAFE TO PUSH

✅ Security: No issues found
✅ Best Practices: Following standards
✅ Performance: No concerns

💡 Suggestions (2):
   • Consider adding unit tests for new methods
   • Document public API methods

⏸️  Push NOT executed (requires manual approval)

To push manually, use:
  push_repo({"repo_name": "example-repo"})
```

---

### Example 2: Auto-Push on Pass

```json
{
  "repo_name": "example-repo",
  "auto_push_on_pass": true
}
```

**What Happens:**
1. Reviews code
2. If score ≥ 8.0 AND no security issues → **Pushes automatically**
3. If score < 8.0 OR security issues → Shows review, waits for manual push

**Output (Passing)**:
```
🤖 AI Code Review for 'example-repo'

📊 Overall Score: 9.0/10.0 🟢
🎯 Recommendation: ✅ SAFE TO PUSH

✅ Security: No issues found
✅ Best Practices: Following standards
✅ Performance: No concerns

✅ AUTO-PUSHED: Score 9.0/10 meets threshold 8.0
📤 Pushed 'example-repo' branch 'develop' to remote
```

---

### Example 3: Thorough Review

```json
{
  "repo_name": "example-release-ui",
  "review_depth": "thorough"
}
```

**Review Depths:**
- **quick**: Fast review (500 tokens, ~10 seconds)
- **standard**: Balanced review (1000 tokens, ~20 seconds) 
- **thorough**: Deep analysis (2000 tokens, ~40 seconds)

---

## Review Criteria

### 1. Code Quality (0-10)
- Clean code principles
- Readability and maintainability
- Code organization
- Naming conventions

### 2. Security (Pass/Fail)
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/Authorization issues
- Sensitive data exposure
- Input validation

### 3. Best Practices (0-10)
- Language conventions
- Framework patterns
- Error handling
- Code duplication
- Documentation

### 4. Performance (0-10)
- Algorithm complexity
- Resource usage
- Database queries
- Memory management
- Optimization opportunities

---

## Scoring System

| Score | Emoji | Recommendation | Action |
|-------|-------|----------------|--------|
| **9.0-10.0** | 🟢 | SAFE TO PUSH | Auto-push approved |
| **8.0-8.9** | 🟢 | SAFE TO PUSH | Auto-push approved |
| **6.0-7.9** | 🟡 | REVIEW RECOMMENDED | Manual approval |
| **0.0-5.9** | 🔴 | FIX ISSUES FIRST | Must fix before push |

**Security Override:** Any security issues → Manual approval required (no auto-push)

---

## Workflow Examples

### Workflow 1: Standard Development

```
1. Make code changes
2. stage_and_commit_repo({"repo_name": "example-repo", "message": "Add feature"})
3. push_with_review({"repo_name": "example-repo"})
4. Review AI feedback
5. If approved: push_repo({"repo_name": "example-repo"})
   If issues: Fix code and repeat from step 2
```

### Workflow 2: Confident Push

```
1. Make code changes
2. stage_and_commit_repo({"repo_name": "example-repo", "message": "Add feature"})
3. push_with_review({
     "repo_name": "example-repo",
     "auto_push_on_pass": true
   })
4. If score ≥ 8.0 → Automatically pushed ✅
   If score < 8.0 → Review feedback, fix, retry
```

### Workflow 3: Semantic-Release Repo with Review

```
1. Make code changes
2. commit_semantic_release_repo({
     "repo_name": "example-release-ui",
     "commit_type": "feat",
     "scope": "dashboard",
     "subject": "add analytics widget"
   })
3. push_with_review({
     "repo_name": "example-release-ui",
     "review_depth": "thorough"
   })
4. Review AI feedback
5. push_repo({"repo_name": "example-release-ui"})
```

---

## Configuration Options

### config/default_config.json

```json
{
  "code_review": {
    "enabled": true,
    "openai_api_key": "<openai-api-key>",
    "model": "gpt-4",
    "auto_push_threshold": 8.0,
    "default_review_depth": "standard"
  }
}
```

**Configuration Fields:**

- **enabled** (boolean): Enable/disable code review feature
- **openai_api_key** (string): Your OpenAI API key
- **model** (string): OpenAI model ("gpt-4", "gpt-3.5-turbo", etc.)
- **auto_push_threshold** (number): Minimum score for auto-push (0-10)
- **default_review_depth** (string): "quick", "standard", or "thorough"

---

## Cost Considerations

### OpenAI API Costs (Approximate)

| Review Depth | Tokens | Cost (GPT-4) | Cost (GPT-3.5) |
|--------------|--------|--------------|----------------|
| Quick | ~500 | $0.015 | $0.001 |
| Standard | ~1000 | $0.030 | $0.002 |
| Thorough | ~2000 | $0.060 | $0.004 |

**Recommendations:**
- Use **"standard"** for regular development
- Use **"quick"** for minor changes
- Use **"thorough"** for critical features
- Consider GPT-3.5 for cost savings (lower quality but cheaper)

---

## Error Handling

### Common Errors

#### 1. No API Key
```
Error: Code review is not enabled. Please add OpenAI API key to config/default_config.json
```
**Solution**: Add your OpenAI API key to config file

#### 2. Invalid API Key
```
Error during code review: Invalid OpenAI API key
```
**Solution**: Verify your API key is correct and active

#### 3. Rate Limit
```
Error during code review: OpenAI API rate limit exceeded
```
**Solution**: Wait a few minutes and retry, or upgrade your OpenAI plan

#### 4. No Changes
```
ℹ️  No unpushed changes in 'repo-name'
```
**Solution**: This is normal - commit changes first before reviewing

---

## Best Practices

### 1. Always Review Before Production Pushes
```json
{
  "repo_name": "critical-repo",
  "review_depth": "thorough",
  "auto_push_on_pass": false
}
```
Manual approval ensures nothing slips through.

### 2. Use Auto-Push for Non-Critical Changes
```json
{
  "repo_name": "dev-repo",
  "auto_push_on_pass": true
}
```
Saves time on straightforward changes.

### 3. Thorough Review for Security-Sensitive Code
```json
{
  "repo_name": "auth-service",
  "review_depth": "thorough"
}
```
Extra scrutiny for authentication, payment, etc.

### 4. Quick Review for Documentation
```json
{
  "repo_name": "docs-repo",
  "review_depth": "quick"
}
```
Docs rarely need deep review.

---

## Advanced Features

### Customizing Review Threshold

Lower threshold for experimental branches:
```json
// In config
"auto_push_threshold": 6.0
```

Higher threshold for production:
```json
"auto_push_threshold": 9.0
```

### Multiple Reviews

Review multiple times with different depths:
```
1. Quick review for initial check
2. Thorough review before production push
```

---

## Integration with Cline

### How Cline Uses This

1. **Cline makes code changes** → write_to_file, replace_in_file
2. **Cline commits** → commit_semantic_release_repo or stage_and_commit_repo
3. **Before pushing**, Cline uses → push_with_review
4. **AI reviews code** → Shows feedback
5. **User decides** → Approve push or fix issues

### Cline Best Practices

**When Cline Should Use push_with_review:**
- ✅ Before pushing to main/develop/production branches
- ✅ When making significant changes
- ✅ For security-sensitive code
- ✅ When user requests code review

**When Cline Can Skip Review:**
- Small documentation changes
- Configuration updates
- Dependency version bumps
- Obvious typo fixes

---

## Limitations

1. **Diff Size**: Reviews first 4000 characters of diff (limits API costs)
2. **Network Required**: Requires internet connection for OpenAI API
3. **API Costs**: Each review costs $0.01-$0.06 depending on depth
4. **No Context**: AI only sees the diff, not the entire codebase
5. **False Positives**: AI may flag non-issues occasionally

---

## Troubleshooting

### Review Taking Too Long
- Use "quick" review depth
- Check internet connection
- Verify OpenAI API status

### Low Scores on Good Code
- AI may not have full context
- Consider the feedback, but use judgment
- Thorough review provides better context

### High Costs
- Use GPT-3.5 instead of GPT-4
- Use "quick" or "standard" depth
- Reserve "thorough" for critical code

---

## Future Enhancements (Potential)

1. **Local Model Support** - Use Ollama/LLaMA for offline reviews
2. **Custom Rules** - Define organization-specific review criteria
3. **Learning Mode** - AI learns from your feedback
4. **Team Reviews** - Share review results with team
5. **Metrics Dashboard** - Track code quality over time

---

## Summary

The **push_with_review** tool adds an intelligent safety layer before pushing code. It helps maintain high code quality, catch bugs early, and ensure security best practices - all before code reaches your remote repository.

**Key Benefits:**
- 🛡️ Catch bugs before they reach production
- 🔒 Identify security vulnerabilities early
- 📚 Learn best practices from AI feedback
- ⚡ Fast reviews (10-40 seconds)
- 🤖 Automated quality gate

**Get Started:**
1. Add OpenAI API key to config
2. Install openai package
3. Use push_with_review instead of push_repo
4. Review AI feedback
5. Push with confidence!
