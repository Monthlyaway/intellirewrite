import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables from .env file
load_dotenv()

class DeepSeekAPI:
    def __init__(self):
        """Initialize the DeepSeek API client."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = "deepseek-ai/DeepSeek-V2.5"
    
    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Generate a response from the DeepSeek Reasoner model.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens for the response
            
        Returns:
            Dictionary containing the reasoning_content and content
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            # Extract content
            content = response.choices[0].message.content
            
            # Check if reasoning_content exists
            reasoning_content = None
            if hasattr(response.choices[0].message, 'reasoning_content'):
                reasoning_content = response.choices[0].message.reasoning_content
            
            return {
                "reasoning_content": reasoning_content,
                "content": content
            }
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            # Return a mock response in case of error
            return {
                "reasoning_content": f"Error: {str(e)}",
                "content": "An error occurred while generating the response. Please try again later."
            } 