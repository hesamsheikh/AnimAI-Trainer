import os
import json
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
from prompts import scene_script_prompt_template, manim_voice_code_prompt_template, manim_code_prompt_template_simple, exmaple_scene_script, manim_code_prompt_template
import time

class SceneScriptor:
    def __init__(self, model_name, base_url, api_key, stream=False):
        load_dotenv()

        self.model_name = model_name
        self.stream = stream
        
        # Get API key from environment
        self.api_key = api_key
        self.base_url = base_url
        
        # Initialize client
        # self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.client = Groq(api_key=self.api_key)
        self.prompt_template = scene_script_prompt_template

    def generate_response(self, prompt):
        # Generate response using API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7,
            stream=self.stream
        )
        
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

    def __call__(self, user_prompt):
        prompt = self.prompt_template.format(user_prompt)
        response = self.generate_response(prompt)
        return response

class ManimCoder:
    def __init__(self, model_name, base_url, api_key, voiceover=False, stream=False):
        load_dotenv()
        
        self.voiceover = voiceover
        self.stream = stream
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        
        # Initialize client
        # self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.client = Groq(api_key=self.api_key)
        # Placeholder for prompt template that will be added later
        if self.voiceover:
            self.prompt_template = manim_voice_code_prompt_template
        else:
            self.prompt_template = manim_code_prompt_template_simple

    def generate_response(self, prompt):
        # Generate response using API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=131072,
            temperature=0.6,
            top_p=0.95,
            top_k=40,
            stream=self.stream,
            repetition_penalty=1.1,
            min_p=0.1
        )
        
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

    def __call__(self, scene_script, user_prompt):
        prompt = self.prompt_template.format(user_prompt=user_prompt, scene_script=scene_script)
        response = self.generate_response(prompt)
        return response


def main():
    # Example prompt
    user_prompt = "Explain the concept of derivatives using geometric intuition"
    
    # Model configuration
    # model_name_scene_script = "deepseek-chat"
    # model_name_manim_code = "deepseek-chat"
    # base_url = "https://api.deepseek.com"
    # api_key = os.getenv('DEEPSEEK_API_KEY')

    model_name_scene_script = "qwen-qwq-32b"
    model_name_manim_code = "qwen-qwq-32b"
    base_url = "https://api.grok.com"
    api_key = os.getenv('GROQ_API_KEY')


    start_time = time.time()
    # Generate scene script first
    scene_generator = SceneScriptor(model_name_scene_script, base_url, api_key, stream=True)
    code_generator = ManimCoder(model_name_manim_code, base_url, api_key, voiceover=False, stream=True)
    
    scene_script = scene_generator(user_prompt)
    # scene_script = exmaple_scene_script

    # print("Scene Script:")
    # print(scene_script)

    # Generate Manim code based on scene script
    manim_code = code_generator(scene_script, user_prompt)
    
    # print("\nManim Code:")
    # print(manim_code)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
