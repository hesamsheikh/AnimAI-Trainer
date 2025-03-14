import os
import time
from glob import glob
from generators import SceneScriptor, ManimCoder, ManimCritic
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.code_utils import eval_manim_code
from dotenv import load_dotenv
from prompts import example_scene_script


def extract_code(response):
    """Extract code between ```python and ``` tags"""
    if "```python" in response and "```" in response:
        code = response.split("```python")[1].split("```")[0]
        return code.strip()
    return response

def run_pipeline(user_prompt):
    """
    Runs the full pipeline to generate and validate Manim animations.
    
    The pipeline maintains conversation history with the ManimCoder to enable
    iterative improvements and error corrections without losing context.
    
    Args:
        user_prompt (str): The user's prompt describing the concept to visualize
        
    Returns:
        bool: Whether the pipeline completed successfully
    """
    # Load environment variables
    load_dotenv()
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

    # Initialize generators
    scene_scriptor = SceneScriptor(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        stream=True
    )
    
    # Only enable history saving for ManimCoder
    # deepseek/deepseek-r1-distill-llama-70b:free
    # google/gemini-2.0-pro-exp-02-05:free BEST
    manim_coder = ManimCoder(
        model_name="google/gemini-2.0-pro-exp-02-05:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        voiceover=False,
        stream=True,
        save_history=True  # Enable conversation history
    )
    
    critic = ManimCritic(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        stream=True
    )

    # Generate initial scene script
    print("\nGenerating scene script...")
    # scene_script = scene_scriptor(user_prompt)
    scene_script = example_scene_script


    print("\nScene script generated.")

    iteration = 0
    max_iterations = 5
    done = False
    code_iterations = 0
    max_code_iterations = 5

    while not done and iteration < max_iterations:
        iteration += 1
        print(f"\nIteration {iteration}")

        # Reset code iterations for each new scene script
        code_iterations = 0
        manim_coder.clear_history()  # Clear conversation history for new scene script
        
        # Generate Manim code
        print("\nGenerating Manim code...")
        manim_code = manim_coder(scene_script=scene_script, user_prompt=user_prompt)
        manim_code = extract_code(manim_code)
        print("\nManim code generated.")

        # Try to fix code if it has errors, up to max_code_iterations
        while code_iterations < max_code_iterations:
            # Evaluate the code
            print("\nEvaluating Manim code...")
            success, details = eval_manim_code(manim_code, save_code_py=True)

            if success:
                print("\nCode evaluation successful!")
                break
                
            # Code has errors, try to fix it
            code_iterations += 1
            print(f"\nCode evaluation failed (attempt {code_iterations}/{max_code_iterations}).")
            print(f"Error: {details['error']}")
            
            if code_iterations >= max_code_iterations:
                print("\nReached maximum code fix attempts. Moving to a new scene script.")
                break

            # Debug conversation history
            print("\nDebugging conversation history before error fix:")
            manim_coder.debug_conversation_history()
                
            print("\nSending error back to ManimCoder for fixing...")
            error_message = details['error']
            manim_code = manim_coder(error_message=error_message, save_history=True)
            manim_code = extract_code(manim_code)
            
            print("\nFixed code generated.")

        # If we couldn't fix the code after max attempts, get a new scene script
        if not success:
            print("\nGenerating a new scene script with error context...")
            error_context = f"The previous scene script led to code that couldn't be fixed after {max_code_iterations} attempts. The error was: {details['error']}"
            scene_script = scene_scriptor(f"{error_context}\n\nPlease create a simpler scene script for: {user_prompt}")
            print("\nNew scene script generated.")
            continue

        if success:
            print("done.")
            break

        # IMPLEMENT LATER

if __name__ == "__main__":
    user_prompt = "Explain the concept of derivatives using geometric intuition"
    run_pipeline(user_prompt)

