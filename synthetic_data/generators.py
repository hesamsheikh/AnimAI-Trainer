import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import scene_script_prompt_template, manim_voice_code_prompt_template, manim_vanilla_code_prompt_template

class SceneScriptor:
    def __init__(self, model_name, base_url, api_key):
        load_dotenv()

        self.model_name = model_name
        
        # Get API key from environment
        self.api_key = api_key
        self.base_url = base_url
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.prompt_template = scene_script_prompt_template

    def generate_response(self, prompt):
        # Generate response using OpenAI API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content

    def __call__(self, user_prompt):
        prompt = self.prompt_template.format(user_prompt)
        response = self.generate_response(prompt)
        return response

class ManimCoder:
    def __init__(self, model_name, base_url, api_key, voiceover=False):
        load_dotenv()
        
        self.voiceover = voiceover
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        # Placeholder for prompt template that will be added later
        if self.voiceover:
            self.prompt_template = manim_voice_code_prompt_template
        else:
            self.prompt_template = manim_vanilla_code_prompt_template

    def generate_response(self, prompt):
        # Generate response using OpenAI API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.6,
            top_p=0.95
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content

    def __call__(self, scene_script, user_prompt):
        prompt = self.prompt_template.format(user_prompt=user_prompt, scene_script=scene_script)
        response = self.generate_response(prompt)
        return response


def main():
    # Example prompt
    user_prompt = "Explain the concept of derivatives using geometric intuition"
    
    # Model configuration
    model_name_scene_script = "deepseek-chat"
    model_name_manim_code = "deepseek-chat"
    base_url = "https://api.deepseek.com"
    api_key = os.getenv('DEEPSEEK_API_KEY')

    # Generate scene script first
    scene_generator = SceneScriptor(model_name_scene_script, base_url, api_key)
    code_generator = ManimCoder(model_name_manim_code, base_url, api_key, voiceover=False)
    
    scene_script = scene_generator(user_prompt)

    print("Scene Script:")
    print(scene_script)

    # Generate Manim code based on scene script
    manim_code = code_generator(scene_script, user_prompt)
    
    print("\nManim Code:")
    print(manim_code)

if __name__ == "__main__":
    main()
