from typing import List
from models.patient_data import PatientData
from models.treatment_plan import EligibilityResult, EligibilityStatus, TreatmentPlan


class ClinicalDecisionEngine:
    def assess_symptom_criteria(self, symptoms) -> bool:
        # UTI symptom criteria: acute dysuria OR 2+ qualifying symptoms
        if symptoms.dysuria:
            return True
        
        symptom_count = sum([
            symptoms.urgency,
            symptoms.frequency, 
            symptoms.suprapubic_pain,
            symptoms.hematuria
        ])
        
        return symptom_count >= 2
    
    def check_complicating_factors(self, patient_data: PatientData) -> List[str]:
        complications = []
        
        # Male patients
        if patient_data.demographics.sex.lower() == 'male':
            complications.append('male_patient')
        
        # Age restrictions
        if patient_data.demographics.age < 12:
            complications.append('pediatric')
        
        # Pregnancy (placeholder - would need proper screening)
        if (patient_data.demographics.sex.lower() == 'female' and 
            patient_data.demographics.pregnancy_status):
            complications.append('pregnancy')
        
        # Immunocompromised
        if patient_data.history.immunocompromised:
            complications.append('immunocompromised')
        
        return complications
    
    def check_recurrence_relapse(self, history) -> bool:
        # Placeholder for recurrence checking
        return len(history.previous_utis) > 3
    
    def determine_eligibility(self, patient_data: PatientData) -> EligibilityResult:
        # Check basic symptom criteria
        if not self.assess_symptom_criteria(patient_data.symptoms):
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_REFERRAL,
                referral_reason="Symptoms do not meet UTI criteria"
            )
        
        # Check for complications
        complications = self.check_complicating_factors(patient_data)
        if complications:
            reason = f"Requires clinical evaluation due to: {', '.join(complications)}"
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_REFERRAL,
                referral_reason=reason
            )
        
        # Check for recent recurrence
        if self.check_recurrence_relapse(patient_data.history):
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_REFERRAL,
                referral_reason="Recurrent UTIs require clinical evaluation"
            )
        
        # If eligible, select treatment
        treatment = self.select_treatment(patient_data)
        return EligibilityResult(
            status=EligibilityStatus.ELIGIBLE,
            treatment_plan=treatment
        )
    
    def select_treatment(self, patient_data: PatientData) -> TreatmentPlan:
        # Check for allergies to guide treatment selection
        allergies = [allergy.lower() for allergy in patient_data.history.allergies]
        
        # First-line: Nitrofurantoin (unless contraindicated)
        if 'nitrofurantoin' not in allergies:
            return TreatmentPlan(
                medication="Nitrofurantoin",
                dosage="100mg twice daily",
                duration="5 days",
                instructions="Take with food to reduce stomach upset",
                side_effects="Nausea, headache, brown urine (harmless)",
                follow_up="If symptoms persist after 3 days, contact healthcare provider"
            )
        
        # Alternative: Trimethoprim (if no sulfa allergy)
        elif 'sulfonamides' not in allergies and 'trimethoprim' not in allergies:
            return TreatmentPlan(
                medication="Trimethoprim",
                dosage="200mg twice daily",
                duration="3 days", 
                instructions="Take with plenty of water",
                side_effects="Nausea, skin rash, headache",
                follow_up="If symptoms persist after 3 days, contact healthcare provider"
            )
        
        # If multiple allergies, refer for clinical evaluation
        else:
            return None
    
    def generate_referral_reason(self, complications: List[str]) -> str:
        return f"Clinical evaluation recommended due to: {', '.join(complications)}"