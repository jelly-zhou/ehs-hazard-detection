"""
Control Measures Generator
Generates engineering, administrative, and PPE controls based on ISO 45001.
"""

from typing import Dict, List
import json


class ControlGenerator:
    """Generate control measures for detected hazards"""
    
    def __init__(self, controls_path: str = "data/control_measures.json"):
        self.controls = self._load_controls(controls_path)
    
    def _load_controls(self, path: str) -> Dict:
        """Load control measures database"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"standard_controls": {}}
    
    def generate_controls(self, hazard: Dict) -> Dict:
        """Generate controls for a specific hazard"""
        hazard_id = hazard.get("hazard_id")
        
        # Get controls from database
        standard_controls = self.controls.get("standard_controls", {})
        hazard_controls = standard_controls.get(hazard_id, {})
        
        return {
            "hazard_id": hazard_id,
            "hazard_name": hazard.get("hazard_name"),
            "engineering_controls": hazard_controls.get("engineering", ["Conduct risk assessment", "Implement engineering solutions"]),
            "administrative_controls": hazard_controls.get("administrative", ["Provide training", "Establish procedures"]),
            "ppe_recommendations": hazard_controls.get("ppe", ["Provide appropriate PPE", "Ensure proper fit and training"])
        }
    
    def generate_all_controls(self, processed_hazards: List[Dict]) -> List[Dict]:
        """Generate controls for all hazards"""
        all_controls = []
        for hazard in processed_hazards:
            controls = self.generate_controls(hazard)
            all_controls.append(controls)
        return all_controls
