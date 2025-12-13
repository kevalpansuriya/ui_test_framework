"""
Script to run linting checks locally
"""
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(command, shell=True, capture_output=False)
    return result.returncode == 0


def main():
    """Main function to run all linting checks"""
    print("Starting linting checks...")
    
    # Check if flake8 and pylint are installed
    try:
        subprocess.run(["flake8", "--version"], capture_output=True, check=True)
        subprocess.run(["pylint", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: flake8 or pylint not found. Please install dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    all_passed = True
    
    # Run flake8 critical errors check
    if not run_command(
        "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics",
        "flake8 - Critical errors"
    ):
        print("\n❌ Critical errors found!")
        all_passed = False
    else:
        print("\n✅ No critical errors found")
    
    # Run flake8 all checks
    if not run_command(
        "flake8 . --count --max-complexity=10 --max-line-length=120 --statistics",
        "flake8 - All checks (max line length: 120)"
    ):
        print("\n❌ flake8 issues found!")
        all_passed = False
    else:
        print("\n✅ flake8 checks passed")
    
    # Run flake8 unused variables check
    if not run_command(
        "flake8 . --select=F841 --show-source --statistics",
        "flake8 - Unused variables check"
    ):
        print("\n❌ Unused variables found!")
        all_passed = False
    else:
        print("\n✅ No unused variables found")
    
    # Run pylint
    print(f"\n{'='*60}")
    print("Running: pylint - Code quality check")
    print(f"{'='*60}\n")
    
    # Find all Python files
    python_files = []
    exclude_paths = {'.venv', 'venv', '__pycache__', '.pytest_cache', '.git', 'build', 'dist'}
    
    for py_file in Path('.').rglob('*.py'):
        if not any(excluded in py_file.parts for excluded in exclude_paths):
            python_files.append(str(py_file))
    
    if python_files:
        files_str = ' '.join(python_files)
        if not run_command(
            f"pylint --rcfile=.pylintrc --fail-under=7.0 {files_str}",
            "pylint - Code quality (camelCase naming, unused variables)"
        ):
            print("\n❌ pylint issues found!")
            all_passed = False
        else:
            print("\n✅ pylint checks passed")
    else:
        print("No Python files found to lint")
    
    # Final summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ All linting checks passed!")
        sys.exit(0)
    else:
        print("❌ Some linting checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

