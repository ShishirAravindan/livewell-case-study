#!/usr/bin/env python3
"""
Quick test script for LLM integration
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from utils.llm_client import GeminiClient
from core.input_parser import InputParser
from core.response_gen import ResponseGenerator

# Load environment variables from .env file
load_dotenv()


def test_basic_functionality():
    """Test basic functionality without LLM first"""
    print("=== Testing without LLM ===")
    parser = InputParser()
    
    # Test symptom extraction
    symptoms = parser.extract_symptoms("I have burning pain when I urinate and I need to go frequently")
    print(f"Symptoms extracted: dysuria={symptoms.dysuria}, frequency={symptoms.frequency}")
    
    # Test demographics
    demographics = parser.extract_demographics("I'm a 25 year old female")
    print(f"Demographics: age={demographics.age}, sex={demographics.sex}")


def test_llm_integration():
    """Test LLM integration if API key is available"""
    print("\n=== Testing with LLM ===")
    
    if not os.getenv('GOOGLE_API_KEY'):
        print("No API key found. Set GOOGLE_API_KEY environment variable to test LLM integration.")
        print("Example: export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    try:
        client = GeminiClient()
        parser = InputParser(client)
        response_gen = ResponseGenerator(client)
        
        # Test symptom extraction
        symptoms = parser.extract_symptoms("I've been having a burning sensation when I pee since yesterday, and I feel like I need to go to the bathroom all the time")
        print(f"LLM Symptoms: dysuria={symptoms.dysuria}, frequency={symptoms.frequency}, onset='{symptoms.onset}'")
        
        # Test demographics
        demographics = parser.extract_demographics("I'm a 28 year old woman")
        print(f"LLM Demographics: age={demographics.age}, sex={demographics.sex}")
        
        # Test response generation
        missing_data = {"onset": "when symptoms started"}
        follow_up = response_gen.generate_followup_question(missing_data)
        print(f"Follow-up question: {follow_up}")
        
    except Exception as e:
        print(f"LLM integration failed: {e}")
        print("Make sure your API key is valid and you have internet connection.")


if __name__ == "__main__":
    test_basic_functionality()
    test_llm_integration()