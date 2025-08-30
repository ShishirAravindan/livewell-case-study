Here's a comprehensive implementation spec for your Livewell Autonomous Care Agent:

## Implementation Specification

### **System Requirements**
- Python 3.9+
- CLI interface (no web dependencies)
- LLM integration (Gemini API or similar)
- Local data persistence for session state

- Structured logging for evaluation

### **Core Components**

#### **1. Patient Interface (CLI)**
```python
class PatientInterface:
    - handle_user_input()
    - display_response()
    - manage_conversation_flow()
    - graceful_exit_handling()
```
- Simple command-line chat loop
- Clear prompts and formatting
- Handle interruptions (Ctrl+C) gracefully
- Session management (start/end conversation)

#### **2. Input Parser (LLM NLU Layer)**
```python
class InputParser:
    - extract_symptoms(user_text) -> SymptomData
    - extract_demographics(user_text) -> DemographicData
    - extract_medical_history(user_text) -> HistoryData
    - validate_extracted_data()
```
**Key Functions:**
- Convert natural language to structured data classes
- Handle ambiguous responses ("sort of", "sometimes")
- Extract temporal information (onset, duration)
- Flag unclear responses for follow-up questions

**Data Structures:**
```python
@dataclass
class SymptomData:
    dysuria: bool
    urgency: bool
    frequency: bool
    suprapubic_pain: bool
    hematuria: bool
    onset: str
    severity: Optional[str]

@dataclass
class DemographicData:
    age: int
    sex: str
    weight: Optional[float]
    pregnancy_status: Optional[bool]

@dataclass
class HistoryData:
    allergies: List[str]
    current_medications: List[str]
    recent_antibiotics: bool
    previous_utis: List[UTIHistory]
    immunocompromised: bool
```

#### **3. Clinical Decision Engine**
```python
class ClinicalDecisionEngine:
    - assess_symptom_criteria(symptoms) -> bool
    - check_complicating_factors(patient_data) -> List[str]
    - check_recurrence_relapse(history) -> bool
    - determine_eligibility() -> EligibilityResult
    - select_treatment(patient_data) -> TreatmentPlan
    - generate_referral_reason() -> str
```

**Core Logic (Following UTI Algorithm):**
1. **Symptom Assessment**: Acute dysuria OR 2+ qualifying symptoms
2. **Exclusion Screening**: 
   - Red flag symptoms (fever, flank pain, systemic illness)
   - Male patients
   - Pregnancy
   - Age <12
   - Immunocompromised
   - Structural urinary abnormalities
3. **Recurrence Check**: Relapse (<4 weeks) or recurrent UTIs
4. **Treatment Selection**: Nitrofurantoin first-line, alternatives based on allergies/contraindications

#### **4. Response Generator (LLM Phrasing Layer)**
```python
class ResponseGenerator:
    - generate_followup_question(missing_data) -> str
    - generate_treatment_explanation(treatment_plan) -> str
    - generate_referral_message(reason) -> str
    - generate_safety_instructions() -> str
```
- Convert structured decisions to empathetic, clear language
- Include dosing instructions, side effects, follow-up timing
- Explain referral reasons without alarming patients

#### **5. Conversation Manager**
```python
class ConversationManager:
    - track_conversation_state()
    - determine_next_question()
    - validate_information_completeness()
    - handle_conversation_flow()
```
**Question Flow Logic:**
1. Initial symptom description
2. Onset and severity questions
3. Red flag symptom screening
4. Demographics collection
5. Medical history (allergies, medications)
6. Final decision and recommendation

#### **6. Evaluation & Logging**
```python
class EvaluationLogger:
    - log_conversation(session_data)
    - log_clinical_decision(decision_rationale)
    - log_treatment_outcome()
    - generate_review_queue()
```

### **Data Flow Specification**

```
1. Patient Input (string) → Input Parser
2. Input Parser → SymptomData/DemographicData/HistoryData
3. Structured Data → Clinical Decision Engine
4. Clinical Decision Engine → EligibilityResult + TreatmentPlan/ReferralReason
5. Decision Data → Response Generator
6. Response Generator → Formatted Response (string)
7. All steps → Evaluation Logger
```

### **Key Implementation Decisions**

**LLM Integration:**
- Use structured prompts with clear output formatting (JSON)
- Implement retry logic for failed parsing
- Separate prompts for NLU vs response generation

**Safety Mechanisms:**
- Hard-coded exclusion criteria (no LLM override)
- Mandatory data validation before treatment decisions
- Default to referral on any uncertainty

**Session Management:**
- Track conversation state in memory
- Allow backtracking to correct information
- Clear session boundaries with proper logging

**Error Handling:**
- Graceful degradation when LLM fails
- Clear escalation paths for technical failures
- User-friendly error messages

### **File Structure**
```
livewell_agent/
├── main.py                 # CLI entry point
├── core/
│   ├── input_parser.py     # LLM NLU component
│   ├── clinical_engine.py  # UTI algorithm implementation
│   ├── response_gen.py     # LLM response formatting
│   └── conversation.py     # Flow management
├── models/
│   ├── patient_data.py     # Data classes
│   └── treatment_plan.py   # Treatment structures
├── utils/
│   ├── llm_client.py       # LLM API wrapper
│   └── logger.py           # Evaluation logging
└── tests/
    ├── test_clinical_logic.py
    └── test_conversation_flow.py
```

