import os
import json
from typing import Dict, Any, Optional
from google import genai
from google.genai import types


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = 'gemini-2.5-flash'
    
    def generate_structured_response(self, prompt: str, system_instruction: str = "", max_tokens: int = 1000, temperature: float = 0.3) -> str:
        """Generate a response with specific formatting requirements"""
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            return response.text.strip() if response.text else ""
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""
    
    def extract_structured_data(self, prompt: str, user_input: str, expected_format: str) -> Dict[str, Any]:
        """Extract structured data from user input using LLM"""
        system_prompt = f"""You are a medical information extraction system. Extract relevant information from patient input and return it in the specified JSON format.

{expected_format}

Only include fields that are explicitly mentioned or clearly implied by the user. Use null for missing information."""
        
        full_prompt = f"""Patient input: "{user_input}"

Extract the relevant information and return as JSON:"""
        
        try:
            response = self.generate_structured_response(
                full_prompt, 
                system_instruction=system_prompt,
                temperature=0.1
            )
            
            # Try to parse JSON response
            if response:
                # Clean response to extract JSON
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
            
            return {}
        
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response}")
            return {}
        except Exception as e:
            print(f"Error extracting structured data: {e}")
            return {}
    
    def generate_conversational_response(self, context: str, user_input: str, response_type: str = "general") -> str:
        """Generate natural, empathetic responses for conversation"""
        system_prompts = {
            "followup": "You are a caring medical assistant asking follow-up questions. Be empathetic, clear, and professional.",
            "treatment": "You are a medical assistant explaining treatment recommendations. Be clear, reassuring, and include all necessary safety information.",
            "referral": "You are a medical assistant explaining referral recommendations. Be supportive and not alarming while explaining why professional care is needed.",
            "general": "You are a helpful medical assistant. Be empathetic, professional, and clear."
        }
        
        system_instruction = system_prompts.get(response_type, system_prompts["general"])
        
        prompt = f"""Context: {context}

Patient said: "{user_input}"

Respond appropriately:"""
        
        return self.generate_structured_response(
            prompt,
            system_instruction=system_instruction,
            temperature=0.7
        )
    
    def validate_response_safety(self, response: str) -> bool:
        """Basic safety validation for generated responses"""
        dangerous_phrases = [
            "guaranteed cure",
            "definitely have",
            "certain diagnosis",
            "no need to see doctor",
            "skip medical care"
        ]
        
        response_lower = response.lower()
        return not any(phrase in response_lower for phrase in dangerous_phrases)