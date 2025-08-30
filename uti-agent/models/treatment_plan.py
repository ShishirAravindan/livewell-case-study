from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TreatmentType(Enum):
    NITROFURANTOIN = "nitrofurantoin"
    TRIMETHOPRIM_SULFAMETHOXAZOLE = "tmp_smx"
    FOSFOMYCIN_3G = "fosfomycin_3g"
    FOSFOMYCIN_200MG = "fosfomycin_200mg"
    REFERRAL = "referral"


class EligibilityStatus(Enum):
    ELIGIBLE = "eligible"
    REQUIRES_REFERRAL = "requires_referral"
    INCOMPLETE_DATA = "incomplete_data"


@dataclass
class TreatmentPlan:
    medication: str
    dosage: str
    duration: str
    instructions: str
    side_effects: str
    follow_up: str


@dataclass
class EligibilityResult:
    status: EligibilityStatus
    treatment_plan: Optional[TreatmentPlan] = None
    referral_reason: Optional[str] = None
    safety_notes: str = ""