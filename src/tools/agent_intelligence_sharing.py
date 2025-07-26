"""
Agent Intelligence Sharing Tool
Enables sharing of SWOT-TOWS and other strategic intelligence across all agents
"""

from typing import Dict, Any, Optional, List
from ..tools.swot_tows_analyzer import swot_tows_analyzer

class AgentIntelligenceSharing:
    """Tool for sharing intelligence across all agents in the system"""
    
    def __init__(self):
        self.shared_cache = {}
    
    def get_swot_tows_intelligence(self, company_name: str) -> Dict[str, Any]:
        """Get SWOT-TOWS intelligence for a specific company"""
        return swot_tows_analyzer.get_shared_intelligence(company_name)
    
    def get_strategic_recommendations(self, company_name: str) -> Dict[str, Any]:
        """Get condensed strategic recommendations for agent consumption"""
        return swot_tows_analyzer.get_strategic_recommendations(company_name)
    
    def get_so_strategies(self, company_name: str) -> List[str]:
        """Get SO (Strengths-Opportunities) strategies for the company"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('top_so_strategies', [])
    
    def get_st_strategies(self, company_name: str) -> List[str]:
        """Get ST (Strengths-Threats) strategies for the company"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('top_st_strategies', [])
    
    def get_wo_strategies(self, company_name: str) -> List[str]:
        """Get WO (Weaknesses-Opportunities) strategies for the company"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('top_wo_strategies', [])
    
    def get_wt_strategies(self, company_name: str) -> List[str]:
        """Get WT (Weaknesses-Threats) strategies for the company"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('top_wt_strategies', [])
    
    def get_strategic_position(self, company_name: str) -> str:
        """Get the company's strategic position assessment"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('strategic_position', 'Unknown position')
    
    def get_immediate_priorities(self, company_name: str) -> List[Dict[str, Any]]:
        """Get immediate strategic priorities for the company"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('immediate_priorities', [])
    
    def has_swot_tows_data(self, company_name: str) -> bool:
        """Check if SWOT-TOWS data is available for the company"""
        intelligence = self.get_swot_tows_intelligence(company_name)
        return bool(intelligence and intelligence.get('swot_analysis'))
    
    def get_confidence_score(self, company_name: str) -> float:
        """Get confidence score for the strategic analysis"""
        recommendations = self.get_strategic_recommendations(company_name)
        return recommendations.get('confidence_score', 0.0)
    
    def format_strategic_context_for_agent(self, company_name: str, agent_type: str = "general") -> str:
        """Format strategic context for inclusion in agent prompts"""
        
        if not self.has_swot_tows_data(company_name):
            return ""
        
        recommendations = self.get_strategic_recommendations(company_name)
        strategic_position = recommendations.get('strategic_position', 'Unknown')
        confidence = recommendations.get('confidence_score', 0.0)
        
        context = f"""
**STRATEGIC INTELLIGENCE FOR {company_name.upper()}:**
Strategic Position: {strategic_position}
Analysis Confidence: {confidence:.1%}

**SO Strategies (Growth/Offensive):**
{chr(10).join([f"• {strategy}" for strategy in recommendations.get('top_so_strategies', [])])}

**ST Strategies (Defensive):**
{chr(10).join([f"• {strategy}" for strategy in recommendations.get('top_st_strategies', [])])}

**WO Strategies (Improvement):**
{chr(10).join([f"• {strategy}" for strategy in recommendations.get('top_wo_strategies', [])])}

**WT Strategies (Mitigation):**
{chr(10).join([f"• {strategy}" for strategy in recommendations.get('top_wt_strategies', [])])}

**Immediate Priorities:**
{chr(10).join([f"• {action.get('title', 'Priority action')}" for action in recommendations.get('immediate_priorities', [])])}
"""
        
        # Customize context based on agent type
        if agent_type == "social_media":
            context += f"""
**SOCIAL MEDIA STRATEGIC GUIDANCE:**
Focus on promoting SO strategies through content and engagement.
Monitor competitive threats (ST strategies) through social listening.
Address weaknesses (WO/WT strategies) through community management.
"""
        elif agent_type == "customer_support":
            context += f"""
**CUSTOMER SUPPORT STRATEGIC GUIDANCE:**
Leverage strengths (SO/ST strategies) in customer interactions.
Address improvement areas (WO strategies) through customer feedback.
Mitigate risks (WT strategies) through proactive support.
"""
        elif agent_type == "sales":
            context += f"""
**SALES STRATEGIC GUIDANCE:**
Emphasize competitive advantages (SO strategies) in sales pitches.
Prepare defenses against competitive threats (ST strategies).
Focus on opportunities (SO/WO strategies) in market expansion.
"""
        
        return context.strip()

# Global intelligence sharing instance
agent_intelligence_sharing = AgentIntelligenceSharing()