# 🎯 **Agent Handoff: TQFA V2 Phase 0.1 Implementation**

**Project**: TQFA V2 Quantitative Financial Analysis Platform  
**Current Phase**: Phase 0.1 - Foundation Enhancement (LLM Document Processing Fix)  
**Repository**: `tqfaAPI-v2` (main branch)  
**Workspace**: `d:\Users\dstac\TQSource\tqfa-api-v2`  

## **🚨 CRITICAL: Read This First**
1. **Primary Guide**: Read `TQFA_V2_ITERATIVE_IMPLEMENTATION_STRATEGY.md` completely - this is your implementation roadmap
2. **Engineering Standards**: Review `.github/copilot-instructions.md` for mandatory engineering practices
3. **Current System**: The Azure AI Agent at `https://ca-api-ffynnnmt4ywus.agreeablemushroom-547b53f8.eastus2.azurecontainerapps.io/` is your enhancement target

## **🎯 Your Mission: Phase 0.1 - Text File Processing Fix**

**Problem**: The current LLM doesn't properly consider uploaded .txt files when answering questions. Users upload documents but the system relies on general knowledge instead of document content.

**Example Issue**: User uploads "txtland_guide.txt" containing "The sky in TXTLand is yellow" but when asked "What color is the sky in TXTLand?" the LLM responds with general knowledge about blue skies instead of finding the document content.

**Your Goal**: Fix the LLM so it ALWAYS searches uploaded documents FIRST before using general knowledge.

## **📋 Specific Tasks for Phase 0.1**

### **Task 1: Analyze Current Document Search Behavior**
```bash
# Examine the current agent instructions and search logic
grep -r "search" src/api/ --include="*.py"
grep -r "document" src/api/ --include="*.py" 
```

### **Task 2: Implement Enhanced Agent Instructions**
The strategy document provides the exact enhanced instructions template in Phase 0 Step 0.2. Update the agent instructions to include:
- MANDATORY DOCUMENT SEARCH PROTOCOL
- Multi-query search strategies  
- Confidence reporting requirements
- Explicit document source reporting

### **Task 3: Create Unit Testing Framework**
Following the strategy document Phase 0 Step 0.3:
- Create automated tests for document processing accuracy
- Implement the mock endpoint protocol (🚨 MOCK ENDPOINT warnings)
- Test the "yellow sky TXTLand" scenario specifically

### **Task 4: Validate Document-First Search**
**Success Criteria**: 
- Upload a .txt file with specific facts
- Ask questions that can ONLY be answered from the document
- LLM should find document content 95%+ of the time
- LLM should explicitly state which document it searched

## **🔧 Technical Implementation Guidance**

### **Files to Focus On**:
```
src/api/main.py          # Agent configuration and instructions
src/api/routes.py        # Chat endpoints and document processing  
src/api/agents.py        # Agent behavior logic (if exists)
tests/                   # Create unit tests here
```

### **Key Code Pattern from Strategy Document**:
```python
# Enhanced instructions template is in the strategy document
enhanced_instructions = """
MANDATORY DOCUMENT SEARCH PROTOCOL:
1. ALWAYS search uploaded documents FIRST before using general knowledge
2. Use multiple search query variations if initial search fails
...
"""
```

## **🧪 Testing Protocol**

### **Create This Test Case**:
1. Upload test file `txtland_guide.txt` with content: "The sky in TXTLand appears yellow due to atmospheric particles."
2. Ask: "What color is the sky in TXTLand?"
3. **Expected Response**: "Found in document 'txtland_guide.txt': 'The sky in TXTLand appears yellow...'"
4. **Current Broken Response**: "The sky is typically blue due to Rayleigh scattering..."

### **Unit Test Requirements**:
```python
def test_document_first_search():
    """Test that LLM searches documents before general knowledge"""
    # Upload test document with unique facts
    # Query facts that exist ONLY in the document  
    # Verify document content is found and cited
    assert "Found in document" in response
    assert "txtland_guide.txt" in response
```

## **📊 Success Metrics for Phase 0.1**
- **Technical**: Document search accuracy ≥95% on test cases
- **User**: Can reliably get answers from uploaded .txt files  
- **Business**: Foundation validated for enhanced document processing

## **🚀 After Phase 0.1 Completion**
Once you've fixed the document search issue:
1. **Commit your changes** with descriptive messages
2. **Run the deployment** to test on UAT environment
3. **Document any issues** you discovered and fixed
4. **Prepare for Phase 0.5** (PDF and CSV processing) using the strategy guide

## **💡 Key Resources**

### **Strategy Document Sections**:
- **Phase 0 Implementation**: Detailed steps for foundation enhancement
- **Technical Guidelines**: Code examples and patterns to follow
- **Testing Framework**: Unit test requirements and mock protocols
- **Architecture Overview**: Understanding the overall system design

### **Current System Context**:
- **Deployed System**: Azure AI Agent with React frontend
- **Base Technology**: Azure Container Apps + Azure AI Project  
- **Document Processing**: Currently basic, needs enhancement
- **Your Enhancement**: Make it actually use uploaded documents

## **🔄 Agent Handoff Protocol**
When you complete Phase 0.1:
1. **Update the strategy document** if you discover architectural changes needed
2. **Create handoff prompt** for Phase 0.5 agent (PDF/CSV processing)
3. **Document lessons learned** for future phases

---

**Ready to start? Begin by reading `TQFA_V2_ITERATIVE_IMPLEMENTATION_STRATEGY.md` and then dive into analyzing the current document search behavior in `src/api/`.**

**Remember**: The goal is to make the LLM find "yellow sky in TXTLand" from uploaded documents instead of defaulting to "blue sky" general knowledge. This seemingly simple fix is the foundation for all advanced document processing in future phases.

---

## **📋 Quick Copy Instructions for New Agent**

**For New Chat Window:**
```
I need to continue TQFA V2 development. I'm in the tqfaAPI-v2 workspace. Please read the file AGENT_HANDOFF_PHASE_0_1.md in the root directory - this contains my complete mission for Phase 0.1 (fixing LLM document processing). After reading that file, confirm you understand the task and begin with analyzing current document search behavior.
```

**For Same Agent (if needed):**
```
Please read AGENT_HANDOFF_PHASE_0_1.md and begin implementing Phase 0.1 - fixing the LLM document processing issue where it ignores uploaded .txt files.
```