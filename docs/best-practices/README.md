# Texas Quantitative Development Best Practices

*A modular guide for building production-ready applications with proper deployment practices across all TQ projects*

**Last Modified**: September 27, 2025  
**Version**: 1.1

**🔗 GitHub Repository**: `https://github.com/Texas-Quantitative/tqfaAPI`  
**📂 Direct Link to This Documentation**: `https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices`

---

## 👨‍💻 **For Developers: How to Direct Agents to This Documentation**

**When working with AI agents on any Texas Quantitative project, use these prompts:**

### **🚀 Getting Started Prompt**
```
"Please reference the Texas Quantitative best practices documentation at: 
https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices

Start with README.md for overview, then check the specific guides for:
- Deployment issues → docker-deployment.md
- Automation scripts → scripts-and-tools.md  
- Common problems → troubleshooting.md"
```

### **🔧 Specific Problem Prompts**
```
"Check the troubleshooting guide: 
https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/troubleshooting.md
for solutions to [describe your issue]"

"Use the automation scripts from:
https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/scripts-and-tools.md
for [deployment/traffic promotion/health checks]"
```

### **📚 Documentation Update Reminder**
```
"After solving this issue, please update the relevant documentation in 
docs/best-practices/ and follow the GitHub push protocol to make changes 
available for future agents"
```

**Why This Works**: These prompts ensure agents access the complete, battle-tested solutions from Texas Quantitative's engineering experience instead of recreating fixes from scratch.

---

## 📋 **Instructions for AI Agents**

### **How to Use This Documentation Collection**

This is a **modular documentation system** designed for efficient agent collaboration:

1. **Start Here**: This README provides overview and navigation
2. **Find Specific Issues**: Use the guide links below for detailed solutions
3. **Update Documentation**: Always update the "Last Modified" date when making changes
4. **Maintain Context**: Each guide contains complete context for standalone use
5. **Copy for New Projects**: The entire `docs/best-practices/` directory is portable

### **🌐 For Agents Working on Other Projects**

**Need these best practices in another project?** Use these GitHub links:

**Quick Reference Commands:**
```bash
# Clone just this documentation to a new project
git clone https://github.com/Texas-Quantitative/tqfaAPI temp-docs
cp -r temp-docs/docs/best-practices/ your-new-project/docs/
rm -rf temp-docs

# Or download specific files directly from GitHub
curl -O https://raw.githubusercontent.com/Texas-Quantitative/tqfaAPI/main/docs/best-practices/docker-deployment.md
```

**Direct Links to Individual Guides:**
- **[docker-deployment.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/docker-deployment.md)** - Azure Container Apps deployment issues
- **[scripts-and-tools.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/scripts-and-tools.md)** - Production-ready automation scripts
- **[troubleshooting.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/troubleshooting.md)** - Common issues and solutions

**🔧 Implementation Protocol:**
1. **Copy Documentation**: Use commands above or GitHub download
2. **Customize Content**: Update project-specific details (names, URLs, etc.)
3. **Update References**: Modify main project docs to reference these guides
4. **Follow Maintenance**: Use the update protocols described below

### **When to Update These Documents**

**ALWAYS update the "Last Modified" date when you:**
- ✅ Add new solutions or workarounds
- ✅ Update scripts or code examples  
- ✅ Fix errors or improve explanations
- ✅ Add new sections or reorganize content
- ✅ Update URLs, commands, or technical details

**Format**: `**Last Modified**: Month Day, Year` (e.g., **Last Modified**: September 27, 2025)

### **Document Maintenance Protocol**

1. **Before Editing**: Check the "Last Modified" date to see if information is current
2. **After Editing**: Update the "Last Modified" date to today's date
3. **Major Changes**: Consider incrementing the version number (if present)
4. **Cross-References**: Update related documents if changes affect multiple guides
5. **Agent Handoffs**: Mention which documents were updated in session summaries

### **🚨 CRITICAL: GitHub Push Protocol**

**MANDATORY when updating documentation:**

```bash
# 1. Commit changes to current branch
git add docs/ .github/copilot-instructions.md TQFA_DEVELOPMENT_BEST_PRACTICES.md
git commit -m "Update documentation: [brief description]"
git push

# 2. Merge to main branch (CRITICAL - GitHub links point to main!)
git checkout main
git merge [current-branch]
git push origin main
git checkout [current-branch]
```

**Why This Protocol Exists:**
- All GitHub documentation links reference the `main` branch
- Other agents need documentation accessible via GitHub URLs
- Documentation updates in feature branches aren't publicly available
- This prevents "404 - page not found" errors when sharing links

---

## 🚨 **CRITICAL: NO SHORTCUTS FROM DAY ONE**

The fundamental rule that will save you **days** of debugging time:

> **ENGINEERING SHORTCUTS ARE TECHNICAL DEBT WITH COMPOUND INTEREST**

Every system component must be production-ready from first deployment. If you wouldn't trust it with real customer traffic, don't deploy it to UAT.

---

## 📚 **Documentation Structure**

This guide is split into focused documents for easy reference and reuse:

### 🚀 **Deployment & Infrastructure**
- **[Docker Deployment Guide](./docker-deployment.md)** - Azure Container Apps, traffic management, health checks
- **[Version Management](./version-management.md)** - Automated versioning, release practices  
- **[CI/CD Pipeline](./cicd-pipeline.md)** - GitHub Actions, automated deployments, rollback strategies

### 🏗️ **Development**
- **[FastAPI Architecture](./fastapi-architecture.md)** - Project structure, API design, best practices
- **[Code Standards](./code-standards.md)** - Python style, type hints, testing approaches
- **[Security Practices](./security.md)** - Authentication, secrets management, secure coding

### ☁️ **Azure & Infrastructure**
- **[Azure Resources Guide](./azure-resources.md)** - Resource management, Key Vault, storage
- **[Environment Configuration](./environment-config.md)** - Settings, secrets, environment variables
- **[Monitoring & Debugging](./monitoring.md)** - Logging, health checks, troubleshooting

### 🤖 **AI Agent Collaboration**
- **[Agent Handoff Guide](./agent-handoff.md)** - Context preservation, session management
- **[Documentation Standards](./documentation-standards.md)** - How to write agent-friendly docs

### 🛠️ **Tools & Scripts**
- **[Essential Scripts](./scripts-and-tools.md)** - Deployment, testing, and utility scripts
- **[Common Issues](./troubleshooting.md)** - Known problems and solutions

---

## 🎯 **Core Principles**

### **1. Production-Ready From Day One**
- All deployments must have health checks and rollback capability
- Never deploy manually-managed infrastructure to production
- Test in appropriate environments before production deployment

### **2. Automation Over Manual Work**  
- Automate version bumping, deployment, and infrastructure management
- Use CI/CD pipelines for all environment deployments
- Scripts should handle error conditions gracefully

### **3. Clear Documentation & Context**
- Every decision should be documented with reasoning
- Agent handoffs require complete context preservation
- Code should be self-documenting with appropriate standards for the technology stack

### **4. Security & Configuration Management**
- Never commit secrets to git
- Use proper secrets management (Azure Key Vault, AWS Secrets Manager, etc.)
- Implement proper authentication and authorization patterns

---

## 🚀 **Quick Start for New Projects**

1. **Copy this entire `best-practices/` directory** to your new project
2. **Update the agent instructions** to reference `docs/best-practices/README.md`
3. **Follow the [Docker Deployment Guide](./docker-deployment.md)** for Azure setup
4. **Implement [CI/CD Pipeline](./cicd-pipeline.md)** for automated deployments
5. **Use [Essential Scripts](./scripts-and-tools.md)** for common tasks

---

## 🎓 **Key Lessons Learned**

### **The Deployment Disaster**
We spent **3+ days** debugging deployments because we took shortcuts early. The lesson:
- Proper deployment practices prevent 90% of infrastructure issues
- Azure Container Apps requires specific traffic management (see [Docker Deployment Guide](./docker-deployment.md))
- Health checks and rollback strategies are mandatory, not optional

### **Documentation Saves Time**
- Well-structured docs prevent repeating the same debugging sessions
- Agent-friendly documentation enables faster problem resolution
- Modular docs allow copying best practices to new projects

### **Automation Prevents Human Error**
- Manual deployments fail at the worst possible times
- Version management scripts prevent deployment confusion
- Automated traffic promotion eliminates Azure Container Apps' confusing defaults

---

## 📞 **Using This Guide**

- **For Development**: Start with [FastAPI Architecture](./fastapi-architecture.md) and [Code Standards](./code-standards.md)
- **For Deployment Issues**: Check [Docker Deployment](./docker-deployment.md) and [Troubleshooting](./troubleshooting.md)  
- **For New Projects**: Follow the **Quick Start** above and adapt the scripts to your needs
- **For Agent Collaboration**: Reference [Agent Handoff Guide](./agent-handoff.md)

---

*This documentation exists because proper engineering practices save exponentially more time than they cost.*