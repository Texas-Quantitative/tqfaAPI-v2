# 🔗 TQFA Best Practices - GitHub Reference

**For Agents Working on Other Projects**

When you need production-ready FastAPI and Azure deployment best practices, reference this centralized documentation:

## 📂 **GitHub Repository**
`https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices`

## 📚 **Direct Links to Guides**

### **Essential Documentation**
- **[README.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/README.md)** - Overview and agent instructions
- **[docker-deployment.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/docker-deployment.md)** - Azure Container Apps deployment fixes
- **[scripts-and-tools.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/scripts-and-tools.md)** - Production-ready automation code
- **[troubleshooting.md](https://github.com/Texas-Quantitative/tqfaAPI/blob/main/docs/best-practices/troubleshooting.md)** - Common issues and solutions

### **Quick Implementation**
```bash
# Copy documentation to new project
git clone https://github.com/Texas-Quantitative/tqfaAPI temp-docs
cp -r temp-docs/docs/best-practices/ your-project/docs/
rm -rf temp-docs
```

## 🎯 **What These Guides Solve**
- **Azure Container Apps** traffic routing confusion (0% traffic issue)
- **CORS configuration** parsing errors in containers
- **Deployment automation** with health checks and rollbacks
- **Documentation maintenance** protocols for agents
- **Production-ready scripts** with error handling

## 📋 **Agent Usage Protocol**
1. **Reference the GitHub links** above when working on deployment issues
2. **Copy relevant documentation** to new projects as needed
3. **Follow the maintenance protocols** described in each guide
4. **Update "Last Modified" dates** when making changes

---

*This reference exists to prevent agents from rediscovering the same solutions across different projects. Always check these guides first for Azure deployment and FastAPI production issues.*