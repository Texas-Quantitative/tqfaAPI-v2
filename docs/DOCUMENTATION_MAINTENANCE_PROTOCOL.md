# 📝 Documentation Maintenance Protocol

**🚨 CRITICAL FOR AI AGENTS: This protocol prevents the architectural drift and resource confusion that has occurred in the past.**

## 🔄 Documentation Update Triggers

**MANDATORY UPDATES** - Update documentation immediately when:

1. **Azure Resource Changes**
   - Creating/deleting resource groups
   - Adding/removing Key Vaults, Container Apps, Storage Accounts
   - Changing resource naming conventions
   - Modifying cross-resource permissions or access patterns

2. **Deployment Configuration Changes**
   - GitHub Actions workflow modifications
   - Docker/container configuration changes
   - Environment variable or secret management changes
   - CI/CD pipeline updates

3. **Architectural Decisions**
   - Security model changes (authentication, authorization patterns)
   - Data flow modifications
   - Integration pattern changes (APIs, external services)
   - Performance or scalability architecture changes

4. **Naming Convention Changes**
   - Resource naming patterns
   - Environment identifiers
   - Service or component naming
   - Branch or deployment target naming

## 📋 Documentation Update Checklist

When making changes, update these documents in order:

### 1. Update Technical Documentation
- [ ] `docs/AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md`
  - Resource inventory by environment
  - Resource group mappings
  - Key Vault configurations
  - Deployment procedures
  
- [ ] `docs/ARCHITECTURAL_DECISIONS.md`
  - Add new ADR entry with date and rationale
  - Update affected architectural patterns
  - Document lessons learned

- [ ] `docs/QUICK_REFERENCE.md`
  - Update commands with new resource names
  - Revise troubleshooting steps if affected
  - Update environment mappings

### 2. Update Integration Points
- [ ] `.github/copilot-instructions.md`
  - Update any environment-specific guidance
  - Revise critical warnings if patterns changed

- [ ] `README.md`
  - Update quick start instructions if affected
  - Revise architecture overview if changed

- [ ] Code comments in:
  - [ ] `app/config.py` (Key Vault mappings)
  - [ ] `app/main_streamlined.py` (deployment reminders)

## 🧠 Context Preservation for Conversation Summaries

**⚠️ CRITICAL CONTEXT THAT MUST NOT BE LOST:**

### Resource Group Mapping (Current State)
```
Environment | Resource Group | Region  | Key Vault          | Notes
------------|---------------|---------|-------------------|------------------
DEV         | rg-tqa-dev    | eastus  | kv-tqa-dev        | Standard naming
UAT         | tqfa-uat-rg   | eastus2 | kv-tqfa-uat       | ⚠️ DIFFERENT NAMING!
PROD        | rg-tqa-prod   | eastus  | kv-tqa-prod       | Standard naming
```

**🔥 KEY INSIGHT**: UAT uses different naming convention due to historical resource consolidation to fix cross-resource-group access issues.

### Historical Issues That Must Not Recur
1. **Cross-Resource-Group Key Vault Access**: Container Apps in `tqfa-uat-rg` trying to access Key Vault in `rg-tqa-uat` - CAUSED DEPLOYMENT FAILURES
2. **Cached Docker Images**: Deployments appearing successful but not updating container code
3. **Missing Managed Identity Permissions**: Key Vault RBAC not configured for Container App identity
4. **Public User Registration**: Security vulnerability that was removed - NEVER re-enable

### Security Architecture (NEVER CHANGE WITHOUT REVIEW)
- Admin-only user creation with X-Admin-Key authentication
- No public registration endpoints (405 Method Not Allowed)
- Azure Key Vault with RBAC authorization (not access policies)
- AES-256 encrypted blob storage for user data

## 📊 Conversation Summary Guidelines

When creating conversation summaries, **ALWAYS INCLUDE**:

### Technical Context Section
```markdown
## Critical Technical Details
- Current resource group mappings by environment
- Any naming convention anomalies (especially UAT differences)
- Recent infrastructure changes and their rationale
- Active security patterns and any recent changes
- Deployment pipeline status and any recent fixes
```

### Decision Context Section  
```markdown
## Recent Architectural Decisions
- [Date] Decision: [Brief description]
- [Date] Problem solved: [What was broken]
- [Date] Security change: [What was hardened]
- [Date] Resource change: [What was moved/created/deleted]
```

### Known Issues & Workarounds
```markdown
## Active Issues & Context
- Any ongoing deployment issues
- Resource configurations that deviate from standard patterns
- Workarounds that must be maintained
- Dependencies on specific resource names or configurations
```

## 🚨 Anti-Patterns to Avoid

**❌ NEVER DO IN SUMMARIES:**
1. Summarize away resource naming details as "minor naming differences"
2. Omit the rationale behind architectural decisions
3. Skip documenting why certain resources are in different groups
4. Generalize security patterns without explaining the specific implementation
5. Lose the context of why certain "temporary" fixes became permanent

**✅ ALWAYS DO IN SUMMARIES:**
1. Preserve exact resource names and their locations
2. Explain the business/technical reason behind naming inconsistencies
3. Document what was tried and why it didn't work
4. Keep the full context of security decisions
5. Maintain the "why" behind architectural choices

## 🔄 Documentation Review Cycle

**Monthly Reviews** (or when onboarding new agents):
1. Verify all resource inventories are current
2. Check that architectural decisions reflect current state  
3. Update any outdated commands or procedures
4. Validate that security patterns haven't drifted

**Per-Deployment Reviews**:
1. Confirm resource mappings are accurate
2. Update deployment procedures with any lessons learned
3. Document any new issues or workarounds discovered

## 📢 Escalation Protocol

**If documentation becomes outdated or contradictory:**
1. **STOP** all infrastructure changes
2. **AUDIT** current Azure resources against documentation
3. **UPDATE** documentation to reflect actual state
4. **TEST** deployment procedures with updated docs
5. **RESUME** development work

---

**🎯 REMEMBER**: These documents are not just reference materials - they are the institutional memory that prevents repeating expensive mistakes. Treat them as critical infrastructure components, not nice-to-have documentation.

**📅 Last Updated**: 2025-09-25  
**🔄 Next Scheduled Review**: 2025-10-25