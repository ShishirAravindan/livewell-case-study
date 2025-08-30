import json
import logging
from datetime import datetime
from typing import Dict, Any


class EvaluationLogger:
    def __init__(self, log_file: str = "uti_agent_sessions.log"):
        self.log_file = log_file
        self.logger = logging.getLogger('uti_agent')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_conversation(self, session_data: Dict[str, Any]):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_type': 'conversation',
            'data': session_data
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_clinical_decision(self, decision_rationale: Dict[str, Any]):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_type': 'clinical_decision',
            'data': decision_rationale
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_treatment_outcome(self, outcome_data: Dict[str, Any]):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_type': 'treatment_outcome',
            'data': outcome_data
        }
        self.logger.info(json.dumps(log_entry))
    
    def generate_review_queue(self) -> list:
        # Placeholder for generating cases that need review
        return []