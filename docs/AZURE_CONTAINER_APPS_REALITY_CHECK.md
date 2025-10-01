# Azure Container Apps: The Real Story

This document explains the **brutal reality** of deploying to Azure Container Apps and how to avoid the common pitfalls that waste **days** of debugging time.

## 🤬 The Central Problem

Azure Container Apps has **INSANE** default behavior that differs from every other container platform:

### What You Expect (Normal Platform Behavior)
1. Deploy new container version
2. Health checks pass  
3. **Traffic automatically routes to healthy new version**
4. Users get new version immediately

### What Actually Happens (Azure Container Apps)
1. Deploy new container version  
2. Health checks pass
3. **New version gets 0% traffic by default** 🤯
4. Users continue getting old version
5. **Manual promotion required** to route traffic

This creates the illusion that deployments are "broken" when they're actually working perfectly.

## 🚨 Critical Commands You Need

### 1. Check Revision Status
```bash
az containerapp revision list --name <APP_NAME> --resource-group <RG> --output table
```
Look for:
- **HealthState**: Should be "Healthy"  
- **TrafficWeight**: Shows actual user traffic percentage
- **A healthy revision with 0% traffic means manual promotion needed**

### 2. Promote Healthy Revision (The Missing Step)
```bash
# Route 100% traffic to specific revision
az containerapp ingress traffic set \
  --name <APP_NAME> \
  --resource-group <RG> \
  --revision-weight <REVISION_NAME>=100
```

### 3. Test What Users Actually See
```bash
curl https://<APP_URL>/
```
**This is the ONLY way to verify users are getting the new version!**

## 🔥 Real-World Example

```bash
# Deploy succeeds, health checks pass
az containerapp update --name myapp --image myimage:v2

# Check status - you'll see this confusing output:
# myapp--v1    Healthy    100%    (users getting this - OLD VERSION)
# myapp--v2    Healthy      0%    (new version - USERS NOT GETTING THIS!)

# Manual promotion required (the missing step):
az containerapp ingress traffic set --name myapp --revision-weight myapp--v2=100

# Now users get v2
```

## 🛠️ Automation Script

Use our `promote_healthy_revision.py` script to automate this stupid manual step:

```python
# This script fixes Azure's idiotic behavior automatically
python promote_healthy_revision.py
```

## 📊 Traffic Management Modes

Azure Container Apps has two modes:

### Single Revision Mode (Default)
- Only one revision active at a time
- New deployments automatically get traffic
- **Recommended for most applications**

### Multiple Revision Mode  
- Multiple revisions can be active
- **Manual traffic management required** 
- Blue-green deployments possible
- **This is the mode causing the confusion**

### How to Check/Change Mode
```bash
# Check current mode
az containerapp show --name <APP> --resource-group <RG> --query "properties.configuration.activeRevisionsMode"

# Set to single revision mode (recommended)
az containerapp revision set-mode --name <APP> --resource-group <RG> --mode single

# Set to multiple revision mode (advanced)
az containerapp revision set-mode --name <APP> --resource-group <RG> --mode multiple
```

## 🎯 Best Practices

### 1. Use Single Revision Mode for Simple Deployments
```bash
az containerapp revision set-mode --mode single
```
This eliminates the traffic promotion problem.

### 2. Automate Traffic Promotion in CI/CD
Add this to your deployment pipeline:
```yaml
- name: Promote Healthy Revision  
  run: python promote_healthy_revision.py
```

### 3. Always Test User Experience
```bash
# Don't trust health checks - test what users actually see
curl https://your-app.azurecontainerapps.io/
```

### 4. Monitor Revision Status
```bash
# Check this after every deployment
az containerapp revision list --output table
```

## 🤔 Why Does This Exist?

Microsoft designed this for "enterprise blue-green deployments" but:

1. **Made it the default behavior** (insane)
2. **Didn't document it clearly** (disaster)  
3. **No warnings during deployment** (users think deployments failed)
4. **Manual intervention required** for basic deployments (ridiculous)

## 🚀 The Solution

1. **Switch to single revision mode** for simple apps
2. **Use our automation script** for multi-revision mode  
3. **Always verify user experience** after deployments
4. **Document this insanity** for your team

## 📈 Success Metrics

You know it's working when:
- ✅ Health checks pass
- ✅ Traffic weight shows 100% on new revision  
- ✅ `curl` returns new version info
- ✅ Users can access the application

## 🎯 TL;DR

**Azure Container Apps doesn't automatically route traffic to healthy containers.** 

You must manually promote them or use single revision mode. This is the #1 cause of "deployment working but users not getting updates" confusion.

---

*This document exists because Microsoft's documentation is terrible and wastes developer time.*