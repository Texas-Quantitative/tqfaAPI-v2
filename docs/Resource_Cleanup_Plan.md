# Resource Cleanup & UAT Migration Plan

## 🧹 **Current Development Setup (Mixed Resources)**

### Current Resource Sources:
- **Azure OpenAI Endpoint**: `qualbe-openai.openai.azure.com` (from another dev project)
- **Chat Deployment**: `qualbe-gpt4o` (from another dev project)  
- **Embedding Deployment**: `qualbe-assistant-embed` (from another dev project)
- **Storage Account**: `qualbedocs` (appears to be shared/dev)

### ⚠️ **Issues to Address Before UAT:**
1. **Resource Ownership**: Using resources from another dev project
2. **Cost Attribution**: Costs are going to wrong project/billing
3. **Access Control**: Potential security/access issues
4. **Environment Isolation**: Dev and UAT should be separate
5. **Resource Naming**: Should follow your project naming conventions

## 🎯 **UAT Migration Checklist**

### **Phase 1: Create Dedicated Resources**

#### **1. Azure OpenAI Service (New)**
- [ ] **Create new Azure OpenAI resource** for tqfaAPI project
- [ ] **Deploy Chat Model**: `gpt-4o` or `gpt-4`
  - Suggested name: `tqfaapi-gpt4o` or `tqfaapi-chat`
- [ ] **Deploy Embedding Model**: `text-embedding-3-small`
  - Suggested name: `tqfaapi-embedding`
- [ ] **Configure rate limits** based on expected UAT usage
- [ ] **Set up proper RBAC** for UAT access

#### **2. Storage Resources (Review)**
- [ ] **Review storage account**: Determine if `qualbedocs` is appropriate for UAT
- [ ] **Create dedicated storage** if needed: `tqfaapistorage` or similar
- [ ] **Set up containers**: `tqfaapi-uat-vault`
- [ ] **Configure access policies** for UAT environment

#### **3. Key Vault (Optional but Recommended)**
- [ ] **Create Azure Key Vault** for UAT secrets management
- [ ] **Store API keys** securely in Key Vault
- [ ] **Set up managed identity** for secure access
- [ ] **Remove secrets from .env files** in UAT

### **Phase 2: Environment Configuration**

#### **UAT Environment Variables Template**
```env
# UAT Environment Configuration
ENVIRONMENT=uat

# Azure OpenAI Configuration (UAT)
AZURE_OPENAI_ENDPOINT=https://tqfaapi-openai.openai.azure.com
AZURE_OPENAI_KEY=[FROM_KEY_VAULT]
AZURE_OPENAI_DEPLOYMENT=tqfaapi-gpt4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=tqfaapi-embedding
AZURE_OPENAI_API_VERSION=2024-06-01

# Storage Configuration (UAT)
AZURE_STORAGE_CONNECTION_STRING=[FROM_KEY_VAULT]
STORAGE_CONTAINER=tqfaapi-uat-vault

# FastAPI Configuration (UAT)
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=false  # No hot reload in UAT
```

#### **Production Environment Variables Template**
```env
# Production Environment Configuration
ENVIRONMENT=production

# Azure OpenAI Configuration (Production)
AZURE_OPENAI_ENDPOINT=https://tqfaapi-prod-openai.openai.azure.com
AZURE_OPENAI_KEY=[FROM_KEY_VAULT]
AZURE_OPENAI_DEPLOYMENT=tqfaapi-prod-gpt4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=tqfaapi-prod-embedding
AZURE_OPENAI_API_VERSION=2024-06-01

# Storage Configuration (Production)
AZURE_STORAGE_CONNECTION_STRING=[FROM_KEY_VAULT]
STORAGE_CONTAINER=tqfaapi-prod-vault
```

### **Phase 3: Migration Steps**

#### **Before UAT Promotion:**
1. **Create UAT Resources**
   ```bash
   # Create resource group
   az group create --name tqfaapi-uat-rg --location eastus
   
   # Create Azure OpenAI
   az cognitiveservices account create \
     --name tqfaapi-uat-openai \
     --resource-group tqfaapi-uat-rg \
     --kind OpenAI \
     --sku S0 \
     --location eastus
   ```

2. **Deploy Models**
   - Use Azure OpenAI Studio to deploy chat and embedding models
   - Use consistent naming: `tqfaapi-chat`, `tqfaapi-embedding`

3. **Update Configuration**
   - Create UAT-specific .env file
   - Test with new resources
   - Validate all functionality

4. **Data Migration (if needed)**
   - Export test data from dev storage
   - Import to UAT storage with proper structure
   - Validate data integrity

#### **Testing Checklist:**
- [ ] **RAG functionality** works with new embedding deployment
- [ ] **File upload/storage** works with new storage account
- [ ] **LLM interactions** work with new chat deployment
- [ ] **Performance** meets expectations
- [ ] **Cost monitoring** is in place

## 🚨 **Current Risks (Until Cleanup)**

### **Immediate Risks:**
1. **Cost Attribution**: Your usage may be billed to another project
2. **Resource Contention**: Other projects might affect your rate limits
3. **Access Issues**: Resources could be modified/deleted by other teams
4. **Security**: Using shared resources may have broader access than needed

### **Mitigation Strategies (Short Term):**
1. **Monitor Usage**: Track your API calls to understand costs
2. **Document Dependencies**: Keep track of what resources you're using
3. **Plan Migration**: Schedule resource creation before UAT
4. **Backup Configuration**: Save current working .env settings

## 📅 **Recommended Timeline**

### **Week 1-2: Planning**
- [ ] Define resource naming conventions
- [ ] Plan resource topology for UAT/Production
- [ ] Get approvals for new Azure resources
- [ ] Create resource provisioning scripts

### **Week 3: Resource Creation**
- [ ] Create UAT Azure OpenAI service
- [ ] Deploy and test models
- [ ] Create storage resources
- [ ] Set up Key Vault (optional)

### **Week 4: Migration & Testing**
- [ ] Update configuration files
- [ ] Test all functionality with new resources
- [ ] Performance and load testing
- [ ] Document new setup

### **Week 5: UAT Promotion**
- [ ] Deploy to UAT environment
- [ ] Validate all systems
- [ ] Monitor costs and performance
- [ ] Clean up dev dependencies

## 🔧 **Code Changes Needed**

### **Environment-Aware Configuration**
Consider adding environment detection to your configuration:

```python
# app/config.py enhancement
import os

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    @property
    def is_development(self):
        return self.ENVIRONMENT == "development"
    
    @property 
    def is_uat(self):
        return self.ENVIRONMENT == "uat"
    
    @property
    def is_production(self):
        return self.ENVIRONMENT == "production"
```

### **Resource Validation**
Add startup checks to validate resource configuration:

```python
async def validate_resources():
    """Validate that all required resources are accessible."""
    # Check Azure OpenAI connectivity
    # Verify storage account access
    # Test embedding deployment
    # Log configuration status
```

## 💰 **Cost Considerations**

### **Current Situation:**
- Unknown cost attribution (costs going to other project)
- Potential overage on other project's budgets
- No dedicated monitoring for your usage

### **After Cleanup:**
- Clear cost attribution to tqfaAPI project
- Dedicated rate limits and budgets
- Proper cost monitoring and alerts
- Ability to optimize for your specific usage patterns

## 📋 **For Now (Continue Development)**

Your current setup is **perfectly fine for development**. The RAG system is working excellently, and you can continue development without any issues. Just keep this cleanup plan in mind for when you're ready to promote to UAT.

### **Immediate Actions:**
- ✅ Continue development with current resources
- ✅ Document any new dependencies
- ✅ Monitor for any access issues
- ✅ Plan UAT resource creation timeline

Would you like me to help create any specific scripts or configurations for the future migration?
