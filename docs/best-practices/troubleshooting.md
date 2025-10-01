# Troubleshooting Guide

*Solutions to common deployment and development issues*

**Last Modified**: September 27, 2025  
**Version**: 1.0

---

## 🚨 **Critical Azure Container Apps Issues**

### **Issue: Deployment "Succeeds" But Users See Old Version**

**Symptoms:**
- GitHub Actions shows ✅ successful deployment
- Health checks pass
- Users still see previous version
- `curl <APP_URL>` returns old version number

**Root Cause:**
Azure Container Apps' insane default behavior - healthy revisions get 0% traffic until manually promoted.

**Solution:**
```bash
# Check revision status
az containerapp revision list --name tqfaapi-uat --resource-group tqfa-uat-rg --output table

# Look for healthy revision with 0% traffic:
# tqfaapi-uat--v1-0-15  Healthy  0%    <- This is your problem!

# Promote to 100% traffic
az containerapp ingress traffic set --name tqfaapi-uat --resource-group tqfa-uat-rg --revision-weight tqfaapi-uat--v1-0-15=100

# Or use our automation script
python promote_healthy_revision.py
```

**Prevention:**
- Use single revision mode: `az containerapp revision set-mode --mode single`
- Add traffic promotion to CI/CD pipeline
- Always test user experience after deployment

---

## 🐳 **Container Startup Failures**

### **Issue: Container Won't Start - Pydantic Settings Error**

**Symptoms:**
```
pydantic_settings.sources.SettingsError: error parsing value for field "ALLOWED_ORIGINS" from source "EnvSettingsSource"
```

**Root Cause:**
Azure sets `ALLOWED_ORIGINS="[*]"` as string, but Pydantic expects `List[str]`.

**Solution:**
Add field validator to handle string formats:

```python
from pydantic import field_validator
from typing import Union, List
import json

class Settings(BaseSettings):
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:3000"]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from various formats."""
        if isinstance(v, str):
            if v.strip() in ["[*]", "*"]:
                return ["*"]
            if "," in v:
                return [origin.strip() for origin in v.split(",")]
            return [v]
        return v if isinstance(v, list) else ["*"]
```

### **Issue: Container Starts But Health Checks Fail**

**Symptoms:**
- Container revision shows "Unhealthy"
- Health endpoint returns errors or doesn't respond

**Debug Steps:**
```bash
# Get container logs
az containerapp logs show --name tqfaapi-uat --resource-group tqfa-uat-rg --revision <REVISION> --tail 50

# Test health endpoint directly
curl https://<APP_URL>/health/

# Check revision details
az containerapp revision show --name tqfaapi-uat --resource-group tqfa-uat-rg --revision <REVISION>
```

**Common Fixes:**
1. **Missing health endpoint**: Ensure `/health/` route exists and returns 200
2. **Database connection errors**: Check Azure SQL/storage connectivity
3. **Port binding issues**: Container must bind to `0.0.0.0:8000`, not `127.0.0.1`
4. **Dependency failures**: Verify all required services are available

---

## 🔧 **Development Issues**

### **Issue: Local Development Server Won't Start**

**Symptoms:**
- Import errors when running `python main.py`
- Module not found errors
- Application won't bind to port

**Solutions:**
```bash
# 1. Activate virtual environment
./.venv/Scripts/Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set Python path
$env:PYTHONPATH = "."  # Windows
export PYTHONPATH="."  # Linux/Mac

# 4. Check port availability
netstat -an | findstr :8000  # Windows
lsof -i :8000                # Mac/Linux

# 5. Use our development script
python run_local.py
```

### **Issue: Import Errors in FastAPI Application**

**Symptoms:**
```python
ImportError: No module named 'app.core.settings'
ModuleNotFoundError: No module named 'app'
```

**Solutions:**
1. **Check project structure**: Ensure `app/` directory has `__init__.py`
2. **Set PYTHONPATH**: Add project root to Python path
3. **Use absolute imports**: `from app.core.settings import get_settings`
4. **Check virtual environment**: Verify correct environment is activated

**Correct Project Structure:**
```
project_root/
├── app/
│   ├── __init__.py          # Required!
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py      # Required!
│   │   └── settings.py
│   └── api/
│       ├── __init__.py      # Required!
│       └── routes.py
├── main.py                  # Entry point
└── requirements.txt
```

---

## ☁️ **Azure Infrastructure Issues**

### **Issue: Key Vault Access Denied**

**Symptoms:**
- `DefaultAzureCredential` authentication failures
- Key Vault secrets not loading
- 403 Forbidden errors

**Solutions:**
```bash
# 1. Check managed identity permissions
az keyvault show --name <KEY_VAULT_NAME> --query "properties.accessPolicies"

# 2. Grant Container App managed identity access
az keyvault set-policy --name <KEY_VAULT_NAME> --object-id <MANAGED_IDENTITY_ID> --secret-permissions get list

# 3. Verify managed identity is enabled on Container App
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "identity"

# 4. Check environment variables
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "properties.template.containers[0].env"
```

### **Issue: Container Registry Authentication**

**Symptoms:**
- Docker image pull failures
- 401 Unauthorized when pulling images
- Deployment fails at image retrieval

**Solutions:**
```bash
# 1. Login to Azure Container Registry
az acr login --name <REGISTRY_NAME>

# 2. Check Container App registry configuration
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "properties.configuration.registries"

# 3. Verify managed identity has ACR pull permissions
az role assignment list --assignee <MANAGED_IDENTITY_ID> --scope /subscriptions/<SUBSCRIPTION>/resourceGroups/<RG>/providers/Microsoft.ContainerRegistry/registries/<REGISTRY>
```

---

## 🔄 **Version Management Issues**

### **Issue: Version Bump Script Fails**

**Symptoms:**
- `bump_version.py` reports no changes made
- Version numbers don't update in files
- Regex patterns not matching

**Debug:**
```python
# Check current version extraction
python -c "
from pathlib import Path
import re
content = Path('app/main.py').read_text()
match = re.search(r'version\s*=\s*[\"\\']([0-9]+\\.[0-9]+\\.[0-9]+)[\"\\']', content)
print('Found version:', match.group(1) if match else 'Not found')
"
```

**Fixes:**
1. **Check file paths**: Ensure `app/main.py` exists
2. **Verify version format**: Must be `version="X.Y.Z"` format
3. **Check regex patterns**: Update patterns if version string format changed
4. **File encoding issues**: Ensure UTF-8 encoding

### **Issue: Deployment Shows Wrong Version**

**Symptoms:**
- Deployed app shows old version number
- GitHub Actions extracts wrong version
- Version mismatch between files

**Solutions:**
```bash
# 1. Verify version in main.py
grep -n "version.*=" app/main.py

# 2. Check version extraction script
python extract_version.py

# 3. Manually update version if needed
# Edit app/main.py, pyproject.toml, setup.py

# 4. Verify Docker build uses correct file
docker build -t test . && docker run --rm test python -c "from app.main import app; print(app.version)"
```

---

## 🌐 **Network & Connectivity Issues**

### **Issue: CORS Errors in Frontend**

**Symptoms:**
- Browser console shows CORS errors
- Frontend can't access API endpoints
- OPTIONS requests failing

**Solutions:**
```python
# 1. Check ALLOWED_ORIGINS in settings
from app.core.settings import get_settings
settings = get_settings()
print("ALLOWED_ORIGINS:", settings.ALLOWED_ORIGINS)

# 2. Update CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.azurewebsites.net", "*"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 3. Set environment variable in Azure
az containerapp update --name tqfaapi-uat --resource-group tqfa-uat-rg --set-env-vars "ALLOWED_ORIGINS=https://your-frontend.azurewebsites.net,http://localhost:3000"
```

### **Issue: SSL/TLS Certificate Errors**

**Symptoms:**
- HTTPS requests fail with SSL errors
- Certificate validation failures
- Mixed content warnings

**Solutions:**
1. **Check Azure Container Apps SSL**: Azure handles SSL automatically for `*.azurecontainerapps.io`
2. **Custom domains**: Configure SSL certificate in Azure
3. **Local development**: Use HTTP for local testing
4. **Mixed content**: Ensure all requests use HTTPS in production

---

## 📊 **Monitoring & Debugging**

### **Issue: Can't Find Application Logs**

**Get Container Logs:**
```bash
# Latest logs
az containerapp logs show --name tqfaapi-uat --resource-group tqfa-uat-rg --tail 100

# Specific revision logs
az containerapp logs show --name tqfaapi-uat --resource-group tqfa-uat-rg --revision tqfaapi-uat--v1-0-15 --tail 50

# Follow logs in real-time
az containerapp logs show --name tqfaapi-uat --resource-group tqfa-uat-rg --follow
```

**View GitHub Actions Logs:**
```bash
# List recent runs
gh run list --branch uat --limit 5

# View specific run
gh run view <RUN_ID>

# Watch run in real-time
gh run watch <RUN_ID>
```

---

## 🆘 **Emergency Recovery**

### **Immediate Rollback**

If a deployment breaks production:

```bash
# 1. List all revisions
az containerapp revision list --name tqfaapi-uat --resource-group tqfa-uat-rg --output table

# 2. Route traffic to last known good revision
az containerapp ingress traffic set --name tqfaapi-uat --resource-group tqfa-uat-rg --revision-weight <GOOD_REVISION>=100

# 3. Deactivate broken revision
az containerapp revision deactivate --name tqfaapi-uat --resource-group tqfa-uat-rg --revision <BROKEN_REVISION>

# 4. Verify users get working version
curl https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io/
```

### **Complete Environment Reset**

For catastrophic failures:

```bash
# 1. Create new Container App revision with known good image
az containerapp update --name tqfaapi-uat --resource-group tqfa-uat-rg --image <GOOD_IMAGE_TAG>

# 2. Wait for health checks
python promote_healthy_revision.py

# 3. Clean up old revisions
az containerapp revision list --name tqfaapi-uat --resource-group tqfa-uat-rg
# Deactivate old unhealthy revisions manually
```

---

## 📞 **Getting Help**

### **Useful Commands for Debugging**
```bash
# Container App status
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg

# All revisions with details  
az containerapp revision list --name tqfaapi-uat --resource-group tqfa-uat-rg --output table

# Environment variables
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "properties.template.containers[0].env"

# Ingress configuration
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "properties.configuration.ingress"

# Managed identity details
az containerapp show --name tqfaapi-uat --resource-group tqfa-uat-rg --query "identity"
```

### **Key Information to Gather**
When reporting issues, include:
- Container App name and resource group
- Revision name and health state
- Error messages from container logs
- GitHub Actions run ID
- Expected vs actual behavior
- Steps to reproduce

---

*This troubleshooting guide exists because Azure Container Apps has confusing behavior and error messages.*