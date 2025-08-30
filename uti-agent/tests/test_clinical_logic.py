import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.clinical_engine import ClinicalDecisionEngine
from models.patient_data import PatientData, SymptomData, DemographicData, HistoryData
from models.treatment_plan import EligibilityStatus


def test_basic_symptom_check():
    """Test: Patient with dysuria should meet symptom criteria"""
    engine = ClinicalDecisionEngine()
    symptoms = SymptomData(dysuria=True)
    
    result = engine.assess_symptom_criteria(symptoms)
    assert result is True


def test_male_patient_referral():
    """Test: Male patients should be referred"""
    engine = ClinicalDecisionEngine()
    patient_data = PatientData(
        symptoms=SymptomData(dysuria=True),
        demographics=DemographicData(age=30, sex='male')
    )
    
    result = engine.determine_eligibility(patient_data)
    assert result.status == EligibilityStatus.REQUIRES_REFERRAL


def test_normal_female_gets_treatment():
    """Test: Normal female patient should get treatment"""
    engine = ClinicalDecisionEngine()
    patient_data = PatientData(
        symptoms=SymptomData(dysuria=True),
        demographics=DemographicData(age=25, sex='female'),
        history=HistoryData(allergies=[])
    )
    
    result = engine.determine_eligibility(patient_data)
    assert result.status == EligibilityStatus.ELIGIBLE
    assert result.treatment_plan is not None


def test_first_line_treatment():
    """Test: Should get nitrofurantoin as first line"""
    engine = ClinicalDecisionEngine()
    patient_data = PatientData(
        demographics=DemographicData(age=25, sex='female'),
        history=HistoryData(allergies=[])
    )
    
    treatment = engine.select_treatment(patient_data)
    assert "Nitrofurantoin" in treatment.medication


if __name__ == "__main__":
    # Simple test runner
    print("Running basic clinical engine tests...")
    
    try:
        test_basic_symptom_check()
        print("✓ Basic symptom check test passed")
        
        test_male_patient_referral()
        print("✓ Male patient referral test passed")
        
        test_normal_female_gets_treatment()
        print("✓ Normal female treatment test passed")
        
        test_first_line_treatment()
        print("✓ First line treatment test passed")
        
        print("\nAll basic tests passed! ✅")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Check your clinical engine implementation")