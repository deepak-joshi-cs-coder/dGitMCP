"""

*** MCP Server ***

"""

from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP(name="MCP Server")

@mcp.tool()
def git_checkout(branch_name: str) -> str:
    """
    Checkout a git branch.

    Args:
        branch_name: Name of the branch to checkout
    """
    try:
        result = subprocess.run(['git', 'checkout',"-b", branch_name], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            return f"Successfully checked out branch: {branch_name}"
        else:
            return f"Error checking out branch: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def git_pull(remote: str = "origin") -> str:
    """
    Pull latest changes from remote repository.

    Args:
        remote: Remote repository name (default: origin)
    """
    try:
        result = subprocess.run(['git', 'pull', remote], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            return f"Successfully pulled latest changes from {remote}"
        else:
            return f"Error pulling changes: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def git_commit(message: str) -> str:
    """
    Commit changes with a message.

    Args:
        message: Commit message
    """
    try:
        status_result = subprocess.run(['git', 'diff', '--cached', '--quiet'],
                                     capture_output=True)
        
        if status_result.returncode == 1:
            commit_result = subprocess.run(['git', 'commit', '-m', message], 
                                         capture_output=True, 
                                         text=True)
            if commit_result.returncode == 0:
                return f"Successfully committed changes with message: {message}"
            else:
                return f"Error committing changes: {commit_result.stderr}"
        else:
            return "No changes staged for commit. Use git_add first to stage your changes."
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def git_push(remote: str = "origin", branch: str = "") -> str:
    """
    Push commits to remote repository.

    Args:
        remote: Remote repository name (default: origin)
        branch: Branch to push (default: current branch)
    """
    try:
        cmd = ['git', 'push', remote]
        if branch:
            cmd.append(branch)
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Successfully pushed changes to {remote}"
        else:
            return f"Error pushing changes: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def git_status() -> str:
    """
    Get the current git status.
    """
    try:
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error getting status: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def git_add(files: list[str]) -> str:
    """
    Add specific files to git staging area.

    Args:
        files: List of file paths to stage. Use ["all"] or ["."] to stage all changes.
    """
    try:
        if len(files) == 1 and files[0].lower() in ["all", "."]:
            cmd = ['git', 'add', '.']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                status = subprocess.run(['git', 'status', '--porcelain'], 
                                     capture_output=True, 
                                     text=True)
                if status.stdout:
                    return f"Successfully staged all changes:\n{status.stdout}"
                return "No changes to stage"
            else:
                return f"Error staging all files: {result.stderr}"
        
        cmd = ['git', 'add'] + files
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Successfully staged files: {', '.join(files)}"
        else:
            return f"Error staging files: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.settings.port = 3005
    mcp.run(transport="sse")