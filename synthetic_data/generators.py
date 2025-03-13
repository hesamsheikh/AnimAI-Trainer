import os
import json
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
from prompts import (
    scene_script_prompt_template,
    manim_code_prompt_template,
    critic_prompt_template
)
import time
from PIL import Image
import base64
import io

class Generator:
    """
    Base class for all generators that use LLM APIs.
    Handles common functionality like API selection and response generation.
    """
    def __init__(self, model_name, api_key, api_type="openai", base_url=None, stream=False):
        """
        Initialize the generator with model and API details.
        
        Args:
            model_name (str): The name of the model to use
            api_key (str): The API key
            api_type (str): The type of API to use ('openai' or 'groq')
            base_url (str, optional): The base URL for the API (if needed)
            stream (bool): Whether to stream the response
        """
        load_dotenv()
        
        self.model_name = model_name
        self.api_key = api_key
        self.api_type = api_type.lower()
        self.base_url = base_url
        self.stream = stream
        
        # Initialize the appropriate client
        if self.api_type == "openai":
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url if base_url else None)
        elif self.api_type == "groq":
            self.client = Groq(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported API type: {api_type}. Use 'openai' or 'groq'.")
    
    def generate_response(self, prompt, max_tokens=4096, temperature=0.7, **kwargs):
        """
        Generate a response using the configured API.
        
        Args:
            prompt (str): The prompt to send to the API
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Temperature for response generation
            **kwargs: Additional parameters specific to the API
            
        Returns:
            str: The generated response
        """
        # Common parameters for both APIs
        params = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": self.stream
        }
        
        # Add API-specific parameters
        if self.api_type == "openai":
            params["max_tokens"] = max_tokens
        elif self.api_type == "groq":
            params["max_completion_tokens"] = max_tokens
            # Default Groq parameters that can be overridden
            params.setdefault("top_p", 0.95)

        
        # Add any additional parameters
        params.update(kwargs)
        
        # Generate response using API
        response = self.client.chat.completions.create(**params)
        
        # Handle streaming response
        if self.stream:
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            return full_response
            
        # Extract and return the generated text
        return response.choices[0].message.content


class SceneScriptor(Generator):
    """
    Generator for creating scene scripts from user prompts.
    """
    def __init__(self, model_name, api_key, api_type="openai", base_url=None, stream=False):
        super().__init__(model_name, api_key, api_type, base_url, stream)
        self.prompt_template = scene_script_prompt_template

    def __call__(self, user_prompt):
        """
        Generate a scene script based on the user prompt.
        
        Args:
            user_prompt (str): The user's prompt describing the concept to visualize
            
        Returns:
            str: The generated scene script
        """
        prompt = self.prompt_template.format(user_prompt)
        response = self.generate_response(prompt)
        return response


class ManimCoder(Generator):
    """
    Generator for creating Manim code from scene scripts.
    """
    def __init__(self, model_name, api_key, api_type="openai", base_url=None, voiceover=False, stream=False):
        super().__init__(model_name, api_key, api_type, base_url, stream)
        self.voiceover = voiceover
        
        # Select the appropriate prompt template
        self.prompt_template = manim_code_prompt_template

    def __call__(self, scene_script, user_prompt):
        """
        Generate Manim code based on the scene script and user prompt.
        
        Args:
            scene_script (str): The scene script to convert to code
            user_prompt (str): The original user prompt
            
        Returns:
            str: The generated Manim code
        """
        prompt = self.prompt_template.format(user_prompt=user_prompt, scene_script=scene_script)
        response = self.generate_response(prompt)
        return response


class ManimCritic(Generator):
    """
    Generator for critiquing Manim animations based on image frames.
    Uses vision-capable models for visual understanding.
    """
    def __init__(self, model_name, api_key, api_type="openai", base_url=None, stream=True):
        super().__init__(model_name, api_key, api_type, base_url, stream)

    def read_image(self, image_path):
        """
        Read an image file and convert it to base64.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Base64-encoded image data
        """
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        return image_b64
    
    def generate_response_with_image(self, prompt, image_data):
        """
        Generate a response based on text prompt and image data.
        
        Args:
            prompt (str): The text prompt
            image_data (str): Base64-encoded image data
            
        Returns:
            str: The generated response
        """
        # Format messages with image for vision models
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    }
                }
            ]}
        ]
        
        # Common parameters
        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "stream": self.stream
        }
        
        # Add API-specific parameters
        if self.api_type == "openai":
            params["max_tokens"] = 1024
        elif self.api_type == "groq":
            params["max_completion_tokens"] = 1024
        
        # Generate response
        response = self.client.chat.completions.create(**params)

        # Handle streaming response
        if self.stream:
            full_response = ""
            try:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        full_response += content
                return full_response
            except Exception as e:
                print(f"Error during streaming: {str(e)}")
                return None

        return response.choices[0].message.content

    def __call__(self, image_path, user_prompt, scene_script, manim_code):
        """
        Generate a critique of a Manim animation frame.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: The generated critique
        """
        image_data = self.read_image(image_path)
        prompt = critic_prompt_template.format(user_prompt=user_prompt,
                                            scene_script=scene_script, 
                                            manim_code=manim_code)
        return self.generate_response_with_image(prompt, image_data)


def main():
    # Load environment variables
    load_dotenv()
    
    # Example prompt
    user_prompt = "Explain the concept of derivatives using geometric intuition"

    # Example usage of SceneScriptor
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    scene_scriptor = SceneScriptor(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        stream=True
    )
    
    # Example usage of ManimCoder with Groq
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    manim_coder = ManimCoder(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai",
        base_url="https://openrouter.ai/api/v1",
        voiceover=False,
        stream=True
    )
    
    # Example usage of ManimCritic with OpenRouter
    openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
    critic = ManimCritic(
        model_name="google/gemma-3-27b-it:free",
        api_key=openrouter_api_key,
        api_type="openai", 
        base_url="https://openrouter.ai/api/v1",
        stream=True
    )
    
    # Example of running the pipeline
    start_time = time.time()
    
    # Step 1: Generate scene script
    print("Generating scene script...")
    scene_script = scene_scriptor(user_prompt)
    print("\n\nScene script generated.\n")
    
    # Step 2: Generate Manim code
    print("Generating Manim code...")
    manim_code = manim_coder(scene_script, user_prompt)
    print("\n\nManim code generated.\n")
    
    # Step 3: Critique an image (assuming it exists)
    print("Generating critique...")
    image_feedback = critic(r"media\images\test\DerivativeGeometricIntuition0009.png",
                            user_prompt,
                            scene_script,
                            manim_code)
    print("\n\nCritique generated.\n")
    
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
