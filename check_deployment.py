#!/usr/bin/env python3
"""
Deployment Status Checker
Quick way to check what version is deployed vs what's in code
"""

import requests
import json
from pathlib import Path

def check_deployment_status():
    """Check deployment status by comparing local vs deployed versions."""
    
    print("🚀 TQFA Deployment Status Check")
    print("=" * 40)
    
    # Get local version
    try:
        main_py = Path("app/main.py")
        content = main_py.read_text(encoding='utf-8')
        
        import re
        version_match = re.search(r'version="(\d+\.\d+\.\d+)"', content)
        if version_match:
            local_version = version_match.group(1)
            print(f"📁 Local version: {local_version}")
        else:
            print("❌ Could not find local version")
            return
    except Exception as e:
        print(f"❌ Error reading local version: {e}")
        return
    
    # Check UAT deployment
    uat_url = "https://tqfaapi-uat.ashyfield-eea5df41.eastus2.azurecontainerapps.io"
    
    print(f"\n🌐 Checking UAT deployment...")
    try:
        response = requests.get(f"{uat_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            deployed_version = data.get('version', 'unknown')
            print(f"☁️ UAT version: {deployed_version}")
            
            if deployed_version == local_version:
                print("✅ UAT is UP TO DATE!")
            else:
                print("⚠️ UAT is BEHIND - deployment may be in progress")
        else:
            print(f"❌ UAT check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ UAT check error: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Local:  {local_version}")
    
    # Test the fixed endpoint if UAT is current
    print(f"\n🧪 Testing /users/validate endpoint...")
    try:
        response = requests.post(
            f"{uat_url}/api/v1/users/validate",
            headers={"Content-Type": "application/json"},
            json={"user_id": "david", "password": "david1234"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ /users/validate: WORKING")
            print(f"   Message: {data.get('message', 'N/A')}")
        elif response.status_code == 401:
            print(f"🔒 /users/validate: Working but auth failed (user may not exist)")
        elif response.status_code == 500:
            print(f"❌ /users/validate: Still broken (500 error)")
        else:
            print(f"❓ /users/validate: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Endpoint test error: {e}")

if __name__ == "__main__":
    check_deployment_status()