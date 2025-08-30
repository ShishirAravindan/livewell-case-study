import re
from models.patient_data import SymptomData, DemographicData, HistoryData


class InputParser:
    def extract_symptoms(self, user_text: str) -> SymptomData:
        symptoms = SymptomData()
        text_lower = user_text.lower()
        
        # Basic keyword matching (placeholder for LLM integration)
        symptoms.dysuria = any(word in text_lower for word in ['burn', 'burning', 'pain', 'hurt', 'sting'])
        symptoms.urgency = any(word in text_lower for word in ['urgent', 'urgency', 'rush', 'sudden'])
        symptoms.frequency = any(word in text_lower for word in ['frequent', 'often', 'many times', 'lot'])
        symptoms.suprapubic_pain = any(word in text_lower for word in ['lower', 'bladder', 'pelvic'])
        symptoms.hematuria = any(word in text_lower for word in ['blood', 'red', 'pink'])
        
        # Extract onset information
        if any(word in text_lower for word in ['today', 'this morning', 'hours']):
            symptoms.onset = "acute"
        elif any(word in text_lower for word in ['yesterday', 'day', 'days']):
            symptoms.onset = "1-2 days"
        elif any(word in text_lower for word in ['week', 'weeks']):
            symptoms.onset = "weeks"
        
        return symptoms
    
    def extract_demographics(self, user_text: str) -> DemographicData:
        demographics = DemographicData()
        
        # Extract age
        age_match = re.search(r'\b(\d{1,2})\b', user_text)
        if age_match:
            demographics.age = int(age_match.group(1))
        
        # Extract sex
        text_lower = user_text.lower()
        if any(word in text_lower for word in ['female', 'woman', 'girl', 'f']):
            demographics.sex = "female"
        elif any(word in text_lower for word in ['male', 'man', 'boy', 'm']):
            demographics.sex = "male"
        
        return demographics
    
    def extract_medical_history(self, user_text: str) -> HistoryData:
        history = HistoryData(allergies=[], current_medications=[], previous_utis=[])
        text_lower = user_text.lower()
        
        # Basic allergy detection
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