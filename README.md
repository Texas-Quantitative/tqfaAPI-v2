# TQFA API V2 - Texas Quantitative Financial Analysis API# TQFA API V2 - Texas Quantitative Financial Analysis API



> **Production-Ready FastAPI Application with Azure AI Foundry Integration**> **Production-Ready FastAPI Application with Azure AI Foundry Integration**



[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-009688.svg)](https://fastapi.tiangolo.com)[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-009688.svg)](https://fastapi.tiangolo.com)

[![Azure Container Apps](https://img.shields.io/badge/Azure-Container%20Apps-blue.svg)](https://azure.microsoft.com/en-us/services/container-apps/)[![Azure Container Apps](https://img.shields.io/badge/Azure-Container%20Apps-blue.svg)](https://azure.microsoft.com/en-us/services/container-apps/)



## 🚀 **Quick Start Guide**## Solution Overview



Get TQFA API V2 running locally in under 5 minutes:This solution deploys a web-based chat application with an AI agent running in Azure Container App.



```bashThe agent leverages the Azure AI Agent service and utilizes Azure AI Search for knowledge retrieval from uploaded files, enabling it to generate responses with citations. The solution also includes built-in monitoring capabilities with tracing to ensure easier troubleshooting and optimized performance.

# Clone and setup

git clone https://github.com/Texas-Quantitative/tqfaAPI-v2.gitThis solution creates an Azure AI Foundry project and Azure AI services. More details about the resources can be found in the [resources](#resources) documentation. There are options to enable logging, tracing, and monitoring.

cd tqfaAPI-v2

Instructions are provided for deployment through GitHub Codespaces, VS Code Dev Containers, and your local development environment.

# Install dependencies

pip install fastapi uvicorn python-multipart azure-identity### Solution Architecture



# Start development server![Architecture diagram showing that user input is provided to the Azure Container App, which contains the app code. With user identity and resource access through managed identity, the input is used to form a response. The input and the Azure monitor are able to use the Azure resources deployed in the solution: Application Insights, Azure AI Foundry Project, Azure AI Services, Storage account, Azure Container App, and Log Analytics Workspace.](docs/images/architecture.png)

uvicorn app.main:app --reload --host localhost --port 8000

The app code runs in Azure Container App to process the user input and generate a response to the user. It leverages Azure AI projects and Azure AI services, including the model and agent.

# Test endpoints

curl http://localhost:8000          # API info### Key Features

curl http://localhost:8000/health   # Health check

curl http://localhost:8000/docs     # Interactive documentation- **[Knowledge Retrieval](./docs/deploy_customization.md#enabling-and-disabling-resources-provision)**<br/>

```The AI agent uses file search or Azure AI Search to retrieve knowledge from uploaded files.



**🎯 Ready to develop in 1-second code change cycles!**- **[Customizable AI Model Deployment](./docs/deploy_customization.md#customizing-model-deployments)**<br/>

The solution allows users to configure and deploy AI models, such as gpt-4o-mini, with options to adjust model capacity, and knowledge retrieval methods.

## 📖 **Project Overview**

- **[Built-in Monitoring and Tracing](./docs/other_features.md#tracing-and-monitoring)**<br/>

TQFA API V2 is a **hybrid development** FastAPI application that solves the container development complexity problem:Integrated monitoring capabilities, including Azure Monitor and Application Insights, enable tracing and logging for easier troubleshooting and performance optimization.



- **🚀 80% Local Development**: Lightning-fast 1-second code cycles with full debugging- **[Flexible Deployment Options](./docs/deployment.md)**<br/>

- **☁️ 20% Container Deployment**: Azure Container Apps for AI integration and productionThe solution supports deployment through GitHub Codespaces, VS Code Dev Containers, or local environments, providing flexibility for different development workflows.

- **🏗️ Production-Ready Architecture**: Following "NO SHORTCUTS FROM DAY ONE" engineering standards

- **🧠 Azure AI Integration**: Enhanced financial analytics with AI capabilities- **[Agent Evaluation](./docs/other_features.md#agent-evaluation)**<br/>

This solution demonstrates how you can evaluate your agent's performance and quality during local development and incorporate it into monitoring and CI/CD workflow.

### **V2 Success Metrics**

- ✅ **Development Speed**: 1-second cycles (vs 5-10 minute container rebuilds)- **[AI Red Teaming Agent](./docs/other_features.md#ai-red-teaming-agent)**<br/>

- ✅ **Setup Time**: 5 minutes (vs 8+ hours Docker complexity)  Facilitates the creation of an AI Red Teaming Agent that can run batch automated scans for safety and security scans on your Agent solution to check your risk posture before deploying it into production.

- ✅ **Architecture**: Production-ready from first deployment

- ✅ **Debugging**: Full VS Code breakpoint support<br/>



## 🏗️ **Architecture Overview**Here is a screenshot showing the chatting web application with requests and responses between the system and the user:



### **Hybrid Development Strategy**![Screenshot of chatting web application showing requests and responses between agent and the user.](docs/images/webapp_screenshot.png)



```mermaid## Getting Started

graph TB

    subgraph "Local Development (80%)"| [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Azure-Samples/get-started-with-ai-agents) | [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/get-started-with-ai-agents) |

        A[FastAPI Development] --> B[1-Second Cycles]|---|---|

        B --> C[Full Debugging]

        C --> D[Interactive Docs]1. Click `Open in GitHub Codespaces` or `Dev Containers` button above

    end2. Wait for the environment to load

    3. Run the following commands in the terminal:

    subgraph "Container Deployment (20%)"   ```bash

        E[Azure Container Apps] --> F[AI Integration]   azd up

        F --> G[Production Environment]   ```

        G --> H[Blue-Green Deployment]4. Follow the prompts to select your Azure subscription and region

    end5. Wait for deployment to complete (5-20 minutes) - you'll get a web app URL when finished

    

    A --> EFor detailed deployment options and troubleshooting, see the [full deployment guide](./docs/deployment.md).

    style A fill:#00ff00**After deployment, try these [sample questions](./docs/sample_questions.md) to test your agent.**

    style E fill:#0066ff

```## Local Development



### **Current V2 Foundation**For developers who want to run the application locally or customize the agent:



The V2 project currently provides a **working FastAPI foundation** with:- **[Local Development Guide](./docs/local_development.md)** - Set up a local development environment, customize the frontend (starting with AgentPreview.tsx), modify agent instructions and tools, and use evaluation to improve your code.



- **Core API Structure**: Professional FastAPI application with proper middlewareThis guide covers:

- **Health Monitoring**: Comprehensive health check endpoints- Environment setup and prerequisites

- **Version Management**: Automated version tracking and deployment pipeline- Running the development server locally

- **Interactive Documentation**: Auto-generated OpenAPI docs at `/docs`- Frontend customization and backend communication

- **Production Architecture**: Ready for Azure Container Apps deployment- Agent instructions and tools modification

- File management and agent recreation

### **Next Phase: TQFA Business Logic**- Using agent evaluation for code improvement



The current foundation uses placeholder content from "get-started-with-ai-agents" template. The next development phase focuses on adding actual TQFA (Texas Quantitative Financial Analysis) business logic to replace placeholders.

## Resource Clean-up

## 🛠️ **Development Workflow**

To prevent incurring unnecessary charges, it's important to clean up your Azure resources after completing your work with the application.

### **Local Development (Daily Work - 80%)**

- **When to Clean Up:**

Perfect for rapid feature development and debugging:  - After you have finished testing or demonstrating the application.

  - If the application is no longer needed or you have transitioned to a different project or environment.

```bash  - When you have completed development and are ready to decommission the application.

# Start development server with hot reload

uvicorn app.main:app --reload --host localhost --port 8000- **Deleting Resources:**

  To delete all associated resources and shut down the application, execute the following command:

# Development endpoints  

http://localhost:8000           # API information    ```bash

http://localhost:8000/health    # Health status      azd down

http://localhost:8000/docs      # Interactive API docs    ```

http://localhost:8000/redoc     # Alternative documentation

```    Please note that this process may take up to 20 minutes to complete.



**Benefits:**⚠️ Alternatively, you can delete the resource group directly from the Azure Portal to clean up resources.

- ⚡ Instant code changes (1-second cycles)

- 🐛 Full VS Code debugging with breakpoints## Guidance

- 📚 Live interactive documentation

- 🔧 Complete development environment### Costs



### **Container Deployment (Integration - 20%)**Pricing varies per region and usage, so it isn't possible to predict exact costs for your usage.

The majority of the Azure resources used in this infrastructure are on usage-based pricing tiers.

Used for Azure AI integration and production deployment:

You can try the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator) for the resources:

```bash

# MANDATORY: Version bump before deployment- **Azure AI Foundry**: Free tier. [Pricing](https://azure.microsoft.com/pricing/details/ai-studio/)  

python bump_version.py- **Azure Storage Account**: Standard tier, LRS. Pricing is based on storage and operations. [Pricing](https://azure.microsoft.com/pricing/details/storage/blobs/)  

- **Azure AI Services**: S0 tier, defaults to gpt-4o-mini. Pricing is based on token count. [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/)  

# Commit and deploy- **Azure Container App**: Consumption tier with 0.5 CPU, 1GiB memory/storage. Pricing is based on resource allocation, and each month allows for a certain amount of free usage. [Pricing](https://azure.microsoft.com/pricing/details/container-apps/)  

git add .- **Log analytics**: Pay-as-you-go tier. Costs based on data ingested. [Pricing](https://azure.microsoft.com/pricing/details/monitor/)  

git commit -m "Version bump to X.Y.Z - [feature description]"- **Agent Evaluations**: Incurs the cost of your provided model deployment used for local evaluations.  

git push- **AI Red Teaming Agent**: Leverages Azure AI Risk and Safety Evaluations to assess attack success from the automated AI red teaming scan. Users are billed based on the consumption of Risk and Safety Evaluations as listed in [our Azure pricing page](https://azure.microsoft.com/pricing/details/ai-foundry/). Click on the tab labeled “Complete AI Toolchain” to view the pricing details.



# Monitor deployment⚠️ To avoid unnecessary costs, remember to take down your app if it's no longer in use,

gh run list --branch main --limit 3either by deleting the resource group in the Portal or running `azd down`.

gh run watch [RUN_ID]

```### Security guidelines



**When to Use Containers:**This template also uses [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) for local development and deployment.

- 🧠 Azure AI Foundry integration testing

- ☁️ Production deployment validationTo ensure continued best practices in your own repository, we recommend that anyone creating solutions based on our templates ensure that the [Github secret scanning](https://docs.github.com/code-security/secret-scanning/about-secret-scanning) setting is enabled.

- 🔄 End-to-end integration testing

- 📊 Performance testing under loadYou may want to consider additional security measures, such as:



## 📚 **Documentation Links**- Enabling Microsoft Defender for Cloud to [secure your Azure resources](https://learn.microsoft.com/azure/defender-for-cloud/).

- Protecting the Azure Container Apps instance with a [firewall](https://learn.microsoft.com/azure/container-apps/waf-app-gateway) and/or [Virtual Network](https://learn.microsoft.com/azure/container-apps/networking?tabs=workload-profiles-env%2Cazure-cli).

### **🚨 Critical Engineering Standards**

- **[Copilot Instructions](.github/copilot-instructions.md)** - MANDATORY engineering standards and deployment protocols> **Important Security Notice** <br/>

- **[Development Best Practices](TQFA_DEVELOPMENT_BEST_PRACTICES.md)** - Essential principles and quick referenceThis template, the application code and configuration it contains, has been built to showcase Microsoft Azure specific services and tools. We strongly advise our customers not to make this code part of their production environments without implementing or enabling additional security features.  <br/><br/>

For a more comprehensive list of best practices and security recommendations for Intelligent Applications, [visit our official documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/).

### **📋 Project Context & Planning**

- **[V2 Project Context](V2_PROJECT_CONTEXT.md)** - Complete development roadmap and current status### Resources

- **[Architectural Decisions](docs/ARCHITECTURAL_DECISIONS.md)** - Design patterns and technical decisions

This template creates everything you need to get started with Azure AI Foundry:

### **🐳 Deployment & Operations**

- **[Docker Deployment Guide](docs/best-practices/docker-deployment.md)** - Azure Container Apps deployment strategies| Resource | Description |

- **[Azure Container Apps Reality Check](docs/AZURE_CONTAINER_APPS_REALITY_CHECK.md)** - Critical deployment gotchas and solutions|----------|-------------|

- **[Scripts and Tools](docs/best-practices/scripts-and-tools.md)** - Production-ready automation scripts| [Azure AI Project](https://learn.microsoft.com/azure/ai-studio/how-to/create-projects) | Provides a collaborative workspace for AI development with access to models, data, and compute resources |

| [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/) | Powers the AI agents for conversational AI and intelligent search capabilities. Default models deployed are gpt-4o-mini, but any Azure AI models can be specified per the [documentation](docs/deploy_customization.md#customizing-model-deployments) |

### **🔧 Development Guides**| [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/) | Hosts and scales the web application with serverless containers |

- **[Local Development](docs/local_development.md)** - Development environment setup| [Azure Container Registry](https://learn.microsoft.com/azure/container-registry/) | Stores and manages container images for secure deployment |

- **[Troubleshooting Guide](docs/best-practices/troubleshooting.md)** - Common issues and solutions| [Storage Account](https://learn.microsoft.com/azure/storage/blobs/) | Provides blob storage for application data and file uploads |

| [AI Search Service](https://learn.microsoft.com/azure/search/) | *Optional* - Enables hybrid search capabilities combining semantic and vector search |

### **🔗 GitHub Repository Documentation**| [Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview) | *Optional* - Provides application performance monitoring, logging, and telemetry for debugging and optimization |

**Reference**: `https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices`| [Log Analytics Workspace](https://learn.microsoft.com/azure/azure-monitor/logs/log-analytics-workspace-overview) | *Optional* - Collects and analyzes telemetry data for monitoring and troubleshooting |



The project uses modular documentation for easy reference and reuse. All GitHub documentation links point to the main branch for public accessibility.## Troubleshooting



## 🚨 **Engineering Standards References**For solutions to common deployment, container app, and agent issues, see the [Troubleshooting Guide](./docs/troubleshooting.md).



### **NO SHORTCUTS FROM DAY ONE**

## Disclaimers

Following **"Production-Ready From Day One Rule"** from [copilot instructions](.github/copilot-instructions.md):

To the extent that the Software includes components or code used in or derived from Microsoft products or services, including without limitation Microsoft Azure Services (collectively, “Microsoft Products and Services”), you must also comply with the Product Terms applicable to such Microsoft Products and Services. You acknowledge and agree that the license governing the Software does not grant you a license or other right to use Microsoft Products and Services. Nothing in the license or this ReadMe file will serve to supersede, amend, terminate or modify any terms in the Product Terms for any Microsoft Products and Services.

**MANDATORY Before Every Deployment:**

1. ✅ **Health Check Validation**: All deployments must pass comprehensive health checksYou must also comply with all domestic and international export laws and regulations that apply to the Software, which include restrictions on destinations, end users, and end use. For further information on export restrictions, visit <https://aka.ms/exporting>.

2. ✅ **Automated Rollback**: Failed deployments must automatically rollback

3. ✅ **Version Bump**: Execute `python bump_version.py` before every pushYou acknowledge that the Software and Microsoft Products and Services (1) are not designed, intended or made available as a medical device(s), and (2) are not designed or intended to be a substitute for professional medical advice, diagnosis, treatment, or judgment and should not be used to replace or as a substitute for professional medical advice, diagnosis, treatment, or judgment. Customer is solely responsible for displaying and/or obtaining appropriate consents, warnings, disclaimers, and acknowledgements to end users of Customer’s implementation of the Online Services.

4. ✅ **Container Testing**: Test locally before pushing to Azure

5. ✅ **Blue-Green Deployment**: Never switch traffic without validationYou acknowledge the Software is not subject to SOC 1 and SOC 2 compliance audits. No Microsoft technology, nor any of its component technologies, including the Software, is intended or made available as a substitute for the professional advice, opinion, or judgement of a certified financial services professional. Do not use the Software to replace, substitute, or provide professional financial advice or judgment.  



**The "Just Get It Working" Trap - AVOID:**BY ACCESSING OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT THE SOFTWARE IS NOT DESIGNED OR INTENDED TO SUPPORT ANY USE IN WHICH A SERVICE INTERRUPTION, DEFECT, ERROR, OR OTHER FAILURE OF THE SOFTWARE COULD RESULT IN THE DEATH OR SERIOUS BODILY INJURY OF ANY PERSON OR IN PHYSICAL OR ENVIRONMENTAL DAMAGE (COLLECTIVELY, “HIGH-RISK USE”), AND THAT YOU WILL ENSURE THAT, IN THE EVENT OF ANY INTERRUPTION, DEFECT, ERROR, OR OTHER FAILURE OF THE SOFTWARE, THE SAFETY OF PEOPLE, PROPERTY, AND THE ENVIRONMENT ARE NOT REDUCED BELOW A LEVEL THAT IS REASONABLY, APPROPRIATE, AND LEGAL, WHETHER IN GENERAL OR IN A SPECIFIC INDUSTRY. BY ACCESSING THE SOFTWARE, YOU FURTHER ACKNOWLEDGE THAT YOUR HIGH-RISK USE OF THE SOFTWARE IS AT YOUR OWN RISK.

- ❌ "We'll fix deployment later" → Later never comes, debt compounds
- ❌ "Manual processes are fine for now" → Manual doesn't scale, fails at worst times
- ❌ "It works locally, Azure will be fine" → Different environments, assumptions kill deployments

### **Version Management Protocol**

**MANDATORY: Version Bump Before Every Push**

```bash
# 1. Run version bump script
python bump_version.py

# 2. Verify version updated in all files
python setup.py --version

# 3. Commit with version
git add . && git commit -m "Version bump to X.Y.Z - [description]"

# 4. Push to deploy  
git push

# 5. Verify deployment
curl https://your-api-url.com/  # Check version in response
```

**Why This Matters:**
- 📊 **Track Deployments**: Know exactly which version is running
- 🐛 **Debug Issues**: Easily identify problematic releases  
- 🔄 **Avoid Confusion**: Prevent "why isn't my change deployed?" situations
- ⚙️ **Pipeline Reliability**: Unique versions ensure container updates

## 🔌 **API Endpoints Documentation**

### **Current Endpoints (V2 Foundation)**

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/` | GET | API information and version | ✅ Working |
| `/health` | GET | Comprehensive health check | ✅ Working |
| `/api/v2/info` | GET | API version and feature info | ✅ Working |
| `/docs` | GET | Interactive OpenAPI documentation | ✅ Working |
| `/redoc` | GET | Alternative API documentation | ✅ Working |

### **Planned TQFA Endpoints (Next Phase)**

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/api/v2/tqfa/analyze` | GET | Available analysis types | 🎯 Planned |
| `/api/v2/tqfa/models` | GET | Available analysis models | 🎯 Planned |
| `/api/v2/tqfa/calculate` | POST | Financial metrics calculation | 🎯 Planned |
| `/api/v2/tqfa/risk` | POST | Risk analysis endpoint | 🎯 Planned |
| `/api/v2/tqfa/portfolio` | POST | Portfolio optimization | 🎯 Planned |

### **Interactive Documentation**

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both provide complete API exploration, request/response examples, and direct endpoint testing.

## ☁️ **Deployment Information**

### **Azure Container Apps Deployment**

**Current Deployment Pattern:**
- **Environment**: Azure Container Apps (East US 2)
- **Deployment Trigger**: Git push to main branch
- **Container Registry**: Azure Container Registry (ACR)
- **Traffic Management**: Blue-green deployment with manual promotion

**Deployment Pipeline:**
1. **Version Bump**: `python bump_version.py` creates unique container tags
2. **GitHub Actions**: Builds and pushes container to ACR
3. **Container Apps**: Deploys new revision with 0% traffic
4. **Health Checks**: Validates application health
5. **Traffic Promotion**: Manual promotion routes 100% traffic to new version

### **Environment URLs**

**Production**: `https://tqfaapi-prod.azurecontainerapps.io`  
**UAT**: `https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io`  
**Development**: `http://localhost:8000`

### **Version Tracking**

All environments display current version at root endpoint:
```json
{
  "service": "TQFA API V2",
  "version": "2.0.0",
  "environment": "production",
  "timestamp": "2025-09-29T22:36:05Z"
}
```

### **Monitoring & Health Checks**

**Health Check Endpoint**: `/health`
```json
{
  "status": "healthy", 
  "version": "2.0.0",
  "service": "TQFA API V2",
  "timestamp": "2025-09-29T22:36:05Z",
  "environment": "production"
}
```

**GitHub CLI Monitoring:**
```bash
# Check deployment status
gh run list --branch main --limit 5

# Watch deployment in real-time
gh run watch [RUN_ID]

# Verify endpoint version
curl https://your-api-url.com/
```

## 💻 **Development Environment Setup**

### **Prerequisites**
- **Python 3.13+** (Required)
- **Git** (For version control)
- **VS Code** (Recommended IDE)
- **Azure CLI** (For deployment)
- **GitHub CLI** (For monitoring)

### **Local Setup**

```bash
# 1. Clone repository
git clone https://github.com/Texas-Quantitative/tqfaAPI-v2.git
cd tqfaAPI-v2

# 2. Install Python dependencies
pip install -r src/requirements.txt

# 3. Start development server
uvicorn app.main:app --reload --host localhost --port 8000

# 4. Verify installation
curl http://localhost:8000/health
```

### **VS Code Setup**

**Recommended Extensions:**
- **Python**: Official Python extension
- **FastAPI**: FastAPI language support  
- **Azure Tools**: Azure integration
- **GitHub Copilot**: AI-powered development

**Debug Configuration** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "python", 
            "request": "launch",
            "program": "-m",
            "args": ["uvicorn", "app.main:app", "--reload"],
            "console": "integratedTerminal"
        }
    ]
}
```

### **Environment Variables**

Create `.env` file for local development:
```env
ENVIRONMENT=local
API_VERSION=2.0.0
DEBUG=true
```

**Production variables** are managed through Azure Key Vault and Container Apps environment settings.

## 🤝 **Contributing Guidelines**

### **Development Process**

1. **Follow Engineering Standards**: Reference [copilot instructions](.github/copilot-instructions.md)
2. **Local Development First**: Build and test features locally
3. **Version Management**: Always bump version before deployment  
4. **Documentation**: Update relevant docs with changes
5. **Code Quality**: Use type hints, Pydantic models, proper error handling

### **Code Standards**

```python
# ✅ Good: Type hints and Pydantic validation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    data: List[float]
    analysis_type: str
    parameters: Optional[dict] = None

@app.post("/api/v2/analyze")
async def analyze_data(request: AnalysisRequest) -> dict:
    """Analyze financial data with proper validation."""
    if not request.data:
        raise HTTPException(status_code=400, detail="Data is required")
    
    # Implementation here
    return {"status": "success", "version": "2.0.0"}
```

### **Pull Request Process**

1. **Create Feature Branch**: `git checkout -b feature/your-feature`
2. **Develop Locally**: Use 1-second development cycles
3. **Version Bump**: Run `python bump_version.py` 
4. **Test Endpoints**: Verify all functionality works
5. **Update Documentation**: Include any API changes
6. **Submit PR**: Include clear description and testing notes

### **Engineering Standards Compliance**

**MANDATORY Checklist:**
- [ ] Version bumped before deployment
- [ ] All endpoints include health checks
- [ ] Pydantic models for request/response validation
- [ ] Proper HTTP status codes and error messages  
- [ ] Type hints on all functions
- [ ] Documentation updated
- [ ] Local testing completed

---

## 📊 **Current Project Status**

### **✅ Completed (V2 Foundation)**
- **Working FastAPI Application**: Professional structure with proper middleware
- **Development Environment**: 1-second code change cycles  
- **Version Management System**: Automated version tracking
- **Health Check Infrastructure**: Comprehensive monitoring endpoints
- **Documentation Structure**: Complete project documentation
- **Deployment Pipeline**: Azure Container Apps integration ready

### **🎯 Next Phase: TQFA Business Logic**
- **Financial Analysis Endpoints**: Risk analysis, portfolio optimization
- **Data Models**: Pydantic schemas for financial operations
- **Business Logic Services**: Core TQFA calculation algorithms  
- **Azure AI Integration**: Enhanced analytics with AI capabilities
- **Authentication**: API security and rate limiting

### **🚀 Ready for Development**
The V2 foundation is **production-ready** and optimized for rapid development. The hybrid architecture solves container complexity while maintaining deployment flexibility. Next phase focuses on building actual TQFA functionality to replace template placeholders.

---

**🔗 Documentation Repository**: https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs/best-practices

**📧 Questions?** Reference the [copilot instructions](.github/copilot-instructions.md) for engineering standards and development protocols.