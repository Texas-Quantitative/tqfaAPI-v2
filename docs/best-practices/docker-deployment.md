# Docker Deployment Guide for Azure Container Apps

*The complete guide to deploying FastAPI applications to Azure Container Apps without losing your sanity*

**Last Modified**: September 27, 2025  
**Version**: 1.0

---

## 🤬 **The Reality of Azure Container Apps**

Azure Container Apps has **INSANE** default behavior that differs from every other container platform. This guide explains how to work with (and around) these issues.

### **The Central Problem**
**Expected Behavior** (Normal Platforms):
1. Deploy new container → Health checks pass → Traffic routes to new version → Users get update

**Azure Container Apps Reality**:
1. Deploy new container → Health checks pass → **New version gets 0% traffic** → Users stay on old version → **Manual promotion required**

This creates the illusion that deployments are "broken" when they're actually working.

---

## 🚀 **Complete Deployment Process**

### **1. Version Management**
Always bump version before deployment:

```bash
# Run this before every deployment
python bump_version.py
git add .
git commit -m "Version bump to X.Y.Z - [description]"
git push
```

### **2. Dockerfile Requirements** 

Your `Dockerfile` must include:

```dockerfile
# Essential health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Production command with proper workers and timeout
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--timeout", "120"]
```

### **3. FastAPI Health Endpoint**

Your app must have a working health endpoint:

```python
@app.get("/health/")
async def health_check():
    """Health check endpoint for deployment validation."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.X",
        "checks": {
            "database": {"status": "healthy"},
            "storage": {"status": "healthy"}
        }
    }
```

### **4. Settings Configuration Fix**

Azure sets environment variables as strings, but Pydantic expects proper types. Fix CORS issues:

```python
from pydantic import field_validator
from typing import Union, List
import json

class Settings(BaseSettings):
    # Use Union to handle string input from Azure
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:3000"]
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from various formats."""
        if isinstance(v, str):
            # Handle Azure's "[*]" format
            if v.strip() in ["[*]", "*"]:
                return ["*"]
            # Parse comma-separated
            if "," in v:
                return [origin.strip() for origin in v.split(",")]
            # Single origin
            return [v]
        return v if isinstance(v, list) else ["*"]
```

---

## 🛠️ **Azure Container Apps Management**

### **Check Deployment Status**
```bash
# See all revisions and their traffic weight
az containerapp revision list --name <APP_NAME> --resource-group <RG> --output table

# Look for:
# - HealthState: Should be "Healthy"  
# - TrafficWeight: Shows actual user traffic %
```

### **Promote Healthy Revision (Critical Step)**
```bash
# Route 100% traffic to latest healthy revision
az containerapp ingress traffic set \
  --name <APP_NAME> \
  --resource-group <RG> \
  --revision-weight <REVISION_NAME>=100
```

### **Test User Experience**
```bash
# This is the ONLY way to verify users get the new version
curl https://<APP_URL>/
```

---

## 🤖 **Automated Traffic Promotion**

Use our script to automate Azure's stupid manual promotion requirement:

### **promote_healthy_revision.py**
```python
#!/usr/bin/env python3
"""
Auto-promotes latest healthy revision to receive 100% traffic.
This fixes Azure Container Apps' idiotic default behavior.
"""

def promote_latest_healthy_revision(app_name, resource_group):
    """Find latest healthy revision and promote it."""
    
    # Get all revisions
    revisions = run_command(f"az containerapp revision list --name {app_name} --resource-group {resource_group}")
    
    # Find healthy revisions, sorted by creation time
    healthy = [r for r in revisions if r.get('properties', {}).get('healthState') == 'Healthy']
    healthy.sort(key=lambda x: x.get('properties', {}).get('createdTime', ''), reverse=True)
    
    if not healthy:
        print("❌ No healthy revisions found!")
        return False
    
    latest = healthy[0]
    revision_name = latest['name']
    current_traffic = latest.get('properties', {}).get('trafficWeight', 0)
    
    if current_traffic == 100:
        print("✅ Latest healthy revision already has 100% traffic")
        return True
    
    # Promote to 100% traffic
    run_command(f"az containerapp ingress traffic set --name {app_name} --resource-group {resource_group} --revision-weight {revision_name}=100")
    print(f"✅ Promoted {revision_name} to 100% traffic!")
    return True
```

### **CI/CD Integration**
Add to your GitHub Actions workflow:

```yaml
- name: Deploy to Container Apps with Health Checks
  run: |
    # ... deployment steps ...
    
    # Auto-promote healthy revision (fixes Azure's default behavior)
    python promote_healthy_revision.py
```

---

## 🔧 **Revision Modes**

Azure Container Apps has two modes that affect traffic behavior:

### **Single Revision Mode (Recommended)**
```bash
# Set single revision mode - automatically routes traffic
az containerapp revision set-mode --name <APP> --resource-group <RG> --mode single
```
- Only one revision active at a time
- New deployments automatically get traffic
- **Eliminates the manual promotion problem**

### **Multiple Revision Mode (Advanced)**
```bash
# Set multiple revision mode - manual traffic management
az containerapp revision set-mode --name <APP> --resource-group <RG> --mode multiple
```
- Multiple revisions can be active
- **Requires manual traffic promotion** (our automation script)
- Enables blue-green deployments
- **This mode causes the confusion**

---

## 🚨 **Common Deployment Failures**

### **Container Won't Start**
**Symptoms**: Revision shows "Unhealthy", logs show startup errors

**Debug**:
```bash
# Get container logs
az containerapp logs show --name <APP> --resource-group <RG> --revision <REVISION> --tail 50
```

**Common Causes**:
- **Settings parsing errors**: Fix CORS/environment variable handling (see above)
- **Missing dependencies**: Check requirements.txt
- **Port binding issues**: Ensure container binds to 0.0.0.0:8000
- **Health check failures**: Verify `/health/` endpoint works

### **Deployment "Succeeds" But Users See Old Version**
**Cause**: Azure's default behavior - healthy revision gets 0% traffic

**Solution**: Run traffic promotion
```bash
python promote_healthy_revision.py
```

### **Health Checks Fail**
**Symptoms**: Revision shows "Unhealthy" even though container starts

**Debug**:
```bash
# Test health endpoint directly
curl https://<REVISION_URL>/health/
```

**Fixes**:
- Ensure `/health/` returns 200 status
- Check health endpoint dependencies (DB, storage, etc.)
- Verify health check timeout settings

---

## 📊 **Monitoring & Validation**

### **Deployment Success Checklist**
- ✅ New revision created with correct version tag
- ✅ Revision health state shows "Healthy"  
- ✅ Traffic weight shows 100% on new revision
- ✅ `curl <APP_URL>` returns new version info
- ✅ Application functions correctly for users

### **Essential Commands**
```bash
# Check revision status
az containerapp revision list --name <APP> --resource-group <RG> --output table

# View container logs  
az containerapp logs show --name <APP> --resource-group <RG> --tail 100

# Test health endpoint
curl https://<APP_URL>/health/

# Get application info
curl https://<APP_URL>/
```

---

## 🎯 **Best Practices Summary**

1. **Always use version bumping** before deployments
2. **Include proper health checks** in your application
3. **Fix settings parsing** to handle Azure environment variables  
4. **Use single revision mode** for simple applications
5. **Automate traffic promotion** with our script for multi-revision mode
6. **Test user experience** after every deployment
7. **Monitor revision health** and traffic distribution

---

## 🔗 **Related Documentation**

- [Version Management](./version-management.md) - Automated version bumping
- [CI/CD Pipeline](./cicd-pipeline.md) - Complete GitHub Actions setup  
- [Troubleshooting](./troubleshooting.md) - Common issues and solutions
- [Scripts and Tools](./scripts-and-tools.md) - Deployment automation scripts

---

*This guide exists because Azure Container Apps' default behavior is confusing and poorly documented.*