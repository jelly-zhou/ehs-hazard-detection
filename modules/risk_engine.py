"""
Risk Assessment Engine
Calculates risk scores based on severity and probability.
Implements ISO 45001 risk matrix logic.
"""

from typing import Dict, List
import json


class RiskEngine:
    """ISO 45001 compliant risk assessment engine"""
    
    RISK_LEVELS = {
        "LOW": {"range": (1, 5), "color": "green", "action": "Monitor"},
        "MEDIUM": {"range": (6, 10), "color": "yellow", "action": "Control"},
        "HIGH": {"range": (11, 15), "color": "orange", "action": "Reduce"},
        "CRITICAL": {"range": (16, 25), "color": "red", "action": "Eliminate"}
    }
    
    def __init__(self, hazard_library_path: str = "data/hazard_dataset.json"):
        self.hazard_library = self._load_library(hazard_library_path)
    
    def _load_library(self, path: str) -> Dict:
        """Load hazard library"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"hazard_categories": []}
    
    def calculate_risk_score(self, severity: int, probability: int) -> int:
        """
        Calculate risk score: Severity × Probability
        
        Args:
            severity: 1-5 (Impact level)
            probability: 1-5 (Likelihood)
        
        Returns:
            Risk score (1-25)
        """
        return severity * probability
    
    def classify_risk(self, risk_score: int) -> Dict:
        """
        Classify risk level based on score
        
        Returns:
            Dict with classification details
        """
        for level, config in self.RISK_LEVELS.items():
            score_range = config["range"]
            if score_range[0] <= risk_score <= score_range[1]:
                return {
                    "level": level,
                    "score": risk_score,
                    "color": config["color"],
                    "action": config["action"],
                    "range": score_range
                }
        
        return {
            "level": "UNKNOWN",
            "score": risk_score,
            "color": "gray",
            "action": "Review"
        }
    
    def process_hazards(self, detected_hazards: List[Dict]) -> List[Dict]:
        """
        Process detected hazards and assign risk scores
        
        Args:
            detected_hazards: List of hazard detections
        
        Returns:
            List of hazards with risk classification
        """
        processed_hazards = []
        
        for hazard in detected_hazards:
            severity = hazard.get("severity", 3)
            probability = hazard.get("probability", 3)
            risk_score = self.calculate_risk_score(severity, probability)
            risk_classification = self.classify_risk(risk_score)
            
            processed_hazard = {
                **hazard,
                "risk_score": risk_score,
                "risk_level": risk_classification["level"],
                "risk_color": risk_classification["color"],
                "action": risk_classification["action"]
            }
            
            processed_hazards.append(processed_hazard)
        
        processed_hazards.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return processed_hazards
    
    def get_risk_summary(self, processed_hazards: List[Dict]) -> Dict:
        """Generate risk summary statistics"""
        if not processed_hazards:
            return {
                "total_hazards": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "average_risk_score": 0,
                "max_risk_score": 0
            }
        
        level_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        risk_scores = []
        
        for hazard in processed_hazards:
            level = hazard.get("risk_level", "LOW")
            if level in level_counts:
                level_counts[level] += 1
            risk_scores.append(hazard.get("risk_score", 0))
        
        return {
            "total_hazards": len(processed_hazards),
            "critical_count": level_counts["CRITICAL"],
            "high_count": level_counts["HIGH"],
            "medium_count": level_counts["MEDIUM"],
            "low_count": level_counts["LOW"],
            "average_risk_score": round(sum(risk_scores) / len(risk_scores), 2),
            "max_risk_score": max(risk_scores) if risk_scores else 0
        }


class RiskMatrix:
    """Risk matrix for visualization"""
    
    @staticmethod
    def get_matrix_data(processed_hazards: List[Dict]) -> Dict:
        """
        Generate data for risk matrix visualization
        
        Returns:
            Dict suitable for plotting
        """
        matrix = {}
        
        for severity in range(1, 6):
            matrix[severity] = {}
            for probability in range(1, 6):
                matrix[severity][probability] = 0
        
        for hazard in processed_hazards:
            severity = hazard.get("severity", 3)
            probability = hazard.get("probability", 3)
            matrix[severity][probability] += 1
        
        return matrix
