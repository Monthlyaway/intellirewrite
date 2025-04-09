import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, Optional, Tuple, List

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
    
    def generate_response(self, prompt: str, memory_context: List[Dict[str, str]] = None, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate a response from the DeepSeek Reasoner model.
        
        Args:
            prompt: The input prompt
            memory_context: Optional list of previous messages for context
            max_tokens: Maximum number of tokens for the response (overrides environment variable)
            
        Returns:
            Dictionary containing the reasoning_content and content
        """
        try:
            # Initialize messages with the system prompt
            system_prompt = "Act as a college professor working on an advanced robotics&deep learning textbook. You are good at making complex ideas simple and understandable. Following is a draft of one section, rewrite it into more understsabdable and fluent format. Do not ignore any math formulas, you need to explain the math like a math teacher, inventing formulas, analyze the idea behind them, not just introduce them. Clarify missing steps and concepts for your students. Do not say trivially or hint. Draft: "
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add memory context if provided
            if memory_context:
                messages.extend(memory_context)
            
            # Format the prompt with the content
            formatted_prompt = f"{system_prompt}\n\n{prompt}"
            messages.append({"role": "user", "content": formatted_prompt})
            
            # Make the API call
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
            
            # Return the response and the assistant's message for memory context
            return {
                "reasoning_content": reasoning_content,
                "content": content,
                "assistant_message": {"role": "assistant", "content": content}
            }
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            # Return a mock response in case of error
            return {
                "reasoning_content": f"Error: {str(e)}",
                "content": "An error occurred while generating the response. Please try again later.",
                "assistant_message": {"role": "assistant", "content": "An error occurred while generating the response. Please try again later."}
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