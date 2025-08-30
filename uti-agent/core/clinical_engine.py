from typing import List
from models.patient_data import PatientData
from models.treatment_plan import EligibilityResult, EligibilityStatus, TreatmentPlan


class ClinicalDecisionEngine:
    def assess_symptom_criteria(self, symptoms) -> bool:
        # OCP Algorithm: Acute dysuria OR 2 or more of the following:
        # new urinary urgency or frequency, suprapubic pain/discomfort, hematuria
        if symptoms.dysuria:
            return True
        
        qualifying_symptoms = [
            symptoms.urgency or False,
            symptoms.frequency or False, 
            symptoms.suprapubic_pain or False,
            symptoms.hematuria or False
        ]
        
        return sum(qualifying_symptoms) >= 2
    
    def check_complicating_factors(self, patient_data: PatientData) -> List[str]:
        complications = []
        
        # Upper urinary tract or systemic disease symptoms
        systemic_symptoms = [
            patient_data.symptoms.fever or False,
            patient_data.symptoms.rigors or False,
            patient_data.symptoms.flank_pain or False,
            patient_data.symptoms.back_pain or False,
            patient_data.symptoms.nausea or False,
            patient_data.symptoms.vomiting or False
        ]
        if any(systemic_symptoms):
            complications.append('systemic_symptoms')
        
        # Male patients
        if patient_data.demographics.sex.lower() == 'male':
            complications.append('male_patient')
        
        # Pregnancy
        if (patient_data.demographics.sex.lower() == 'female' and 
            patient_data.demographics.pregnancy_status):
            complications.append('pregnancy')
        
        # Age restrictions - pediatric (<12) or elderly considerations
        if patient_data.demographics.age < 12:
            complications.append('pediatric')
        
        # Immunocompromised
        if patient_data.history.immunocompromised:
            complications.append('immunocompromised')
        
        # Abnormal urinary tract function or structure
        urinary_complications = [
            patient_data.history.abnormal_urinary_function or False,
            patient_data.history.indwelling_catheter or False,
            patient_data.history.neurogenic_bladder or False,
            patient_data.history.renal_stones or False,
            patient_data.history.renal_dysfunction or False
        ]
        if any(urinary_complications):
            complications.append('abnormal_urinary_tract')
        
        return complications
    
    def check_recurrence_relapse(self, history) -> tuple[bool, str]:
        """
        OCP Algorithm defines:
        - Relapse: return of symptoms within 4 weeks of completing antibiotic treatment
        - Recurrent: 2 or more UTIs in 6 months OR 3 or more UTIs in 12 months
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        
        # Check for relapse (within 4 weeks of treatment completion)
        for uti in history.previous_utis:
            if uti.treatment_completion_date:
                time_since_completion = now - uti.treatment_completion_date
                if time_since_completion <= timedelta(weeks=4):
                    return True, "relapse"
        
        # Check for recurrence patterns
        # Count UTIs in last 6 months
        six_months_ago = now - timedelta(days=180)
        recent_utis_6m = [uti for uti in history.previous_utis 
                         if uti.date >= six_months_ago]
        
        if len(recent_utis_6m) >= 2:
            return True, "recurrent_6_months"
        
        # Count UTIs in last 12 months  
        twelve_months_ago = now - timedelta(days=365)
        recent_utis_12m = [uti for uti in history.previous_utis 
                          if uti.date >= twelve_months_ago]
        
        if len(recent_utis_12m) >= 3:
            return True, "recurrent_12_months"
        
        return False, ""
    
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
        
        # Check for relapse or recurrence
        has_recurrence, recurrence_type = self.check_recurrence_relapse(patient_data.history)
        if has_recurrence:
            reason_map = {
                "relapse": "Relapse within 4 weeks of treatment requires clinical evaluation",
                "recurrent_6_months": "Recurrent UTIs (2+ in 6 months) require clinical evaluation", 
                "recurrent_12_months": "Recurrent UTIs (3+ in 12 months) require clinical evaluation"
            }
            return EligibilityResult(
                status=EligibilityStatus.REQUIRES_REFERRAL,
                referral_reason=reason_map.get(recurrence_type, "Recurrent UTIs require clinical evaluation")
            )
        
        # If eligible, select treatment
        treatment = self.select_treatment(patient_data)
        return EligibilityResult(
            status=EligibilityStatus.ELIGIBLE,
            treatment_plan=treatment
        )
    
    def select_treatment(self, patient_data: PatientData) -> TreatmentPlan:
        """
        OCP Algorithm prescribing recommendations:
        1. Nitrofurantoin macrocrystals 100 mg PO BID × 5 days
        2. Trimethoprim/sulfamethoxazole (TMP/SMX) 160 mg/800 mg BID × 3 days  
        3. Fosfomycin trometamol 200 mg PO once daily × 3 days OR 100 mg PO BID × 3 days
        4. Fosfomycin trometamol 3 g PO × 1 dose
        """
        allergies = [allergy.lower() for allergy in patient_data.history.allergies]
        
        # First-line: Nitrofurantoin macrocrystals
        if 'nitrofurantoin' not in allergies:
            return TreatmentPlan(
                medication="Nitrofurantoin macrocrystals",
                dosage="100 mg PO BID",
                duration="5 days",
                instructions="Take with food to reduce stomach upset",
                side_effects="Nausea, headache, brown urine (harmless)",
                follow_up="If symptoms persist after 3 days, contact healthcare provider"
            )
        
        # Second-line: Trimethoprim/sulfamethoxazole
        elif ('sulfonamides' not in allergies and 'trimethoprim' not in allergies and 
              'sulfamethoxazole' not in allergies and 'tmp/smx' not in allergies):
            return TreatmentPlan(
                medication="Trimethoprim/sulfamethoxazole (TMP/SMX)",
                dosage="160 mg/800 mg PO BID",
                duration="3 days",
                instructions="Take with plenty of water",
                side_effects="Nausea, skin rash, headache",
                follow_up="If symptoms persist after 3 days, contact healthcare provider"
            )
        
        # Third-line: Fosfomycin 3g single dose
        elif 'fosfomycin' not in allergies:
            return TreatmentPlan(
                medication="Fosfomycin trometamol",
                dosage="3 g PO",
                duration="Single dose",
                instructions="Mix with water and take on empty stomach, preferably at bedtime",
                side_effects="Nausea, diarrhea, headache",
                follow_up="If symptoms persist after 3 days, contact healthcare provider"
            )
        
        # If multiple allergies contraindicate all options, refer for clinical evaluation
        else:
            return None
    
    def generate_referral_reason(self, complications: List[str]) -> str:
        return f"Clinical evaluation recommended due to: {', '.join(complications)}"