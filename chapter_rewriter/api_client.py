import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, Optional, Tuple

# Load environment variables from .env file
load_dotenv()

class DeepSeekAPI:
    def __init__(self):
        """Initialize the DeepSeek API client."""
        api_key = os.getenv("API_KEY")
        base_url = os.getenv("BASE_URL", "https://api.deepseek.com/v1")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        
        if not api_key:
            raise ValueError("API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = os.getenv("MODEL_NAME")
        if not self.model:
            raise ValueError("MODEL_NAME environment variable is not set")
    
    def generate_response(self, prompt: str, memory_context: str = "", max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate a response from the DeepSeek Reasoner model.
        
        Args:
            prompt: The input prompt
            memory_context: Optional context from previous chunks
            max_tokens: Maximum number of tokens for the response (overrides environment variable)
            
        Returns:
            Dictionary containing the reasoning_content and content
        """
        try:
            # Prepare the full prompt with memory context if provided
            full_prompt = f"Act as a professional technical editor working on a mathematics/physics textbook manuscript. Following is a draft, rewrite it into more understsabdable and fluent format, do not ignore any math formulas, clarify missing logics if needed. Paragraph: \n\n{prompt}"
            
            if memory_context:
                full_prompt = f"{memory_context}\n\n{full_prompt}"
                
            messages = [{"role": "user", "content": full_prompt}]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens if max_tokens is not None else self.max_tokens
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
            
    def parse_response(self, response: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        Parse the response from the API into answer and reasoning content.
        
        Args:
            response: The response dictionary from generate_response
            
        Returns:
            Tuple containing (answer, reasoning_content)
        """
        return response.get("content", ""), response.get("reasoning_content") 