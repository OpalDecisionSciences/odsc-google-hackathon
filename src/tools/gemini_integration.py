"""
Advanced Gemini AI Integration for Strategic Business Analysis
Enhanced AI capabilities for business intelligence and decision making
"""

import google.generativeai as genai
import json
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import os
from dataclasses import dataclass
import logging

@dataclass
class AnalysisResult:
    analysis_type: str
    confidence: float
    insights: Dict[str, Any]
    recommendations: List[str]
    data_sources: List[str]
    timestamp: datetime
    metadata: Dict[str, Any]

class GeminiAnalyzer:
    """Advanced Gemini-powered business analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Analysis templates
        self.analysis_templates = {
            "swot": self._get_swot_template(),
            "market_analysis": self._get_market_analysis_template(),
            "competitive_intelligence": self._get_competitive_template(),
            "financial_analysis": self._get_financial_template(),
            "customer_insights": self._get_customer_template(),
            "operational_efficiency": self._get_operational_template(),
            "risk_assessment": self._get_risk_template(),
            "growth_strategy": self._get_growth_template()
        }
    
    async def perform_swot_analysis(self, 
                                   company_data: Dict[str, Any],
                                   market_data: Dict[str, Any],
                                   competitive_data: Dict[str, Any]) -> AnalysisResult:
        """Comprehensive SWOT analysis using Gemini AI"""
        
        prompt = self.analysis_templates["swot"].format(
            company_data=json.dumps(company_data, indent=2),
            market_data=json.dumps(market_data, indent=2),
            competitive_data=json.dumps(competitive_data, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="swot",
                confidence=analysis.get("confidence", 0.8),
                insights=analysis.get("swot_matrix", {}),
                recommendations=analysis.get("strategic_recommendations", []),
                data_sources=["company_data", "market_data", "competitive_data"],
                timestamp=datetime.now(),
                metadata={
                    "model": "gemini-pro",
                    "prompt_length": len(prompt),
                    "response_length": len(response.text)
                }
            )
        except Exception as e:
            logging.error(f"SWOT analysis failed: {e}")
            raise
    
    async def analyze_market_opportunity(self, 
                                       market_data: Dict[str, Any],
                                       business_model: Dict[str, Any]) -> AnalysisResult:
        """Market opportunity analysis with TAM/SAM/SOM calculation"""
        
        prompt = self.analysis_templates["market_analysis"].format(
            market_data=json.dumps(market_data, indent=2),
            business_model=json.dumps(business_model, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="market_opportunity",
                confidence=analysis.get("confidence", 0.75),
                insights=analysis.get("market_insights", {}),
                recommendations=analysis.get("market_recommendations", []),
                data_sources=["market_data", "business_model"],
                timestamp=datetime.now(),
                metadata={"tam_sam_som": analysis.get("market_sizing", {})}
            )
        except Exception as e:
            logging.error(f"Market analysis failed: {e}")
            raise
    
    async def competitive_intelligence_analysis(self, 
                                              competitors: List[Dict[str, Any]],
                                              own_company: Dict[str, Any]) -> AnalysisResult:
        """Deep competitive intelligence analysis"""
        
        prompt = self.analysis_templates["competitive_intelligence"].format(
            competitors=json.dumps(competitors, indent=2),
            own_company=json.dumps(own_company, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="competitive_intelligence",
                confidence=analysis.get("confidence", 0.8),
                insights=analysis.get("competitive_landscape", {}),
                recommendations=analysis.get("competitive_strategy", []),
                data_sources=["competitor_data", "company_data"],
                timestamp=datetime.now(),
                metadata={
                    "competitors_analyzed": len(competitors),
                    "competitive_positioning": analysis.get("positioning", {})
                }
            )
        except Exception as e:
            logging.error(f"Competitive analysis failed: {e}")
            raise
    
    async def financial_health_analysis(self, 
                                      financial_data: Dict[str, Any],
                                      industry_benchmarks: Dict[str, Any]) -> AnalysisResult:
        """Comprehensive financial health and performance analysis"""
        
        prompt = self.analysis_templates["financial_analysis"].format(
            financial_data=json.dumps(financial_data, indent=2),
            benchmarks=json.dumps(industry_benchmarks, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="financial_health",
                confidence=analysis.get("confidence", 0.85),
                insights=analysis.get("financial_insights", {}),
                recommendations=analysis.get("financial_recommendations", []),
                data_sources=["financial_data", "industry_benchmarks"],
                timestamp=datetime.now(),
                metadata={
                    "key_ratios": analysis.get("key_ratios", {}),
                    "financial_score": analysis.get("overall_score", 0)
                }
            )
        except Exception as e:
            logging.error(f"Financial analysis failed: {e}")
            raise
    
    async def customer_insights_analysis(self, 
                                       customer_data: Dict[str, Any],
                                       behavioral_data: Dict[str, Any]) -> AnalysisResult:
        """Advanced customer behavior and segmentation analysis"""
        
        prompt = self.analysis_templates["customer_insights"].format(
            customer_data=json.dumps(customer_data, indent=2),
            behavioral_data=json.dumps(behavioral_data, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="customer_insights",
                confidence=analysis.get("confidence", 0.8),
                insights=analysis.get("customer_insights", {}),
                recommendations=analysis.get("customer_strategy", []),
                data_sources=["customer_data", "behavioral_data"],
                timestamp=datetime.now(),
                metadata={
                    "segments_identified": analysis.get("segments", []),
                    "churn_risk": analysis.get("churn_analysis", {})
                }
            )
        except Exception as e:
            logging.error(f"Customer analysis failed: {e}")
            raise
    
    async def operational_efficiency_analysis(self, 
                                            process_data: Dict[str, Any],
                                            performance_metrics: Dict[str, Any]) -> AnalysisResult:
        """Operational efficiency and process optimization analysis"""
        
        prompt = self.analysis_templates["operational_efficiency"].format(
            process_data=json.dumps(process_data, indent=2),
            metrics=json.dumps(performance_metrics, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="operational_efficiency",
                confidence=analysis.get("confidence", 0.75),
                insights=analysis.get("efficiency_insights", {}),
                recommendations=analysis.get("optimization_recommendations", []),
                data_sources=["process_data", "performance_metrics"],
                timestamp=datetime.now(),
                metadata={
                    "bottlenecks": analysis.get("bottlenecks", []),
                    "efficiency_score": analysis.get("efficiency_score", 0)
                }
            )
        except Exception as e:
            logging.error(f"Operational analysis failed: {e}")
            raise
    
    async def risk_assessment_analysis(self, 
                                     business_data: Dict[str, Any],
                                     market_conditions: Dict[str, Any],
                                     regulatory_environment: Dict[str, Any]) -> AnalysisResult:
        """Comprehensive business risk assessment"""
        
        prompt = self.analysis_templates["risk_assessment"].format(
            business_data=json.dumps(business_data, indent=2),
            market_conditions=json.dumps(market_conditions, indent=2),
            regulatory_environment=json.dumps(regulatory_environment, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="risk_assessment",
                confidence=analysis.get("confidence", 0.8),
                insights=analysis.get("risk_insights", {}),
                recommendations=analysis.get("risk_mitigation", []),
                data_sources=["business_data", "market_conditions", "regulatory_environment"],
                timestamp=datetime.now(),
                metadata={
                    "risk_level": analysis.get("overall_risk_level", "medium"),
                    "critical_risks": analysis.get("critical_risks", [])
                }
            )
        except Exception as e:
            logging.error(f"Risk analysis failed: {e}")
            raise
    
    async def growth_strategy_analysis(self, 
                                     current_state: Dict[str, Any],
                                     growth_objectives: Dict[str, Any],
                                     market_opportunities: Dict[str, Any]) -> AnalysisResult:
        """Strategic growth planning and opportunity analysis"""
        
        prompt = self.analysis_templates["growth_strategy"].format(
            current_state=json.dumps(current_state, indent=2),
            objectives=json.dumps(growth_objectives, indent=2),
            opportunities=json.dumps(market_opportunities, indent=2)
        )
        
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            analysis = self._parse_json_response(response.text)
            
            return AnalysisResult(
                analysis_type="growth_strategy",
                confidence=analysis.get("confidence", 0.8),
                insights=analysis.get("growth_insights", {}),
                recommendations=analysis.get("growth_roadmap", []),
                data_sources=["current_state", "growth_objectives", "market_opportunities"],
                timestamp=datetime.now(),
                metadata={
                    "growth_vectors": analysis.get("growth_vectors", []),
                    "timeline": analysis.get("implementation_timeline", {})
                }
            )
        except Exception as e:
            logging.error(f"Growth strategy analysis failed: {e}")
            raise
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from Gemini, handling potential formatting issues"""
        try:
            # Clean up response text
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            # Return a structured error response
            return {
                "error": "Failed to parse AI response",
                "raw_response": response_text,
                "confidence": 0.0,
                "insights": {},
                "recommendations": ["Review data quality and try again"]
            }
    
    def _get_swot_template(self) -> str:
        return """
        Perform a comprehensive SWOT analysis based on the provided data.
        
        Company Data: {company_data}
        Market Data: {market_data}
        Competitive Data: {competitive_data}
        
        Provide a detailed SWOT analysis as JSON with the following structure:
        {{
            "swot_matrix": {{
                "strengths": [
                    {{"factor": "strength description", "impact": "high/medium/low", "strategic_value": "explanation"}}
                ],
                "weaknesses": [
                    {{"factor": "weakness description", "impact": "high/medium/low", "improvement_potential": "explanation"}}
                ],
                "opportunities": [
                    {{"factor": "opportunity description", "market_size": "large/medium/small", "timeframe": "short/medium/long-term"}}
                ],
                "threats": [
                    {{"factor": "threat description", "probability": "high/medium/low", "mitigation_strategy": "explanation"}}
                ]
            }},
            "strategic_implications": {{
                "so_strategies": ["leverage strengths to capture opportunities"],
                "wo_strategies": ["overcome weaknesses to capture opportunities"],
                "st_strategies": ["use strengths to defend against threats"],
                "wt_strategies": ["minimize weaknesses and avoid threats"]
            }},
            "strategic_recommendations": [
                "prioritized list of strategic actions"
            ],
            "confidence": 0.85,
            "key_insights": [
                "most important insights from the analysis"
            ]
        }}
        """
    
    def _get_market_analysis_template(self) -> str:
        return """
        Analyze market opportunity and provide TAM/SAM/SOM estimates.
        
        Market Data: {market_data}
        Business Model: {business_model}
        
        Provide comprehensive market analysis as JSON:
        {{
            "market_sizing": {{
                "tam": {{"value": "total addressable market", "currency": "USD", "timeframe": "annual"}},
                "sam": {{"value": "serviceable addressable market", "currency": "USD", "reasoning": "explanation"}},
                "som": {{"value": "serviceable obtainable market", "currency": "USD", "assumptions": "key assumptions"}}
            }},
            "market_insights": {{
                "growth_rate": "market growth percentage",
                "key_trends": ["important market trends"],
                "customer_segments": ["primary customer segments"],
                "market_maturity": "emerging/growth/mature/decline"
            }},
            "market_recommendations": [
                "actionable market entry/expansion strategies"
            ],
            "competitive_dynamics": {{
                "market_concentration": "fragmented/consolidated",
                "barriers_to_entry": ["key barriers"],
                "differentiation_opportunities": ["ways to differentiate"]
            }},
            "confidence": 0.8
        }}
        """
    
    def _get_competitive_template(self) -> str:
        return """
        Perform competitive intelligence analysis.
        
        Competitors: {competitors}
        Own Company: {own_company}
        
        Provide competitive analysis as JSON:
        {{
            "competitive_landscape": {{
                "market_leaders": ["top competitors"],
                "competitive_intensity": "high/medium/low",
                "competitive_advantages": ["our key advantages"],
                "competitive_gaps": ["areas where we lag"]
            }},
            "competitor_profiles": [
                {{
                    "name": "competitor name",
                    "market_share": "percentage",
                    "strengths": ["key strengths"],
                    "weaknesses": ["key weaknesses"],
                    "strategy": "their apparent strategy"
                }}
            ],
            "positioning": {{
                "our_position": "market position description",
                "positioning_strategy": "recommended positioning",
                "differentiation_factors": ["unique value propositions"]
            }},
            "competitive_strategy": [
                "strategic recommendations to compete effectively"
            ],
            "threats_and_opportunities": {{
                "competitive_threats": ["immediate threats"],
                "market_gaps": ["opportunities to exploit"]
            }},
            "confidence": 0.8
        }}
        """
    
    def _get_financial_template(self) -> str:
        return """
        Analyze financial health and performance.
        
        Financial Data: {financial_data}
        Industry Benchmarks: {benchmarks}
        
        Provide financial analysis as JSON:
        {{
            "financial_insights": {{
                "profitability": {{
                    "gross_margin": "percentage and trend",
                    "operating_margin": "percentage and trend", 
                    "net_margin": "percentage and trend"
                }},
                "liquidity": {{
                    "current_ratio": "value and assessment",
                    "quick_ratio": "value and assessment",
                    "cash_position": "strength assessment"
                }},
                "efficiency": {{
                    "asset_turnover": "value and trend",
                    "inventory_turnover": "value if applicable",
                    "receivables_turnover": "value and trend"
                }},
                "leverage": {{
                    "debt_to_equity": "value and risk assessment",
                    "interest_coverage": "value and sustainability",
                    "debt_service_capacity": "assessment"
                }}
            }},
            "key_ratios": {{
                "compared_to_industry": "above/at/below average",
                "trending": "improving/stable/declining",
                "critical_ratios": ["most important ratios to watch"]
            }},
            "financial_recommendations": [
                "specific actions to improve financial health"
            ],
            "overall_score": 75,
            "confidence": 0.85
        }}
        """
    
    def _get_customer_template(self) -> str:
        return """
        Analyze customer behavior and segments.
        
        Customer Data: {customer_data}
        Behavioral Data: {behavioral_data}
        
        Provide customer analysis as JSON:
        {{
            "customer_insights": {{
                "customer_lifetime_value": {{
                    "average_clv": "value",
                    "clv_by_segment": {{"segment": "value"}},
                    "clv_trends": "improving/stable/declining"
                }},
                "customer_acquisition": {{
                    "cost_per_acquisition": "value",
                    "best_channels": ["most effective channels"],
                    "conversion_rates": "percentage by channel"
                }},
                "customer_retention": {{
                    "retention_rate": "percentage",
                    "churn_rate": "percentage",
                    "retention_drivers": ["key factors"]
                }}
            }},
            "segments": [
                {{
                    "name": "segment name",
                    "size": "percentage of customer base",
                    "characteristics": ["key characteristics"],
                    "value": "high/medium/low value",
                    "growth_potential": "high/medium/low"
                }}
            ],
            "customer_strategy": [
                "recommendations for customer growth and retention"
            ],
            "churn_analysis": {{
                "high_risk_indicators": ["warning signs"],
                "prevention_strategies": ["retention tactics"]
            }},
            "confidence": 0.8
        }}
        """
    
    def _get_operational_template(self) -> str:
        return """
        Analyze operational efficiency and identify improvements.
        
        Process Data: {process_data}
        Performance Metrics: {metrics}
        
        Provide operational analysis as JSON:
        {{
            "efficiency_insights": {{
                "process_efficiency": {{
                    "cycle_times": "current vs optimal",
                    "throughput": "current capacity utilization",
                    "quality_metrics": "defect rates and quality scores"
                }},
                "resource_utilization": {{
                    "human_resources": "utilization and productivity",
                    "equipment": "utilization and effectiveness",
                    "facilities": "space and resource efficiency"
                }},
                "cost_analysis": {{
                    "cost_per_unit": "current cost structure",
                    "cost_drivers": ["primary cost components"],
                    "cost_reduction_opportunities": ["areas for savings"]
                }}
            }},
            "bottlenecks": [
                {{
                    "process": "bottleneck location",
                    "impact": "high/medium/low",
                    "solution": "recommended fix"
                }}
            ],
            "optimization_recommendations": [
                "specific process improvements with expected ROI"
            ],
            "efficiency_score": 78,
            "confidence": 0.75
        }}
        """
    
    def _get_risk_template(self) -> str:
        return """
        Assess business risks across multiple dimensions.
        
        Business Data: {business_data}
        Market Conditions: {market_conditions}
        Regulatory Environment: {regulatory_environment}
        
        Provide risk assessment as JSON:
        {{
            "risk_insights": {{
                "strategic_risks": [
                    {{
                        "risk": "risk description",
                        "probability": "high/medium/low",
                        "impact": "high/medium/low",
                        "mitigation": "mitigation strategy"
                    }}
                ],
                "operational_risks": [
                    {{
                        "risk": "operational risk",
                        "probability": "high/medium/low",
                        "impact": "high/medium/low",
                        "controls": "existing controls"
                    }}
                ],
                "financial_risks": [
                    {{
                        "risk": "financial risk",
                        "probability": "high/medium/low",
                        "impact": "high/medium/low",
                        "hedging": "risk management approach"
                    }}
                ],
                "compliance_risks": [
                    {{
                        "risk": "regulatory/compliance risk",
                        "probability": "high/medium/low",
                        "impact": "high/medium/low",
                        "compliance_measures": "required actions"
                    }}
                ]
            }},
            "overall_risk_level": "high/medium/low",
            "critical_risks": [
                "risks requiring immediate attention"
            ],
            "risk_mitigation": [
                "prioritized risk mitigation strategies"
            ],
            "confidence": 0.8
        }}
        """
    
    def _get_growth_template(self) -> str:
        return """
        Develop growth strategy and roadmap.
        
        Current State: {current_state}
        Growth Objectives: {objectives}
        Market Opportunities: {opportunities}
        
        Provide growth strategy as JSON:
        {{
            "growth_insights": {{
                "growth_potential": {{
                    "market_expansion": "opportunity size and feasibility",
                    "product_expansion": "new product/service opportunities",
                    "geographic_expansion": "new market opportunities",
                    "customer_expansion": "customer base growth potential"
                }},
                "growth_drivers": [
                    {{
                        "driver": "growth driver",
                        "impact_potential": "high/medium/low",
                        "timeline": "short/medium/long-term",
                        "investment_required": "high/medium/low"
                    }}
                ]
            }},
            "growth_vectors": [
                {{
                    "strategy": "growth strategy",
                    "market": "target market",
                    "investment": "required investment",
                    "timeline": "implementation timeline",
                    "expected_roi": "return on investment"
                }}
            ],
            "growth_roadmap": [
                "prioritized growth initiatives with timelines"
            ],
            "implementation_timeline": {{
                "phase_1": "months 1-6 initiatives",
                "phase_2": "months 7-12 initiatives", 
                "phase_3": "year 2+ initiatives"
            }},
            "success_metrics": [
                "KPIs to track growth progress"
            ],
            "confidence": 0.8
        }}
        """

class BusinessIntelligenceEngine:
    """Comprehensive business intelligence using Gemini AI"""
    
    def __init__(self, gemini_analyzer: GeminiAnalyzer):
        self.analyzer = gemini_analyzer
        self.analysis_cache: Dict[str, AnalysisResult] = {}
        self.analysis_history: List[AnalysisResult] = []
    
    async def comprehensive_business_analysis(self, 
                                            business_data: Dict[str, Any]) -> Dict[str, AnalysisResult]:
        """Perform comprehensive multi-dimensional business analysis"""
        
        analyses = {}
        
        # Extract relevant data for each analysis type
        company_data = business_data.get("company", {})
        market_data = business_data.get("market", {})
        financial_data = business_data.get("financial", {})
        competitive_data = business_data.get("competitive", {})
        customer_data = business_data.get("customer", {})
        
        # Perform parallel analyses
        analysis_tasks = []
        
        if company_data and market_data and competitive_data:
            analysis_tasks.append(
                ("swot", self.analyzer.perform_swot_analysis(company_data, market_data, competitive_data))
            )
        
        if market_data and company_data.get("business_model"):
            analysis_tasks.append(
                ("market_opportunity", self.analyzer.analyze_market_opportunity(market_data, company_data["business_model"]))
            )
        
        if financial_data and business_data.get("industry_benchmarks"):
            analysis_tasks.append(
                ("financial_health", self.analyzer.financial_health_analysis(financial_data, business_data["industry_benchmarks"]))
            )
        
        if customer_data and business_data.get("behavioral_data"):
            analysis_tasks.append(
                ("customer_insights", self.analyzer.customer_insights_analysis(customer_data, business_data["behavioral_data"]))
            )
        
        # Execute analyses
        for analysis_name, analysis_task in analysis_tasks:
            try:
                result = await analysis_task
                analyses[analysis_name] = result
                self.analysis_history.append(result)
            except Exception as e:
                logging.error(f"Analysis {analysis_name} failed: {e}")
                continue
        
        return analyses
    
    async def generate_executive_summary(self, 
                                       analyses: Dict[str, AnalysisResult]) -> Dict[str, Any]:
        """Generate executive summary from multiple analyses"""
        
        # Combine insights from all analyses
        combined_insights = {}
        all_recommendations = []
        confidence_scores = []
        
        for analysis_name, result in analyses.items():
            combined_insights[analysis_name] = result.insights
            all_recommendations.extend(result.recommendations)
            confidence_scores.append(result.confidence)
        
        # Generate summary using Gemini
        summary_prompt = f"""
        Generate an executive summary based on these business analyses:
        
        {json.dumps(combined_insights, indent=2)}
        
        Provide executive summary as JSON:
        {{
            "executive_summary": {{
                "overall_business_health": "excellent/good/fair/poor",
                "key_strengths": ["top 3 strengths"],
                "critical_challenges": ["top 3 challenges"],
                "immediate_priorities": ["top 3 priorities"],
                "strategic_direction": "recommended strategic focus"
            }},
            "key_metrics": {{
                "financial_health_score": "0-100",
                "market_opportunity_score": "0-100", 
                "competitive_position_score": "0-100",
                "operational_efficiency_score": "0-100"
            }},
            "action_plan": {{
                "immediate_actions": ["next 30 days"],
                "short_term_initiatives": ["next 90 days"],
                "long_term_strategy": ["next 12 months"]
            }},
            "investment_priorities": [
                {{
                    "area": "investment area",
                    "rationale": "why invest here",
                    "expected_roi": "expected return",
                    "timeline": "implementation timeline"
                }}
            ]
        }}
        """
        
        try:
            response = await asyncio.to_thread(self.analyzer.model.generate_content, summary_prompt)
            executive_summary = self.analyzer._parse_json_response(response.text)
            
            # Add metadata
            executive_summary["analysis_metadata"] = {
                "analyses_included": list(analyses.keys()),
                "overall_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "analysis_timestamp": datetime.now().isoformat(),
                "recommendations_count": len(all_recommendations)
            }
            
            return executive_summary
            
        except Exception as e:
            logging.error(f"Executive summary generation failed: {e}")
            return {
                "error": "Failed to generate executive summary",
                "analyses_available": list(analyses.keys())
            }
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get history of all analyses performed"""
        return [
            {
                "analysis_type": result.analysis_type,
                "timestamp": result.timestamp.isoformat(),
                "confidence": result.confidence,
                "recommendations_count": len(result.recommendations)
            }
            for result in self.analysis_history
        ]