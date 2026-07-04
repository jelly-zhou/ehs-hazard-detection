"""
Vision Detection Module
Handles AI-based hazard detection from images.
MVP uses simulated detection based on image analysis and predefined rules.
"""

import json
import base64
from typing import List, Dict, Tuple
from PIL import Image
import io
import random


class HazardDetector:
    """Simulated hazard detection system for MVP"""
    
    def __init__(self, hazard_library_path: str = "data/hazard_dataset.json"):
        self.hazards = self._load_hazard_library(hazard_library_path)
        self.confidence_threshold = 0.5
    
    def _load_hazard_library(self, path: str) -> Dict:
        """Load hazard taxonomy"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "hazard_categories": [
                    {
                        "id": "PPE_VIOLATION",
                        "name": "Personal Protective Equipment Violation",
                        "default_severity": 4,
                        "default_probability": 5
                    },
                    {
                        "id": "FIRE_HAZARD",
                        "name": "Fire Hazard",
                        "default_severity": 5,
                        "default_probability": 2
                    }
                ]
            }
    
    def detect_hazards(self, image: Image.Image, image_description: str = None) -> List[Dict]:
        """
        Simulate hazard detection from factory image.
        MVP uses rule-based detection based on image characteristics.
        
        Args:
            image: PIL Image object
            image_description: Optional user-provided description
        
        Returns:
            List of detected hazards with confidence scores
        """
        detected_hazards = []
        
        width, height = image.size
        image_data = self._analyze_image(image)
        
        hazard_rules = {
            "dark_areas": {"hazard": "PPE_VIOLATION", "confidence": 0.72},
            "clutter": {"hazard": "HOUSEKEEPING_HAZARD", "confidence": 0.65},
            "bright_spots": {"hazard": "FIRE_HAZARD", "confidence": 0.58},
            "machinery_shapes": {"hazard": "MACHINERY_HAZARD", "confidence": 0.68},
        }
        
        for feature, rule in hazard_rules.items():
            if image_data.get(feature, False):
                if rule["confidence"] > self.confidence_threshold:
                    hazard = self._create_hazard_detection(
                        rule["hazard"],
                        rule["confidence"]
                    )
                    detected_hazards.append(hazard)
        
        if random.random() > 0.6:
            additional_hazard = self._create_random_hazard()
            detected_hazards.append(additional_hazard)
        
        return detected_hazards
    
    def _analyze_image(self, image: Image.Image) -> Dict:
        """
        Analyze image characteristics for rule-based detection
        Returns dict of detected features
        """
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        pixels = list(image.getdata())
        brightness = sum([sum(p[:3]) / 3 for p in pixels]) / len(pixels) if pixels else 128
        
        return {
            "dark_areas": brightness < 100,
            "clutter": len(pixels) > 100000,
            "bright_spots": brightness > 180,
            "machinery_shapes": True
        }
    
    def _create_hazard_detection(self, hazard_id: str, confidence: float) -> Dict:
        """Create hazard detection object"""
        hazard_template = None
        for cat in self.hazards.get("hazard_categories", []):
            if cat["id"] == hazard_id:
                hazard_template = cat
                break
        
        if not hazard_template:
            hazard_template = {
                "id": hazard_id,
                "name": "Unknown Hazard",
                "default_severity": 3,
                "default_probability": 3
            }
        
        return {
            "hazard_id": hazard_id,
            "hazard_name": hazard_template["name"],
            "description": hazard_template.get("description", ""),
            "confidence": round(confidence, 2),
            "severity": hazard_template["default_severity"],
            "probability": hazard_template["default_probability"],
            "bounding_box": None,
            "timestamp": None
        }
    
    def _create_random_hazard(self) -> Dict:
        """Create a random hazard detection for simulation"""
        categories = self.hazards.get("hazard_categories", [])
        if not categories:
            return self._create_hazard_detection("PPE_VIOLATION", 0.65)
        
        random_category = random.choice(categories)
        confidence = round(random.uniform(0.55, 0.95), 2)
        
        return self._create_hazard_detection(random_category["id"], confidence)
    
    def get_hazard_by_id(self, hazard_id: str) -> Dict:
        """Get full hazard information"""
        for cat in self.hazards.get("hazard_categories", []):
            if cat["id"] == hazard_id:
                return cat
        return None


class ImageProcessor:
    """Handle image processing and validation"""
    
    @staticmethod
    def validate_image(image: Image.Image) -> Tuple[bool, str]:
        """Validate uploaded image"""
        if image.size[0] < 100 or image.size[1] < 100:
            return False, "Image too small (minimum 100x100)"
        
        if image.size[0] > 4000 or image.size[1] > 4000:
            return False, "Image too large (maximum 4000x4000)"
        
        return True, "Image valid"
    
    @staticmethod
    def resize_for_display(image: Image.Image, max_width: int = 800) -> Image.Image:
        """Resize image for display"""
        if image.width > max_width:
            ratio = max_width / image.width
            new_height = int(image.height * ratio)
            return image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        return image
