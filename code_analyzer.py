import ast
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from testsprite_parser import TestFailure, FailureCategory, TestSpriteParsedReport

@dataclass
class CodeIssue:
    file_path: str
    line_number: Optional[int]
    issue_type: str
    description: str
    suggested_fix: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    related_test_failure: Optional[str] = None

@dataclass
class CodeRevision:
    file_path: str
    original_code: str
    revised_code: str
    explanation: str
    addresses_failures: List[str]  # List of test IDs this revision addresses

class CodeAnalyzer:
    """Analyzes code to identify root causes of test failures"""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.frontend_files = []
        self.backend_files = []
        self._scan_project_files()
    
    def _scan_project_files(self):
        """Scan project for relevant files"""
        for root, dirs, files in os.walk(self.project_root):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache']]
            
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.py', '.html', '.js', '.css')):
                    if 'frontend' in file_path or file.endswith(('.html', '.js', '.css')):
                        self.frontend_files.append(file_path)
                    elif file.endswith('.py'):
                        self.backend_files.append(file_path)
    
    def analyze_failures(self, report: TestSpriteParsedReport) -> List[CodeIssue]:
        """Analyze test failures and identify code issues"""
        issues = []
        
        for failure in report.failures:
            category_issues = self._analyze_failure_category(failure)
            issues.extend(category_issues)
        
        return issues
    
    def _analyze_failure_category(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze a specific failure category"""
        issues = []
        
        if failure.category == FailureCategory.FILE_UPLOAD:
            issues.extend(self._analyze_file_upload_issues(failure))
        elif failure.category == FailureCategory.GITHUB_INTEGRATION:
            issues.extend(self._analyze_github_issues(failure))
        elif failure.category == FailureCategory.AUTHENTICATION:
            issues.extend(self._analyze_auth_issues(failure))
        elif failure.category == FailureCategory.API_ERROR:
            issues.extend(self._analyze_api_issues(failure))
        elif failure.category == FailureCategory.VALIDATION:
            issues.extend(self._analyze_validation_issues(failure))
        elif failure.category == FailureCategory.UI_INTERACTION:
            issues.extend(self._analyze_ui_issues(failure))
        
        return issues
    
    def _analyze_file_upload_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze file upload related issues"""
        issues = []
        
        # Check frontend HTML for file upload implementation
        html_files = [f for f in self.frontend_files if f.endswith('.html')]
        for html_file in html_files:
            try:
                with open(html_file, 'r') as f:
                    content = f.read()
                
                # Check for file input elements
                if 'type="file"' not in content and 'file-drop' in content:
                    issues.append(CodeIssue(
                        file_path=html_file,
                        line_number=None,
                        issue_type="missing_file_input",
                        description="File upload area exists but no actual file input element",
                        suggested_fix="Add hidden file input element and connect it to the drop area",
                        severity="critical",
                        related_test_failure=failure.test_id
                    ))
                
                # Check for drag and drop handlers
                if 'ondrop' not in content and 'drop' not in content:
                    issues.append(CodeIssue(
                        file_path=html_file,
                        line_number=None,
                        issue_type="missing_drag_drop",
                        description="Missing drag and drop event handlers",
                        suggested_fix="Add ondrop, ondragover, and ondragenter event handlers",
                        severity="high",
                        related_test_failure=failure.test_id
                    ))
                
            except Exception as e:
                continue
        
        return issues
    
    def _analyze_github_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze GitHub integration issues"""
        issues = []
        
        # Check backend for GitHub API implementation
        backend_files = [f for f in self.backend_files if 'app.py' in f]
        for backend_file in backend_files:
            try:
                with open(backend_file, 'r') as f:
                    content = f.read()
                
                # Check for GitHub API token handling
                if 'GITHUB_TOKEN' not in content and 'github' in content.lower():
                    issues.append(CodeIssue(
                        file_path=backend_file,
                        line_number=None,
                        issue_type="missing_github_token",
                        description="GitHub API calls without proper token configuration",
                        suggested_fix="Add GITHUB_TOKEN environment variable and use it in API calls",
                        severity="critical",
                        related_test_failure=failure.test_id
                    ))
                
                # Check for error handling in GitHub endpoints
                if '/github-issue' in content and 'try:' not in content:
                    issues.append(CodeIssue(
                        file_path=backend_file,
                        line_number=None,
                        issue_type="missing_error_handling",
                        description="GitHub endpoint lacks proper error handling",
                        suggested_fix="Add try-catch blocks and proper error responses",
                        severity="high",
                        related_test_failure=failure.test_id
                    ))
                
            except Exception as e:
                continue
        
        return issues
    
    def _analyze_auth_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze authentication issues"""
        issues = []
        
        # Check for API key configuration
        env_files = [os.path.join(self.project_root, '.env'), 
                    os.path.join(self.project_root, '.env.example')]
        
        for env_file in env_files:
            if os.path.exists(env_file):
                try:
                    with open(env_file, 'r') as f:
                        content = f.read()
                    
                    if 'OPENAI_API_KEY' not in content or 'GITHUB_TOKEN' not in content:
                        issues.append(CodeIssue(
                            file_path=env_file,
                            line_number=None,
                            issue_type="missing_api_keys",
                            description="Missing required API keys in environment configuration",
                            suggested_fix="Add OPENAI_API_KEY and GITHUB_TOKEN to environment file",
                            severity="critical",
                            related_test_failure=failure.test_id
                        ))
                except Exception as e:
                    continue
        
        return issues
    
    def _analyze_api_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze API error issues"""
        issues = []
        
        backend_files = [f for f in self.backend_files if 'app.py' in f]
        for backend_file in backend_files:
            try:
                with open(backend_file, 'r') as f:
                    content = f.read()
                
                # Check for proper error handling
                if '@app.route' in content and 'except' not in content:
                    issues.append(CodeIssue(
                        file_path=backend_file,
                        line_number=None,
                        issue_type="missing_exception_handling",
                        description="API endpoints lack comprehensive exception handling",
                        suggested_fix="Add try-catch blocks with proper HTTP error responses",
                        severity="high",
                        related_test_failure=failure.test_id
                    ))
                
                # Check for input validation
                if 'request.json' in content and 'validate' not in content:
                    issues.append(CodeIssue(
                        file_path=backend_file,
                        line_number=None,
                        issue_type="missing_input_validation",
                        description="API endpoints lack input validation",
                        suggested_fix="Add input validation for all request parameters",
                        severity="medium",
                        related_test_failure=failure.test_id
                    ))
                
            except Exception as e:
                continue
        
        return issues
    
    def _analyze_validation_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze validation issues"""
        issues = []
        
        # Check frontend for form validation
        html_files = [f for f in self.frontend_files if f.endswith('.html')]
        for html_file in html_files:
            try:
                with open(html_file, 'r') as f:
                    content = f.read()
                
                # Check for form validation
                if '<form' in content and 'required' not in content:
                    issues.append(CodeIssue(
                        file_path=html_file,
                        line_number=None,
                        issue_type="missing_form_validation",
                        description="Form inputs lack validation attributes",
                        suggested_fix="Add required, pattern, and other validation attributes to form inputs",
                        severity="medium",
                        related_test_failure=failure.test_id
                    ))
                
                # Check for JavaScript validation
                if 'function' in content and 'validate' not in content.lower():
                    issues.append(CodeIssue(
                        file_path=html_file,
                        line_number=None,
                        issue_type="missing_js_validation",
                        description="Missing JavaScript form validation",
                        suggested_fix="Add JavaScript validation functions for form inputs",
                        severity="medium",
                        related_test_failure=failure.test_id
                    ))
                
            except Exception as e:
                continue
        
        return issues
    
    def _analyze_ui_issues(self, failure: TestFailure) -> List[CodeIssue]:
        """Analyze UI interaction issues"""
        issues = []
        
        # Check for common UI issues based on test failure patterns
        if "locator" in failure.error_message:
            issues.append(CodeIssue(
                file_path="frontend/templates/index.html",
                line_number=None,
                issue_type="element_selector_issue",
                description="UI elements not properly accessible for testing",
                suggested_fix="Add stable IDs and data attributes to UI elements",
                severity="medium",
                related_test_failure=failure.test_id
            ))
        
        if "timeout" in failure.error_message.lower():
            issues.append(CodeIssue(
                file_path="frontend/templates/index.html",
                line_number=None,
                issue_type="slow_ui_response",
                description="UI elements taking too long to respond",
                suggested_fix="Add loading states and optimize UI responsiveness",
                severity="medium",
                related_test_failure=failure.test_id
            ))
        
        return issues
    
    def generate_code_revisions(self, issues: List[CodeIssue]) -> List[CodeRevision]:
        """Generate specific code revisions to fix identified issues"""
        revisions = []
        
        # Group issues by file
        issues_by_file = {}
        for issue in issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)
        
        for file_path, file_issues in issues_by_file.items():
            revision = self._generate_file_revision(file_path, file_issues)
            if revision:
                revisions.append(revision)
        
        return revisions
    
    def _generate_file_revision(self, file_path: str, issues: List[CodeIssue]) -> Optional[CodeRevision]:
        """Generate revision for a specific file"""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                original_code = f.read()
        except Exception as e:
            return None
        
        revised_code = original_code
        explanations = []
        addressed_failures = []
        
        for issue in issues:
            if issue.issue_type == "missing_file_input" and file_path.endswith('.html'):
                revised_code = self._fix_file_input_issue(revised_code)
                explanations.append("Added hidden file input element connected to drop area")
                addressed_failures.append(issue.related_test_failure)
            
            elif issue.issue_type == "missing_drag_drop" and file_path.endswith('.html'):
                revised_code = self._fix_drag_drop_issue(revised_code)
                explanations.append("Added drag and drop event handlers")
                addressed_failures.append(issue.related_test_failure)
            
            elif issue.issue_type == "missing_github_token" and file_path.endswith('.py'):
                revised_code = self._fix_github_token_issue(revised_code)
                explanations.append("Added GitHub token configuration and usage")
                addressed_failures.append(issue.related_test_failure)
            
            elif issue.issue_type == "missing_error_handling" and file_path.endswith('.py'):
                revised_code = self._fix_error_handling_issue(revised_code)
                explanations.append("Added comprehensive error handling")
                addressed_failures.append(issue.related_test_failure)
            
            elif issue.issue_type == "missing_form_validation" and file_path.endswith('.html'):
                revised_code = self._fix_form_validation_issue(revised_code)
                explanations.append("Added form validation attributes")
                addressed_failures.append(issue.related_test_failure)
        
        if revised_code != original_code:
            return CodeRevision(
                file_path=file_path,
                original_code=original_code,
                revised_code=revised_code,
                explanation="; ".join(explanations),
                addresses_failures=list(set(addressed_failures))
            )
        
        return None
    
    def _fix_file_input_issue(self, code: str) -> str:
        """Fix missing file input issue"""
        # Add hidden file input if missing
        if 'type="file"' not in code and 'file-drop' in code:
            # Find the file drop area and add input
            import re
            pattern = r'(<div[^>]*class="[^"]*file-drop[^"]*"[^>]*>)'
            replacement = r'\1\n                <input type="file" id="fileInput" style="display: none;" accept=".txt,.md,.json,.py,.js,.html,.css">'
            code = re.sub(pattern, replacement, code)
        return code
    
    def _fix_drag_drop_issue(self, code: str) -> str:
        """Fix missing drag and drop handlers"""
        # Add drag and drop event handlers
        if 'ondrop' not in code and 'file-drop' in code:
            # Add JavaScript for drag and drop
            js_code = '''
            // Drag and drop functionality
            const fileDropArea = document.querySelector('.file-drop');
            const fileInput = document.getElementById('fileInput');
            
            if (fileDropArea) {
                fileDropArea.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    fileDropArea.classList.add('drag-over');
                });
                
                fileDropArea.addEventListener('dragleave', (e) => {
                    e.preventDefault();
                    fileDropArea.classList.remove('drag-over');
                });
                
                fileDropArea.addEventListener('drop', (e) => {
                    e.preventDefault();
                    fileDropArea.classList.remove('drag-over');
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        handleFileUpload(files[0]);
                    }
                });
                
                fileDropArea.addEventListener('click', () => {
                    fileInput.click();
                });
            }
            
            if (fileInput) {
                fileInput.addEventListener('change', (e) => {
                    if (e.target.files.length > 0) {
                        handleFileUpload(e.target.files[0]);
                    }
                });
            }
            '''
            
            # Insert before closing script tag
            if '</script>' in code:
                code = code.replace('</script>', js_code + '\n        </script>')
        
        return code
    
    def _fix_github_token_issue(self, code: str) -> str:
        """Fix missing GitHub token issue"""
        # Add GitHub token configuration
        if 'GITHUB_TOKEN' not in code and 'github' in code.lower():
            # Add token loading at the top
            import re
            pattern = r'(import os\n|from flask import Flask\n)'
            replacement = r'\1\n# Load GitHub token\nGITHUB_TOKEN = os.getenv("GITHUB_TOKEN")\n'
            code = re.sub(pattern, replacement, code, count=1)
            
            # Add token to GitHub API calls
            pattern = r'(requests\.get\([^)]*github\.com[^)]*\))'
            replacement = r'\1, headers={"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {})'
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _fix_error_handling_issue(self, code: str) -> str:
        """Fix missing error handling issue"""
        # Add try-catch blocks around route handlers
        import re
        pattern = r'(@app\.route[^\n]*\n[^\n]*def [^(]*\([^)]*\):[^\n]*\n)'
        replacement = r'\1    try:\n'
        code = re.sub(pattern, replacement, code)
        
        # Add except blocks before return statements
        pattern = r'(    return [^\n]*\n)'
        replacement = r'    except Exception as e:\n        return jsonify({"error": str(e)}), 500\n\1'
        code = re.sub(pattern, replacement, code)
        
        return code
    
    def _fix_form_validation_issue(self, code: str) -> str:
        """Fix missing form validation issue"""
        # Add required attributes to form inputs
        import re
        
        # Add required to repository URL input
        pattern = r'(<input[^>]*name="repo_url"[^>]*)(>)'
        replacement = r'\1 required pattern="https://github\.com/[^/]+/[^/]+"\2'
        code = re.sub(pattern, replacement, code)
        
        # Add required to issue number input
        pattern = r'(<input[^>]*name="issue_number"[^>]*)(>)'
        replacement = r'\1 required pattern="[0-9]+" min="1"\2'
        code = re.sub(pattern, replacement, code)
        
        return code

# Example usage
if __name__ == "__main__":
    from testsprite_parser import TestSpriteReportParser
    
    # Parse test report
    parser = TestSpriteReportParser()
    report = parser.parse_report_file("/Users/luxin/Desktop/SF AI Hackathon 2025/bugsy/testsprite_tests/tmp/test_results.json")
    
    # Analyze code issues
    analyzer = CodeAnalyzer("/Users/luxin/Desktop/SF AI Hackathon 2025/bugsy")
    issues = analyzer.analyze_failures(report)
    
    print(f"Found {len(issues)} code issues:")
    for issue in issues:
        print(f"  - {issue.file_path}: {issue.issue_type} ({issue.severity})")
        print(f"    {issue.description}")
        print(f"    Fix: {issue.suggested_fix}")
        print()
    
    # Generate revisions
    revisions = analyzer.generate_code_revisions(issues)
    print(f"\nGenerated {len(revisions)} code revisions:")
    for revision in revisions:
        print(f"  - {revision.file_path}")
        print(f"    {revision.explanation}")
        print(f"    Addresses: {revision.addresses_failures}")
        print()