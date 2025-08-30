from typing import Dict, Any
from models.treatment_plan import TreatmentPlan


class ResponseGenerator:
    def generate_followup_question(self, missing_data: Dict[str, Any]) -> str:
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