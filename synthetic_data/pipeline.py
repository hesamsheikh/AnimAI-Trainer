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
    
    The pipeline maintains conversation history with each model, allowing for
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
    
    manim_coder = ManimCoder(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        voiceover=False,
        stream=True
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
    max_code_iterations = 3

    while not done and iteration < max_iterations:
        iteration += 1
        print(f"\nIteration {iteration}")

        # Reset code iterations for each new scene script
        code_iterations = 0
        manim_coder.reset_conversation()  # Reset conversation for new scene script
        
        # Generate Manim code
        print("\nGenerating Manim code...")
        response = manim_coder(scene_script, user_prompt, continue_conversation=True)
        manim_code = extract_code(response)
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
                
            print("\nSending error back to ManimCoder for fixing...")
            response = manim_coder.fix_code_with_error(details['error'])
            manim_code = extract_code(response)
            print("\nFixed code generated.")

        # If we couldn't fix the code after max attempts, get a new scene script
        if not success:
            print("\nGenerating a new scene script with error context...")
            error_context = f"The previous scene script led to code that couldn't be fixed after {max_code_iterations} attempts. The error was: {details['error']}"
            scene_script = scene_scriptor(f"{error_context}\n\nPlease create a simpler scene script for: {user_prompt}", continue_conversation=True)
            print("\nNew scene script generated.")
            continue

        # Get generated images
        print("\nLooking for generated images...")
        image_files = glob("media/images/*/*.png")
        
        if not image_files:
            print("No images were generated. Retrying with a new scene script...")
            scene_script = scene_scriptor(f"The previous scene script didn't produce any images. Please create a simpler scene script for: {user_prompt}", continue_conversation=True)
            continue

        # Have critic evaluate each image
        print("\nCritiquing generated images...")
        critic.reset_conversation()  # Reset conversation for new images
        
        for image_path in image_files:
            critique = critic(image_path, user_prompt, scene_script, manim_code)
            
            # Check if the critic approved the animation
            if critique.startswith("Approved"):
                print("\nCritic approved the animation!")
                print(f"Approval message: {critique}")
                done = True
                break
            
            print("\nCritic suggested improvements. Updating scene script...")
            scene_script = scene_scriptor(f"Update this scene script based on the following critique: {critique}\nOriginal script: {scene_script}", continue_conversation=True)

    if not done:
        print("\nMaximum iterations reached without critic approval.")
    
    return done

if __name__ == "__main__":
    user_prompt = "Explain the concept of derivatives using geometric intuition"
    run_pipeline(user_prompt)

