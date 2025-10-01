# 🚀 Quick Reference for AI Agents

## 🔍 Essential Files to Check BEFORE Making Changes

| File | Purpose | When to Check |
|------|---------|---------------|
| `docs/AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md` | Azure infrastructure mapping | Any Azure/deployment changes |
| `docs/ARCHITECTURAL_DECISIONS.md` | Design principles & patterns | Any architectural changes |
| `.github/copilot-instructions.md` | Code standards & practices | All development work |
| `app/api/routes.py` | Main route aggregation | Adding new endpoints |
| `app/config.py` | Key Vault and environment config | Configuration changes |

## ⚡ Common Tasks - Quick Commands

### Check Deployment Status
```bash
gh run list --branch uat --limit 3
az containerapp logs show -n tqfaapi-uat -g tqfa-uat-rg --tail 20
```

### Test Admin Endpoints  
```bash
# Local testing
$env:ADMIN_API_KEY = "gHKouDVn1eYUh6j2MFAkcaGYOtidSYiD"; python test_admin_endpoints.py

# UAT testing
Invoke-WebRequest -Uri "https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io/api/v1/admin/system/status" -Headers @{"X-Admin-Key" = "gHKouDVn1eYUh6j2MFAkcaGYOtidSYiD"}
```

### Create UAT User
```bash
python uat_create_user.py [username] [password]
```

## 🚨 Critical Rules (NEVER VIOLATE)

1. **🔐 NEVER expose public user registration**
2. **🏢 NEVER mix Azure resource groups** 
3. **🔗 NEVER bypass `app/api/routes.py` for route inclusion**
4. **🔑 NEVER store secrets in code or environment files**
5. **📝 ALWAYS update docs when changing infrastructure**

## 🏗️ Architecture at a Glance

```
Local Dev (Windows) → GitHub Actions → Azure Container Apps (Linux)
                              ↓
                         Key Vault Secrets
                              ↓
                         Storage & AI Services
```

**Resource Groups by Environment:**
- DEV: `rg-tqa-dev` (eastus)
- UAT: `tqfa-uat-rg` (eastus2) ⚠️ Different naming!
- PROD: `rg-tqa-prod` (eastus)

## 🔄 Standard Troubleshooting Flow

1. **Check logs**: Container app logs first
2. **Verify Key Vault**: Managed identity permissions
3. **Test locally**: Ensure code works before deployment
4. **Check resource groups**: Ensure resources are co-located
5. **Verify routes**: Admin endpoints properly included

## 📞 When Things Break

| Problem | Most Likely Cause | First Check |
|---------|-------------------|-------------|
| 404 on admin endpoints | Routes not included | `app/api/routes.py` |
| Key Vault access denied | Wrong RG or permissions | Managed identity roles |
| Container won't start | Missing secrets | Azure Key Vault contents |
| Deployment succeeds but no changes | Cached Docker image | Force rebuild |

## 💡 Pro Tips

- **Always test locally first** with the production entry point
- **Use the debug scripts** in the repo root for troubleshooting  
- **Check both the deployment logs AND container logs** when debugging
- **Resource group naming is inconsistent** - check the docs for each environment
- **UAT uses different Key Vault** due to consolidation (kv-tqfa-uat vs kv-tqa-uat)

---
**📚 For detailed information, see the full documentation files listed above.**