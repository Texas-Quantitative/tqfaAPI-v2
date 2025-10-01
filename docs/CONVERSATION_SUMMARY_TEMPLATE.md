# 🤖 Conversation Summary Template for AI Agents

**USE THIS TEMPLATE when summarizing conversations to prevent context loss!**

## Summary Structure

### 1. Context Overview
```markdown
## Conversation Summary - [Date]

### Primary Objectives
- [Main goal 1]
- [Main goal 2] 
- [Main goal 3]

### Session Context  
- **User Intent**: [What the user was trying to accomplish]
- **Starting State**: [What was the situation when conversation began]
- **Environment**: [Which branch/environment was being worked on]
```

### 2. Critical Technical Details (NEVER OMIT)
```markdown
### Critical Technical Details
- **Current Resource Groups**: 
  - DEV: rg-tqa-dev (eastus) → kv-tqa-dev
  - UAT: tqfa-uat-rg (eastus2) → kv-tqfa-uat ⚠️ DIFFERENT NAMING
  - PROD: rg-tqa-prod (eastus) → kv-tqa-prod
- **Recent Infrastructure Changes**: [Any resource changes made]
- **Security Model**: [Current auth/security patterns]
- **Deployment State**: [What's currently deployed, any issues]
```

### 3. Problem Resolution Progress
```markdown
### Problems Encountered & Solutions
1. **Issue**: [Specific problem]
   - **Cause**: [Root cause identified]
   - **Solution**: [What was done to fix it]
   - **Status**: [Resolved/Partial/Ongoing]
   - **Context**: [Why this happened, how to prevent recurrence]

2. **Issue**: [Next problem]
   - [Same format...]
```

### 4. Architectural Decisions Made
```markdown
### New Architectural Decisions
- **[Date] ADR-XXX**: [Decision made]
  - **Problem**: [What was the issue]
  - **Solution**: [Approach taken]
  - **Impact**: [What this changes]
  - **Rationale**: [Why this approach was chosen]
```

### 5. Working Code & Verified Outcomes
```markdown
### Working Solutions & Code
- **Local Functionality**: [What works locally]
- **Production Functionality**: [What works in UAT/prod]
- **Verified Commands**: [Commands that were tested and work]
- **Working Scripts**: [Scripts that function correctly]
```

### 6. Active Issues & Next Steps
```markdown
### Outstanding Issues
- **Issue 1**: [Description] - [Why it's not yet resolved]
- **Issue 2**: [Description] - [Blocking factors]

### Next Steps for Future Sessions
1. [Specific action needed]
2. [Another specific action]
3. [Third action]

### Continuation Context
- **Last Working State**: [Where things were left]
- **Environment State**: [What deployments are active]
- **Required Verification**: [What needs to be tested]
```

### 7. Documentation Updates Made
```markdown
### Documentation Changes
- [ ] Updated AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md
- [ ] Updated ARCHITECTURAL_DECISIONS.md  
- [ ] Updated QUICK_REFERENCE.md
- [ ] Updated copilot-instructions.md
- [ ] Updated README.md
- [ ] Other: [specify]

### Critical Context for Future Agents
- [Key insight that must not be lost]
- [Important pattern or decision rationale]
- [Warning about what not to do]
```

## 🚨 Summary Quality Checklist

**Before finalizing any summary, verify:**

- [ ] **Resource names are EXACT** (not generalized)
- [ ] **UAT naming difference is explicitly mentioned**
- [ ] **Security decisions include full context**
- [ ] **Failed approaches are documented with reasons**
- [ ] **Working solutions include exact commands/code**
- [ ] **Next steps are specific and actionable**
- [ ] **Documentation updates are tracked**
- [ ] **All "why" context is preserved, not just "what"**

## ❌ Common Summary Anti-Patterns

**NEVER DO THIS:**
- "Made some configuration changes" → BE SPECIFIC
- "Fixed minor naming issues" → EXPLAIN THE EXACT ISSUE
- "Updated Azure resources" → LIST EXACT CHANGES
- "Resolved deployment problems" → DOCUMENT ROOT CAUSE & SOLUTION
- "Made architectural improvements" → EXPLAIN DECISIONS & RATIONALE

**ALWAYS DO THIS:**
- "Changed Key Vault URL from kv-tqa-uat to kv-tqfa-uat because..."
- "Moved resources from rg-tqa-uat to tqfa-uat-rg to resolve cross-resource-group access failures"
- "Removed public user creation endpoint for security, implemented X-Admin-Key authentication"
- "Container deployment failed because managed identity lacked Key Vault RBAC permissions, granted Key Vault Secrets User role"

---

**🎯 Remember**: Future agents depend on these summaries to avoid repeating expensive mistakes and losing architectural context. Every detail you preserve saves hours of rediscovery work.