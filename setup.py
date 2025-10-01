"""
Setup configuration for TQFA API V2 - Azure AI Foundry Integration
Following Copilot Instructions: Production-Ready From Day One
"""
from setuptools import setup, find_packages
from pathlib import Path
import re

# Read the current version from app/main.py (primary source)
def get_version():
    """
    Extract version from FastAPI app/main.py.
    Following Copilot Instructions: ALWAYS include version in root endpoint.
    """
    main_py_path = Path(__file__).parent / "app" / "main.py"
    
    if main_py_path.exists():
        content = main_py_path.read_text(encoding='utf-8')
        
        # Look for FastAPI version patterns
        patterns = [
            r'version\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']',
            r'__version__\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
    
    # Fallback to V2 base version
    return "2.0.0"

# Read requirements from requirements.txt if it exists
def get_requirements():
    """Get requirements from requirements.txt or define minimal set."""
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as fh:
            return [
                line.strip() 
                for line in fh 
                if line.strip() and not line.startswith("#")
            ]
    else:
        # Minimal requirements for V2 if requirements.txt doesn't exist
        return [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.5.0",
            "python-multipart>=0.0.6",
            "email-validator>=2.1.0"
        ]

# Read long description from README if it exists
def get_long_description():
    """Get long description from README file."""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return "TQFA API V2 - Texas Quantitative Financial Analysis API with Azure AI Foundry Integration"

setup(
    name="tqfa-api-v2",
    version=get_version(),
    author="Texas Quantitative Financial Analysis Team",
    author_email="dev@texasquantitative.com",
    description="TQFA API V2 - Texas Quantitative Financial Analysis API with Azure AI Foundry Integration",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Texas-Quantitative/tqfaAPI",
    project_urls={
        "Documentation": "https://github.com/Texas-Quantitative/tqfaAPI/tree/main/docs",
        "Source": "https://github.com/Texas-Quantitative/tqfaAPI",
        "Tracker": "https://github.com/Texas-Quantitative/tqfaAPI/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial Services",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: FastAPI",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0",
            "black>=23.9.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
        "azure": [
            "azure-identity>=1.15.0",
            "azure-keyvault-secrets>=4.7.0",
            "azure-storage-blob>=12.19.0",
            "azure-ai-formrecognizer>=3.3.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "uvicorn[standard]>=0.24.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "tqfa-api-v2=app.main:main",
            "start-tqfa-v2=app.main:start_server",
        ],
    },
    include_package_data=True,
    package_data={
        "app": ["*.json", "*.yaml", "*.yml"],
    },
    keywords=[
        "fastapi",
        "financial-analysis", 
        "quantitative-finance",
        "azure-ai",
        "api",
        "texas-quantitative",
        "tqfa"
    ],
    zip_safe=False,
)