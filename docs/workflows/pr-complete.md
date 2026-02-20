# PR Complete Workflow

This document describes the complete workflow for Marty AI code review system.

## Overview

The system consists of four distinct phases that work together to provide comprehensive PR management:

1. **Initial Analysis** - When a PR is first created
2. **Continuous Review** - Senior developer review on each update
3. **Continuous Development** - Discussion and fix capabilities
4. **Manual Review** - Triggered on demand

---

## Phase 1: Initial Analysis

**Trigger**: When a PR is created (`pull_request` event, type: `opened`)

### Purpose

Perform initial analysis of the PR and set up the main tracking comment.

### Actions

- Analyze the PR content (title, description, changed files)
- Add appropriate labels (e.g., bug, enhancement, security)
- Assign reviewers if needed
- **Create the main tracking comment** that will be updated throughout the lifecycle

### Technical Implementation

1. **Main Comment Strategy**: Instead of using PR description (which would overwrite user content), create a dedicated comment with a unique identifier.

2. **Unique Marker**: Use a marker like `[Marty Review #<PR_NUMBER>]` to identify the main comment.

3. **Comment Structure**: The main comment contains:
   - PR overview and summary
   - Current status (In Progress / Changes Requested / Approved)
   - Key concerns to address
   - Progress tracking (what's been addressed)
   - Last updated timestamp

### Example Comment Structure

```markdown
# Marty Review #123

## Overview
[Summary of what the PR does]

## Status
🟡 In Progress

## Key Concerns
- [ ] Security: Input validation missing in auth.py
- [ ] Performance: N+1 query in user service

## Progress
- ✅ Fixed: Code duplication in utils.py
- 🔄 In Progress: Adding tests for new endpoint

---
*Last updated: 2024-01-15 10:30 UTC*
```

---

## Phase 2: Continuous Review

**Trigger**: On PR events (`synchronize`, `ready_for_review`, `reopened`)

### Purpose

Provide senior developer-level review on each PR update, ensuring production readiness.

### Key Principle: Update, Don't Create

**IMPORTANT**: On each push (synchronize event), Marty must:
1. **Find the existing main comment** using the unique marker `[Marty Review #<PR_NUMBER>]`
2. **UPDATE that comment** with new information - do NOT create new comments
3. Only post inline comments for specific code issues

**Fallback**: If main comment doesn't exist (e.g., `opened` workflow failed), create it first, then continue with update.

This ensures:
- No duplicate comments
- Clean conversation flow
- Single source of truth for PR status

### Features

#### Analyze Previous Reviews
- Check existing reviews and comments on the PR
- Understand what issues were already raised
- Focus on NEW changes only
- Mark addressed points as outdated when possible

#### Holistic Code Analysis
- Understand the codebase architecture
- Look at related files that might be affected
- Check if changes fit existing patterns and design
- Verify code follows project conventions

#### Production Readiness Checklist

**Code Quality**
- Follows best practices and design patterns
- Proper error handling and edge cases
- No code duplication (DRY principle)
- Clear and maintainable structure
- Consistent conventions with rest of codebase

**Security**
- No hardcoded secrets or credentials
- Proper input validation and sanitization
- No SQL injection or XSS vulnerabilities
- Authentication and authorization checks
- Sensitive data handling
- Use web research for known vulnerabilities

**Testing**
- Tests exist for new functionality
- Adequate test coverage
- Edge cases covered
- Test quality and assertions
- Run existing tests to ensure nothing breaks

**Performance**
- No potential bottlenecks
- Efficient database queries
- Proper caching strategies
- Resource cleanup

**Documentation**
- README updated if needed
- Inline comments for complex logic
- API documentation updated
- Breaking changes documented

#### Review Output Guidelines

- Use inline comments for specific issues
- DO NOT post global summary comments (pollutes conversation)
- Keep summaries brief and focused on critical issues only
- Mark addressed points as outdated when possible

#### Final Verdict

Provide a brief verdict:
- **APPROVED** - Ready for merge
- **CHANGES REQUESTED** - Needs modifications before merge
- **COMMENTED** - Notes provided, no blocking issues

---

## Phase 3: Continuous Development

**Triggers**:
- `issue_comment` (on PR issues)
- `pull_request_review_comment` (inline comments)

### Workflows

#### PR Discussion (`pr-discussion.yml`)

Triggered when someone mentions `@martyy-code` in a comment.

Capabilities:
- Respond to questions about the PR
- Explain code sections
- Suggest improvements
- Discuss implementation details

#### PR Fix (`pr-fix.yml`)

Triggered by commands:
- `@martyy-code fix`
- `@martyy-code fix this`
- `@martyy-code correct`
- `@martyy-code apply`

Capabilities:
- Read PR details and comments
- Review changed files
- Implement requested fixes
- Commit and push changes

---

## Phase 4: Manual Review

**Trigger**: `workflow_dispatch` (manual) or via comment command

### Purpose

Allow triggering a full senior review on demand, useful for:
- After significant changes
- Before merge
- On request from PR author

---

## Technical Notes

### Token Management

The workflow uses a GitHub App token generated via `actions/create-github-app-token`:
- App ID: `${{ secrets.MARTY_APP_ID }}`
- Private Key: `${{ secrets.MARTY_APP_PRIVATE_KEY }}`

### Permissions Required

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
  actions: read
  id-token: write
```

### Tools Available

- `gh pr` - PR operations
- `gh api` - GitHub API calls
- `gh run` - CI/CD information
- `WebFetch` - Up-to-date information from web
- `git` - Version control operations

### Finding and Updating Main Comment

The comment ID is found each time by searching for the unique marker in the comment body:

```bash
# Find Marty's main review comment and get its ID
# Note: GitHub Apps appear as user.type == "Bot"
COMMENT_ID=$(gh api repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments \
  --jq '.[] | select(.user.type == "Bot" and .body | contains("[Marty Review #'${PR_NUMBER}'")) | .id')
```

Then **edit (PATCH)** the same comment - this updates the content while keeping the same comment ID:

```bash
# Update the comment (PATCH keeps same comment ID)
gh api -X PATCH repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments/$COMMENT_ID \
  -f body="Updated content with same [Marty Review #${PR_NUMBER}] marker"
```

**Key points**:
- The marker `[Marty Review #<PR_NUMBER>]` stays in the comment body at each update
- The comment ID remains the same because we PATCH (edit) rather than POST (create)
- GitHub App users appear as `user.type == "Bot"` in the API

### Concurrency

To prevent conflicts when multiple runs happen simultaneously, use GitHub Actions concurrency:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number }}
  cancel-in-progress: true
```

### Marking Comments as Outdated

GitHub marks comments as outdated when:
- A new commit addresses the comment
- Uses `PATCH` API with `line` or `side` changes

---

## Workflow Events Summary

| Event | Type | Action |
|-------|------|--------|
| `pull_request` | `opened` | Create main comment |
| `pull_request` | `synchronize` | Update main comment |
| `pull_request` | `ready_for_review` | Update main comment |
| `pull_request` | `reopened` | Update main comment |
| `issue_comment` | `created` | Discussion / Fix |
| `pull_request_review_comment` | `created` | Discussion |
| `workflow_dispatch` | - | Manual Review |

---

## Future Enhancements

1. **Auto-update main comment** - Parse previous reviews to update status
2. **Security scanning** - Integrate dependency vulnerability checks
3. **Test execution** - Run tests and report results in review
4. **Multi-language support** - Adapt review style to project language
5. **Learning from feedback** - Track which suggestions are accepted
