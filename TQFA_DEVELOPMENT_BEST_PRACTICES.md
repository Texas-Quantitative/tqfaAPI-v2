# TQFA API Development Best Practices

*Essential principles and quick reference for building production-ready FastAPI applications*

**Last Modified**: September 27, 2025  
**Version**: 2.1

---

## 📋 **Instructions for AI Agents**

### **How to Use This Documentation**

This document is the **main entry point** for TQFA API development practices:

1. **Quick Reference**: This document provides essential commands and principles
2. **Detailed Guides**: Link to `docs/best-practices/` for specific problems
3. **Update Protocol**: Always update "Last Modified" date when making changes
4. **Context Preservation**: Use this for agent handoffs and project setup
5. **New Projects**: Copy the entire structure for reuse

### **When to Update Documentation**

**ALWAYS update the "Last Modified" date when you:**
- ✅ Add new deployment lessons or solutions
- ✅ Update scripts, commands, or code examples
- ✅ Fix errors or improve existing explanations  
- ✅ Add new sections or reorganize content
- ✅ Update Azure resource information or URLs

### **📚 CRITICAL: Documentation GitHub Workflow**

**MANDATORY for all agents updating documentation:**

#### **Step 1: Update Documentation**
- Make changes to files in `docs/best-practices/` or root documentation
- Update "Last Modified" date to current date
- Save all changes

#### **Step 2: Commit to Current Branch**
```bash
git add docs/ .github/copilot-instructions.md TQFA_DEVELOPMENT_BEST_PRACTICES.md
git commit -m "Update documentation: [brief description of changes]"
git push
```

#### **Step 3: Merge to Main Branch (CRITICAL for GitHub links)**
```bash
# Switch to main branch
git checkout main

# Merge current branch (usually uat) 
git merge uat

# Push to GitHub - makes documentation publicly accessible
git push origin main

# Switch back to working branch
git checkout uat
```

#### **Why This Matters**
- **GitHub Links**: All documentation references point to the `main` branch
- **Cross-Project Access**: Other agents need documentation available on GitHub
- **Permanent Record**: Documentation changes must be in main branch to persist

**🚨 CRITICAL**: Documentation updates are worthless if they're not pushed to the main branch on GitHub!

**Critical**: This documentation represents hard-learned lessons. Keep it current to prevent repeating the same mistakes.

---

## 🚨 **CRITICAL: NO SHORTCUTS FROM DAY ONE**

> **ENGINEERING SHORTCUTS ARE TECHNICAL DEBT WITH COMPOUND INTEREST**

The #1 lesson learned: Taking shortcuts early cost us **days** of debugging time. Every system component must be production-ready from first deployment.

**If you wouldn't trust it with real customer traffic, don't deploy it to UAT.**

---

## 🎯 **Core Principles**

### **1. Production-Ready From Day One**
- All deployments must have health checks and automated rollback
- Never deploy manually-managed infrastructure
- Test containers locally before Azure deployment

### **2. Automation Over Manual Work**  
- Automate version bumping, deployment, and traffic promotion
- Use CI/CD pipelines for all environments
- Scripts must handle error conditions gracefully

### **3. Clear Documentation & Context**
- Document every architectural decision with reasoning
- Preserve complete context for agent handoffs
- Code should be self-documenting with type hints

### **4. Security & Secrets Management**
- Never commit secrets to git
- Use Azure Key Vault for sensitive configuration
- Implement proper authentication from the start

---

## 📚 **Detailed Guides**

### 🚀 **Deployment & Infrastructure** 
- **[Docker Deployment Guide](./docs/best-practices/docker-deployment.md)** - Azure Container Apps, traffic management, health checks
- **[Scripts & Tools](./docs/best-practices/scripts-and-tools.md)** - Production-ready automation scripts
- **[Troubleshooting](./docs/best-practices/troubleshooting.md)** - Common issues and solutions

### 🏗️ **Development**
- **[FastAPI Architecture](./docs/best-practices/fastapi-architecture.md)** - Project structure, API design
- **[Code Standards](./docs/best-practices/code-standards.md)** - Python style, testing, type hints

---

## 🚀 **Quick Start Checklist**

For new projects or team members:

### **Setup (One-time)**
- [ ] Copy `docs/best-practices/` directory to new project
- [ ] Set up Azure Container Apps with health checks
- [ ] Configure Key Vault and managed identity
- [ ] Set up GitHub Actions with automated deployment

### **Every Development Session**
- [ ] Use version bumping: `python bump_version.py`
- [ ] Test locally before deploying: `python run_local.py`
- [ ] Commit with descriptive messages
- [ ] Verify deployment health: `python check_deployment.py`

### **Every Deployment**
- [ ] Health checks pass
- [ ] Traffic automatically promoted to healthy revision
- [ ] Users can access new version
- [ ] Monitor for issues in first 30 minutes

---

## ⚡ **Essential Commands**

### **Development**
```bash
# Version bump and deploy
python bump_version.py
git add . && git commit -m "Version bump to X.Y.Z - [feature]" && git push

# Local development
python run_local.py

# Test container locally  
./test_container_locally.sh
```

### **Deployment Monitoring**
```bash
# Check revision status
az containerapp revision list --name <APP> --resource-group <RG> --output table

# Promote healthy revision (fixes Azure's stupid behavior)
python promote_healthy_revision.py

# Validate deployment
python check_deployment.py

# View logs
az containerapp logs show --name <APP> --resource-group <RG> --tail 50
```

### **Emergency Recovery**
```bash
# Immediate rollback
az containerapp ingress traffic set --name <APP> --resource-group <RG> --revision-weight <GOOD_REVISION>=100

# Check what users see
curl https://<APP_URL>/
```

---

## 🔥 **Critical Deployment Lessons**

### **Azure Container Apps Reality Check**
Azure has **INSANE** default behavior:
- ✅ New containers deploy and become healthy
- ❌ But get **0% traffic by default**
- ❌ Users continue seeing old version until **manual promotion**

**Solution**: Use our `promote_healthy_revision.py` script or single revision mode.

### **Common "Deployment Working But Users Don't See It"**
This is **always** the traffic promotion issue. Check:
```bash
az containerapp revision list --name <APP> --resource-group <RG> --output table
# Look for: Healthy revision with 0% traffic
```

### **Container Startup Failures**
Usually caused by:
- **Settings parsing**: CORS environment variables (see [troubleshooting guide](./docs/best-practices/troubleshooting.md))
- **Missing dependencies**: Check requirements.txt
- **Port binding**: Must bind to `0.0.0.0:8000`

---

## 📊 **Success Metrics**

You know it's working when:
- ✅ Version bumping is automated and consistent
- ✅ Deployments complete without manual intervention  
- ✅ Health checks pass and traffic routes automatically
- ✅ Users immediately see new versions after deployment
- ✅ Rollback works automatically for failed deployments
- ✅ No more "why isn't my change deployed?" confusion

---

## 🎓 **Key Pain Points We Solved**

### **The Deployment Disaster (Days 1-3)**
- **Problem**: Manual deployment, no health checks, no rollback
- **Cost**: 3+ days debugging, zero confidence in deployments
- **Solution**: Automated health validation and traffic promotion

### **The URL Confusion (Day 4)**  
- **Problem**: Testing wrong Azure service URLs (.azurewebsites.net vs .azurecontainerapps.io)
- **Cost**: Hours debugging "failed" deployments that were working
- **Solution**: Clear URL reference guide and validation scripts

### **The Azure Traffic Mystery (Day 5)**
- **Problem**: Healthy deployments getting 0% traffic by default
- **Cost**: Constant confusion about deployment status
- **Solution**: Automated traffic promotion script

---

## 🔮 **For New Projects**

1. **Copy this entire `docs/best-practices/` directory** to your new project
2. **Update agent instructions** to reference the guides
3. **Follow the [Docker Deployment Guide](./docs/best-practices/docker-deployment.md)** for Azure setup
4. **Use the [Scripts & Tools](./docs/best-practices/scripts-and-tools.md)** for automation
5. **Reference [Troubleshooting](./docs/best-practices/troubleshooting.md)** when issues arise

This documentation structure allows you to:
- **Quick reference** for daily work (this document)
- **Detailed guides** for specific problems
- **Copy to new projects** easily
- **Agent-friendly** modular structure

---

*This guide exists because proper engineering practices save exponentially more time than they cost.*

---

## 🚀 **Deployment & Version Management**

### **Mandatory Workflow**
```bash
# 1. Make your changes
# 2. Bump version
python bump_version.py

# 3. Commit with version
git add .
git commit -m "Version bump to X.Y.Z - [description]"

# 4. Push to deploy (triggers version-based container build)
git push

# 5. Verify deployment (should see version match within 5 min)
python check_deployment.py
```

### **Version Numbering Strategy**
- **Patch (X.Y.Z+1)**: Bug fixes, endpoint fixes, minor changes
- **Minor (X.Y+1.0)**: New features, new endpoints, significant changes  
- **Major (X+1.0.0)**: Breaking changes, architecture overhauls

### **Deployment Monitoring**
- Always check deployment status with `check_deployment.py`
- Wait for UAT version to match local version before testing
- Azure Container Apps may take 2-5 minutes to pick up new images

### **🎯 GITHUB CLI FOR DEPLOYMENT DEBUGGING**

**ESSENTIAL SKILL**: Use GitHub CLI (`gh`) for accurate deployment status, not web UI

**Key Commands for Agents**:
```bash
# Check recent workflow status (more reliable than GitHub web UI)
gh run list --branch uat --limit 5

# Get detailed job information
gh run view [RUN_ID]
gh run view --job=[JOB_ID]  # Specific job details

# Get full logs (critical for debugging)
gh run view --log --job=[JOB_ID]

# Monitor deployment in real-time
gh run watch [RUN_ID]
```

**Critical Debugging Pattern**:
1. **Always verify with GitHub CLI first**: Web UI may show ✓ for failed workflows
2. **Check build logs for version extraction**: Look for `VERSION=1.0.X` and `IMAGE_TAG=uat-1.0.X`
3. **Verify container push success**: Look for "Successfully pushed" messages
4. **Check deployment command success**: Look for "Deployed X.Y.Z with revision suffix"

**Why GitHub CLI is Essential**:
- GitHub web UI sometimes shows "completed" for failed workflows
- Only GitHub CLI shows the real command output and error details
- Critical for debugging version extraction and container tagging issues
- Provides immediate access to build logs without navigating web interface

### **🚨 CRITICAL: Container Image Tagging Strategy**

**PROBLEM**: Flaky deployments where GitHub shows "completed" but containers run old versions

**ROOT CAUSE**: Inconsistent container tagging creates caching issues and race conditions
- Git SHA tags (`uat-abc123def`) are unpredictable and hard to debug
- Multiple tags can reference similar code states
- Azure Container Registry may cache layers unexpectedly
- No clear version mapping between code and deployed containers

**SOLUTION**: Version-based container tagging (implemented in workflows)

```yaml
# ✅ FIXED: Version-based tagging in GitHub Actions
VERSION=$(python -c "import sys; sys.path.append('app'); import main; print(main.app.version)")
IMAGE_TAG="uat-$VERSION"  # Results in: uat-1.0.6
REVISION_SUFFIX="v$(echo $VERSION | tr '.' '-')"  # Results in: v1-0-6
```

**Benefits**:
- ✅ **Predictable**: Version 1.0.6 = Container `uat-1.0.6`
- ✅ **Unique**: Every version bump = guaranteed new container
- ✅ **Debuggable**: Clear mapping between code version and deployment
- ✅ **Cache-proof**: Unique tags prevent Azure caching issues
- ✅ **Traceable**: Easy to verify which version is actually running

**Deployment Workflow Impact**:
```bash
# Before (flaky)
Container: uat-a1b2c3d (what version is this?)
Revision: rev-a1b2c3d (meaningless SHA fragment)

# After (reliable)  
Container: uat-1.0.6 (clearly version 1.0.6)
Revision: v1-0-6 (version-based, readable)
```

**Critical Lesson**: When deployments seem "completed" but don't work:
1. Check if container tags match your expected version
2. Verify the GitHub Actions logs show the correct VERSION extraction
3. Confirm Azure Container Apps picked up the new image tag
4. Use `monitor_deployment.py` to watch for version changes in real-time

### **🚨 DEPLOYMENT DEBUGGING: When "Success" Isn't Success**

**CRITICAL PATTERN**: GitHub Actions shows ✓ but endpoint shows old version

**Step-by-Step Debugging Protocol**:

```bash
# 1. Verify GitHub Actions actually succeeded
gh run list --branch uat --limit 3
gh run view [RUN_ID]  # Look for ✓ on ALL jobs

# 2. Check if new revision exists but is unhealthy
az containerapp revision list --name tqfaapi-uat --resource-group tqfa-uat-rg --output table

# 3. If revision shows "Unhealthy", check container logs
az containerapp logs show --name tqfaapi-uat --resource-group tqfa-uat-rg --revision [REVISION-NAME] --tail 50

# 4. Force traffic to new revision (for immediate testing)
az containerapp revision set-mode --name tqfaapi-uat --resource-group tqfa-uat-rg --mode single
```

**Common "Silent Failure" Patterns**:
- ✅ **Container builds successfully** BUT ❌ **Import errors at runtime**
- ✅ **Container pushes to registry** BUT ❌ **Health checks fail**  
- ✅ **Azure deployment completes** BUT ❌ **Traffic stays on old revision**
- ✅ **GitHub shows all green** BUT ❌ **Container crashes immediately**

**Real Example from This Project**:
```bash
# GitHub Actions: ✓ SUCCESS (all steps completed)
# UAT Endpoint: version 1.0.1 (old version, should be 1.0.8)
# Real Issue: ModuleNotFoundError: No module named 'app.main_streamlined'
# Root Cause: Dockerfile CMD still referenced old file after rename
```

**Key Lesson**: **"Deployment Success" ≠ "Application Success"**
- GitHub Actions can succeed while the application fails to start
- Always verify the endpoint actually responds with expected version
- Container startup failures are often silent in Azure Container Apps
- Use container logs to debug "healthy build, unhealthy runtime" scenarios

### **🔧 DOCKERFILE CONSISTENCY CHECKS**

**CRITICAL**: When renaming entry point files, update ALL references:

```dockerfile
# ❌ BAD: Dockerfile references old file
CMD ["gunicorn", "app.main_streamlined:app", ...]

# ✅ GOOD: Updated after file rename  
CMD ["gunicorn", "app.main:app", ...]
```

**Mandatory Checklist After File Renames**:
- [ ] `Dockerfile` CMD entry point
- [ ] `docker-compose.yml` commands
- [ ] Test files import statements  
- [ ] Documentation references
- [ ] VS Code launch configurations

### **🔑 CRITICAL: Azure Container Apps + Key Vault Configuration**

**THE MOST IMPORTANT DISCOVERY**: User-assigned managed identities require `AZURE_CLIENT_ID`

**Problem**: Container Apps with user-assigned managed identities fail to access Key Vault with error:
```
ManagedIdentityCredential: App Service managed identity configuration not found in environment
DefaultAzureCredential: No credential available
```

**Root Cause**: `DefaultAzureCredential` doesn't know WHICH managed identity to use in Container Apps

**Solution**: Set the `AZURE_CLIENT_ID` environment variable:
```bash
# Get the client ID from your user-assigned managed identity
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "identity.userAssignedIdentities"

# Add it to the container app environment
az containerapp update --name tqfaapi-uat --resource-group tqfa-uat-rg --set-env-vars AZURE_CLIENT_ID=5a419532-06ba-438c-bbe2-37a08e8989e0
```

**Complete Container Apps + Key Vault Setup Checklist**:
1. ✅ **Create user-assigned managed identity**
2. ✅ **Assign identity to Container App**
3. ✅ **Grant "Key Vault Secrets User" role to identity**
4. ✅ **Verify Key Vault secrets exist and are accessible**
5. ✅ **Create referenced Azure Blob Storage containers**
6. 🚨 **SET AZURE_CLIENT_ID ENVIRONMENT VARIABLE** ← THIS IS CRITICAL!

**Debugging Commands**:
```bash
# Check if managed identity is assigned
az containerapp show --name [APP] --resource-group [RG] --query "identity"

# Check if identity has Key Vault access
az role assignment list --assignee [PRINCIPAL-ID] --scope "/subscriptions/[SUB]/resourceGroups/[RG]/providers/Microsoft.KeyVault/vaults/[KV-NAME]"

# Check if secrets exist in Key Vault
az keyvault secret list --vault-name [KV-NAME] --query "[].name" --output table

# Check if storage containers exist
az storage container list --connection-string "[CONNECTION-STRING]" --query "[].name" --output table

# Most important: Check if AZURE_CLIENT_ID is set
az containerapp show --name [APP] --resource-group [RG] --query "properties.template.containers[0].env[?name=='AZURE_CLIENT_ID']"
```

**Why This Matters**:
- **Without AZURE_CLIENT_ID**: Container starts successfully but ALL Key Vault access fails at runtime
- **Symptoms**: 500 errors on endpoints that use Azure services, "Secret not available" errors in logs
- **Time Cost**: This single missing environment variable cost us **3+ days of debugging**
- **Deployment Confusion**: Container appears healthy but authentication system completely broken

**Critical Lesson**: Container Apps managed identity requires explicit client ID specification - this is NOT documented clearly in Azure Container Apps documentation.

---

## 🏗️ **Architecture & Code Organization**

### **File Naming Conventions**
- **Avoid confusing names**: No `main_streamlined.py` or `enhanced_main.py`
- **Use standard patterns**: `main.py`, `routes.py`, `models.py`
- **Clean up legacy files**: Remove obsolete files to prevent confusion

### **Endpoint Strategy**
- **Multiple auth methods**: In-memory (testing), file-based (dev), environment (prod)
- **Graceful fallbacks**: Try multiple storage methods in validation
- **Maintain compatibility**: Keep existing endpoint contracts while improving internals

### **Error Handling Patterns**
```python
# ✅ Good: Specific error handling
try:
    # Try primary method
    result = primary_auth_method()
except SpecificError:
    # Fall back to secondary method
    result = fallback_auth_method()
except Exception as e:
    # Log and re-raise as HTTP exception
    logger.error(f"Auth failed: {e}")
    raise HTTPException(status_code=500, detail="Authentication error")

# ❌ Bad: Generic exception handling that hides issues
try:
    complex_operation()
except:
    pass  # This hides real problems
```

---

## 🛡️ **Security Best Practices**

### **Authentication Architecture**
- **Salted hashing**: Each user gets unique salt (`salt_{username}_{method}`)
- **Constant-time comparison**: Use `hmac.compare_digest()` to prevent timing attacks
- **Multiple storage options**: Environment variables (prod), file-based (dev), in-memory (test)

### **Password Management**
```python
# ✅ Secure password handling
def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    expected_hash = hash_password(password, salt)
    return hmac.compare_digest(expected_hash, stored_hash)
```

### **Environment Variable Strategy**
```bash
# Production users stored as JSON in environment
TQFA_USERS='{"admin":{"password_hash":"...","salt":"...","user_id":"admin"}}'
```

---

## 📋 **Agent Handoff & Context Management**

### **Critical Files for Context**
1. **`docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md`** - How to maintain docs
2. **`docs/ARCHITECTURAL_DECISIONS.md`** - Why we made specific choices
3. **`.github/copilot-instructions.md`** - Instructions for new agents
4. **`AGENT_HANDOFF_STATUS.md`** - Current work status
5. **`AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md`** - Infrastructure details

### **Handoff Checklist**
- [ ] Update version number and deploy status
- [ ] Document any unfinished work in AGENT_HANDOFF_STATUS.md
- [ ] Note any architectural decisions made
- [ ] Update user credentials if changed
- [ ] Test all modified endpoints
- [ ] Verify deployment status

### **Context Preservation Techniques**
- **Conversation Summaries**: Use the template in `docs/CONVERSATION_SUMMARY_TEMPLATE.md`
- **Decision Documentation**: Record WHY decisions were made, not just WHAT was done
- **Status Files**: Maintain current status in dedicated markdown files
- **Code Comments**: Explain complex business logic inline

---

## 🧠 **AI Agent Collaboration Insights**

### **Multi-Agent Development Patterns**
- **Context Handoffs**: Each agent must understand previous decisions
- **Documentation First**: Write decisions down before making changes
- **Version Tracking**: Critical for multi-agent environments where confusion is common
- **Incremental Progress**: Small, testable changes work better than large rewrites

### **Agent Communication Protocol**
1. **Read existing context**: Check AGENT_HANDOFF_STATUS.md first
2. **Update status**: Document current work and blockers
3. **Preserve decisions**: Record WHY choices were made
4. **Test thoroughly**: Verify changes work before handoff
5. **Document handoff**: Clear status for next agent

### **Common Agent Pitfalls**
- **Context loss**: Forgetting critical infrastructure details
- **Repeated mistakes**: Not learning from previous agent failures  
- **Complex solutions**: Overengineering when simple approaches work
- **Version confusion**: Not tracking what's deployed vs what's in code
- **Documentation drift**: Making changes without updating docs

---

## 🔧 **Development Workflow**

### **Local Development Setup**
```bash
# 1. Environment setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Start development server
python main.py

# 3. Test endpoints
python test_local.py
```

### **Testing Strategy**
- **Multiple test scripts**: `test_local.py`, `test_simple.py`, `complete_user_demo.py`
- **Layered testing**: Unit tests, integration tests, deployment verification
- **Endpoint verification**: Always test both success and failure cases
- **Integration tests**: Test the full user flow, not just individual functions

### **Testing Scripts Hierarchy**
```
test_local.py              # Basic local development testing
test_simple.py             # Simple API health checks  
test_cleaned_validate.py   # Authentication endpoint testing
complete_user_demo.py      # Full user management flow testing
check_deployment.py        # Deployment status verification
endpoint_usage_guide.py    # Generate documentation and examples
```

### **Testing Best Practices**
- **Test at multiple levels**: Local → UAT → Production
- **Verify version alignment**: Always check local vs deployed versions
- **Test authentication flows**: Success, failure, and edge cases
- **Use proper HTTP methods**: Follow REST conventions
- **Handle encoding properly**: Always use UTF-8 for file operations

### **Debugging Techniques**
1. **Check version alignment**: Local vs deployed version
2. **Verify user storage**: Check `users.json` or environment variables
3. **Test authentication**: Use multiple methods (file, env, hardcoded)
4. **Monitor logs**: Check container logs in Azure for deployment issues

---

## ☁️ **Azure Infrastructure**

### **Critical UAT Environment Details** 
- **Resource Group**: `tqfa-uat-rg` (eastus2) ⚠️ Different from dev/prod naming!
- **Key Vault**: `kv-tqfa-uat` ⚠️ Not following standard pattern!  
- **Container App**: Uses managed identity for Key Vault access
- **Deployment**: Triggered by git push, uses unique image tags

### **Infrastructure Anomaly Explanation**
**WHY UAT uses different naming:**
- Historical consolidation to fix cross-resource-group access issues
- UAT was moved to dedicated resource group for isolation  
- Key Vault naming had to change to avoid conflicts
- **NEVER** treat this as "minor naming differences" - it's critical for deployments

### **Standard vs Anomaly Patterns**
```
STANDARD (Dev/Prod):
- Resource Group: rg-tqa-{env}  
- Key Vault: kv-tqa-{env}
- Standard managed identity permissions

UAT ANOMALY:
- Resource Group: tqfa-uat-rg
- Key Vault: kv-tqfa-uat  
- Special RBAC role assignments required
```

### **Common Pitfalls**
- **Resource naming**: UAT uses non-standard naming (historical reasons)
- **Key Vault permissions**: Managed identity must have proper RBAC roles
- **Container updates**: Same image tags aren't detected, use unique tags
- **Cross-region issues**: Keep resources in same region/resource group

### **Deployment Pipeline**
- **Trigger**: Git push to `uat` branch
- **Process**: Builds unique image tag with git SHA
- **Updates**: Container app with new revision
- **Verification**: Check root endpoint for version number

---

## 📊 **User Management**

### **Three-Tier User System**
1. **In-Memory** (`/simple/`): Quick testing, lost on restart
2. **File-Based** (`/file/`): Persistent in `users.json`, good for development
3. **Environment** (`/env/`): Production-ready, stored in environment variables

### **User Creation Methods**
```bash
# API-based (in-memory)
curl -X POST "localhost:8000/api/v1/simple/create-user?username=user&password=pass"

# File-based (persistent)
curl -X POST "localhost:8000/api/v1/file/create-user?username=user&password=pass"

# Production (environment variable)
python create_production_users.py
```

### **User Validation Endpoint**
```bash
# The main validation endpoint (fixed)
curl -X POST '/api/v1/users/validate' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "username", "password": "password"}'

# Expected response
{
  "user_id": "username",
  "success": true,
  "message": "Authentication successful for username (file-based)"
}
```

---

## 🚨 **Common Issues & Solutions**

### **500 Internal Server Error on /users/validate**
- **Cause**: Complex blob storage system failures
- **Solution**: Replaced with simple multi-tier authentication
- **Prevention**: Favor simple, testable authentication methods

### **Deployment Not Updating** 
- **Cause**: Flaky container tagging (git SHA) causing caching issues and race conditions
- **Solution**: Use version-based image tags (`uat-1.0.6`) and version-based revision suffixes (`v1-0-6`)
- **Prevention**: Always bump version before pushing + use predictable container naming
- **Verification**: Check that deployed version matches local version with `python check_deployment.py`

### **Unicode Encoding Errors**
- **Cause**: Windows CP1252 encoding vs UTF-8 files
- **Solution**: Always specify `encoding='utf-8'` in file operations
- **Prevention**: Use UTF-8 consistently in all file operations

### **Agent Context Loss**
- **Cause**: Complex projects lose important details in handoffs  
- **Solution**: Maintain persistent documentation and status files
- **Prevention**: Document decisions in files, not just conversations

### **Key Vault Access Failures**
- **Cause**: Managed identity lacking proper RBAC permissions
- **Solution**: Ensure container app identity has Key Vault access
- **Prevention**: Check permissions after any infrastructure changes

---

## 📚 **Essential Scripts & Tools**

### **Version Management**
- `bump_version.py` - Increment version before pushing
- `check_deployment.py` - Verify deployment status

### **User Management**  
- `create_production_users.py` - Interactive user creation for production
- `user_management_demo.py` - Demonstrate all authentication methods
- `create_david.py` - Example user creation script

### **Testing & Validation**
- `test_local.py` - Test local development server
- `simple_test.py` - Basic API health checks
- `test_cleaned_validate.py` - Test authentication endpoints

### **Development Utilities**
- `endpoint_usage_guide.py` - Generate usage documentation
- `show_security.py` - Display security implementation details

---

## ❌ **What NOT To Do** (Painful Lessons)

### **Architecture Anti-Patterns**
- **Don't**: Build complex encryption systems without understanding the full stack
- **Don't**: Use blob storage for simple user authentication
- **Don't**: Create multiple similar files (main.py, main_streamlined.py, main_simple.py)
- **Don't**: Assume complex is better - simple solutions often work better

### **Deployment Anti-Patterns** 
- **Don't**: Push code without bumping version numbers
- **Don't**: Use the same Docker image tag repeatedly
- **Don't**: Assume deployments are instant - they take 2-5 minutes
- **Don't**: Test on old versions and expect new features to work

### **Agent Collaboration Anti-Patterns**
- **Don't**: Start work without reading handoff documentation
- **Don't**: Summarize infrastructure anomalies as "minor differences"
- **Don't**: Make changes without documenting WHY
- **Don't**: Handoff unfinished work without status documentation

### **Security Anti-Patterns**
- **Don't**: Store passwords in plain text anywhere
- **Don't**: Use generic exception handling that hides auth failures
- **Don't**: Ignore timing attack vulnerabilities in auth comparison
- **Don't**: Create public endpoints for user creation without admin validation

### **Development Anti-Patterns**
- **Don't**: Mix file encodings (always use UTF-8)
- **Don't**: Create endpoints without testing both success AND failure cases
- **Don't**: Copy/paste authentication code without understanding it
- **Don't**: Remove legacy code without understanding what depends on it

---

## 🎓 **Key Lessons Learned**

### **Architecture Evolution**
1. **Started**: Complex blob storage with encryption layers
2. **Problem**: "Incorrect padding" errors, 500 failures
3. **Solution**: Simple file-based and environment storage
4. **Result**: Same security level, much better reliability

### **Deployment Tracking**
1. **Problem**: Couldn't tell which version was deployed
2. **Solution**: Mandatory version bumps with unique tags
3. **Result**: Clear deployment status and rollback capability

### **Context Preservation**
1. **Problem**: Agent handoffs lost critical infrastructure context
2. **Solution**: Persistent documentation and handoff protocols  
3. **Result**: Smoother transitions and fewer repeated mistakes

### **Development Efficiency**
1. **Problem**: Complex file naming confused developers
2. **Solution**: Clean, standard naming conventions
3. **Result**: Faster onboarding and fewer mistakes

---

## 🔮 **Future Considerations**

### **Scalability Improvements**
- Consider PostgreSQL for user storage at scale
- Implement proper JWT tokens for stateless auth
- Add rate limiting and abuse prevention

### **Security Enhancements**
- Add password complexity requirements
- Implement account lockout after failed attempts  
- Consider 2FA for admin users

### **Operational Improvements**
- Add comprehensive logging and metrics
- Implement health check endpoints
- Create automated deployment rollback

### **Development Experience**
- Add pre-commit hooks for version bumping
- Create development environment automation
- Implement automated testing in CI/CD

---

## 📞 **Getting Help**

### **When Things Go Wrong**
1. **Check deployment status**: `python check_deployment.py`
2. **Verify local setup**: `python test_local.py`
3. **Review recent changes**: Check git log and version numbers
4. **Consult documentation**: Especially the architectural decisions
5. **Test authentication**: Use the user management demo scripts

### **Key Documentation Files**
- `docs/ARCHITECTURAL_DECISIONS.md` - Design rationale
- `docs/QUICK_REFERENCE.md` - Common operations
- `AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md` - Infrastructure details
- `.github/copilot-instructions.md` - Agent instructions

---

*Last Updated: September 26, 2025*  
*Project: TQFA API v1.0.4+*  
*Authors: Development team via AI agent collaboration*

---

**Remember: Simplicity, Version Control, and Context Preservation are the three pillars of maintainable development on this project.**