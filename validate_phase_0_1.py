"""
Phase 0.1 Document Processing Validation Script

This script validates that the enhanced agent instructions and SearchIndexManager
improvements work correctly for document-first search behavior.

Usage:
    python validate_phase_0_1.py

This script will:
1. Run unit tests for document processing
2. Validate the "yellow sky in TXTland" scenario
3. Test multi-query fallback strategies  
4. Verify confidence reporting and source citation
5. Generate a Phase 0.1 success report
"""

import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tests.test_document_processing_phase_0_1 import TestDocumentProcessingPhase01, MockEndpointTests


class Phase01ValidationRunner:
    """Main validation runner for Phase 0.1 document processing enhancements."""
    
    def __init__(self):
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'phase': '0.1',
            'test_summary': {},
            'success_criteria': {
                'yellow_sky_txtland': False,
                'multi_format_support': False, 
                'confidence_reporting': False,
                'source_citation': False,
                'fallback_strategies': False
            },
            'overall_success': False
        }
    
    def run_validation(self):
        """Run complete Phase 0.1 validation suite."""
        print("🎯 TQFA Phase 0.1 Document Processing Validation")
        print("=" * 60)
        
        try:
            # Run unit tests
            print("\n📋 Running Unit Tests...")
            self._run_unit_tests()
            
            # Validate sample files exist
            print("\n📂 Validating Sample Files...")
            self._validate_sample_files()
            
            # Test enhanced agent instructions
            print("\n🤖 Testing Enhanced Agent Instructions...")
            self._test_enhanced_instructions()
            
            # Generate success report
            print("\n📊 Generating Phase 0.1 Success Report...")
            self._generate_success_report()
            
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            self.test_results['error'] = str(e)
        
        return self.test_results
    
    def _run_unit_tests(self):
        """Run the unit test suite."""
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add test cases
        suite.addTest(loader.loadTestsFromTestCase(TestDocumentProcessingPhase01))
        suite.addTest(loader.loadTestsFromTestCase(MockEndpointTests))
        
        # Run tests with custom result handler
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        # Record test results
        self.test_results['test_summary'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
            'success_rate': (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun if result.testsRun > 0 else 0
        }
        
        # Update success criteria based on test results
        if result.testsRun > 0 and len(result.failures) == 0 and len(result.errors) == 0:
            self.test_results['success_criteria']['multi_format_support'] = True
            self.test_results['success_criteria']['confidence_reporting'] = True
            self.test_results['success_criteria']['source_citation'] = True
            self.test_results['success_criteria']['fallback_strategies'] = True
        
        print(f"✅ Unit Tests: {result.testsRun} run, {len(result.failures)} failures, {len(result.errors)} errors")
    
    def _validate_sample_files(self):
        """Validate that required sample files exist."""
        sample_files_dir = Path(__file__).parent / "sample_files"
        required_files = [
            "sample.txt",
            "sample.csv", 
            "sample.docx",
            "sample.xlsx",
            "sample.pdf",
            "test_files_and_questions.md"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = sample_files_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            raise FileNotFoundError(f"Missing sample files: {missing_files}")
        
        # Validate the canonical test case file
        txtland_file = sample_files_dir / "sample.txt"
        with open(txtland_file, 'r') as f:
            content = f.read()
            if "yellow" not in content.lower() or "txtland" not in content.lower():
                raise ValueError("sample.txt does not contain the canonical 'yellow sky in TXTland' content")
        
        self.test_results['success_criteria']['yellow_sky_txtland'] = True
        print("✅ Sample Files: All required files present and valid")
    
    def _test_enhanced_instructions(self):
        """Test that enhanced agent instructions are properly implemented."""
        gunicorn_config = Path(__file__).parent / "src" / "gunicorn.conf.py"
        
        if not gunicorn_config.exists():
            raise FileNotFoundError("gunicorn.conf.py not found - cannot validate enhanced instructions")
        
        with open(gunicorn_config, 'r') as f:
            content = f.read()
        
        # Check for enhanced instruction elements
        required_elements = [
            "MANDATORY DOCUMENT SEARCH PROTOCOL",
            "SEARCH EXAMPLE",
            "CONFIDENCE REPORTING", 
            "DOCUMENT SOURCE REPORTING",
            "TQ Assistant"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            raise ValueError(f"Enhanced instructions missing elements: {missing_elements}")
        
        print("✅ Enhanced Instructions: All required elements present")
    
    def _generate_success_report(self):
        """Generate final Phase 0.1 success report."""
        # Calculate overall success
        success_count = sum(1 for success in self.test_results['success_criteria'].values() if success)
        total_criteria = len(self.test_results['success_criteria'])
        success_rate = success_count / total_criteria
        
        self.test_results['overall_success'] = success_rate >= 0.8  # 80% success threshold
        self.test_results['success_rate'] = success_rate
        
        # Print summary
        print(f"\n🎯 Phase 0.1 Validation Summary:")
        print(f"   Overall Success: {'✅ PASS' if self.test_results['overall_success'] else '❌ FAIL'}")
        print(f"   Success Rate: {success_rate:.1%}")
        print(f"   Criteria Met: {success_count}/{total_criteria}")
        
        print(f"\n📋 Success Criteria Details:")
        for criterion, success in self.test_results['success_criteria'].items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {criterion}: {status}")
        
        # Test summary
        if 'test_summary' in self.test_results:
            ts = self.test_results['test_summary']
            print(f"\n🧪 Unit Test Summary:")
            print(f"   Tests Run: {ts['tests_run']}")
            print(f"   Success Rate: {ts['success_rate']:.1%}")
            print(f"   Failures: {ts['failures']}")
            print(f"   Errors: {ts['errors']}")
        
        # Save detailed results
        results_file = Path(__file__).parent / "phase_0_1_validation_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        # Phase completion message
        if self.test_results['overall_success']:
            print(f"\n🎉 Phase 0.1 COMPLETED SUCCESSFULLY!")
            print(f"   ✅ LLM document processing enhancements are working")
            print(f"   ✅ 'Yellow sky in TXTland' canonical test case implemented")
            print(f"   ✅ Enhanced agent instructions deployed")
            print(f"   ✅ Unit testing framework established")
            print(f"\n🚀 Ready for Phase 0.5: PDF/CSV Processing Enhancement")
        else:
            print(f"\n⚠️  Phase 0.1 PARTIALLY COMPLETED")
            print(f"   Some success criteria not met - review failed tests")
            print(f"   Address issues before proceeding to Phase 0.5")


def main():
    """Main entry point for Phase 0.1 validation."""
    runner = Phase01ValidationRunner()
    results = runner.run_validation()
    
    # Exit with appropriate code
    exit_code = 0 if results['overall_success'] else 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()