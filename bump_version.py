#!/usr/bin/env python3
"""
TQFA API V2 - Version Bump Script
Following Copilot Instructions: MANDATORY Version Bump Before Every Push

Integrated with FastAPI structure and following V1 production standards.
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class V2VersionBumper:
    """
    Production-ready version management for TQFA API V2.
    Following Copilot Instructions: NO SHORTCUTS FROM DAY ONE.
    """
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        
        # Azure AI Foundry agent structure file patterns
        self.version_files = {
            'pyproject.toml': self._update_pyproject_version,
            'setup.py': self._update_setup_version,
            'version.json': self._update_version_json,
            'src/pyproject.toml': self._update_pyproject_version,
        }
    
    def get_current_version(self) -> str:
        """
        Extract current version from version.json (primary source for Azure AI Foundry).
        """
        # Try version.json first (Azure AI Foundry version)
        version_json_path = self.project_root / 'version.json'
        
        if version_json_path.exists():
            try:
                import json
                with open(version_json_path, 'r') as f:
                    data = json.load(f)
                    if 'version' in data:
                        return data['version']
            except:
                pass
        
        # Fallback patterns for other files
        for file_path in ['pyproject.toml', 'src/pyproject.toml', 'setup.py']:
            full_path = self.project_root / file_path
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                
                patterns = [
                    r'version\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']',
                    r'__version__\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, content)
                    if match:
                        return match.group(1)
        
        return "1.0.0"  # Default version
        
        # Try version.json as fallback
        version_json_path = self.project_root / 'version.json'
        if version_json_path.exists():
            try:
                version_data = json.loads(version_json_path.read_text(encoding='utf-8'))
                if 'version' in version_data:
                    return version_data['version']
            except json.JSONDecodeError:
                pass
        
        # Default to V2 base version if nothing found
        print("⚠️ No existing version found, starting with V2 base version")
        return "2.0.0"
    
    def bump_version(self, version: str, bump_type: str = 'patch') -> str:
        """
        Increment version number based on bump type.
        Following Copilot Instructions: Version Numbering Standards.
        """
        major, minor, patch = map(int, version.split('.'))
        
        if bump_type == 'major':
            return f"{major + 1}.0.0"
        elif bump_type == 'minor':
            return f"{major}.{minor + 1}.0"
        elif bump_type == 'patch':
            return f"{major}.{minor}.{patch + 1}"
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
    
    def _update_fastapi_version(self, file_path: Path, new_version: str) -> bool:
        """
        Update version in FastAPI app/main.py.
        Following Copilot Instructions: FastAPI must show version in root endpoint.
        """
        if not file_path.exists():
            print(f"⚠️ {file_path} not found, skipping...")
            return False
        
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Update FastAPI app version declaration
        patterns = [
            # FastAPI constructor version
            (r'(version\s*=\s*["\'])[0-9]+\.[0-9]+\.[0-9]+(["\'])', f'\\g<1>{new_version}\\g<2>'),
            # Module-level version
            (r'(__version__\s*=\s*["\'])[0-9]+\.[0-9]+\.[0-9]+(["\'])', f'\\g<1>{new_version}\\g<2>'),
            # JSON version in responses
            (r'("version":\s*")[0-9]+\.[0-9]+\.[0-9]+("))', f'\\g<1>{new_version}\\g<2>'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"   ✅ Updated {file_path}")
            return True
        else:
            print(f"   ⚠️ No version pattern found in {file_path}")
            return False
    
    def _update_pyproject_version(self, file_path: Path, new_version: str) -> bool:
        """Update version in pyproject.toml."""
        if not file_path.exists():
            print(f"   ℹ️ {file_path} not found, skipping (optional)...")
            return False
        
        content = file_path.read_text(encoding='utf-8')
        pattern = r'(version\s*=\s*["\'])[0-9]+\.[0-9]+\.[0-9]+(["\'])'
        replacement = f'\\g<1>{new_version}\\g<2>'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"   ✅ Updated {file_path}")
            return True
        return False
    
    def _update_setup_version(self, file_path: Path, new_version: str) -> bool:
        """Update version in setup.py (if exists)."""
        if not file_path.exists():
            print(f"   ℹ️ {file_path} not found, skipping (optional)...")
            return False
        
        content = file_path.read_text(encoding='utf-8')
        pattern = r'(version\s*=\s*["\'])[0-9]+\.[0-9]+\.[0-9]+(["\'])'
        replacement = f'\\g<1>{new_version}\\g<2>'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"   ✅ Updated {file_path}")
            return True
        return False
    
    def _update_version_json(self, file_path: Path, new_version: str) -> bool:
        """
        Update V2 version.json file.
        Following V2 template structure.
        """
        version_info = {
            "version": new_version,
            "template": "Azure AI Foundry Agent", 
            "project": "TQFA API V2",
            "infrastructure": "Azure Container Apps",
            "updated": datetime.utcnow().isoformat() + "Z",
            "deployment_ready": True
        }
        
        try:
            file_path.write_text(json.dumps(version_info, indent=2), encoding='utf-8')
            print(f"   ✅ Updated {file_path}")
            return True
        except Exception as e:
            print(f"   ❌ Failed to update {file_path}: {e}")
            return False
    
    def update_all_files(self, new_version: str) -> None:
        """
        Update version in all V2 project files.
        Following Copilot Instructions: Comprehensive version tracking.
        """
        print(f"🔄 Updating all V2 files to version {new_version}...")
        
        updated_files = []
        
        for file_path, update_func in self.version_files.items():
            full_path = self.project_root / file_path
            if update_func(full_path, new_version):
                updated_files.append(file_path)
        
        if updated_files:
            print(f"\n✅ Successfully updated version to {new_version} in:")
            for file_path in updated_files:
                print(f"   - {file_path}")
        else:
            print("⚠️ No files were updated")
    
    def run(self, bump_type: str = 'patch') -> str:
        """
        Execute V2 version bump process.
        Following Copilot Instructions: MANDATORY Version Bump Before Every Push.
        """
        print(f"🚀 TQFA API V2 - Version Bump ({bump_type})")
        print("=" * 70)
        print("Following Copilot Instructions: MANDATORY Version Bump Before Every Push")
        
        try:
            # Get current version
            current_version = self.get_current_version()
            print(f"📦 Current version: {current_version}")
            
            # Calculate new version
            new_version = self.bump_version(current_version, bump_type)
            print(f"📦 New version: {new_version}")
            
            # Update all files
            self.update_all_files(new_version)
            
            # Success message with deployment instructions
            print(f"\n🎯 Version bump complete: {current_version} → {new_version}")
            print(f"📅 Timestamp: {datetime.now().isoformat()}")
            
            print(f"\n📋 Next Steps (Following Copilot Instructions):")
            print(f"   1. git add .")
            print(f"   2. git commit -m 'Version bump to {new_version} - [description]'")
            print(f"   3. git push")
            print(f"   4. Monitor deployment: gh run list --branch uat --limit 3")
            print(f"   5. Verify deployment: curl https://[container-app-url]/")
            print(f"   6. Check version appears in root endpoint response")
            
            print(f"\n🚨 Critical (Following Copilot Instructions):")
            print(f"   - ALWAYS verify URLs from official sources")
            print(f"   - Use Azure CLI to get correct container app URL")
            print(f"   - Never guess or assume endpoint URLs")
            
            return new_version
            
        except Exception as e:
            print(f"❌ Version bump failed: {e}")
            sys.exit(1)


def main():
    """
    Main entry point for V2 version bump script.
    Following Copilot Instructions: Production-Ready From Day One.
    """
    parser = argparse.ArgumentParser(
        description="TQFA API V2 Version Bump Script",
        epilog="Following Copilot Instructions: MANDATORY Version Bump Before Every Push"
    )
    parser.add_argument(
        '--major',
        action='store_true',
        help='Bump major version (X+1.0.0)'
    )
    parser.add_argument(
        '--minor', 
        action='store_true',
        help='Bump minor version (X.Y+1.0)'
    )
    parser.add_argument(
        '--patch',
        action='store_true',
        help='Bump patch version (X.Y.Z+1) - default'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    
    args = parser.parse_args()
    
    # Determine bump type
    if args.major:
        bump_type = 'major'
    elif args.minor:
        bump_type = 'minor'
    else:
        bump_type = 'patch'  # Default
    
    # Create version bumper
    bumper = V2VersionBumper()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        try:
            current_version = bumper.get_current_version()
            new_version = bumper.bump_version(current_version, bump_type)
            print(f"📊 Would update: {current_version} → {new_version}")
            print(f"📁 Files that would be updated:")
            for file_path in bumper.version_files.keys():
                full_path = bumper.project_root / file_path
                status = "✅ exists" if full_path.exists() else "⚠️ not found"
                print(f"   {file_path} ({status})")
        except Exception as e:
            print(f"❌ Dry run failed: {e}")
            sys.exit(1)
    else:
        # Execute version bump
        bumper.run(bump_type)


if __name__ == "__main__":
    main()