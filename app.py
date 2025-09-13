from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import json
import requests
import re
from pathlib import Path
import sys

# Load environment variables from get_test_stripe_plan/.env
from dotenv import load_dotenv
load_dotenv('./get_test_stripe_plan/.env')

sys.path.append('./get_test_stripe_plan')

# Import our existing bug solver functionality
from bug_solver import process_bug_report
from revision_engine import OpenAIRevisionEngine

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main upload page."""
    return render_template('index.html')

def fetch_github_issue(repo_url, issue_number):
    """Fetch GitHub issue details and convert to text format"""
    try:
        # Parse repository URL to extract owner and repo name
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?', repo_url.strip())
        if not match:
            raise ValueError("Invalid GitHub repository URL format")
        
        owner, repo = match.groups()
        
        # GitHub API endpoint for issues
        api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        
        # Make API request
        response = requests.get(api_url)
        response.raise_for_status()
        
        issue_data = response.json()
        
        # Convert issue to text format
        bug_text = f"""Title: {issue_data['title']}

Description:
{issue_data['body'] or 'No description provided'}

Labels: {', '.join([label['name'] for label in issue_data.get('labels', [])])}
State: {issue_data['state']}
Created: {issue_data['created_at']}
Updated: {issue_data['updated_at']}

URL: {issue_data['html_url']}
"""
        
        # Fetch comments if any
        if issue_data.get('comments', 0) > 0:
            comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
            comments_response = requests.get(comments_url)
            if comments_response.status_code == 200:
                comments = comments_response.json()
                if comments:
                    bug_text += "\n\nComments:\n"
                    for i, comment in enumerate(comments[:5], 1):  # Limit to first 5 comments
                        bug_text += f"\nComment {i} by {comment['user']['login']}:\n{comment['body']}\n"
        
        return bug_text
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch GitHub issue: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing GitHub issue: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process bug report."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .txt files are allowed'}), 400
        
        # Read file content
        bug_content = file.read().decode('utf-8')
        
        # Read the default prompt file
        prompt_file_path = Path('get_test_stripe_plan/prompt.txt')
        if not prompt_file_path.exists():
            return jsonify({'error': 'Prompt file not found'}), 500
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        
        # Process the bug report
        test_plan = process_bug_report(bug_content, prompt_content)
        
        # Convert to the exact format requested
        test_cases_list = []
        for test_case in test_plan.test_cases:
            test_case_dict = {
                "id": test_case.id,
                "title": test_case.title,
                "description": test_case.description,
                "category": test_case.category,
                "priority": test_case.priority,
                "steps": [{
                    "type": step.type,
                    "description": step.description
                } for step in test_case.steps]
            }
            test_cases_list.append(test_case_dict)
        
        # Save to test_plan.txt file (overwrite each time)
        test_plan_path = Path('get_test_stripe_plan/test_plan.txt')
        with open(test_plan_path, 'w', encoding='utf-8') as f:
            json.dump(test_cases_list, f, indent=2, ensure_ascii=False)
        
        # Also save to temporary file for download
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
            json.dump(test_cases_list, temp_file, indent=2, ensure_ascii=False)
            temp_file_path = temp_file.name
        
        return jsonify({
            'success': True,
            'message': 'Test plan generated successfully!',
            'test_cases': test_cases_list,
            'download_url': f'/download/{os.path.basename(temp_file_path)}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/github-issue', methods=['POST'])
def process_github_issue():
    """Handle GitHub issue processing."""
    try:
        data = request.get_json()
        repo_url = data.get('repo_url')
        issue_number = data.get('issue_number')
        
        if not repo_url or not issue_number:
            return jsonify({'error': 'Repository URL and issue number are required'}), 400
        
        # Fetch GitHub issue
        bug_content = fetch_github_issue(repo_url, issue_number)
        
        # Read the default prompt file
        prompt_file_path = Path('get_test_stripe_plan/prompt.txt')
        if not prompt_file_path.exists():
            return jsonify({'error': 'Prompt file not found'}), 500
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        
        # Process the bug report
        test_plan = process_bug_report(bug_content, prompt_content)
        
        # Convert to the exact format requested
        test_cases_list = []
        for test_case in test_plan.test_cases:
            test_case_dict = {
                "id": test_case.id,
                "title": test_case.title,
                "description": test_case.description,
                "category": test_case.category,
                "priority": test_case.priority,
                "steps": [{
                    "type": step.type,
                    "description": step.description
                } for step in test_case.steps]
            }
            test_cases_list.append(test_case_dict)
        
        # Save to test_plan.txt file (overwrite each time)
        test_plan_path = Path('get_test_stripe_plan/test_plan.txt')
        with open(test_plan_path, 'w', encoding='utf-8') as f:
            json.dump(test_cases_list, f, indent=2, ensure_ascii=False)
        
        # Also save to temporary file for download
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as temp_file:
            json.dump(test_cases_list, temp_file, indent=2, ensure_ascii=False)
            temp_file_path = temp_file.name
        
        return jsonify({
            'success': True,
            'message': f'GitHub issue analysis completed successfully with {len(test_cases_list)} test cases!',
            'test_cases': test_cases_list,
            'download_url': f'/download/{os.path.basename(temp_file_path)}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated test plan file."""
    try:
        temp_file_path = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(temp_file_path):
            return send_file(temp_file_path, as_attachment=True, download_name='test_plan.txt')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/revise-code', methods=['POST'])
def revise_code():
    """Analyze TestSprite report and generate AI-powered code revisions."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Get report path - can be from uploaded file or existing report
        report_path = data.get('report_path')
        apply_fixes = data.get('apply_fixes', False)  # Whether to automatically apply fixes
        
        if not report_path:
            # Check if there's a default test results file
            default_report = os.path.join(os.getcwd(), 'testsprite_tests', 'tmp', 'test_results.json')
            if os.path.exists(default_report):
                report_path = default_report
            else:
                return jsonify({'error': 'No test report provided and no default report found'}), 400
        
        # Validate report file exists
        if not os.path.exists(report_path):
            return jsonify({'error': f'Test report file not found: {report_path}'}), 404
        
        # Initialize revision engine
        try:
            engine = OpenAIRevisionEngine()
        except ValueError as e:
            return jsonify({'error': f'OpenAI API configuration error: {str(e)}'}), 500
        
        # Analyze failures and generate revisions
        project_root = os.getcwd()
        revisions = engine.analyze_and_fix_failures(report_path, project_root)
        
        if not revisions:
            return jsonify({
                'success': True,
                'message': 'No code revisions needed - all tests are passing or no fixable issues found',
                'revisions': [],
                'applied': False
            })
        
        # Convert revisions to JSON-serializable format
        revisions_data = []
        for revision in revisions:
            revision_dict = {
                'file_path': revision.file_path,
                'original_code': revision.original_code,
                'revised_code': revision.revised_code,
                'explanation': revision.explanation,
                'confidence_score': revision.confidence_score,
                'addresses_test_ids': revision.addresses_test_ids,
                'change_type': revision.change_type
            }
            
            # Add git diff if available
            if revision.git_diff:
                revision_dict['git_diff'] = {
                    'unified_diff': revision.git_diff.unified_diff,
                    'additions': revision.git_diff.additions,
                    'deletions': revision.git_diff.deletions
                }
            
            revisions_data.append(revision_dict)
        
        # Apply fixes if requested
        applied_results = {}
        if apply_fixes:
            applied_results = engine.apply_revisions(revisions, backup=True)
            
            # Generate and save revision report
            report_content = engine.generate_revision_report(revisions, applied_results)
            report_filename = f"revision_report_{int(os.path.getmtime(report_path))}.md"
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(report_content)
                temp_report_path = temp_file.name
            
            return jsonify({
                'success': True,
                'message': f'Generated and applied {len(revisions)} AI-powered code revisions',
                'revisions': revisions_data,
                'applied': True,
                'results': applied_results,
                'report_download_url': f'/download/{os.path.basename(temp_report_path)}'
            })
        else:
            return jsonify({
                'success': True,
                'message': f'Generated {len(revisions)} AI-powered code revision suggestions',
                'revisions': revisions_data,
                'applied': False
            })
        
    except Exception as e:
        return jsonify({'error': f'Code revision failed: {str(e)}'}), 500

@app.route('/apply-revision', methods=['POST'])
def apply_single_revision():
    """Apply a single code revision."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract revision data
        file_path = data.get('file_path')
        original_code = data.get('original_code')
        revised_code = data.get('revised_code')
        
        if not all([file_path, original_code, revised_code]):
            return jsonify({'error': 'Missing required fields: file_path, original_code, revised_code'}), 400
        
        # Validate file exists
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404
        
        # Create backup
        backup_path = f"{file_path}.backup"
        with open(file_path, 'r') as original:
            with open(backup_path, 'w') as backup_file:
                backup_file.write(original.read())
        
        # Read current file
        with open(file_path, 'r') as f:
            current_content = f.read()
        
        # Apply revision
        if original_code in current_content:
            new_content = current_content.replace(original_code, revised_code, 1)
            
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            return jsonify({
                'success': True,
                'message': f'Successfully applied revision to {file_path}',
                'backup_created': backup_path
            })
        else:
            return jsonify({'error': 'Original code not found in file - file may have been modified'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Failed to apply revision: {str(e)}'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)