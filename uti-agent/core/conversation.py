from typing import Dict, Any, Optional
from enum import Enum
from models.patient_data import PatientData, SymptomData, DemographicData, HistoryData
from models.treatment_plan import EligibilityResult
from core.input_parser import InputParser
from core.clinical_engine import ClinicalDecisionEngine
from core.response_gen import ResponseGenerator


class ConversationState(Enum):
    GREETING = "greeting"
    SYMPTOM_COLLECTION = "symptom_collection"
    DEMOGRAPHIC_COLLECTION = "demographic_collection"
    HISTORY_COLLECTION = "history_collection"
    CLINICAL_ASSESSMENT = "clinical_assessment"
    COMPLETE = "complete"


class ConversationManager:
    def __init__(self):
        self.state = ConversationState.GREETING
        self.patient_data = PatientData()
        self.input_parser = InputParser()
        self.clinical_engine = ClinicalDecisionEngine()
        self.response_generator = ResponseGenerator()
        self.conversation_history = []
    
    def track_conversation_state(self, user_input: str, response: str):
        self.conversation_history.append({
            'user_input': user_input,
            'response': response,
            'state': self.state.value,
            'patient_data': self.patient_data
        })
    
    def determine_next_question(self) -> str:
        if self.state == ConversationState.GREETING:
            return "Hello! I'm here to help assess your urinary symptoms. Can you tell me what symptoms you're experiencing?"
        
        elif self.state == ConversationState.SYMPTOM_COLLECTION:
            missing_symptoms = self._check_missing_symptom_data()
            if missing_symptoms:
                return self.response_generator.generate_followup_question(missing_symptoms)
            else:
                self.state = ConversationState.DEMOGRAPHIC_COLLECTION
                return "Thank you. Now I need some basic information about you. What is your age and biological sex?"
        
        elif self.state == ConversationState.DEMOGRAPHIC_COLLECTION:
            missing_demographics = self._check_missing_demographic_data()
            if missing_demographics:
                return self.response_generator.generate_followup_question(missing_demographics)
            else:
                self.state = ConversationState.HISTORY_COLLECTION
                return "Do you have any allergies to medications, and are you currently taking any medications?"
        
        elif self.state == ConversationState.HISTORY_COLLECTION:
            missing_history = self._check_missing_history_data()
            if missing_history:
                return self.response_generator.generate_followup_question(missing_history)
            else:
                self.state = ConversationState.CLINICAL_ASSESSMENT
                return self._perform_clinical_assessment()
        
        return "Thank you for the information."
    
    def _check_missing_symptom_data(self) -> Dict[str, Any]:
        missing = {}
        if not hasattr(self.patient_data.symptoms, 'onset') or not self.patient_data.symptoms.onset:
            missing['onset'] = 'When did your symptoms start?'
        return missing
    
    def _check_missing_demographic_data(self) -> Dict[str, Any]:
        missing = {}
        if not self.patient_data.demographics.age:
            missing['age'] = 'your age'
        if not self.patient_data.demographics.sex:
            missing['sex'] = 'your biological sex'
        return missing
    
    def _check_missing_history_data(self) -> Dict[str, Any]:
        missing = {}
        if not hasattr(self.patient_data.history, 'allergies_collected'):
            missing['allergies'] = 'any medication allergies'
        return missing
    
    def _perform_clinical_assessment(self) -> str:
        eligibility = self.clinical_engine.determine_eligibility(self.patient_data)
        
        if eligibility.treatment_plan:
            response = self.response_generator.generate_treatment_explanation(eligibility.treatment_plan)
        else:
            response = self.response_generator.generate_referral_message(eligibility.referral_reason)
        
        self.state = ConversationState.COMPLETE
        return response
    
    def validate_information_completeness(self) -> bool:
        return (
            bool(self.patient_data.symptoms.onset) and
            bool(self.patient_data.demographics.age) and
            bool(self.patient_data.demographics.sex) and
            hasattr(self.patient_data.history, 'allergies_collected')
        )
    
    def process_input(self, user_input: str) -> str:
        if self.state == ConversationState.GREETING:
            self.patient_data.symptoms = self.input_parser.extract_symptoms(user_input)
            self.state = ConversationState.SYMPTOM_COLLECTION
        
        elif self.state == ConversationState.SYMPTOM_COLLECTION:
            updated_symptoms = self.input_parser.extract_symptoms(user_input)
            # Merge with existing symptoms
            for attr in ['dysuria', 'urgency', 'frequency', 'suprapubic_pain', 'hematuria', 'onset', 'severity']:
                if hasattr(updated_symptoms, attr) and getattr(updated_symptoms, attr):
                    setattr(self.patient_data.symptoms, attr, getattr(updated_symptoms, attr))
        
        elif self.state == ConversationState.DEMOGRAPHIC_COLLECTION:
            demographics = self.input_parser.extract_demographics(user_input)
            if demographics.age:
                self.patient_data.demographics.age = demographics.age
            if demographics.sex:
                self.patient_data.demographics.sex = demographics.sex
        
        elif self.state == ConversationState.HISTORY_COLLECTION:
            history = self.input_parser.extract_medical_history(user_input)
            self.patient_data.history.allergies.extend(history.allergies)
            self.patient_data.history.current_medications.extend(history.current_medications)
            self.patient_data.history.allergies_collected = True
        
        response = self.determine_next_question()
        self.track_conversation_state(user_input, response)
        return response
    
    def is_complete(self) -> bool:
        return self.state == ConversationState.COMPLETE