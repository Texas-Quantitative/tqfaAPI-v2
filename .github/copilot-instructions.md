<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FastAPI Project - Copilot Instructions

## Project Overview
This is a FastAPI Python web API project with a modular structure. The project follows modern Python development practices with type hints, Pydantic models, and clean architecture.

## 🚨 CRITICAL: NO SHORTCUTS FROM DAY ONE
**MANDATORY ENGINEERING STANDARDS - NO EXCEPTIONS**

**The Deployment Disaster Lesson**: Taking shortcuts early ("just get it working") cost us DAYS of debugging deployment failures. Engineering shortcuts are technical debt with compound interest.

**Production-Ready From Day One Rule**: If you wouldn't trust it with real customer traffic, don't deploy it to UAT. Every system component must be production-ready from first deployment.

## 📚 **REFERENCE: Modular Best Practices Documentation**

This project uses modular documentation for easy reference and reuse:

**🔗 GitHub Repository**: `https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices`

**Primary Reference**: `TQFA_DEVELOPMENT_BEST_PRACTICES.md` - Essential principles and quick reference

**🎯 CRITICAL: TQFA V2 Implementation Strategy**
- **[TQFA_V2_ITERATIVE_IMPLEMENTATION_STRATEGY.md](./TQFA_V2_ITERATIVE_IMPLEMENTATION_STRATEGY.md)** - **DEFINITIVE implementation guide for TQFA V2 development**
  - Modular unified architecture with iterative phases
  - Enhanced Azure AI Agent foundation (abandoned parallel FastAPI)
  - GNN framework for quantitative analysis (relationship modeling, risk analysis, portfolio optimization)  
  - Multi-format document processing with OCR capabilities
  - Azure OpenAI routing with manual model selection
  - Comprehensive testing strategy for rapid iteration

**Detailed Guides** in `docs/best-practices/`:
- **[docker-deployment.md](./docs/best-practices/docker-deployment.md)** - Azure Container Apps, traffic management, health checks, container issues
- **[scripts-and-tools.md](./docs/best-practices/scripts-and-tools.md)** - Production-ready automation scripts with code examples
- **[troubleshooting.md](./docs/best-practices/troubleshooting.md)** - Common issues and detailed solutions

**When to Reference Each Guide**:
- **Deployment issues** → Check docker-deployment.md and troubleshooting.md
- **Automation needs** → Use scripts-and-tools.md for ready-to-use code
- **New projects** → Copy entire docs/best-practices/ directory or reference GitHub links above

### **🚨 CRITICAL: Documentation Update Protocol**

**If you update ANY documentation files, you MUST push changes to GitHub:**

```bash
# 1. Commit changes to current branch
git add docs/ .github/copilot-instructions.md TQFA_DEVELOPMENT_BEST_PRACTICES.md
git commit -m "Update documentation: [brief description]"
git push

# 2. Merge to main branch (CRITICAL - makes documentation publicly accessible)
git checkout main
git merge [current-branch]  # usually 'uat'
git push origin main
git checkout [current-branch]
```

**Why This Matters**: All GitHub documentation links point to the main branch. Documentation updates are useless if they're not accessible via the GitHub URLs referenced throughout the system.

## Code Standards & Practices

### Python Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Use descriptive variable and function names
- Add docstrings to all functions, classes, and modules
- Prefer f-strings for string formatting

### FastAPI Specific
- Use Pydantic models for request/response validation
- Always include proper HTTP status codes in responses
- Use dependency injection for shared logic
- Group related endpoints with APIRouter
- Include proper tags for API documentation
- Use async/await for all route handlers

### Project Structure Guidelines
- Keep route handlers in `app/api/routes.py`
- Define Pydantic schemas in `app/schemas/`
- Database models (future) go in `app/models/`
- Shared utilities in separate modules
- Configuration should be environment-based

### Error Handling
- Use HTTPException for API errors
- Include meaningful error messages
- Provide proper status codes (400, 401, 403, 404, 422, 500)
- Log errors appropriately

### Documentation
- Update README.md when adding new features
- Include API endpoint documentation
- Add inline comments for complex business logic
- Keep docstrings up to date

## Dependencies
- FastAPI with standard extras
- Uvicorn for ASGI server
- Pydantic for data validation
- python-multipart for form data
- email-validator for email validation

## Development Workflow
- Use virtual environment (.venv)
- Run with hot reload during development
- Test endpoints using the interactive docs at /docs
- Follow RESTful API conventions

## � CRITICAL: NO SHORTCUTS FROM DAY ONE
**MANDATORY ENGINEERING STANDARDS - NO EXCEPTIONS**

**The Deployment Disaster Lesson**: Taking shortcuts early ("just get it working") cost us DAYS of debugging deployment failures. Engineering shortcuts are technical debt with compound interest.

**NEVER deploy or implement without:**
1. **Health Check Validation**: All deployments must pass comprehensive health checks
2. **Automated Rollback**: Failed deployments must automatically rollback  
3. **Container Testing**: Test locally before pushing to Azure
4. **Blue-Green Deployment**: Never switch traffic without validation
5. **Monitoring & Alerts**: Know immediately when things fail

**The "Just Get It Working" Trap - AVOID:**
- ❌ "We'll fix deployment later" → Later never comes, debt compounds
- ❌ "Manual processes are fine for now" → Manual doesn't scale, fails at worst times
- ❌ "It works locally, Azure will be fine" → Different environments, assumptions kill deployments
- ❌ "Moving fast, no time for proper testing" → Moving fast = doing it right the first time

**Production-Ready From Day One Rule**: If you wouldn't trust it with real customer traffic, don't deploy it to UAT. Every system component must be production-ready from first deployment.

## �🚀 DEPLOYMENT & VERSION MANAGEMENT
**MANDATORY: Version Bump Before Every Push**

**ALWAYS bump version before pushing to track deployments:**

1. **Run Version Bump Script**: Execute `python bump_version.py` to increment patch version
2. **Verify Version Updated**: Check that version appears in app/main.py, pyproject.toml, setup.py
3. **Commit with Version**: `git add . && git commit -m "Version bump to X.Y.Z - [description]"`
4. **Push to Deploy**: `git push` triggers automatic deployment
5. **Verify Deployment**: Check UAT root endpoint shows new version number

**Why This Matters:**
- **Track Deployments**: Easily see which version is deployed vs which is in code
- **Debug Issues**: Know exactly which code is running in each environment  
- **Avoid Confusion**: Prevent "why isn't my change deployed?" situations
- **Pipeline Reliability**: Unique versions ensure container updates are detected

**Version Numbering:**
- **Patch bumps** (X.Y.Z+1): Bug fixes, endpoint fixes, minor changes
- **Minor bumps** (X.Y+1.0): New features, new endpoints, significant changes
- **Major bumps** (X+1.0.0): Breaking changes, architecture overhauls

**Current System:**
- Version tracked in multiple files automatically
- Deployment pipeline uses unique tags based on version number (uat-1.0.7)
- Each push creates new container revision
- Root endpoint (`/`) shows current deployed version

## 📊 DEPLOYMENT MONITORING: GitHub CLI Commands
**ALWAYS use GitHub CLI to check REAL deployment status when GitHub shows "completed" but endpoints show old versions:**

```bash
# Check recent workflow runs for current branch
gh run list --branch uat --limit 5

# Watch a specific deployment in real-time  
gh run watch [RUN_ID]

# Get detailed view of a specific run
gh run view [RUN_ID]

# Get detailed logs from specific job (build-and-deploy)
gh run view --job=[JOB_ID]

# Check if workflows are failing
gh run list --status failure --limit 3
```

**Critical Deployment Debugging Workflow:**
1. **Check GitHub Actions status**: `gh run list --branch uat --limit 3`
2. **Verify latest run succeeded**: Look for ✓ not X in status  
3. **Check build logs**: `gh run view [RUN_ID]` to see version extraction
4. **Verify container tag**: Logs should show `uat-1.0.X` tag being built
5. **Check endpoint version**: `python check_deployment.py` for actual deployed version
6. **Wait for Azure Container Apps**: Can take 5+ minutes to pick up new images

**Why GitHub CLI is Essential:**
- GitHub web UI may show "completed" for failed workflows
- GitHub CLI shows REAL workflow status (✓ vs X)  
- Provides access to detailed logs showing version extraction
- Can monitor deployments in real-time with `gh run watch`
- Critical for debugging version-based container tagging issues

## ⚠️ CRITICAL: Azure Infrastructure Documentation
**BEFORE making any Azure deployment changes, ALWAYS:**

1. **Read the Documentation Maintenance Protocol**: Check `docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md` - PREVENTS RESOURCE CONFUSION
2. **Read the Azure Resources Guide**: Check `docs/AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md` for current infrastructure state
3. **Review Architectural Decisions**: Check `docs/ARCHITECTURAL_DECISIONS.md` for design patterns and principles
4. **Use Quick Reference**: See `docs/QUICK_REFERENCE.md` for common tasks and troubleshooting
5. **Update Documentation**: If you make Azure resource changes, update the guide using the instructions at the top of that file
6. **Cross-Reference Resources**: Verify that Key Vaults, resource groups, and container apps are in the same region/RG
7. **Test Deployments**: After infrastructure changes, always test UAT deployment with admin endpoints

**🔥 CRITICAL CONTEXT - UAT Environment Anomaly:**
- UAT uses `tqfa-uat-rg` (eastus2) with `kv-tqfa-uat` - DIFFERENT from dev/prod naming!
- This was done to fix cross-resource-group access issues
- DEV/PROD use standard `rg-tqa-{env}` with `kv-tqa-{env}` naming
- **NEVER** summarize this as "minor naming differences" - it's critical infrastructure context!

**Common Issues to Avoid:**
- Mismatched resource groups causing Key Vault access failures
- Cross-region resource access problems
- Forgetting to grant managed identity permissions to new Key Vaults
- Using cached container images during deployment
- Violating established architectural patterns (see ARCHITECTURAL_DECISIONS.md)
- Losing critical context in conversation summaries (see DOCUMENTATION_MAINTENANCE_PROTOCOL.md)

The documentation contains step-by-step troubleshooting for deployment failures and admin endpoint issues.

## 🚨 CRITICAL: Azure Service URL Reference
**ALWAYS VERIFY URLS FROM OFFICIAL SOURCES - NEVER GUESS OR ASSUME**

**URL Confusion Prevention Protocol:**
1. **BEFORE testing any endpoint**: Verify the actual URL using Azure CLI
2. **NEVER mix Azure service types**: Different services = different URL patterns
3. **ALWAYS reference CRITICAL_URLS_REFERENCE.md** before testing

### Azure Service URL Patterns
- **Azure Container Apps** (API Backend): `.azurecontainerapps.io`
  - Example: `tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io`
  - Get URL: `az containerapp show --name [APP_NAME] --resource-group [RG] --query "properties.configuration.ingress.fqdn"`

- **Azure App Service** (Frontend): `.azurewebsites.net`  
  - Example: `tqfa-frontend-uat.azurewebsites.net`
  - Get URL: `az webapp show --name [APP_NAME] --resource-group [RG] --query "defaultHostName"`

### UAT Environment - Definitive URLs
**API (Container Apps)**: `https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io`
**Frontend (App Service)**: `https://tqfa-frontend-uat.azurewebsites.net`

### 🔥 DANGEROUS URL PATTERNS TO AVOID
❌ **NEVER USE**: `tqfa-api-uat.azurewebsites.net` - DOESN'T EXIST
❌ **NEVER USE**: `tqfaapi-uat.azurewebsites.net` - WRONG SERVICE TYPE
❌ **NEVER MIX**: App Service naming with Container Apps services

### Verification Commands
```bash
# Get Container App URL (API)
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "properties.configuration.ingress.fqdn" --output tsv

# List all Container Apps in resource group  
az containerapp list --resource-group tqfa-uat-rg --query "[].name" --output table

# Get App Service URL (Frontend)
az webapp show --name tqfa-frontend-uat --resource-group [RG] --query "defaultHostName" --output tsv
```

**Root Cause Analysis of URL Confusion:**
1. **Azure uses different services**: Container Apps vs App Service
2. **Each service has different URL patterns**: `.azurecontainerapps.io` vs `.azurewebsites.net`  
3. **Naming conventions differ**: `tqfaapi-uat` (Container Apps) vs `tqfa-frontend-uat` (App Service)
4. **Mental extrapolation error**: Seeing frontend pattern and incorrectly assuming API pattern

**Cost of URL Confusion:**
- Days of debugging "failed" deployments that were actually successful
- Testing wrong endpoints while real deployments worked correctly
- Version tracking confusion when checking non-existent URLs
- Time wasted on "fixing" infrastructure that wasn't broken
