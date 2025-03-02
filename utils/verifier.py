import ast
import sys
import tempfile
import os
import importlib.util
import subprocess
import shutil
import functools
from pathlib import Path

# Quick pre-checks before running expensive Manim validation
def quick_syntax_check(code_string):
    """Perform quick syntax and basic structural checks before launching subprocess"""
    try:
        ast.parse(code_string)
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"
    
    # Basic check for manim imports
    if "from manim import" not in code_string and "import manim" not in code_string:
        return False, "Missing manim import"
    
    # Basic check for Scene subclass declaration
    if "class" not in code_string or "Scene" not in code_string:
        return False, "No Scene subclass found"
    
    return True, ""

@functools.lru_cache(maxsize=256)
def syntax_checker(code_string):
    """
    Verifies the syntax and renderability of Manim code by trying to run it with --dry_run
    
    Args:
        code_string (str): The Manim code to verify
        
    Returns:
        tuple: (is_valid, error_message) where:
            - is_valid (bool): True if the code passes all checks, False otherwise
            - error_message (str): Description of any errors found, empty if is_valid is True
    """
    # Run quick checks first to avoid expensive subprocess for obvious errors
    quick_valid, quick_error = quick_syntax_check(code_string)
    if not quick_valid:
        return False, quick_error
    
    # Create temporary directory for Manim files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Create a manim.cfg configuration file with optimized settings for speed
        config_path = temp_dir_path / "manim.cfg"
        with open(config_path, "w") as config_file:
            config_file.write("""[CLI]
            media_dir = {}
            log_to_file = False
            verbosity = ERROR
            
            [renderer]
            use_opengl_renderer = False
            
            [preview]
            disable_caching = True
            
            [logger]
            logging_keyword = None
            
            [output]
            flush_cache = False
            disable_caching = True
            
            [performance]
            skip_animations = True
            """.format(str(temp_dir_path / "media")))
        
        # Create a temporary Python file with the Manim code
        script_path = temp_dir_path / "temp_script.py"
        with open(script_path, "w") as script_file:
            script_file.write(code_string)
        
        try:
            # Run manim with --dry_run and additional performance flags
            cmd = [
                "manim", 
                "render",
                str(script_path),
                "--dry_run",
                "--disable_caching",
                "--format=png",
                "--quality=l",  # Use low quality for faster processing
                "--verbosity=ERROR"
            ]
            
            # Capture output and errors
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(temp_dir_path),
                env={**os.environ, "PYTHONOPTIMIZE": "2"}  # Add Python optimization
            )
            
            # Check if the command failed or if there's an error in the output
            if result.returncode != 0 or "ERROR" in result.stderr or "ERROR" in result.stdout:
                error_output = result.stderr if result.stderr else result.stdout
                return False, f"Compilation error: {error_output}"
                
        except Exception as e:
            return False, f"Error during compilation check: {str(e)}"
    
    return True, ""
