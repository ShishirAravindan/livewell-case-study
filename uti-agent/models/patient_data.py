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


@dataclass
class HistoryData:
    allergies: List[str] = field(default_factory=list)
    current_medications: List[str] = field(default_factory=list)
    recent_antibiotics: bool = False
    previous_utis: List[UTIHistory] = field(default_factory=list)
    immunocompromised: bool = False


@dataclass
class PatientData:
    symptoms: SymptomData = field(default_factory=SymptomData)
    demographics: DemographicData = field(default_factory=DemographicData)
    history: HistoryData = field(default_factory=HistoryData)
    session_id: str = ""