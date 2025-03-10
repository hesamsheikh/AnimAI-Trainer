from manim import tempconfig
import sys
from io import StringIO
import inspect
from textwrap import dedent
import ast
import sys
import functools

def add_necessary_imports(code_string):
    """
    Adds required imports if they're not already present in the code.
    """
    required_imports = [
        "from manim import *",
        "import numpy as np",
        "from utils.bounding_box import create_bounding_box, check_mobject_overlaps"
    ]
    
    existing_imports = [line.strip() for line in code_string.split('\n') if line.strip().startswith(('import', 'from'))]
    
    new_imports = []
    for imp in required_imports:
        if imp not in existing_imports:
            new_imports.append(imp)
    
    if new_imports:
        return '\n'.join(new_imports) + '\n\n' + code_string
    return code_string

def inject_overlap_check(code_string):
    """
    Injects overlap checking code after self.play calls, except for FadeOut.
    """
    lines = code_string.split('\n')
    modified_lines = []
    i = 0
    line_number = 0  # Track actual line numbers

    
    while i < len(lines):
        line = lines[i]
        modified_lines.append(line)
        line_number += 1

        # Functions that we don't want to check for overlaps after
        ignore_functions = ['FadeOut']
        
        # Check if line contains self.play and none of the ignored functions
        if 'self.play' in line and not any(func in line for func in ignore_functions):
            # Look ahead to find the end of the self.play statement
            next_i = i + 1
            open_parens = line.count('(') - line.count(')')
            
            while open_parens > 0 and next_i < len(lines):
                modified_lines.append(lines[next_i])
                line_number += 1
                open_parens += lines[next_i].count('(') - lines[next_i].count(')')
                i = next_i
                next_i += 1
            
            # Get the indentation of the self.play line
            indentation = len(line) - len(line.lstrip())
            indent = ' ' * indentation
            
            # Add a blank line before overlap check
            modified_lines.append("")
            # Add the overlap check with proper indentation and line number capture
            modified_lines.append(f"{indent}self.overlap_objects = check_mobject_overlaps(self)")
            modified_lines.append(f"{indent}if self.overlap_objects:")
            modified_lines.append(f"{indent}    self.overlap_line = {line_number}")  # Store line number
            modified_lines.append(f"{indent}    return")
            # Add a blank line after overlap check
            modified_lines.append("")
            line_number += 6  # Account for the added lines
        
        i += 1
    
    return '\n'.join(modified_lines)

def remove_wait_calls(code_string):
    """
    Removes all self.wait() calls from the code.
    
    Args:
        code_string (str): Original Manim code string
        
    Returns:
        str: Code string with self.wait() calls removed
    """
    lines = code_string.split('\n')
    return '\n'.join(line for line in lines if not line.strip().startswith('self.wait'))


def get_tempconfig_settings():
    """Returns the default tempconfig settings as a dictionary"""
    return {
        "quality": "low_quality",
        "frame_rate": 1,
        "preview": False,
        "format": "png",
        "disable_caching": True,
        "write_to_movie": False,
        "save_last_frame": False,
        "verbosity": "ERROR",
        # "dry_run": True,
    }

def find_scene_class_name(code_string):
    """
    Finds the name of the Scene class in the code.
    
    Args:
        code_string (str): Original Manim code string
        
    Returns:
        str: Name of the Scene class, or None if not found
    """
    import re
    # Look for class definition that inherits from Scene
    match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code_string)
    if match:
        return match.group(1)
    return None

def template_scene():
    """
    with tempconfig({CONFIG}):
        # Create scene instance
        scene = {SCENE_CLASS}()
        scene.render()
    """
    pass

def add_tempconfig(code_string):
    """
    Adds tempconfig settings to the code if not already present.
    
    Args:
        code_string (str): Original Manim code string
        
    Returns:
        str: Code string with tempconfig added
    """
    if "tempconfig" not in code_string:
        # Get the scene class name
        scene_class = find_scene_class_name(code_string)
        if not scene_class:
            return False
            
        # Get the template from the docstring
        template = dedent(template_scene.__doc__)
        
        # Convert config dictionary to a formatted string
        config_dict = get_tempconfig_settings()
        config_str = "{\n    " + ",\n    ".join(
            f'"{k}": {repr(v)}' for k, v in config_dict.items()
        ) + "\n}"
        
        # Replace the placeholders
        template = template.replace("{CONFIG}", config_str)
        template = template.replace("{SCENE_CLASS}", scene_class)
        
        # Add the template to the original code
        code_string += "\n" + template
        
    return code_string

def add_result_return(code_string):
    """
    Adds lines to store both overlap_objects and overlap_line in return_dict.
    """
    return_lines = """
    # Store the results in the provided return_dict
    return_dict['result'] = getattr(scene, 'overlap_objects', None)
    return_dict['line_number'] = getattr(scene, 'overlap_line', None)
    """
    return code_string + return_lines

def process_manim_code(code_string):
    """
    Processes a Manim code string by:
    1. Adding necessary imports
    2. Injecting overlap checking code after self.play calls 
    3. Removing self.wait() calls
    4. Adding tempconfig settings
    5. Adding result return line
    
    Args:
        code_string (str): Original Manim code string
        
    Returns:
        str: Processed Manim code string
    """
    code_string = add_necessary_imports(code_string)
    code_string = remove_wait_calls(code_string)
    code_string = inject_overlap_check(code_string)
    code_string = add_tempconfig(code_string)
    if not code_string: return False
    code_string = add_result_return(code_string)
    return code_string

def run_manim_code(code_string, save_code_py=False):
    """
    Executes a string containing Manim code.
    
    Args:
        code_string (str): A string containing valid Manim Python code.
        save_code_py (bool): If True, saves the processed code to a Python file in the temp folder.
            Defaults to False.
        
    Returns:
        tuple: (success, output, error) where:
            - success (bool): True if execution was successful, False otherwise
            - output (str): Standard output captured during execution
            - error (str): Error message if execution failed, empty string otherwise
    """
    # Save original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # Create string buffers to capture output
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    
    # Redirect stdout and stderr
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer
    
    success = True
    
    try:
        # Process the code string
        code_string = process_manim_code(code_string)
        if not code_string: return False, "", 
        "manim code processing failed, code likely has errors", None
        
        # Save processed code if requested
        if save_code_py:
            import os
            
            # Create temp directory if it doesn't exist
            temp_dir = 'temp'
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save code to file with UTF-8 encoding
            temp_file = os.path.join(temp_dir, 'manim_scene.py')
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code_string)
        
        # Create a dictionary that will be used to return values
        globals_dict = {'return_dict': {}}

        # Compile the code to catch syntax errors
        compiled_code = compile(code_string, '<string>', 'exec')
        
        # Execute the code
        exec(compiled_code, globals_dict)
        
    except Exception as e:
        success = False
        print(f"Error executing Manim code: {str(e)}")
    
    finally:
        # Get the output
        output = stdout_buffer.getvalue()
        log = stderr_buffer.getvalue()

        # Get the result from the return dictionary
        overlap_result = globals_dict['return_dict'].get('result')
        line_number = globals_dict['return_dict'].get('line_number')

        # Get the last two lines before the overlap line number
        if line_number:
            code_lines = code_string.split('\n')
            context_lines = code_lines[max(0, line_number-2):line_number]

        # Restore original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        # Close the buffers
        stdout_buffer.close()
        stderr_buffer.close()

    return success, {
        'output': output,
        'log': log,
        'overlap_result': overlap_result,
        'line_number': line_number,
        'context_lines': context_lines
    }

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
    if "class " not in code_string or "Scene" not in code_string:
        return False, "No Scene subclass found"
    
    return True, ""

@functools.lru_cache(maxsize=256)
def eval_manim_code(code_string):
    """
    Verifies the syntax and renderability of Manim code by running it
    
    Args:
        code_string (str): The Manim code to verify
        
    Returns:
        tuple: (is_valid, error_message) where:
            - is_valid (bool): True if the code passes all checks, False otherwise
            - error_message (str): Description of any errors found, empty if is_valid is True
    """

    # Run quick checks first to avoid expensive processing for obvious errors
    quick_valid, quick_error = quick_syntax_check(code_string)
    if not quick_valid:
        return False, {"error": quick_error, "result": None}

    # Run the code through code_utils
    success, details = run_manim_code(code_string, save_code_py=False)
    
    return success, details
