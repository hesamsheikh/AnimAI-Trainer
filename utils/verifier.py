import ast
import sys
import tempfile
import os
import importlib.util
import subprocess
import shutil
from pathlib import Path

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
    # Check for valid Python syntax first
    try:
        ast.parse(code_string)
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"
    
    # Create temporary directory for Manim files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Create a manim.cfg configuration file with minimal settings
        config_path = temp_dir_path / "manim.cfg"
        with open(config_path, "w") as config_file:
            config_file.write("""[CLI]
            media_dir = {}
            log_to_file = False
            verbosity = ERROR
            """.format(str(temp_dir_path / "media")))
        
        # Create a temporary Python file with the Manim code
        script_path = temp_dir_path / "temp_script.py"
        with open(script_path, "w") as script_file:
            script_file.write(code_string)
        
        try:
            # Run manim with --dry_run to check if it compiles correctly without rendering
            cmd = ["manim", "--dry_run", str(script_path)]
            
            # Capture output and errors
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(temp_dir_path)
            )
            
            # Check if the command failed
            if result.returncode != 0:
                error_output = result.stderr if result.stderr else result.stdout
                return False, f"Compilation error: {error_output}"
                
        except Exception as e:
            return False, f"Error during compilation check: {str(e)}"
    
    return True, ""

