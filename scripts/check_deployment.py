import requests
import subprocess
import sys
from datetime import datetime

def check_v2_deployment(environment="uat"):
    """Check V2 deployment status following V1 standards."""
    
    print(f"🔍 TQFA API V2 - Deployment Check ({environment.upper()})")
    print("=" * 60)
    print("Following V1 Standards: Never assume deployment success")
    
    try:
        # Get Container App URL using Azure CLI (V1 lesson: always verify URLs)
        print(f"\n🌐 Getting verified URL for {environment} environment...")
        
        if environment == "uat":
            app_name = "tqfaapi-uat"
            resource_group = "tqfa-uat-rg"
        elif environment == "dev":
            app_name = "tqfaapi-v2-dev"
            resource_group = "tqfa-dev-rg"
        else:  # prod
            app_name = "tqfaapi-v2-prod"
            resource_group = "tqfa-prod-rg"
        
        # Get FQDN using Azure CLI
        result = subprocess.run([
            "az", "containerapp", "show", 
            "--name", app_name, 
            "--resource-group", resource_group,
            "--query", "properties.configuration.ingress.fqdn",
            "--output", "tsv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Could not retrieve Container App URL: {result.stderr}")
            return
        
        fqdn = result.stdout.strip()
        if not fqdn:
            print(f"❌ Container App FQDN is empty")
            return
            
        app_url = f"https://{fqdn}"
        
        print(f"✅ Verified Container App URL: {app_url}")
        print(f"📦 Container App: {app_name}")
        
        # Test root endpoint (V1 standards: comprehensive endpoint testing)
        try:
            print(f"\n🧪 Testing Root Endpoint...")
            response = requests.get(app_url, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Root endpoint: HTTP {response.status_code}")
                    if 'version' in data:
                        print(f"📦 Version: {data['version']}")
                    print(f"📝 Response: {data}")
                except:
                    print(f"✅ Root endpoint: HTTP {response.status_code} (non-JSON response)")
                    print(f"📝 Response: {response.text[:200]}...")
            else:
                print(f"⚠️ Root endpoint: HTTP {response.status_code}")
                print(f"📝 Response: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Root endpoint: Connection failed - {e}")
        
        # Test health endpoint
        try:
            print(f"\n🏥 Testing Health Endpoint...")
            health_response = requests.get(f"{app_url}/health", timeout=10)
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"✅ Health endpoint: HTTP {health_response.status_code}")
                print(f"💚 Status: {health_data.get('status', 'Unknown')}")
            else:
                print(f"⚠️ Health endpoint: HTTP {health_response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"📝 Health endpoint: Not available in template (will add in customization)")
        
        # Show manual test commands
        print(f"\n📋 Manual Testing Commands:")
        print(f"curl {app_url}")
        print(f"curl {app_url}/health")
        print(f"Invoke-RestMethod -Uri '{app_url}'")
        
        # Check recent GitHub Actions (V1 standards: monitor deployment pipeline)
        print(f"\n📊 Recent Deployments (if GitHub Actions configured):")
        try:
            gh_result = subprocess.run(
                ["gh", "run", "list", "--limit", "3"],
                capture_output=True, text=True
            )
            if gh_result.returncode == 0:
                print(gh_result.stdout)
            else:
                print("📝 GitHub Actions not configured yet (will add in customization)")
        except:
            print("📝 GitHub CLI not available or no workflows configured")
            
    except Exception as e:
        print(f"❌ Deployment check failed: {e}")

if __name__ == "__main__":
    environment = sys.argv[1] if len(sys.argv) > 1 else "uat"
    check_v2_deployment(environment)
