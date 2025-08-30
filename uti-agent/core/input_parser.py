import re
from typing import Optional
from models.patient_data import SymptomData, DemographicData, HistoryData
from utils.llm_client import GeminiClient


class InputParser:
    def __init__(self, llm_client: Optional[GeminiClient] = None):
        self.llm_client = llm_client
    
    def extract_symptoms(self, user_text: str) -> SymptomData:
        if self.llm_client:
            return self._extract_symptoms_llm(user_text)
        else:
            return self._extract_symptoms_basic(user_text)
    
    def _extract_symptoms_llm(self, user_text: str) -> SymptomData:
        """Extract symptoms using LLM with structured output"""
        expected_format = """
        {
            "dysuria": boolean (burning pain during urination),
            "urgency": boolean (sudden strong urge to urinate),
            "frequency": boolean (urinating more often than usual),
            "suprapubic_pain": boolean (pain in lower abdomen/bladder area),
            "hematuria": boolean (blood in urine),
            "onset": string (when symptoms started: "hours", "1-2 days", "days", "weeks", or "unknown"),
            "severity": string or null (mild, moderate, severe, or null if not mentioned)
        }"""
        
        extracted_data = self.llm_client.extract_structured_data(
            "Extract urinary symptoms from the following patient description:",
            user_text,
            expected_format
        )
        
        symptoms = SymptomData()
        if extracted_data:
            symptoms.dysuria = extracted_data.get('dysuria', False)
            symptoms.urgency = extracted_data.get('urgency', False) 
            symptoms.frequency = extracted_data.get('frequency', False)
            symptoms.suprapubic_pain = extracted_data.get('suprapubic_pain', False)
            symptoms.hematuria = extracted_data.get('hematuria', False)
            symptoms.onset = extracted_data.get('onset', '')
            symptoms.severity = extracted_data.get('severity')
        
        return symptoms
    
    def _extract_symptoms_basic(self, user_text: str) -> SymptomData:
        """Fallback basic keyword extraction"""
        symptoms = SymptomData()
        text_lower = user_text.lower()
        
        symptoms.dysuria = any(word in text_lower for word in ['burn', 'burning', 'pain', 'hurt', 'sting'])
        symptoms.urgency = any(word in text_lower for word in ['urgent', 'urgency', 'rush', 'sudden'])
        symptoms.frequency = any(word in text_lower for word in ['frequent', 'often', 'many times', 'lot'])
        symptoms.suprapubic_pain = any(word in text_lower for word in ['lower', 'bladder', 'pelvic'])
        symptoms.hematuria = any(word in text_lower for word in ['blood', 'red', 'pink'])
        
        if any(word in text_lower for word in ['today', 'this morning', 'hours']):
            symptoms.onset = "hours"
        elif any(word in text_lower for word in ['yesterday', 'day', 'days']):
            symptoms.onset = "1-2 days"
        elif any(word in text_lower for word in ['week', 'weeks']):
            symptoms.onset = "weeks"
        
        return symptoms
    
    def extract_demographics(self, user_text: str) -> DemographicData:
        if self.llm_client:
            return self._extract_demographics_llm(user_text)
        else:
            return self._extract_demographics_basic(user_text)
    
    def _extract_demographics_llm(self, user_text: str) -> DemographicData:
        """Extract demographics using LLM"""
        expected_format = """
{
    "age": integer or null (age in years),
    "sex": string or null ("male" or "female", biological sex),
    "weight": number or null (weight in kg or lbs),
    "pregnancy_status": boolean or null (true if pregnant, null if unknown/not applicable)
}"""
        
        extracted_data = self.llm_client.extract_structured_data(
            "Extract demographic information:",
            user_text,
            expected_format
        )
        
        demographics = DemographicData()
        if extracted_data:
            demographics.age = extracted_data.get('age', 0)
            demographics.sex = extracted_data.get('sex', '')
            demographics.weight = extracted_data.get('weight')
            demographics.pregnancy_status = extracted_data.get('pregnancy_status')
        
        return demographics
    
    def _extract_demographics_basic(self, user_text: str) -> DemographicData:
        """Fallback basic demographic extraction"""
        demographics = DemographicData()
        
        age_match = re.search(r'\b(\d{1,2})\b', user_text)
        if age_match:
            demographics.age = int(age_match.group(1))
        
        text_lower = user_text.lower()
        if any(word in text_lower for word in ['female', 'woman', 'girl', 'f']):
            demographics.sex = "female"
        elif any(word in text_lower for word in ['male', 'man', 'boy', 'm']):
            demographics.sex = "male"
        
        return demographics
    
    def extract_medical_history(self, user_text: str) -> HistoryData:
        if self.llm_client:
            return self._extract_history_llm(user_text)
        else:
            return self._extract_history_basic(user_text)
    
    def _extract_history_llm(self, user_text: str) -> HistoryData:
        """Extract medical history using LLM"""
        expected_format = """
{
    "allergies": array of strings (medication allergies, empty array if none),
    "current_medications": array of strings (current medications, empty array if none),
    "recent_antibiotics": boolean (antibiotics in last 4 weeks),
    "immunocompromised": boolean (immunosuppressed, diabetes, etc.),
    "previous_utis": array (history of UTIs, can be empty)
}"""
        
        extracted_data = self.llm_client.extract_structured_data(
            "Extract medical history information:",
            user_text,
            expected_format
        )
        
        history = HistoryData()
        if extracted_data:
            history.allergies = extracted_data.get('allergies', [])
            history.current_medications = extracted_data.get('current_medications', [])
            history.recent_antibiotics = extracted_data.get('recent_antibiotics', False)
            history.immunocompromised = extracted_data.get('immunocompromised', False)
        
        return history
    
    def _extract_history_basic(self, user_text: str) -> HistoryData:
        """Fallback basic history extraction"""
        history = HistoryData()
        text_lower = user_text.lower()
        
        if 'no' in text_lower and ('allerg' in text_lower or 'medication' in text_lower):
            history.allergies = []
        elif any(word in text_lower for word in ['penicillin', 'sulfa', 'trimethoprim']):
            if 'penicillin' in text_lower:
                history.allergies.append('penicillin')
            if 'sulfa' in text_lower:
                history.allergies.append('sulfonamides')
        
        return history
    
    def validate_extracted_data(self, data) -> bool:
        # Basic validation placeholder
        return True