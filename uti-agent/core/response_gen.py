from typing import Dict, Any, Optional
from models.treatment_plan import TreatmentPlan
from utils.llm_client import GeminiClient


class ResponseGenerator:
    def __init__(self, llm_client: Optional[GeminiClient] = None):
        self.llm_client = llm_client
    def generate_followup_question(self, missing_data: Dict[str, Any]) -> str:
        if self.llm_client:
            return self._generate_followup_llm(missing_data)
        else:
            return self._generate_followup_basic(missing_data)
    
    def _generate_followup_llm(self, missing_data: Dict[str, Any]) -> str:
        """Generate empathetic follow-up questions using LLM"""
        missing_items = list(missing_data.keys())
        context = f"Patient consultation for UTI symptoms. Need to ask about: {', '.join(missing_items)}"
        
        return self.llm_client.generate_conversational_response(
            context=context,
            user_input="Need follow-up information",
            response_type="followup"
        )
    
    def _generate_followup_basic(self, missing_data: Dict[str, Any]) -> str:
        """Fallback basic follow-up questions"""
        if 'onset' in missing_data:
            return "When did your symptoms start? (e.g., today, yesterday, a few days ago)"
        elif 'age' in missing_data:
            return "Could you please tell me your age?"
        elif 'sex' in missing_data:
            return "What is your biological sex (male/female)?"
        elif 'allergies' in missing_data:
            return "Do you have any known allergies to medications?"
        else:
            return "Could you provide more details about that?"
    
    def generate_treatment_explanation(self, treatment_plan: TreatmentPlan) -> str:
        if self.llm_client:
            return self._generate_treatment_llm(treatment_plan)
        else:
            return self._generate_treatment_basic(treatment_plan)
    
    def _generate_treatment_llm(self, treatment_plan: TreatmentPlan) -> str:
        """Generate empathetic treatment explanation using LLM"""
        treatment_info = f"""
            Medication: {treatment_plan.medication}
            Dosage: {treatment_plan.dosage}
            Duration: {treatment_plan.duration}
            Instructions: {treatment_plan.instructions}
            Side effects: {treatment_plan.side_effects}
            Follow-up: {treatment_plan.follow_up}
        """
        
        context = f"UTI treatment recommendation: {treatment_info}"
        
        return self.llm_client.generate_conversational_response(
            context=context,
            user_input="Explain treatment plan",
            response_type="treatment"
        )
    
    def _generate_treatment_basic(self, treatment_plan: TreatmentPlan) -> str:
        """Fallback basic treatment explanation"""
        explanation = f"""Based on your symptoms, I recommend the following treatment:

**Medication:** {treatment_plan.medication}
**Dosage:** {treatment_plan.dosage}
**Duration:** {treatment_plan.duration}

**Instructions:** {treatment_plan.instructions}

**Possible side effects:** {treatment_plan.side_effects}

**Important:** {treatment_plan.follow_up}

**Additional advice:**
- Drink plenty of water
- Urinate frequently and completely
- Avoid caffeine and alcohol during treatment
- Contact a healthcare provider if symptoms worsen or don't improve

This recommendation is based on clinical guidelines for uncomplicated UTIs. Always consult with a healthcare professional for personalized medical advice."""
        
        return explanation
    
    def generate_referral_message(self, reason: str) -> str:
        if self.llm_client:
            return self._generate_referral_llm(reason)
        else:
            return self._generate_referral_basic(reason)
    
    def _generate_referral_llm(self, reason: str) -> str:
        """Generate empathetic referral message using LLM"""
        context = f"Patient needs referral to healthcare provider. Reason: {reason}"
        
        return self.llm_client.generate_conversational_response(
            context=context,
            user_input="Need referral recommendation",
            response_type="referral"
        )
    
    def _generate_referral_basic(self, reason: str) -> str:
        """Fallback basic referral message"""
        return f"""Based on your symptoms and medical history, I recommend that you see a healthcare provider for proper evaluation and treatment.

**Reason for referral:** {reason}

**What to do:**
- Contact your primary care provider or urgent care clinic
- Mention your urinary symptoms and when they started
- Bring a list of your current medications and allergies

**Seek immediate care if you experience:**
- Fever or chills
- Back or flank pain
- Nausea or vomiting
- Severe symptoms

This is a precautionary recommendation to ensure you receive the most appropriate care for your specific situation."""
    
    def generate_safety_instructions(self) -> str:
        return """**Important Safety Information:**
- This tool is for guidance only and does not replace professional medical advice
- Seek immediate medical attention if you experience severe symptoms
- Always complete the full course of any prescribed antibiotics
- Contact a healthcare provider if symptoms don't improve within 3 days"""