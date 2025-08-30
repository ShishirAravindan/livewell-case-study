from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class SymptomData:
    dysuria: bool = False
    urgency: bool = False
    frequency: bool = False
    suprapubic_pain: bool = False
    hematuria: bool = False
    onset: str = ""
    severity: Optional[str] = None
    # Systemic symptoms that indicate complications
    fever: bool = False
    rigors: bool = False
    flank_pain: bool = False
    back_pain: bool = False
    nausea: bool = False
    vomiting: bool = False


@dataclass
class DemographicData:
    age: int = 0
    sex: str = ""
    weight: Optional[float] = None
    pregnancy_status: Optional[bool] = None


@dataclass
class UTIHistory:
    date: datetime
    treatment: str
    resolved: bool
    treatment_completion_date: Optional[datetime] = None


@dataclass
class HistoryData:
    allergies: List[str] = field(default_factory=list)
    current_medications: List[str] = field(default_factory=list)
    recent_antibiotics: bool = False
    previous_utis: List[UTIHistory] = field(default_factory=list)
    immunocompromised: bool = False
    # Urinary tract complications
    abnormal_urinary_function: bool = False
    indwelling_catheter: bool = False
    neurogenic_bladder: bool = False
    renal_stones: bool = False
    renal_dysfunction: bool = False


@dataclass
class PatientData:
    symptoms: SymptomData = field(default_factory=SymptomData)
    demographics: DemographicData = field(default_factory=DemographicData)
    history: HistoryData = field(default_factory=HistoryData)
    session_id: str = ""