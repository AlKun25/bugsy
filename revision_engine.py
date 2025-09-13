import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import openai
import difflib
from datetime import datetime
from testsprite_parser import TestSpriteReportParser, TestSpriteParsedReport, TestFailure
from code_analyzer import CodeAnalyzer, CodeIssue, CodeRevision

@dataclass
class RevisionRequest:
    test_failures: List[TestFailure]
    code_context: Dict[str, str]  # file_path -> file_content
    project_structure: List[str]
    error_patterns: List[str]

@dataclass
class GitDiff:
    file_path: str
    unified_diff: str
    additions: int
    deletions: int
    
@dataclass
class AIRevisionSuggestion:
    file_path: str
    original_code: str
    revised_code: str
    explanation: str
    confidence_score: float
    addresses_test_ids: List[str]
    change_type: str  # 'fix', 'enhancement', 'refactor'
    git_diff: Optional[GitDiff] = None

class OpenAIRevisionEngine:
    """AI-powered code revision engine using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def analyze_and_fix_failures(self, report_path: str, project_root: str) -> List[AIRevisionSuggestion]:
        """Main method to analyze test failures and generate AI-powered fixes"""
        # Parse test report
        parser = TestSpriteReportParser()
        report = parser.parse_report_file(report_path)
        
        if not report.failures:
            return []
        
        # Gather code context
        code_context = self._gather_code_context(project_root, report.failures)
        
        # Get project structure
        project_structure = self._get_project_structure(project_root)
        
        # Create revision request
        revision_request = RevisionRequest(
            test_failures=report.failures,
            code_context=code_context,
            project_structure=project_structure,
            error_patterns=self._extract_error_patterns(report.failures)
        )
        
        # Generate AI-powered revisions
        revisions = self._generate_ai_revisions(revision_request)
        
        # Generate git-style diffs for each revision
        for revision in revisions:
            revision.git_diff = self._generate_git_diff(revision)
        
        return revisions
    
    def _gather_code_context(self, project_root: str, failures: List[TestFailure]) -> Dict[str, str]:
        """Gather relevant code files based on test failures (limited for token efficiency)"""
        code_context = {}
        
        # Prioritize most important files only
        main_files = [
            os.path.join(project_root, 'app.py'),
            os.path.join(project_root, 'frontend', 'templates', 'index.html')
        ]
        
        # Add one additional file based on failure patterns
        for failure in failures:
            if 'file upload' in failure.error_message.lower():
                main_files.append(os.path.join(project_root, 'frontend', 'static', 'js', 'main.js'))
                break
            elif 'github' in failure.error_message.lower():
                main_files.append(os.path.join(project_root, '.env.example'))
                break
        
        # Read existing files (limit to 2-3 files max)
        for file_path in main_files[:3]:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Truncate very large files immediately
                        if len(content) > 10000:  # ~10KB limit per file
                            lines = content.split('\n')
                            if len(lines) > 100:
                                content = '\n'.join(lines[:50] + ['... (file truncated) ...'] + lines[-25:])
                        code_context[file_path] = content
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        return code_context
    
    def _get_project_structure(self, project_root: str) -> List[str]:
        """Get project structure for context"""
        structure = []
        
        for root, dirs, files in os.walk(project_root):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.pytest_cache', 'tmp']]
            
            level = root.replace(project_root, '').count(os.sep)
            indent = ' ' * 2 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if not file.startswith('.') and file.endswith(('.py', '.html', '.js', '.css', '.json', '.md')):
                    structure.append(f"{subindent}{file}")
        
        return structure[:50]  # Limit to avoid token overflow
    
    def _extract_error_patterns(self, failures: List[TestFailure]) -> List[str]:
        """Extract common error patterns from failures"""
        patterns = []
        
        for failure in failures:
            # Extract key error information
            error_msg = failure.error_message.lower()
            
            if 'timeout' in error_msg:
                patterns.append("UI element timeout - elements not responding quickly enough")
            
            if 'locator' in error_msg or 'element not found' in error_msg:
                patterns.append("Element selector issues - UI elements not properly accessible")
            
            if 'file' in error_msg and 'upload' in error_msg:
                patterns.append("File upload functionality issues")
            
            if 'github' in error_msg:
                patterns.append("GitHub API integration problems")
            
            if 'api' in error_msg and ('key' in error_msg or 'token' in error_msg):
                patterns.append("API authentication and configuration issues")
            
            if 'validation' in error_msg or 'required' in error_msg:
                patterns.append("Form validation and input handling issues")
        
        return list(set(patterns))
    
    def _generate_ai_revisions(self, request: RevisionRequest) -> List[AIRevisionSuggestion]:
        """Generate AI-powered code revisions using OpenAI"""
        revisions = []
        
        # Group failures by likely root cause
        failure_groups = self._group_failures_by_cause(request.test_failures)
        
        for group_name, group_failures in failure_groups.items():
            revision = self._generate_revision_for_group(group_name, group_failures, request)
            if revision:
                revisions.append(revision)
        
        return revisions
    
    def _group_failures_by_cause(self, failures: List[TestFailure]) -> Dict[str, List[TestFailure]]:
        """Group test failures by likely root cause"""
        groups = {
            'file_upload': [],
            'github_integration': [],
            'ui_interaction': [],
            'api_authentication': [],
            'form_validation': [],
            'general': []
        }
        
        for failure in failures:
            error_msg = failure.error_message.lower()
            
            if 'file' in error_msg and 'upload' in error_msg:
                groups['file_upload'].append(failure)
            elif 'github' in error_msg:
                groups['github_integration'].append(failure)
            elif 'locator' in error_msg or 'timeout' in error_msg or 'element' in error_msg:
                groups['ui_interaction'].append(failure)
            elif 'api' in error_msg and ('key' in error_msg or 'token' in error_msg):
                groups['api_authentication'].append(failure)
            elif 'validation' in error_msg or 'required' in error_msg:
                groups['form_validation'].append(failure)
            else:
                groups['general'].append(failure)
        
        # Remove empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _generate_revision_for_group(self, group_name: str, failures: List[TestFailure], request: RevisionRequest) -> Optional[AIRevisionSuggestion]:
        """Generate revision for a specific group of failures"""
        # Create context-specific prompt
        prompt = self._create_revision_prompt(group_name, failures, request)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer specializing in debugging and fixing code issues. You analyze test failures and provide precise, working code fixes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response, failures)
            
        except Exception as e:
            print(f"Error generating AI revision for {group_name}: {e}")
            return None
    
    def _create_revision_prompt(self, group_name: str, failures: List[TestFailure], request: RevisionRequest) -> str:
        """Create a detailed prompt for AI revision generation"""
        
        # Build failure summary
        failure_summary = "\n".join([
            f"Test {f.test_id}: {f.error_message}" for f in failures
        ])
        
        # Get relevant code files
        relevant_files = self._get_relevant_files_for_group(group_name, request.code_context)
        
        code_context = "\n\n".join([
            f"=== {file_path} ===\n{content}" 
            for file_path, content in relevant_files.items()
        ])
        
        prompt = f"""
Failing tests ({group_name}):
{failure_summary}

Code:
{code_context}

Errors: {', '.join(request.error_patterns[:3])}

Provide JSON fix:
{{
    "file_path": "path/to/file",
    "original_code": "code to change",
    "revised_code": "fixed code",
    "explanation": "what was wrong and how fix addresses it",
    "confidence_score": 0.95,
    "addresses_test_ids": ["TC001"],
    "change_type": "fix"
}}

Only JSON response.
"""
        
        return prompt
    
    def _truncate_content(self, content: str, max_lines: int = 200) -> str:
        """Truncate content to reduce token usage"""
        lines = content.split('\n')
        if len(lines) <= max_lines:
            return content
        
        # Keep first half and last quarter of the file
        first_part = lines[:max_lines//2]
        last_part = lines[-(max_lines//4):]
        
        return '\n'.join(first_part + ['\n... (content truncated) ...\n'] + last_part)
    
    def _get_relevant_files_for_group(self, group_name: str, code_context: Dict[str, str]) -> Dict[str, str]:
        """Get relevant files for a specific failure group with content truncation"""
        relevant = {}
        
        if group_name == 'file_upload':
            # Focus on frontend and upload handling
            for path, content in code_context.items():
                if 'index.html' in path or 'app.py' in path:
                    relevant[path] = self._truncate_content(content, 150)
        
        elif group_name == 'github_integration':
            # Focus on backend GitHub handling
            for path, content in code_context.items():
                if 'app.py' in path or '.env' in path:
                    relevant[path] = self._truncate_content(content, 100)
        
        elif group_name == 'ui_interaction':
            # Focus on frontend
            for path, content in code_context.items():
                if 'index.html' in path or '.js' in path or '.css' in path:
                    relevant[path] = self._truncate_content(content, 150)
        
        elif group_name == 'api_authentication':
            # Focus on backend and config
            for path, content in code_context.items():
                if 'app.py' in path or '.env' in path:
                    relevant[path] = self._truncate_content(content, 100)
        
        elif group_name == 'form_validation':
            # Focus on frontend forms
            for path, content in code_context.items():
                if 'index.html' in path or '.js' in path:
                    relevant[path] = self._truncate_content(content, 150)
        
        else:
            # Include all for general issues but truncated
            for path, content in code_context.items():
                relevant[path] = self._truncate_content(content, 100)
        
        return relevant
    
    def _parse_ai_response(self, ai_response: str, failures: List[TestFailure]) -> Optional[AIRevisionSuggestion]:
        """Parse AI response into structured revision suggestion"""
        try:
            # Extract JSON from response
            response_text = ai_response.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            data = json.loads(response_text)
            
            return AIRevisionSuggestion(
                file_path=data['file_path'],
                original_code=data['original_code'],
                revised_code=data['revised_code'],
                explanation=data['explanation'],
                confidence_score=data.get('confidence_score', 0.8),
                addresses_test_ids=data.get('addresses_test_ids', [f.test_id for f in failures]),
                change_type=data.get('change_type', 'fix')
            )
            
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            print(f"Raw response: {ai_response}")
            return None
    
    def apply_revisions(self, revisions: List[AIRevisionSuggestion], backup: bool = True) -> Dict[str, bool]:
        """Apply AI-generated revisions to files"""
        results = {}
        
        for revision in revisions:
            try:
                # Create backup if requested
                if backup and os.path.exists(revision.file_path):
                    backup_path = f"{revision.file_path}.backup"
                    with open(revision.file_path, 'r') as original:
                        with open(backup_path, 'w') as backup_file:
                            backup_file.write(original.read())
                
                # Read current file
                if os.path.exists(revision.file_path):
                    with open(revision.file_path, 'r') as f:
                        current_content = f.read()
                    
                    # Apply revision
                    if revision.original_code in current_content:
                        new_content = current_content.replace(
                            revision.original_code, 
                            revision.revised_code, 
                            1  # Replace only first occurrence
                        )
                        
                        # Write updated content
                        with open(revision.file_path, 'w') as f:
                            f.write(new_content)
                        
                        results[revision.file_path] = True
                        print(f"✅ Applied revision to {revision.file_path}")
                        print(f"   Explanation: {revision.explanation}")
                    else:
                        results[revision.file_path] = False
                        print(f"❌ Could not find original code in {revision.file_path}")
                else:
                    results[revision.file_path] = False
                    print(f"❌ File not found: {revision.file_path}")
                    
            except Exception as e:
                results[revision.file_path] = False
                print(f"❌ Error applying revision to {revision.file_path}: {e}")
        
        return results
    
    def _generate_git_diff(self, revision: AIRevisionSuggestion) -> GitDiff:
        """Generate git-style unified diff for a code revision"""
        original_lines = revision.original_code.splitlines(keepends=True)
        revised_lines = revision.revised_code.splitlines(keepends=True)
        
        # Generate unified diff
        diff_lines = list(difflib.unified_diff(
            original_lines,
            revised_lines,
            fromfile=f"a/{revision.file_path}",
            tofile=f"b/{revision.file_path}",
            fromfiledate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tofiledate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lineterm=''
        ))
        
        unified_diff = '\n'.join(diff_lines)
        
        # Count additions and deletions
        additions = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))
        
        return GitDiff(
            file_path=revision.file_path,
            unified_diff=unified_diff,
            additions=additions,
            deletions=deletions
        )
    
    def generate_revision_report(self, revisions: List[AIRevisionSuggestion], results: Dict[str, bool]) -> str:
        """Generate a comprehensive revision report"""
        report = ["# AI Code Revision Report\n"]
        
        successful = sum(1 for success in results.values() if success)
        total = len(revisions)
        
        report.append(f"## Summary")
        report.append(f"- Total revisions: {total}")
        report.append(f"- Successfully applied: {successful}")
        report.append(f"- Failed: {total - successful}")
        report.append("")
        
        for revision in revisions:
            status = "✅ Applied" if results.get(revision.file_path, False) else "❌ Failed"
            
            report.append(f"## {status}: {revision.file_path}")
            report.append(f"**Change Type:** {revision.change_type}")
            report.append(f"**Confidence:** {revision.confidence_score:.2f}")
            report.append(f"**Addresses Tests:** {', '.join(revision.addresses_test_ids)}")
            report.append(f"**Explanation:** {revision.explanation}")
            report.append("")
            
            if revision.original_code and revision.revised_code:
                report.append("**Original Code:**")
                report.append(f"```\n{revision.original_code}\n```")
                report.append("")
                report.append("**Revised Code:**")
                report.append(f"```\n{revision.revised_code}\n```")
                report.append("")
        
        return "\n".join(report)

# Example usage
if __name__ == "__main__":
    # Initialize the revision engine
    engine = OpenAIRevisionEngine()
    
    # Analyze and fix failures
    project_root = "/Users/luxin/Desktop/SF AI Hackathon 2025/bugsy"
    report_path = "/Users/luxin/Desktop/SF AI Hackathon 2025/bugsy/testsprite_tests/tmp/test_results.json"
    
    print("🔍 Analyzing test failures with AI...")
    revisions = engine.analyze_and_fix_failures(report_path, project_root)
    
    if revisions:
        print(f"\n🤖 Generated {len(revisions)} AI-powered revisions:")
        for i, revision in enumerate(revisions, 1):
            print(f"  {i}. {revision.file_path} ({revision.change_type})")
            print(f"     Confidence: {revision.confidence_score:.2f}")
            print(f"     Addresses: {', '.join(revision.addresses_test_ids)}")
        
        # Apply revisions
        print("\n🔧 Applying revisions...")
        results = engine.apply_revisions(revisions)
        
        # Generate report
        report = engine.generate_revision_report(revisions, results)
        
        # Save report
        report_file = os.path.join(project_root, "ai_revision_report.md")
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Revision report saved to: {report_file}")
    else:
        print("\n❌ No revisions generated. Check test report and API key.")