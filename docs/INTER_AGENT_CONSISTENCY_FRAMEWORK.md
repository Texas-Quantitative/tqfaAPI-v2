# 🤖 Inter-Agent Consistency Framework Template

**Copy and customize this framework for any project requiring consistent AI agent behavior across sessions.**

---

## 📋 Project-Specific Copilot Instructions Template

**File**: `.github/copilot-instructions.md`

```markdown
<!-- Use this file to provide workspace-specific custom instructions to Copilot -->

# [PROJECT NAME] - Copilot Instructions

## Project Overview
[Brief description of the project, tech stack, and architecture]

## ⚠️ CRITICAL: Project Infrastructure Documentation
**BEFORE making any infrastructure/deployment changes, ALWAYS:**

1. **Read the Documentation Maintenance Protocol**: Check `docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md` - PREVENTS RESOURCE CONFUSION
2. **Read the Infrastructure Guide**: Check `docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md` for current state
3. **Review Architectural Decisions**: Check `docs/ARCHITECTURAL_DECISIONS.md` for design patterns
4. **Use Quick Reference**: See `docs/QUICK_REFERENCE.md` for common tasks and troubleshooting
5. **Update Documentation**: If you make infrastructure changes, update the guides
6. **Cross-Reference Resources**: Verify resource relationships and dependencies
7. **Test Changes**: Always test after infrastructure modifications

**🔥 CRITICAL CONTEXT - Environment Anomalies:**
- [List any environment-specific naming or configuration differences]
- [Document any historical decisions that differ from standards]
- **NEVER** summarize these as "minor differences" - they're critical infrastructure context!

**Common Issues to Avoid:**
- [Project-specific anti-patterns]
- [Common deployment pitfalls]
- [Security vulnerabilities to watch for]
- [Resource configuration mistakes]
- Losing critical context in conversation summaries

## Code Standards & Practices
[Your project-specific coding standards]

## Development Workflow
[Your project-specific development practices]
```

---

## 📚 Documentation Structure Template

### 1. Documentation Maintenance Protocol
**File**: `docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md`

```markdown
# 📝 Documentation Maintenance Protocol

**🚨 CRITICAL FOR AI AGENTS: This protocol prevents architectural drift and resource confusion.**

## 🔄 Documentation Update Triggers

**MANDATORY UPDATES** - Update documentation immediately when:

1. **Infrastructure Changes**
   - [List your infrastructure types: cloud resources, databases, services, etc.]

2. **Deployment Configuration Changes**
   - [List your deployment mechanisms: CI/CD, container configs, etc.]

3. **Architectural Decisions**
   - [List your key architectural areas: security, integrations, etc.]

4. **Naming Convention Changes**
   - [List your naming patterns: resources, environments, etc.]

## 📋 Documentation Update Checklist

When making changes, update these documents in order:
- [ ] `docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md`
- [ ] `docs/ARCHITECTURAL_DECISIONS.md`  
- [ ] `docs/QUICK_REFERENCE.md`
- [ ] `.github/copilot-instructions.md`
- [ ] `README.md`
- [ ] [Other project-specific docs]

## 🧠 Context Preservation for Conversation Summaries

**⚠️ CRITICAL CONTEXT THAT MUST NOT BE LOST:**

### Resource Mapping (Current State)
```
Environment | [Resource Type] | [Location] | [Key Config] | Notes
------------|----------------|------------|--------------|-------
DEV         | [details]      | [region]   | [config]     | [notes]
STAGING     | [details]      | [region]   | [config]     | [notes]  
PROD        | [details]      | [region]   | [config]     | [notes]
```

### Historical Issues That Must Not Recur
1. **[Issue Type]**: [Description] - CAUSED [Impact]
2. **[Issue Type]**: [Description] - [Prevention method]

### [Project] Architecture (NEVER CHANGE WITHOUT REVIEW)
- [Key security pattern 1]
- [Key security pattern 2] 
- [Key integration pattern]
- [Key data pattern]

## 📊 Conversation Summary Guidelines
[Include the conversation summary template - see section below]
```

### 2. Architectural Decision Record Template
**File**: `docs/ARCHITECTURAL_DECISIONS.md`

```markdown
# 🏗️ Architectural Decision Record (ADR) & Design Principles

**📋 PROMPT FOR FUTURE AGENTS:**
```
When making architectural changes to this [PROJECT TYPE] project, ALWAYS:
1. Read this entire file to understand existing design decisions
2. Read docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md to prevent context loss
3. Update this file if you make changes that affect system architecture
4. Follow the established patterns and principles documented here
5. Verify that new decisions don't conflict with existing ones
6. Add new ADRs at the bottom with date, rationale, and impact assessment
7. Use the conversation summary template to preserve critical context
```

## 🎯 Core Architectural Principles

### 1. **[Principle Name]** ✅ ESTABLISHED
- **Decision**: [What was decided]
- **Rationale**: [Why this decision was made]
- **Impact**: [What this affects]
- **Status**: [ACTIVE/DEPRECATED/CRITICAL - change policy]

### 2. **[Next Principle]** ✅ ESTABLISHED
[Same format...]

## 🏛️ System Architecture Patterns

### [System Component 1]
```
[ASCII diagram or description]
```
**🔒 RULE**: [Key rule about this component]

### [System Component 2]
**Pattern**: [Established pattern]
**Configuration**: [Current setup]
**🚨 CRITICAL**: [Important constraint]

## Historical Decisions & Lessons Learned

### ADR-001: [Decision Name] ([Date])
- **Problem**: [What problem were you solving?]
- **Solution**: [What approach did you take?]
- **Impact**: [What does this change?]
- **Lesson**: [What should future agents know?]

## 🚨 Critical Warnings for Future Agents

### ❌ NEVER DO THIS:
1. **[Anti-pattern 1]** - [Consequence]
2. **[Anti-pattern 2]** - [Consequence]

### ✅ ALWAYS DO THIS:
1. **[Good practice 1]** - [Benefit]
2. **[Good practice 2]** - [Benefit]
```

### 3. Infrastructure Guide Template
**File**: `docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md`

```markdown
# 🏗️ Infrastructure & Deployment Guide

**📋 PROMPT FOR UPDATING THIS DOCUMENT:**
When you make infrastructure changes, follow these steps:
1. Update the resource inventory below with exact names and configurations
2. Update the deployment procedures with any new steps or changes
3. Add troubleshooting entries for any new issues encountered
4. Test all updated procedures before marking them as current
5. Update the "Last Updated" date at the bottom

## 🗺️ Current Infrastructure Mapping

### [Environment 1] Environment
**Resource Group**: [name]
**Region**: [region]
**Resources**:
- [Resource Type]: [exact name] - [purpose]
- [Resource Type]: [exact name] - [purpose]

### [Environment 2] Environment
[Same format...]

## 🚀 Deployment Procedures

### [Deployment Method 1]
**Trigger**: [when this runs]
**Steps**:
1. [Step 1]
2. [Step 2]
**Verification**: [how to confirm success]

## 🔧 Troubleshooting Guide

### Common Issues

| Problem | Symptoms | Root Cause | Solution |
|---------|----------|------------|----------|
| [Issue 1] | [How to identify] | [Why it happens] | [How to fix] |
| [Issue 2] | [How to identify] | [Why it happens] | [How to fix] |

**📅 Last Updated**: [Date]
```

### 4. Quick Reference Template
**File**: `docs/QUICK_REFERENCE.md`

```markdown
# 🚀 Quick Reference for AI Agents

## 🔍 Essential Files to Check BEFORE Making Changes

| File | Purpose | When to Check |
|------|---------|---------------|
| `docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md` | Infrastructure mapping | Any infrastructure changes |
| `docs/ARCHITECTURAL_DECISIONS.md` | Design principles | Any architectural changes |
| `.github/copilot-instructions.md` | Code standards | All development work |

## ⚡ Common Tasks - Quick Commands

### [Common Task 1]
```bash
[command 1]
[command 2]
```

### [Common Task 2]
```bash
[command 1]
[command 2]
```

## 🚨 Critical Rules (NEVER VIOLATE)

1. **🔐 NEVER [security violation]**
2. **🏢 NEVER [infrastructure mistake]**
3. **🔗 NEVER [architectural violation]**
4. **📝 ALWAYS [documentation requirement]**

## 🏗️ Architecture at a Glance

```
[Simple architecture diagram]
```

## 💡 Pro Tips

- **[Tip 1]** - [Explanation]
- **[Tip 2]** - [Explanation]
```

### 5. Conversation Summary Template
**File**: `docs/CONVERSATION_SUMMARY_TEMPLATE.md`

```markdown
# 🤖 Conversation Summary Template for AI Agents

## Summary Structure

### 1. Context Overview
```markdown
## Conversation Summary - [Date]

### Primary Objectives
- [Main goal 1]
- [Main goal 2]

### Session Context  
- **User Intent**: [What user wanted]
- **Starting State**: [Initial situation]
- **Environment**: [Which environment worked on]
```

### 2. Critical Technical Details (NEVER OMIT)
```markdown
### Critical Technical Details
- **Current [Resource Type]**: [Exact configurations]
- **Recent Changes**: [Any modifications made]
- **Security Model**: [Current patterns]
- **Deployment State**: [Current status]
```

### 3. Problem Resolution Progress
```markdown
### Problems & Solutions
1. **Issue**: [Specific problem]
   - **Cause**: [Root cause]
   - **Solution**: [What was done]
   - **Status**: [Resolved/Partial/Ongoing]
   - **Context**: [Why this happened, prevention]
```

### 4. Working Code & Verified Outcomes
```markdown
### Verified Solutions
- **Local Functionality**: [What works locally]
- **Production Functionality**: [What works in production]
- **Tested Commands**: [Commands that work]
```

### 5. Documentation Updates Made
```markdown
### Documentation Changes
- [ ] Updated [INFRASTRUCTURE_GUIDE]
- [ ] Updated [ARCHITECTURAL_DECISIONS]
- [ ] Updated [QUICK_REFERENCE]
- [ ] Other: [specify]

### Critical Context for Future Agents
- [Key insight that must not be lost]
- [Important decision rationale]
- [Warning about what not to do]
```

## 🚨 Summary Quality Checklist

- [ ] **Resource names are EXACT** (not generalized)
- [ ] **Environment differences explicitly mentioned**
- [ ] **Security decisions include full context**
- [ ] **Failed approaches documented with reasons**
- [ ] **Next steps are specific and actionable**
```

---

## 🎯 VS Code Settings Template

**File**: `.vscode/settings.json`

```json
{
  "workbench.startupEditor": "readme",
  
  "todo-tree.general.tags": [
    "TODO",
    "FIXME", 
    "INFRA-DOCS",
    "DEPLOY-CHECK"
  ],
  
  "todo-tree.highlights.customHighlight": {
    "INFRA-DOCS": {
      "icon": "cloud",
      "foreground": "#0078d4",
      "background": "#e1f5fe"
    },
    "DEPLOY-CHECK": {
      "icon": "rocket", 
      "foreground": "#f57c00",
      "background": "#fff3e0"
    }
  }
}
```

---

## 📖 README Template Addition

Add this section to your `README.md`:

```markdown
## ⚠️ **IMPORTANT: Infrastructure Documentation**

**📋 Documentation Protocol**: READ [`docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md`](./docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md) FIRST

**🔍 Before infrastructure changes:** Read [`docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md`](./docs/INFRASTRUCTURE_AND_DEPLOYMENT_GUIDE.md)

**🏗️ Before architectural changes:** Read [`docs/ARCHITECTURAL_DECISIONS.md`](./docs/ARCHITECTURAL_DECISIONS.md)

**⚡ For quick help:** See [`docs/QUICK_REFERENCE.md`](./docs/QUICK_REFERENCE.md)

**🚨 CRITICAL**: [List your environment-specific anomalies here]
```

---

## 🚀 Implementation Checklist

To implement this framework in a new project:

- [ ] Create `.github/copilot-instructions.md` with project-specific content
- [ ] Create `docs/` folder with all template files
- [ ] Customize templates with your project's specifics
- [ ] Add infrastructure documentation requirements to README
- [ ] Set up VS Code settings for consistency reminders
- [ ] Train team/agents on documentation maintenance protocol
- [ ] Establish regular documentation review cycle

---

## 🎯 Customization Guide

**For each new project, customize:**

1. **Technology Stack**: Replace [PROJECT TYPE] with your stack (FastAPI, React, etc.)
2. **Infrastructure Types**: Replace Azure resources with your cloud provider
3. **Environment Names**: Update DEV/UAT/PROD to match your environments
4. **Common Issues**: Document your project's specific pitfalls
5. **Anti-Patterns**: List your domain-specific things to avoid
6. **Commands**: Replace example commands with your project's tools

**Key Success Factors:**
- Be specific, not generic
- Document the "why" behind decisions, not just the "what"
- Include exact resource names and configurations
- Update immediately when changes occur
- Never lose historical context in summaries

---

**💡 This framework prevents the architectural drift, resource confusion, and context loss that plague multi-agent development projects. Adapt it to your specific needs and maintain it religiously!**