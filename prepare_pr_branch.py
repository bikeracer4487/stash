#!/usr/bin/env python3
"""
Script to prepare a PR branch by:
1. Creating/recreating PR-branch
2. Syncing README.md with parent repo
3. Removing Claude-specific files from git tracking
4. Switching back to develop branch
"""

import subprocess
import os
import sys
import urllib.request

def run_command(cmd, check=True):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.stderr.strip(), e.returncode

def branch_exists(branch_name):
    """Check if a branch exists locally."""
    stdout, _, returncode = run_command(f"git rev-parse --verify {branch_name}", check=False)
    return returncode == 0

def delete_branch(branch_name):
    """Delete a branch if it exists."""
    if branch_exists(branch_name):
        print(f"Deleting existing branch '{branch_name}'...")
        # First switch to a different branch if we're on the branch to delete
        current_branch, _, _ = run_command("git branch --show-current")
        if current_branch == branch_name:
            run_command("git checkout develop")
        
        # Delete the branch
        run_command(f"git branch -D {branch_name}")
        print(f"Branch '{branch_name}' deleted.")

def create_and_checkout_branch(branch_name):
    """Create and checkout a new branch."""
    print(f"Creating and checking out new branch '{branch_name}'...")
    run_command(f"git checkout -b {branch_name}")
    print(f"Switched to new branch '{branch_name}'.")

def sync_readme():
    """Sync README.md with the parent repository."""
    print("Syncing README.md with parent repository...")
    parent_readme_url = "https://raw.githubusercontent.com/stashapp/stash/develop/README.md"
    
    try:
        # Download the parent repo's README
        with urllib.request.urlopen(parent_readme_url) as response:
            readme_content = response.read().decode('utf-8')
        
        # Write to local README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("README.md synced successfully.")
    except Exception as e:
        print(f"Error syncing README.md: {e}")
        sys.exit(1)

def read_claude_files():
    """Read the list of Claude-specific files from CLAUDE_FILES.md."""
    try:
        with open('CLAUDE_FILES.md', 'r') as f:
            content = f.read().strip()
        
        # Extract file paths (skip empty lines)
        files = [line.strip() for line in content.split('\n') if line.strip()]
        return files
    except FileNotFoundError:
        print("CLAUDE_FILES.md not found. Creating with default files...")
        # Default Claude files if CLAUDE_FILES.md doesn't exist
        default_files = [
            "CLAUDE.md",
            "docs/WINDOWS_DEVELOPMENT_SETUP.md"
        ]
        with open('CLAUDE_FILES.md', 'w') as f:
            f.write('\n'.join(default_files))
        return default_files

def remove_from_git_tracking(file_path):
    """Remove a file from git tracking without deleting it."""
    if os.path.exists(file_path):
        print(f"Removing '{file_path}' from git tracking...")
        stdout, stderr, returncode = run_command(f"git rm --cached {file_path}", check=False)
        if returncode == 0:
            print(f"  ✓ Removed from tracking")
        else:
            # File might not be tracked
            print(f"  - Not tracked in git (skipping)")
    else:
        print(f"  - File '{file_path}' does not exist (skipping)")

def main():
    """Main function to orchestrate the PR branch preparation."""
    print("=== PR Branch Preparation Script ===\n")
    
    # Store current branch to return if needed
    original_branch, _, _ = run_command("git branch --show-current")
    
    try:
        # Step 1: Check for PR-branch and create/recreate it
        pr_branch = "PR-branch"
        delete_branch(pr_branch)
        create_and_checkout_branch(pr_branch)
        
        # Step 2: Sync README.md
        sync_readme()
        
        # Step 3: Remove Claude files from git tracking
        print("\nRemoving Claude-specific files from git tracking...")
        claude_files = read_claude_files()
        
        # Add CLAUDE_FILES.md itself to the list
        if "CLAUDE_FILES.md" not in claude_files:
            claude_files.append("CLAUDE_FILES.md")
        
        for file_path in claude_files:
            remove_from_git_tracking(file_path)
        
        # Step 4: Remove this script from git tracking
        script_name = os.path.basename(__file__)
        print(f"\nRemoving script '{script_name}' from git tracking...")
        remove_from_git_tracking(script_name)
        
        # Step 5: Switch back to develop branch
        print(f"\nSwitching back to 'develop' branch...")
        run_command("git checkout develop")
        
        print("\n=== PR branch preparation complete! ===")
        print(f"- Created clean PR-branch")
        print(f"- README.md synced with parent repo")
        print(f"- Claude-specific files removed from git tracking")
        print(f"- Switched back to develop branch")
        print(f"\nTo use the PR branch: git checkout PR-branch")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        # Try to switch back to original branch
        if original_branch:
            run_command(f"git checkout {original_branch}", check=False)
        sys.exit(1)

if __name__ == "__main__":
    main()