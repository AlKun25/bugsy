import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class FailureCategory(Enum):
    FILE_UPLOAD = "file_upload"
    GITHUB_INTEGRATION = "github_integration"
    API_ERROR = "api_error"
    VALIDATION = "validation"
    UI_INTERACTION = "ui_interaction"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    DOCKER = "docker"
    GENERIC = "generic"

@dataclass
class TestFailure:
    test_id: str
    title: str
    description: str
    error_message: str
    category: FailureCategory
    code_snippet: Optional[str] = None
    visualization_url: Optional[str] = None
    suggested_fixes: List[str] = None

@dataclass
class TestSpriteParsedReport:
    total_tests: int
    passed_tests: int
    failed_tests: int
    failures: List[TestFailure]
    summary: Dict[str, Any]

class TestSpriteReportParser:
    """Parser for TestSprite test execution reports"""
    
    def __init__(self):
        self.failure_patterns = {
            "file upload": FailureCategory.FILE_UPLOAD,
            "file drop area": FailureCategory.FILE_UPLOAD,
            "upload": FailureCategory.FILE_UPLOAD,
            "github": FailureCategory.GITHUB_INTEGRATION,
            "repository": FailureCategory.GITHUB_INTEGRATION,
            "401 unauthorized": FailureCategory.AUTHENTICATION,
            "api key": FailureCategory.AUTHENTICATION,
            "500 internal server error": FailureCategory.API_ERROR,
            "network failure": FailureCategory.NETWORK,
            "validation": FailureCategory.VALIDATION,
            "docker": FailureCategory.DOCKER,
            "health check": FailureCategory.DOCKER,
            "ui": FailureCategory.UI_INTERACTION,
            "click": FailureCategory.UI_INTERACTION,
            "locator": FailureCategory.UI_INTERACTION
        }
    
    def parse_report_file(self, file_path: str) -> TestSpriteParsedReport:
        """Parse TestSprite report from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return self.parse_report_data(data)
    
    def parse_report_data(self, data: List[Dict]) -> TestSpriteParsedReport:
        """Parse TestSprite report from JSON data"""
        failures = []
        passed_count = 0
        failed_count = 0
        
        for test_case in data:
            status = TestStatus(test_case.get('testStatus', 'FAILED'))
            
            if status == TestStatus.PASSED:
                passed_count += 1
            elif status == TestStatus.FAILED:
                failed_count += 1
                failure = self._extract_failure(test_case)
                failures.append(failure)
        
        total_tests = len(data)
        
        summary = self._generate_summary(failures)
        
        return TestSpriteParsedReport(
            total_tests=total_tests,
            passed_tests=passed_count,
            failed_tests=failed_count,
            failures=failures,
            summary=summary
        )
    
    def _extract_failure(self, test_case: Dict) -> TestFailure:
        """Extract failure information from a test case"""
        test_id = test_case.get('testId', '')
        title = test_case.get('title', '')
        description = test_case.get('description', '')
        error_message = test_case.get('testError', '')
        code_snippet = test_case.get('code', '')
        visualization_url = test_case.get('testVisualization', '')
        
        category = self._categorize_failure(error_message, title, description)
        suggested_fixes = self._generate_suggested_fixes(category, error_message)
        
        return TestFailure(
            test_id=test_id,
            title=title,
            description=description,
            error_message=error_message,
            category=category,
            code_snippet=code_snippet,
            visualization_url=visualization_url,
            suggested_fixes=suggested_fixes
        )
    
    def _categorize_failure(self, error_message: str, title: str, description: str) -> FailureCategory:
        """Categorize failure based on error patterns"""
        text_to_analyze = f"{error_message} {title} {description}".lower()
        
        for pattern, category in self.failure_patterns.items():
            if pattern in text_to_analyze:
                return category
        
        return FailureCategory.GENERIC
    
    def _generate_suggested_fixes(self, category: FailureCategory, error_message: str) -> List[str]:
        """Generate suggested fixes based on failure category"""
        fixes = {
            FailureCategory.FILE_UPLOAD: [
                "Fix file upload drag-and-drop functionality in frontend",
                "Add proper file validation and error messaging",
                "Implement file type checking and size limits",
                "Add visual feedback for file upload status"
            ],
            FailureCategory.GITHUB_INTEGRATION: [
                "Verify GitHub API token configuration",
                "Add proper error handling for GitHub API responses",
                "Implement rate limiting and retry logic",
                "Add validation for GitHub URL format"
            ],
            FailureCategory.AUTHENTICATION: [
                "Configure valid API keys in environment variables",
                "Add API key validation before making requests",
                "Implement proper error handling for authentication failures",
                "Add user-friendly error messages for auth issues"
            ],
            FailureCategory.API_ERROR: [
                "Add comprehensive error handling in backend endpoints",
                "Implement proper HTTP status code responses",
                "Add logging for debugging API issues",
                "Add input validation and sanitization"
            ],
            FailureCategory.VALIDATION: [
                "Add client-side form validation",
                "Implement server-side input validation",
                "Add user-friendly validation error messages",
                "Prevent form submission with invalid data"
            ],
            FailureCategory.UI_INTERACTION: [
                "Fix element selectors and locators",
                "Add proper loading states and feedback",
                "Implement better error handling in UI",
                "Add accessibility improvements"
            ],
            FailureCategory.NETWORK: [
                "Add network error handling and retry logic",
                "Implement offline mode detection",
                "Add timeout handling for network requests",
                "Provide user feedback for network issues"
            ],
            FailureCategory.DOCKER: [
                "Fix Docker health check configuration",
                "Add proper container restart policies",
                "Implement monitoring and alerting",
                "Fix container networking issues"
            ]
        }
        
        return fixes.get(category, ["Review and fix the underlying issue"])
    
    def _generate_summary(self, failures: List[TestFailure]) -> Dict[str, Any]:
        """Generate summary statistics from failures"""
        category_counts = {}
        for failure in failures:
            category = failure.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        most_common_issues = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "failure_categories": category_counts,
            "most_common_issues": most_common_issues,
            "critical_issues": [f for f in failures if f.category in [FailureCategory.FILE_UPLOAD, FailureCategory.AUTHENTICATION, FailureCategory.API_ERROR]],
            "total_suggested_fixes": sum(len(f.suggested_fixes) for f in failures)
        }
    
    def get_failures_by_category(self, report: TestSpriteParsedReport, category: FailureCategory) -> List[TestFailure]:
        """Get all failures of a specific category"""
        return [f for f in report.failures if f.category == category]
    
    def get_critical_failures(self, report: TestSpriteParsedReport) -> List[TestFailure]:
        """Get failures that are considered critical"""
        critical_categories = [FailureCategory.FILE_UPLOAD, FailureCategory.AUTHENTICATION, FailureCategory.API_ERROR]
        return [f for f in report.failures if f.category in critical_categories]

# Example usage
if __name__ == "__main__":
    parser = TestSpriteReportParser()
    
    # Parse the test results
    try:
        report = parser.parse_report_file("/Users/luxin/Desktop/SF AI Hackathon 2025/bugsy/testsprite_tests/tmp/test_results.json")
        
        print(f"Test Results Summary:")
        print(f"Total Tests: {report.total_tests}")
        print(f"Passed: {report.passed_tests}")
        print(f"Failed: {report.failed_tests}")
        print(f"Success Rate: {(report.passed_tests/report.total_tests)*100:.1f}%")
        
        print(f"\nFailure Categories:")
        for category, count in report.summary['failure_categories'].items():
            print(f"  {category}: {count}")
        
        print(f"\nCritical Failures:")
        critical_failures = parser.get_critical_failures(report)
        for failure in critical_failures:
            print(f"  - {failure.title}: {failure.category.value}")
            print(f"    Error: {failure.error_message[:100]}...")
            print(f"    Suggested fixes: {len(failure.suggested_fixes)}")
            print()
        
    except Exception as e:
        print(f"Error parsing report: {e}")