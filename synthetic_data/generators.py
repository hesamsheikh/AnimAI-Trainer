import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import scene_script_prompt_template

class SceneScriptor:
    def __init__(self, model_name):
        load_dotenv()

        self.model_name = model_name
        
        # Get API key from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        self.prompt_template = scene_script_prompt_template

    def generate_response(self, prompt):
        # Generate response using OpenAI API
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content

    def __call__(self, user_prompt):
        prompt = self.prompt_template.format(user_prompt)
        return self.generate_response(prompt)


def main():
    # Example prompt
    user_prompt = "Explain the concept of derivatives using geometric intuition"
    
    # Model configuration
    model_name = "gpt-4o-mini"
    
    # Initialize and call generator
    generator = SceneScriptor(model_name)
    scene_script = generator(user_prompt)
    
    print(scene_script)

if __name__ == "__main__":
    main()
