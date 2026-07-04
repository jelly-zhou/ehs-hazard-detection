"""
Report Generator
Generates structured EHS inspection reports.
"""

from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generate EHS inspection reports"""
    
    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report(self, risk_summary: Dict, processed_hazards: List[Dict], controls: List[Dict]) -> Dict:
        """
        Generate comprehensive EHS report
        
        Returns:
            Dict with report structure
        """
        report = {
            "metadata": {
                "report_date": self.report_date,
                "report_type": "AI-Powered EHS Inspection Report",
                "standard": "ISO 45001:2018",
                "version": "1.0"
            },
            "executive_summary": self._generate_summary(risk_summary),
            "risk_overview": risk_summary,
            "detected_hazards": processed_hazards,
            "control_measures": controls,
            "iso_compliance": self._map_iso_compliance(processed_hazards),
            "recommendations": self._generate_recommendations(processed_hazards, risk_summary)
        }
        return report
    
    def _generate_summary(self, risk_summary: Dict) -> str:
        """Generate executive summary"""
        total = risk_summary.get("total_hazards", 0)
        critical = risk_summary.get("critical_count", 0)
        high = risk_summary.get("high_count", 0)
        
        summary = f"Inspection Summary:\n"
        summary += f"- Total Hazards Detected: {total}\n"
        summary += f"- Critical Issues: {critical}\n"
        summary += f"- High Risk Issues: {high}\n"
        summary += f"- Average Risk Score: {risk_summary.get('average_risk_score', 0)}/25"
        
        return summary
    
    def _map_iso_compliance(self, processed_hazards: List[Dict]) -> Dict:
        """Map hazards to ISO 45001 clauses"""
        iso_mapping = {
            "clause_6": "Risk Assessment & Management",
            "clause_8": "Operational Control",
            "clause_10": "Continuous Improvement",
            "related_hazards": len(processed_hazards)
        }
        return iso_mapping
    
    def _generate_recommendations(self, processed_hazards: List[Dict], risk_summary: Dict) -> List[str]:
        """Generate action recommendations"""
        recommendations = []
        
        if risk_summary.get("critical_count", 0) > 0:
            recommendations.append("🔴 URGENT: Address all critical hazards immediately")
        
        if risk_summary.get("high_count", 0) > 0:
            recommendations.append("🟠 Prioritize high-risk issues within 7 days")
        
        recommendations.append("📋 Implement all recommended control measures")
        recommendations.append("👥 Conduct safety training for affected personnel")
        recommendations.append("📅 Schedule follow-up inspection in 30 days")
        
        return recommendations
    
    def export_markdown(self, report: Dict) -> str:
        """Export report as Markdown"""
        md = f"# EHS Inspection Report\n\n"
        md += f"**Report Date:** {report['metadata']['report_date']}\n"
        md += f"**Standard:** {report['metadata']['standard']}\n\n"
        
        md += f"## Executive Summary\n{report['executive_summary']}\n\n"
        
        md += f"## Risk Overview\n"
        summary = report['risk_overview']
        md += f"- Total Hazards: {summary['total_hazards']}\n"
        md += f"- Critical: {summary['critical_count']} | High: {summary['high_count']} | Medium: {summary['medium_count']} | Low: {summary['low_count']}\n\n"
        
        md += f"## Detected Hazards\n"
        for hazard in report['detected_hazards']:
            md += f"### {hazard['hazard_name']}\n"
            md += f"- Confidence: {hazard['confidence']*100:.0f}%\n"
            md += f"- Risk Score: {hazard['risk_score']}/25 ({hazard['risk_level']})\n"
            md += f"- Severity: {hazard['severity']}/5 | Probability: {hazard['probability']}/5\n\n"
        
        md += f"## Recommendations\n"
        for rec in report['recommendations']:
            md += f"- {rec}\n"
        
        return md
