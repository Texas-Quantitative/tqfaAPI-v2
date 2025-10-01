# Essential Scripts & Tools

*Production-ready scripts for FastAPI deployment and management*

**Last Modified**: September 27, 2025  
**Version**: 1.0

---

## 🚀 **Deployment Scripts**

### **1. Version Bump Script (`bump_version.py`)**

Automatically updates version numbers across all project files:

```python
#!/usr/bin/env python3
"""
Version Bump Utility for TQFA API

Automatically increments patch version and updates:
- app/main.py (FastAPI version)
- pyproject.toml (package version) 
- setup.py (package version)

Usage: python bump_version.py
"""

import re
from pathlib import Path

def bump_patch_version(version_string):
    """Increment patch version (X.Y.Z -> X.Y.Z+1)"""
    major, minor, patch = version_string.split('.')
    return f"{major}.{minor}.{int(patch) + 1}"

def update_file_version(file_path, version_pattern, new_version):
    """Update version in a file using regex pattern"""
    if not file_path.exists():
        print(f"📋 File not found: {file_path}")
        return 0
    
    content = file_path.read_text(encoding='utf-8')
    updated_content, count = re.subn(version_pattern, f'version="{new_version}"', content)
    
    if count > 0:
        file_path.write_text(updated_content, encoding='utf-8')
        print(f"✅ Updated {file_path} ({count} changes)")
    else:
        print(f"📋 No changes needed in {file_path}")
    
    return count

def main():
    print("🔢 Version Bump Utility")
    print("=" * 30)
    
    # Extract current version from main.py
    main_py = Path("app/main.py")
    current_version = extract_current_version(main_py)
    new_version = bump_patch_version(current_version)
    
    print(f"📋 Current version: {current_version}")
    print(f"🚀 New version: {new_version}")
    
    # Update all files
    files_updated = 0
    files_updated += update_file_version(main_py, r'version\s*=\s*["\'][^"\']+["\']', new_version)
    files_updated += update_file_version(Path("pyproject.toml"), r'version\s*=\s*["\'][^"\']+["\']', new_version)
    files_updated += update_file_version(Path("setup.py"), r'version\s*=\s*["\'][^"\']+["\']', new_version)
    
    if files_updated > 0:
        print(f"\n🎯 Successfully bumped version from {current_version} to {new_version}")
        print(f"📁 Updated {files_updated} file(s)")
        print("\n💡 Next steps:")
        print("   git add .")
        print(f'   git commit -m "Version bump to {new_version}"')
        print("   git push")
    else:
        print("\n❌ No files were updated. Check version patterns.")

if __name__ == "__main__":
    main()
```

### **2. Traffic Promotion Script (`promote_healthy_revision.py`)**

Fixes Azure Container Apps' idiotic default behavior:

```python
#!/usr/bin/env python3
"""
Azure Container Apps Traffic Promotion Script

Automatically promotes the latest healthy revision to receive 100% traffic.
This fixes Azure's insane default behavior of keeping healthy revisions at 0% traffic.

Usage: python promote_healthy_revision.py
"""

import subprocess
import json
import sys
from datetime import datetime

def run_command(command):
    """Run Azure CLI command and return JSON result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON from: {command}")
        return None

def promote_latest_healthy_revision(app_name, resource_group):
    """Find the latest healthy revision and promote it to 100% traffic."""
    print(f"🔍 Checking revisions for {app_name}...")
    
    revisions = run_command(f"az containerapp revision list --name {app_name} --resource-group {resource_group}")
    if not revisions:
        return False
    
    # Find healthy revisions sorted by creation time (latest first)
    healthy_revisions = [
        r for r in revisions 
        if r.get('properties', {}).get('healthState') == 'Healthy'
    ]
    
    if not healthy_revisions:
        print("❌ No healthy revisions found!")
        return False
    
    healthy_revisions.sort(
        key=lambda x: x.get('properties', {}).get('createdTime', ''), 
        reverse=True
    )
    
    latest_healthy = healthy_revisions[0]
    revision_name = latest_healthy['name']
    current_traffic = latest_healthy.get('properties', {}).get('trafficWeight', 0)
    
    print(f"📊 Latest healthy revision: {revision_name}")
    print(f"📊 Current traffic weight: {current_traffic}%")
    
    if current_traffic == 100:
        print("✅ Latest healthy revision already has 100% traffic")
        return True
    
    print(f"🚀 Promoting {revision_name} to 100% traffic...")
    
    result = run_command(f"az containerapp ingress traffic set --name {app_name} --resource-group {resource_group} --revision-weight {revision_name}=100")
    
    if result:
        print(f"✅ Successfully promoted {revision_name} to 100% traffic!")
        return True
    else:
        print(f"❌ Failed to promote {revision_name}")
        return False

def main():
    """Main function for UAT environment."""
    app_name = "tqfaapi-uat"
    resource_group = "tqfa-uat-rg"
    
    print("🚀 Azure Container Apps Traffic Promotion Tool")
    print("=" * 50)
    print(f"App: {app_name}")
    print(f"Resource Group: {resource_group}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = promote_latest_healthy_revision(app_name, resource_group)
    
    if success:
        print("\n🎉 Traffic promotion completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Traffic promotion failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### **3. Deployment Health Check (`check_deployment.py`)**

Validates that deployments are working correctly:

```python
#!/usr/bin/env python3
"""
Deployment Health Check Script

Validates that the deployed application is healthy and serving the expected version.
"""

import requests
import sys
import json
from datetime import datetime

def check_endpoint_health(url, timeout=10):
    """Check if an endpoint is responding and healthy."""
    try:
        response = requests.get(f"{url}/health/", timeout=timeout)
        
        if response.status_code == 200:
            health_data = response.json()
            return True, health_data
        else:
            return False, f"HTTP {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return False, str(e)

def check_app_version(url, timeout=10):
    """Get the current application version."""
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            app_data = response.json()
            return app_data.get('version', 'unknown')
        else:
            return f"HTTP {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    """Check UAT deployment health."""
    base_url = "https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io"
    
    print("🏥 Deployment Health Check")
    print("=" * 30)
    print(f"URL: {base_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check health endpoint
    print("🔍 Checking health endpoint...")
    is_healthy, health_info = check_endpoint_health(base_url)
    
    if is_healthy:
        print("✅ Health check passed")
        print(f"📊 Status: {health_info.get('status', 'unknown')}")
        
        checks = health_info.get('checks', {})
        if checks:
            for check_name, check_info in checks.items():
                status = check_info.get('status', 'unknown')
                emoji = "✅" if status == 'healthy' else "❌"
                print(f"{emoji} {check_name}: {status}")
    else:
        print(f"❌ Health check failed: {health_info}")
        sys.exit(1)
    
    # Check application version
    print("\n🔍 Checking application version...")
    version = check_app_version(base_url)
    print(f"📋 Current version: {version}")
    
    print("\n🎉 Deployment health check completed successfully!")

if __name__ == "__main__":
    main()
```

---

## 🛠️ **Development Tools**

### **4. Local Development Server (`run_local.py`)**

Starts the development server with proper configuration:

```python
#!/usr/bin/env python3
"""
Local Development Server

Starts FastAPI with proper development configuration.
"""

import uvicorn
import os
from pathlib import Path

def main():
    """Start development server."""
    
    # Ensure we're in the right directory
    if not Path("app/main.py").exists():
        print("❌ Run this script from the project root directory")
        return
    
    print("🚀 Starting TQFA API development server...")
    print("📋 Environment: development")
    print("🌐 URL: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print()
    
    # Set development environment
    os.environ['ENVIRONMENT'] = 'development'
    
    # Start server with hot reload
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
```

### **5. Container Testing Script (`test_container_locally.py`)**

Tests Docker container before Azure deployment:

```bash
#!/bin/bash
# test_container_locally.sh
# Tests Docker container locally before deploying to Azure

set -e

echo "🐳 Local Container Testing"
echo "========================="

# Build container
echo "🔨 Building container..."
docker build -t tqfaapi-test .

# Stop any existing container
echo "🛑 Stopping existing containers..."
docker stop tqfaapi-test-container 2>/dev/null || true
docker rm tqfaapi-test-container 2>/dev/null || true

# Run container
echo "🚀 Starting container..."
docker run -d --name tqfaapi-test-container -p 8001:8000 tqfaapi-test

# Wait for startup
echo "⏳ Waiting for container to start..."
sleep 10

# Test health endpoint
echo "🏥 Testing health endpoint..."
if curl -f http://localhost:8001/health/ > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    echo "📋 Container logs:"
    docker logs tqfaapi-test-container
    exit 1
fi

# Test main endpoint
echo "🔍 Testing main endpoint..."
VERSION=$(curl -s http://localhost:8001/ | python3 -c "import sys, json; print(json.load(sys.stdin).get('version', 'unknown'))")
echo "📋 Version: $VERSION"

# Cleanup
echo "🧹 Cleaning up..."
docker stop tqfaapi-test-container
docker rm tqfaapi-test-container

echo "✅ Container test completed successfully!"
echo "🚀 Ready for Azure deployment"
```

---

## 📊 **Monitoring Scripts**

### **6. Deployment Monitor (`monitor_deployment.py`)**

Watches GitHub Actions deployment status:

```python
#!/usr/bin/env python3
"""
GitHub Actions Deployment Monitor

Watches the latest deployment and reports status.
"""

import subprocess
import json
import time
import sys

def run_gh_command(command):
    """Run GitHub CLI command."""
    try:
        result = subprocess.run(f"gh {command}", shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ GitHub CLI error: {e.stderr}")
        return None

def get_latest_workflow_run():
    """Get the latest workflow run on UAT branch."""
    output = run_gh_command("run list --branch uat --limit 1 --json id,status,conclusion,workflowName")
    if output:
        runs = json.loads(output)
        return runs[0] if runs else None
    return None

def monitor_deployment():
    """Monitor the latest deployment."""
    print("👀 Monitoring latest deployment...")
    
    latest_run = get_latest_workflow_run()
    if not latest_run:
        print("❌ No workflow runs found")
        return
    
    run_id = latest_run['id']
    workflow_name = latest_run['workflowName']
    
    print(f"📋 Workflow: {workflow_name}")
    print(f"🆔 Run ID: {run_id}")
    
    while True:
        run = get_latest_workflow_run()
        if not run or run['id'] != run_id:
            break
            
        status = run['status']
        conclusion = run.get('conclusion')
        
        if status == 'completed':
            if conclusion == 'success':
                print("✅ Deployment completed successfully!")
                return True
            else:
                print(f"❌ Deployment failed: {conclusion}")
                return False
        else:
            print(f"⏳ Deployment in progress... ({status})")
            time.sleep(30)
    
    return False

if __name__ == "__main__":
    success = monitor_deployment()
    sys.exit(0 if success else 1)
```

---

## 🎯 **Usage Examples**

### **Complete Deployment Workflow**
```bash
# 1. Bump version
python bump_version.py

# 2. Commit and push
git add .
git commit -m "Version bump to 1.0.X - [feature description]"
git push

# 3. Monitor deployment
python monitor_deployment.py

# 4. Promote healthy revision (if needed)
python promote_healthy_revision.py

# 5. Validate deployment
python check_deployment.py
```

### **Local Testing Before Deployment**
```bash
# Test container locally
./test_container_locally.sh

# Start development server
python run_local.py
```

### **Emergency Operations**
```bash
# Force traffic promotion
python promote_healthy_revision.py

# Check current deployment status
python check_deployment.py

# Roll back to previous version (manual)
az containerapp ingress traffic set --name tqfaapi-uat --resource-group tqfa-uat-rg --revision-weight tqfaapi-uat--0000005=100
```

---

## 🔗 **Integration with CI/CD**

These scripts integrate with your GitHub Actions workflow:

```yaml
steps:
  - name: Test Container Locally
    run: ./test_container_locally.sh
    
  - name: Deploy to Azure Container Apps
    run: |
      # ... Azure deployment steps ...
      
  - name: Promote Healthy Revision
    run: python promote_healthy_revision.py
    
  - name: Validate Deployment
    run: python check_deployment.py
```

---

*These scripts exist because Azure Container Apps requires manual intervention that other platforms handle automatically.*