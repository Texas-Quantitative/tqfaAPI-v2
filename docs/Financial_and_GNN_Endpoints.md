# Financial Instruments & GNN Processing API Guide

This guide explains how to use the new financial instrument processing and Graph Neural Network (GNN) enhanced endpoints in tqfaAPI.

## Table of Contents

1. [Overview](#overview)
2. [Financial Instrument Processing](#financial-instrument-processing)
3. [Enhanced File Upload with GNN](#enhanced-file-upload-with-gnn)
4. [GNN-Enhanced LLM Interactions](#gnn-enhanced-llm-interactions)
5. [Portfolio Analysis](#portfolio-analysis)
6. [Request Examples](#request-examples)
7. [Response Schemas](#response-schemas)

## Overview

The tqfaAPI now supports advanced financial instrument processing with integrated Graph Neural Network capabilities. These features enable:

- Processing various financial instruments (options, swaps, futures, etc.)
- Automatic GNN representation generation from uploaded files
- Enhanced LLM queries using graph-based context
- Portfolio-level scenario analysis
- Risk assessment with AI-driven insights

## Financial Instrument Processing

### Base URL
All financial endpoints are prefixed with `/financial`

### Supported Instrument Types

- `confirm` - Trade confirmations
- `term_sheet` - Term sheets and prospectuses
- `option` - Options contracts
- `swap` - Swap agreements
- `swaption` - Swaption contracts
- `future` - Futures contracts
- `forward` - Forward agreements
- `repo` - Repurchase agreements
- `public_equity` - Public equity instruments

### Endpoints

#### 1. Process Single Instrument
**POST** `/financial/instruments/process`

Process a single financial instrument and generate GNN representation.

```http
POST /financial/instruments/process
Content-Type: application/json

{
  "instrument_type": "option",
  "identifier": "AAPL_240315_C_150",
  "counterparty": "Goldman Sachs",
  "trade_date": "2024-03-01",
  "settlement_date": "2024-03-03",
  "notional": 1000000.0,
  "currency": "USD",
  "raw_data": {
    "option_type": "call",
    "strike": 150.0,
    "expiry": "2024-03-15",
    "underlying": "AAPL",
    "premium": 5.50,
    "quantity": 100
  },
  "parse_gnn": true
}
```

#### 2. Batch Process Instruments
**POST** `/financial/instruments/batch-process`

Process multiple instruments concurrently.

```http
POST /financial/instruments/batch-process
Content-Type: application/json

[
  {
    "instrument_type": "option",
    "identifier": "AAPL_240315_C_150",
    "raw_data": { /* option data */ },
    "parse_gnn": true
  },
  {
    "instrument_type": "swap",
    "identifier": "USD_LIBOR_5Y_SWAP",
    "raw_data": { /* swap data */ },
    "parse_gnn": true
  }
]
```

#### 3. Portfolio Scenario Analysis
**POST** `/financial/portfolio/scenario-analysis`

Perform portfolio-level scenario analysis for liquid markets.

```http
POST /financial/portfolio/scenario-analysis
Content-Type: application/json

{
  "portfolio_id": "PORTFOLIO_001",
  "instrument_ids": ["AAPL_240315_C_150", "USD_LIBOR_5Y_SWAP"],
  "scenario_type": "stress_test",
  "parameters": {
    "rate_change": 0.01,
    "vol_change": 0.05,
    "corr_change": 0.1,
    "confidence_level": 0.95
  }
}
```

#### 4. Get Supported Types
**GET** `/financial/instruments/types` - Get list of supported instrument types
**GET** `/financial/risk/types` - Get list of supported risk measurement types

## Enhanced File Upload with GNN

### Enhanced Upload Endpoint
**POST** `/files/upload-enhanced`

Upload files with automatic GNN processing and entity extraction.

```http
POST /files/upload-enhanced
Content-Type: multipart/form-data

file: [binary file data]
user_id: user123
password: userpassword
workspace_id: portfolio_workspace (optional)
enable_gnn: true (optional, default: true)
```

### Supported File Types for GNN Processing

- **Text files** (.txt, .csv) - Direct text analysis and entity extraction
- **JSON files** (.json) - Structure analysis and relationship mapping
- **Documents** (.pdf, .docx, .doc) - OCR and content parsing
- **Spreadsheets** (.xlsx, .xls) - Data structure analysis
- **HTML/XML** - Markup structure analysis

### GNN Processing Features

The enhanced upload automatically:

1. **Parses file content** based on file type
2. **Extracts entities** (financial terms, numerical values, relationships)
3. **Generates graph structure** with nodes and edges
4. **Creates GNN representation** suitable for machine learning
5. **Provides metadata** about graph complexity and features

## GNN-Enhanced LLM Interactions

### Enhanced LLM Interaction
**POST** `/llm/interact-gnn`

Query LLM with enhanced context from GNN representations.

```http
POST /llm/interact-gnn
Content-Type: application/json

{
  "user_id": "user123",
  "password": "userpassword",
  "workspace_id": "portfolio_workspace",
  "query": "What are the key risks in my portfolio based on the uploaded documents?",
  "include_gnn_context": true,
  "gnn_focus_areas": ["financial", "numerical"],
  "analysis_type": "risk"
}
```

### Financial Analysis with AI
**POST** `/llm/financial-analysis`

Comprehensive financial analysis combining GNN and LLM capabilities.

```http
POST /llm/financial-analysis
Content-Type: application/json

{
  "user_id": "user123",
  "password": "userpassword",
  "workspace_id": "portfolio_workspace",
  "analysis_type": "portfolio_risk",
  "parameters": {
    "confidence_level": 0.95,
    "time_horizon": "1d",
    "stress_scenarios": ["rates_up", "vol_up", "credit_spread"]
  },
  "include_llm_interpretation": true
}
```

### Analysis Types

- **`portfolio_risk`** - Portfolio-level risk assessment
- **`instrument_analysis`** - Individual instrument analysis
- **`scenario`** - Scenario analysis and stress testing

## Request Examples

### Complete Workflow Example

1. **Upload a financial document with GNN processing:**

```bash
curl -X POST "http://localhost:8000/files/upload-enhanced" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@portfolio_report.pdf" \
  -F "user_id=trader123" \
  -F "password=secure_password" \
  -F "workspace_id=trading_desk" \
  -F "enable_gnn=true"
```

2. **Process financial instruments:**

```bash
curl -X POST "http://localhost:8000/financial/instruments/process" \
  -H "Content-Type: application/json" \
  -d '{
    "instrument_type": "option",
    "identifier": "SPY_240320_C_500",
    "raw_data": {
      "option_type": "call",
      "strike": 500.0,
      "expiry": "2024-03-20",
      "underlying": "SPY"
    },
    "parse_gnn": true
  }'
```

3. **Get AI analysis with GNN context:**

```bash
curl -X POST "http://localhost:8000/llm/interact-gnn" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "trader123",
    "password": "secure_password",
    "workspace_id": "trading_desk",
    "query": "Analyze the risk profile of my uploaded portfolio and suggest hedging strategies",
    "include_gnn_context": true,
    "analysis_type": "risk"
  }'
```

4. **Run portfolio scenario analysis:**

```bash
curl -X POST "http://localhost:8000/financial/portfolio/scenario-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": "DESK_001",
    "instrument_ids": ["SPY_240320_C_500"],
    "scenario_type": "stress_test",
    "parameters": {
      "rate_change": 0.005,
      "vol_change": 0.02
    }
  }'
```

## Response Schemas

### Financial Instrument Processing Response

```json
{
  "instrument_id": "SPY_240320_C_500",
  "instrument_type": "option",
  "processed_data": {
    "instrument_type": "option",
    "option_type": "call",
    "strike": 500.0,
    "expiry": "2024-03-20",
    "underlying": "SPY",
    "processed_timestamp": "2024-03-01T10:30:00Z"
  },
  "gnn_representation": {
    "graph_id": "abc123",
    "nodes": [
      {
        "id": "instrument",
        "type": "option",
        "features": [500.0, 1.0, 0.5]
      }
    ],
    "edges": [
      {
        "source": "instrument",
        "target": "underlying",
        "type": "depends_on",
        "weight": 1.0
      }
    ],
    "graph_properties": {
      "node_count": 3,
      "edge_count": 2,
      "complexity_score": 5
    }
  },
  "risk_metrics": {
    "delta": 0.5,
    "gamma": 0.02,
    "vega": 15.5,
    "theta": -0.05,
    "var_1d": 12500.0
  },
  "processing_timestamp": "2024-03-01T10:30:00Z",
  "status": "processed"
}
```

### Enhanced File Upload Response

```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file_name": "portfolio_report.pdf",
  "workspace_id": "trading_desk",
  "file_size": 1048576,
  "upload_timestamp": "2024-03-01T10:30:00Z",
  "gnn_processing": {
    "processing_id": "gnn_abc123",
    "filename": "portfolio_report.pdf",
    "file_type": "pdf",
    "processed_timestamp": "2024-03-01T10:30:05Z",
    "content_summary": {
      "file_type": "pdf",
      "content_indicators": {
        "requires_ocr": true,
        "estimated_pages": 25
      }
    },
    "gnn_representation": {
      "graph_id": "def456",
      "nodes": [
        {
          "id": "file_xyz",
          "type": "file",
          "properties": {
            "filename": "portfolio_report.pdf",
            "file_type": "pdf"
          }
        }
      ],
      "entities": [
        {
          "text": "option",
          "type": "financial",
          "confidence": 0.9
        }
      ]
    }
  }
}
```

### GNN-Enhanced LLM Response

```json
{
  "response": "Based on the GNN analysis of your portfolio documents, I've identified several key risks...",
  "gnn_insights": {
    "total_graphs": 3,
    "total_nodes": 45,
    "total_edges": 67,
    "entity_types": ["financial_instrument", "counterparty", "risk_metric"],
    "complexity_score": 0.73
  },
  "workspace_files_analyzed": ["portfolio_report.pdf", "risk_metrics.xlsx"],
  "prompt_tokens_used": 1250,
  "completion_tokens_used": 800,
  "total_tokens_used": 2050,
  "model": "gpt-4",
  "workspace_id": "trading_desk",
  "timestamp": "2024-03-01T10:35:00Z",
  "gnn_processing_time": 2.5
}
```

### Portfolio Scenario Analysis Response

```json
{
  "portfolio_id": "DESK_001",
  "scenario_results": {
    "base_case": {
      "portfolio_value": 10000000.0,
      "var": 250000.0
    },
    "stressed_case": {
      "portfolio_value": 9750000.0,
      "var": 375000.0
    },
    "scenario_type": "stress_test",
    "parameters_applied": {
      "rate_change": 0.005,
      "vol_change": 0.02
    }
  },
  "risk_summary": {
    "total_var": 375000.0,
    "marginal_var": 125000.0,
    "concentration_risk": 0.15,
    "correlation_risk": 0.08
  },
  "impact_analysis": {
    "rate_sensitivity": 500000.0,
    "volatility_impact": 100000.0,
    "correlation_impact": 25000.0
  },
  "confidence_level": 0.95,
  "timestamp": "2024-03-01T10:40:00Z"
}
```

### Financial Analysis Response

```json
{
  "analysis_results": {
    "portfolio_var": 250000.0,
    "expected_shortfall": 375000.0,
    "risk_metrics": {
      "total_exposure": 10000000.0,
      "diversification_ratio": 0.73
    },
    "confidence_score": 0.85
  },
  "llm_interpretation": "The portfolio shows moderate risk concentration in technology sector options...",
  "gnn_graph_summary": {
    "total_graphs": 3,
    "complexity_score": 0.73
  },
  "risk_metrics": {
    "portfolio_var": 250000.0,
    "concentration_risk": 0.15
  },
  "recommendations": [
    "Consider hedging strategies for high-risk instruments",
    "Review portfolio diversification metrics quarterly",
    "Monitor correlation patterns between major positions"
  ],
  "confidence_score": 0.85,
  "timestamp": "2024-03-01T10:45:00Z"
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- **200** - Success
- **201** - Created (for uploads)
- **400** - Bad Request (invalid parameters)
- **401** - Unauthorized (invalid credentials)
- **500** - Internal Server Error

Error responses include details:

```json
{
  "detail": "Failed to process instrument: Invalid option type"
}
```

## Best Practices

1. **File Upload**: Enable GNN processing for documents containing financial data
2. **Batch Processing**: Use batch endpoints for multiple instruments to improve performance
3. **GNN Context**: Include GNN context in LLM queries for enhanced insights
4. **Workspace Organization**: Use meaningful workspace IDs to organize related documents
5. **Risk Analysis**: Combine instrument processing with portfolio analysis for comprehensive risk assessment

## Integration Examples

### Python Client Example

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
USER_ID = "trader123"
PASSWORD = "secure_password"
WORKSPACE_ID = "trading_desk"

# Upload file with GNN processing
def upload_file_with_gnn(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'user_id': USER_ID,
            'password': PASSWORD,
            'workspace_id': WORKSPACE_ID,
            'enable_gnn': True
        }
        response = requests.post(f"{BASE_URL}/files/upload-enhanced", 
                               files=files, data=data)
    return response.json()

# Process financial instrument
def process_instrument(instrument_data):
    response = requests.post(f"{BASE_URL}/financial/instruments/process",
                           json=instrument_data)
    return response.json()

# Get AI analysis
def get_ai_analysis(query):
    data = {
        "user_id": USER_ID,
        "password": PASSWORD,
        "workspace_id": WORKSPACE_ID,
        "query": query,
        "include_gnn_context": True,
        "analysis_type": "risk"
    }
    response = requests.post(f"{BASE_URL}/llm/interact-gnn", json=data)
    return response.json()

# Example workflow
upload_result = upload_file_with_gnn("portfolio.pdf")
print("Upload result:", upload_result)

instrument_result = process_instrument({
    "instrument_type": "option",
    "identifier": "SPY_240320_C_500",
    "raw_data": {"option_type": "call", "strike": 500.0},
    "parse_gnn": True
})
print("Instrument processing:", instrument_result)

analysis = get_ai_analysis("What are the main risks in my portfolio?")
print("AI Analysis:", analysis["response"])
```

This completes the comprehensive guide for using the new financial and GNN endpoints in tqfaAPI.
