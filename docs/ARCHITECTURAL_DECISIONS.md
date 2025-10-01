# 🏗️ Architectural Decision Record (ADR) & Design Principles

**📋 PROMPT FOR FUTURE AGENTS:**
```
When making architectural changes to this FastAPI project, ALWAYS:
1. Read this entire file to understand existing design decisions
2. Read docs/DOCUMENTATION_MAINTENANCE_PROTOCOL.md to prevent context loss
3. Update this file if you make changes that affect system architecture
4. Follow the established patterns and principles documented here
5. Verify that new decisions don't conflict with existing ones
6. Add new ADRs at the bottom with date, rationale, and impact assessment
7. Use the conversation summary template to preserve critical context
```

---

## 🎯 Core Architectural Principles

### 1. **Hybrid Deployment Strategy** ✅ ESTABLISHED
- **Decision**: Windows development + Azure Linux containers for production
- **Rationale**: Leverages developer familiarity while ensuring cloud scalability
- **Impact**: Requires cross-platform compatibility considerations
- **Status**: ACTIVE - Do not change without major business case

### 2. **Security-First Design** ✅ ESTABLISHED  
- **Decision**: Admin-only user creation, no public registration endpoints
- **Rationale**: Prevents unauthorized access and maintains enterprise security
- **Impact**: All user management must go through secure admin endpoints
- **Status**: CRITICAL - Never expose public user creation

### 3. **Consolidated Resource Architecture** ✅ ESTABLISHED
- **Decision**: Single resource group per environment (tqfa-{env}-rg)
- **Rationale**: Simplifies permissions, billing, and reduces cross-RG access issues
- **Impact**: All Azure resources for an environment must be co-located
- **Status**: MANDATORY - See docs/AZURE_RESOURCES_AND_DEPLOYMENT_GUIDE.md

---

## 🏛️ System Architecture Patterns

### Application Structure
```
app/
├── api/              # API routes and endpoints
│   ├── routes.py     # Main router aggregation - DO NOT BYPASS
│   ├── admin_routes.py # Secure admin endpoints
│   └── *_routes.py   # Feature-specific routes
├── core/             # Core system services
├── services/         # Business logic services  
├── models/           # Data models (Pydantic)
├── schemas/          # Request/response schemas
└── config/           # Configuration management
```

**🔒 RULE**: All routes MUST be included through `app/api/routes.py` - never import directly in main app.

### Configuration Management
- **Pattern**: Environment-based configuration with Azure Key Vault
- **Key Vault Mapping**: 
  ```python
  {
      "dev": "kv-tqa-dev.vault.azure.net",
      "uat": "kv-tqfa-uat.vault.azure.net",  # Note: consolidated RG
      "prod": "kv-tqa-prod.vault.azure.net"
  }
  ```
- **🚨 CRITICAL**: UAT uses different naming due to resource consolidation

---

## 🔐 Security Architecture

### Authentication & Authorization
- **Admin API**: X-Admin-Key header authentication for administrative operations
- **User Management**: Admin-only user creation with secure password handling
- **Storage**: AES-256 encryption for sensitive data in Azure Blob Storage
- **Key Management**: Azure Key Vault with RBAC (not access policies)

### Security Boundaries
```
Internet → Azure Container Apps → FastAPI App → Azure Key Vault
                ↓
        Admin Routes (X-Admin-Key required)
                ↓
        User Services (Internal only)
```

**🚫 FORBIDDEN PATTERNS**:
- Public user registration endpoints
- Plaintext storage of sensitive data
- Cross-resource-group Key Vault access

---

## 🚀 Deployment Architecture

### Container Strategy
- **Base Image**: `python:3.11-slim` with multi-stage build
- **Entry Point**: `app.main_streamlined:app` (production) vs `app.main:app` (development)
- **Process**: Gunicorn + Uvicorn workers for production
- **Health Checks**: `/health/` endpoint with 30s intervals

### Environment Promotion Flow
```
Local Development → UAT (Container Apps) → Production (Container Apps)
                      ↑                        ↑
                GitHub Actions            GitHub Actions
                (uat branch)             (main branch)
```

### CI/CD Principles
- **Testing**: All deployments require passing tests
- **Image Caching**: Optimize Docker layer caching
- **Secret Management**: Never expose secrets in logs or environment variables
- **Rollback Strategy**: Blue-green deployment with revision management

---

## 📊 Data Architecture

### Storage Strategy
- **User Data**: Azure Blob Storage with structured hierarchy
- **Configuration**: Azure Key Vault secrets
- **Application State**: Stateless design with external storage
- **Caching**: In-memory caching for non-sensitive data only

### Data Flow Patterns
```
User Request → FastAPI → Business Service → Azure Storage
                  ↓
            Configuration Service → Key Vault
                  ↓
            AI Service → Azure OpenAI
```

---

## 🧠 AI & Integration Architecture

### Azure AI Services Integration
- **OpenAI**: Centralized through configured endpoints per environment  
- **Computer Vision**: Document processing and OCR capabilities
- **Conversation Management**: Blob-based conversation persistence

### RAG (Retrieval-Augmented Generation) Pattern
- **Document Processing**: Multi-format support (PDF, DOCX, TXT, etc.)
- **Context Enhancement**: Document-based knowledge augmentation
- **System Prompts**: Environment-specific prompt management

---

## 🔄 Development Patterns

### Code Quality Standards
- **Type Hints**: Required for all function parameters and returns
- **Async/Await**: Mandatory for all route handlers and I/O operations
- **Error Handling**: Structured HTTPException usage with proper status codes
- **Logging**: JSON structured logging in production

### Testing Strategy
- **Unit Tests**: Business logic and service layer testing
- **Integration Tests**: Full API endpoint testing with mock Azure services
- **Load Testing**: Container resource optimization
- **Security Testing**: Authentication and authorization validation

### Dependency Management
```python
# Established dependency injection pattern
from app.core.container import Container

# Service resolution through container
container = Container()
service = container.get_service_instance()
```

---

## 📚 Historical Decisions & Lessons Learned

### ADR-001: Resource Group Consolidation (2025-09-25)
- **Problem**: Cross-resource-group access causing deployment failures
- **Solution**: Consolidated all UAT resources into `tqfa-uat-rg`
- **Impact**: Simplified permissions and eliminated cross-region issues
- **Lesson**: Always co-locate related Azure resources in same RG/region

### ADR-002: Admin-Only Architecture (2025-09-25)  
- **Problem**: Public user creation endpoint was security vulnerability
- **Solution**: Removed public endpoint, implemented X-Admin-Key authentication
- **Impact**: All user creation now requires administrative access
- **Lesson**: Security-first design prevents future vulnerabilities

### ADR-003: Streamlined Production App (2025-09-25)
- **Problem**: Complex middleware causing Windows Defender issues
- **Solution**: Created `main_streamlined.py` with minimal middleware
- **Impact**: Reduced attack surface and improved startup performance  
- **Lesson**: Simplicity in production reduces operational complexity

---

## 🚨 Critical Warnings for Future Agents

### ❌ NEVER DO THIS:
1. **Expose public user registration** - Security violation
2. **Mix resource groups** - Causes permission failures  
3. **Bypass route aggregation** - Breaks maintainability
4. **Store secrets in code** - Security violation
5. **Skip integration tests** - Causes deployment failures

### ✅ ALWAYS DO THIS:
1. **Update documentation when changing infrastructure**
2. **Test admin endpoints after deployment changes**
3. **Verify Key Vault permissions for managed identities**
4. **Use structured logging for troubleshooting**
5. **Follow the established naming conventions**

---

## 🔄 Process for Architectural Changes

### Before Making Changes:
1. Review this ADR and related documentation
2. Assess impact on existing patterns and decisions
3. Consider security implications
4. Plan rollback strategy

### When Making Changes:
1. Follow established patterns where possible
2. Document new patterns if deviating from existing ones
3. Update relevant configuration files
4. Ensure comprehensive testing

### After Making Changes:
1. Update this ADR with new decisions
2. Update Azure documentation if infrastructure changed
3. Update README and other relevant docs
4. Verify end-to-end functionality

---

## 📝 New Architectural Decisions

**Template for new entries:**
```
### ADR-XXX: [Decision Title] ([Date])
- **Problem**: [What problem were you solving?]
- **Solution**: [What approach did you take?]
- **Impact**: [What does this change?]
- **Lesson**: [What should future agents know?]
```

<!-- Add new ADRs above this line -->

---

**📅 Last Updated**: 2025-09-25  
**🔄 Next Review**: When making significant architectural changes

**💡 Remember**: This document is your architectural compass. When in doubt, favor consistency with established patterns over innovation.