from manim import tempconfig
import sys
from io import StringIO

def run_manim_code(code_string):
    """
    Executes a string containing Manim code.
    
    Args:
        code_string (str): A string containing valid Manim Python code.
        
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
        # Add the tempconfig to the code if it's not already there
        if "tempconfig" not in code_string:
            code_string += """

with tempconfig({
    "quality": "low_quality", 
    "frame_rate": 1, 
    "preview": False, 
    "format": "png",
    "disable_caching": True, 
    "write_to_movie": False, 
    "save_last_frame": False,
    "verbosity": "ERROR"
    }):
    # Create a scene with a fixed name
    scene = MainScene()
    scene.render()
"""
        
        # Replace any Scene class name with MainScene before compiling
        import re
        code_string = re.sub(r'class\s+(\w+)\s*\(\s*Scene\s*\)', r'class MainScene(Scene)', code_string)
        
        # Compile the code to catch syntax errors
        compiled_code = compile(code_string, '<string>', 'exec')
        
        # Execute the code
        exec(compiled_code, {})
        
    except Exception as e:
        success = False
        print(f"Error executing Manim code: {str(e)}")
    
    finally:
        # Get the output
        output = stdout_buffer.getvalue()
        error = stderr_buffer.getvalue()
        
        # Restore original stdout and stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        # Close the buffers
        stdout_buffer.close()
        stderr_buffer.close()
    
    return success, output, error
