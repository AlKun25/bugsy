#!/usr/bin/env python3
"""
Main CLI interface for the bug solver application.
This file handles command-line arguments and orchestrates the bug solving process.
"""

import os
import sys
import json
import argparse
from typing import NoReturn

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, continue without it

from bug_solver import process_bug_report, TestPlan





def validate_files(bug_file: str, prompt_file: str) -> None:
    """
    Validate that required input files exist.
    
    Args:
        bug_file: Path to the bug report file
        prompt_file: Path to the prompt template file
        
    Raises:
        SystemExit: If any required file is missing
    """
    if not os.path.exists(bug_file):
        print(f"Bug file not found: {bug_file}", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(prompt_file):
        print(f"Prompt file not found: {prompt_file}", file=sys.stderr)
        sys.exit(1)


def save_test_plan(test_plan: TestPlan) -> None:
    """
    Save the test plan to test_plan.txt file in the exact requested format.
    
    Args:
        test_plan: The TestPlan object to save
    """
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
    
    # Write to file with exact formatting
    with open('test_plan.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(test_cases_list, indent=2, ensure_ascii=False))


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description="Generate a bug fix plan with OpenAI using a prompt template and a bug input file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python main.py --bug_file bug.txt --prompt_file prompt.txt --pretty
  
File formats:
  - Bug file: First non-empty line = title; remainder = description
  - Prompt file: .txt or .docx with {bug_title} and {bug_description} placeholders
        """
    )
    
    parser.add_argument(
        "--bug_file",
        required=True,
        help="Path to a text file containing the bug. First non-empty line = title; remainder = description.",
    )
    
    parser.add_argument(
        "--prompt_file",
        required=True,
        help="Path to a .txt or .docx prompt template with {bug_title} and {bug_description} placeholders.",
    )
    

    
    return parser


def main() -> None:
    """
    Main entry point for the application.
    """
    try:
        # Parse command-line arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Validate files
        validate_files(args.bug_file, args.prompt_file)
        
        # Read the input files
        with open(args.bug_file, 'r', encoding='utf-8') as f:
            bug_content = f.read().strip()
        
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()
        
        # Process the bug report
        test_plan = process_bug_report(bug_content, prompt_content)
        
        # Save the test plan
        save_test_plan(test_plan)
        print("Test plan saved to test_plan.txt")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()