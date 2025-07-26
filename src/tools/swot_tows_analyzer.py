"""
SWOT-TOWS Matrix MCP Tool
Advanced strategic analysis tool that transforms business intelligence into actionable strategies
"""

import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
from enum import Enum

class StrategyType(Enum):
    """TOWS Strategy Types"""
    SO = "SO"  # Strengths-Opportunities (Offensive/Growth)
    ST = "ST"  # Strengths-Threats (Defensive)
    WO = "WO"  # Weaknesses-Opportunities (Improvement)
    WT = "WT"  # Weaknesses-Threats (Survival/Mitigation)

@dataclass
class SWOTFactor:
    """Individual SWOT factor with metadata"""
    category: str  # 'strength', 'weakness', 'opportunity', 'threat'
    description: str
    impact_level: float  # 1-10 scale
    confidence: float  # 0-1 scale
    source: str  # Where this factor came from
    evidence: List[str]  # Supporting evidence

@dataclass
class TOWSStrategy:
    """Individual TOWS strategy with implementation details"""
    strategy_type: StrategyType
    title: str
    description: str
    priority: str  # 'high', 'medium', 'low'
    implementation_complexity: str  # 'low', 'medium', 'high'
    expected_impact: str  # 'high', 'medium', 'low'
    timeline: str  # 'immediate', 'short_term', 'medium_term', 'long_term'
    resources_required: List[str]
    success_metrics: List[str]
    risk_factors: List[str]
    contributing_factors: Dict[str, List[str]]  # Which S/W/O/T factors contribute

class SWOTTOWSAnalyzer:
    """Advanced SWOT-TOWS Matrix Analyzer MCP Tool"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        self.shared_intelligence = {}  # In-memory cache for current session
        
        # Import persistent memory with Docker-compatible path handling
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from memory.persistent_memory import persistent_memory
            self.persistent_memory = persistent_memory
            self._load_persistent_intelligence()
        except ImportError:
            self.logger.warning("Persistent memory not available - using in-memory only")
            self.persistent_memory = None
    
    def _load_persistent_intelligence(self):
        """Load SWOT intelligence from persistent storage"""
        if self.persistent_memory:
            # Load all stored SWOT intelligence into memory
            stored_intelligence = self.persistent_memory.swot_intelligence
            for company_name, analysis_data in stored_intelligence.items():
                self.shared_intelligence[company_name] = analysis_data
                print(f"📂 Loaded SWOT intelligence for {company_name}")
    
    def _save_to_persistent_memory(self, company_name: str, analysis_result: Dict[str, Any]):
        """Save analysis result to persistent storage"""
        if self.persistent_memory:
            self.persistent_memory.store_swot_intelligence(company_name, analysis_result)
        
    async def analyze_business_intelligence(self, 
                                          business_context: Dict[str, Any],
                                          research_data: Dict[str, Any],
                                          competitive_intelligence: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive SWOT-TOWS analysis using real business intelligence
        
        Args:
            business_context: Core business information from Research Agent
            research_data: Live data from enhanced scraper
            competitive_intelligence: Social media competitive analysis
            
        Returns:
            Complete SWOT-TOWS matrix with actionable strategies
        """
        
        print(f"🔬 SWOT-TOWS Analysis for {business_context.get('business_name', 'Unknown Company')}")
        
        # Step 1: Extract SWOT factors from business intelligence
        swot_factors = await self._extract_swot_factors(business_context, research_data, competitive_intelligence)
        
        # Step 2: Generate TOWS strategies
        tows_strategies = await self._generate_tows_strategies(swot_factors, business_context)
        
        # Step 3: Prioritize and rank strategies
        prioritized_strategies = await self._prioritize_strategies(tows_strategies, business_context)
        
        # Step 4: Create implementation roadmap
        implementation_roadmap = await self._create_implementation_roadmap(prioritized_strategies)
        
        # Step 5: Generate strategic insights summary
        strategic_insights = await self._generate_strategic_insights(swot_factors, prioritized_strategies, business_context)
        
        # Complete analysis result
        analysis_result = {
            "company": business_context.get('business_name', 'Unknown'),
            "industry": business_context.get('industry', 'Unknown'),
            "analysis_timestamp": datetime.now().isoformat(),
            "swot_analysis": {
                "strengths": [f.__dict__ for f in swot_factors if f.category == 'strength'],
                "weaknesses": [f.__dict__ for f in swot_factors if f.category == 'weakness'],
                "opportunities": [f.__dict__ for f in swot_factors if f.category == 'opportunity'],
                "threats": [f.__dict__ for f in swot_factors if f.category == 'threat']
            },
            "tows_matrix": {
                "SO_strategies": [s.__dict__ for s in prioritized_strategies if s.strategy_type == StrategyType.SO],
                "ST_strategies": [s.__dict__ for s in prioritized_strategies if s.strategy_type == StrategyType.ST],
                "WO_strategies": [s.__dict__ for s in prioritized_strategies if s.strategy_type == StrategyType.WO],
                "WT_strategies": [s.__dict__ for s in prioritized_strategies if s.strategy_type == StrategyType.WT]
            },
            "implementation_roadmap": implementation_roadmap,
            "strategic_insights": strategic_insights,
            "data_sources": research_data.get('data_sources', []),
            "confidence_score": self._calculate_overall_confidence(swot_factors),
            "competitive_context": competitive_intelligence is not None
        }
        
        # Store in shared intelligence for all agents to access
        company_name = business_context.get('business_name', 'default')
        self.shared_intelligence[company_name] = analysis_result
        
        # Save to persistent memory for cross-session access
        self._save_to_persistent_memory(company_name, analysis_result)
        
        print(f"✅ SWOT-TOWS Analysis Complete: {len(prioritized_strategies)} strategies generated")
        
        return analysis_result
    
    async def _extract_swot_factors(self, 
                                   business_context: Dict[str, Any], 
                                   research_data: Dict[str, Any],
                                   competitive_intelligence: Dict[str, Any] = None) -> List[SWOTFactor]:
        """Extract SWOT factors from business intelligence data"""
        
        factors = []
        
        # Extract from financial data
        financial_data = research_data.get('financial_data', {})
        if financial_data:
            factors.extend(await self._extract_financial_factors(financial_data, business_context))
        
        # Extract from news sentiment
        news_data = research_data.get('news_sentiment', {})
        if news_data:
            factors.extend(await self._extract_news_factors(news_data, business_context))
        
        # Extract from competitive data
        competitor_data = research_data.get('competitor_data', {})
        if competitor_data:
            factors.extend(await self._extract_competitive_factors(competitor_data, business_context))
        
        # Extract from social intelligence
        if competitive_intelligence:
            factors.extend(await self._extract_social_factors(competitive_intelligence, business_context))
        
        # Extract from industry trends
        industry_data = research_data.get('industry_trends', {})
        if industry_data:
            factors.extend(await self._extract_industry_factors(industry_data, business_context))
        
        return factors
    
    async def _extract_financial_factors(self, financial_data: Dict[str, Any], business_context: Dict[str, Any]) -> List[SWOTFactor]:
        """Extract SWOT factors from financial data"""
        factors = []
        
        # Financial strengths
        if financial_data.get('profit_margin', 0) > 0.15:
            factors.append(SWOTFactor(
                category='strength',
                description=f"Strong profit margins ({financial_data.get('profit_margin', 0)*100:.1f}%)",
                impact_level=8.5,
                confidence=0.9,
                source='yahoo_finance',
                evidence=[f"Profit margin: {financial_data.get('profit_margin', 0)*100:.1f}%"]
            ))
        
        if financial_data.get('month_performance', 0) > 10:
            factors.append(SWOTFactor(
                category='strength',
                description=f"Excellent recent stock performance ({financial_data.get('month_performance', 0):.1f}% monthly gain)",
                impact_level=7.5,
                confidence=0.95,
                source='yahoo_finance',
                evidence=[f"Monthly performance: +{financial_data.get('month_performance', 0):.1f}%"]
            ))
        
        # Financial weaknesses
        if financial_data.get('pe_ratio', 0) > 40:
            factors.append(SWOTFactor(
                category='weakness',
                description=f"High valuation risk (P/E ratio: {financial_data.get('pe_ratio', 0):.1f})",
                impact_level=6.0,
                confidence=0.8,
                source='yahoo_finance',
                evidence=[f"P/E ratio: {financial_data.get('pe_ratio', 0):.1f} (high valuation)"]
            ))
        
        if financial_data.get('month_performance', 0) < -10:
            factors.append(SWOTFactor(
                category='weakness',
                description=f"Recent stock underperformance ({financial_data.get('month_performance', 0):.1f}% monthly decline)",
                impact_level=7.0,
                confidence=0.95,
                source='yahoo_finance',
                evidence=[f"Monthly performance: {financial_data.get('month_performance', 0):.1f}%"]
            ))
        
        return factors
    
    async def _extract_news_factors(self, news_data: Dict[str, Any], business_context: Dict[str, Any]) -> List[SWOTFactor]:
        """Extract SWOT factors from news sentiment"""
        factors = []
        
        sentiment_label = news_data.get('sentiment_label', 'Neutral')
        articles_count = news_data.get('articles_analyzed', 0)
        
        if sentiment_label == 'Positive' and articles_count > 5:
            factors.append(SWOTFactor(
                category='strength',
                description="Strong positive media coverage and public perception",
                impact_level=7.0,
                confidence=0.8,
                source='news_sentiment',
                evidence=[f"Positive sentiment from {articles_count} recent articles"]
            ))
        elif sentiment_label == 'Negative' and articles_count > 3:
            factors.append(SWOTFactor(
                category='threat',
                description="Negative media coverage affecting brand reputation",
                impact_level=6.5,
                confidence=0.8,
                source='news_sentiment',
                evidence=[f"Negative sentiment from {articles_count} recent articles"]
            ))
        
        return factors
    
    async def _extract_competitive_factors(self, competitor_data: Dict[str, Any], business_context: Dict[str, Any]) -> List[SWOTFactor]:
        """Extract SWOT factors from competitive analysis"""
        factors = []
        
        primary_competitors = competitor_data.get('primary_competitors', [])
        competitive_analysis = competitor_data.get('competitive_analysis', [])
        
        # Competitive opportunities and threats
        if len(primary_competitors) >= 3:
            factors.append(SWOTFactor(
                category='threat',
                description=f"Intense competition from {len(primary_competitors)} major players: {', '.join(primary_competitors[:3])}",
                impact_level=8.0,
                confidence=0.9,
                source='competitive_analysis',
                evidence=[f"Major competitors: {', '.join(primary_competitors)}"]
            ))
        
        # Analyze competitive positioning
        our_market_cap = business_context.get('market_cap', 0)
        if competitive_analysis and our_market_cap:
            competitor_caps = [c.get('market_cap', 0) for c in competitive_analysis if isinstance(c.get('market_cap'), (int, float))]
            if competitor_caps:
                avg_competitor_cap = sum(competitor_caps) / len(competitor_caps)
                if our_market_cap > avg_competitor_cap * 1.5:
                    factors.append(SWOTFactor(
                        category='strength',
                        description="Market leadership position with superior market capitalization",
                        impact_level=9.0,
                        confidence=0.95,
                        source='competitive_analysis',
                        evidence=[f"Market cap ${our_market_cap/1e9:.1f}B vs avg competitor ${avg_competitor_cap/1e9:.1f}B"]
                    ))
        
        return factors
    
    async def _extract_social_factors(self, competitive_intelligence: Dict[str, Any], business_context: Dict[str, Any]) -> List[SWOTFactor]:
        """Extract SWOT factors from social media competitive intelligence"""
        factors = []
        
        if competitive_intelligence.get('analysis_type') == 'competitor_performance':
            intel = competitive_intelligence.get('competitive_intelligence', {})
            
            # Social media competitive advantages
            competitive_advantages = intel.get('competitive_advantages', [])
            for advantage in competitive_advantages[:2]:  # Top 2
                factors.append(SWOTFactor(
                    category='strength',
                    description=f"Social media competitive advantage: {advantage}",
                    impact_level=6.5,
                    confidence=0.7,
                    source='social_competitive_analysis',
                    evidence=[f"Competitive advantage identified: {advantage}"]
                ))
            
            # Social media opportunities
            opportunity_gaps = intel.get('opportunity_gaps', [])
            for opportunity in opportunity_gaps[:2]:  # Top 2
                factors.append(SWOTFactor(
                    category='opportunity',
                    description=f"Social media market opportunity: {opportunity}",
                    impact_level=7.0,
                    confidence=0.7,
                    source='social_competitive_analysis',
                    evidence=[f"Opportunity gap identified: {opportunity}"]
                ))
        
        return factors
    
    async def _extract_industry_factors(self, industry_data: Dict[str, Any], business_context: Dict[str, Any]) -> List[SWOTFactor]:
        """Extract SWOT factors from industry trends"""
        factors = []
        
        # Industry growth opportunities
        growth_trend = industry_data.get('growth_trend', '')
        if 'High Growth' in growth_trend:
            factors.append(SWOTFactor(
                category='opportunity',
                description=f"Industry experiencing high growth: {growth_trend}",
                impact_level=8.5,
                confidence=0.85,
                source='industry_analysis',
                evidence=[f"Growth trend: {growth_trend}", f"Market size: {industry_data.get('market_size', 'N/A')}"]
            ))
        
        # Industry drivers as opportunities
        key_drivers = industry_data.get('key_drivers', [])
        for driver in key_drivers[:2]:  # Top 2 drivers
            factors.append(SWOTFactor(
                category='opportunity',
                description=f"Industry growth driver: {driver}",
                impact_level=7.5,
                confidence=0.8,
                source='industry_analysis',
                evidence=[f"Key industry driver: {driver}"]
            ))
        
        # Industry challenges as threats
        challenges = industry_data.get('challenges', [])
        for challenge in challenges[:2]:  # Top 2 challenges
            factors.append(SWOTFactor(
                category='threat',
                description=f"Industry challenge: {challenge}",
                impact_level=6.5,
                confidence=0.8,
                source='industry_analysis',
                evidence=[f"Industry challenge: {challenge}"]
            ))
        
        return factors
    
    async def _generate_tows_strategies(self, swot_factors: List[SWOTFactor], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Generate TOWS strategies by matching internal and external factors"""
        
        strategies = []
        
        # Categorize factors
        strengths = [f for f in swot_factors if f.category == 'strength']
        weaknesses = [f for f in swot_factors if f.category == 'weakness']
        opportunities = [f for f in swot_factors if f.category == 'opportunity']
        threats = [f for f in swot_factors if f.category == 'threat']
        
        # Generate SO Strategies (Strengths-Opportunities)
        strategies.extend(await self._generate_so_strategies(strengths, opportunities, business_context))
        
        # Generate ST Strategies (Strengths-Threats)
        strategies.extend(await self._generate_st_strategies(strengths, threats, business_context))
        
        # Generate WO Strategies (Weaknesses-Opportunities)
        strategies.extend(await self._generate_wo_strategies(weaknesses, opportunities, business_context))
        
        # Generate WT Strategies (Weaknesses-Threats)
        strategies.extend(await self._generate_wt_strategies(weaknesses, threats, business_context))
        
        return strategies
    
    async def _generate_so_strategies(self, strengths: List[SWOTFactor], opportunities: List[SWOTFactor], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Generate Strengths-Opportunities (Offensive/Growth) strategies"""
        strategies = []
        
        company_name = business_context.get('business_name', 'Company')
        industry = business_context.get('industry', 'Technology')
        
        # Match high-impact strengths with high-impact opportunities
        for strength in strengths[:3]:  # Top 3 strengths
            for opportunity in opportunities[:3]:  # Top 3 opportunities
                if strength.impact_level >= 7 and opportunity.impact_level >= 7:
                    
                    strategy = TOWSStrategy(
                        strategy_type=StrategyType.SO,
                        title=f"Leverage {strength.description.split(':')[0] if ':' in strength.description else strength.description[:30]} for {opportunity.description.split(':')[0] if ':' in opportunity.description else opportunity.description[:30]}",
                        description=f"Utilize {company_name}'s {strength.description.lower()} to capitalize on {opportunity.description.lower()}. This offensive strategy maximizes competitive advantage in the {industry} sector.",
                        priority='high' if (strength.impact_level + opportunity.impact_level) > 15 else 'medium',
                        implementation_complexity='medium',
                        expected_impact='high' if (strength.impact_level + opportunity.impact_level) > 15 else 'medium',
                        timeline='short_term' if strength.source == 'yahoo_finance' else 'medium_term',
                        resources_required=['Strategic planning team', 'Market analysis', 'Investment capital'],
                        success_metrics=['Market share growth', 'Revenue increase', 'Competitive positioning improvement'],
                        risk_factors=['Market volatility', 'Competitive response', 'Execution challenges'],
                        contributing_factors={
                            'strengths': [strength.description],
                            'opportunities': [opportunity.description]
                        }
                    )
                    strategies.append(strategy)
        
        # If no high-impact matches, create at least one SO strategy
        if not strategies and strengths and opportunities:
            top_strength = max(strengths, key=lambda x: x.impact_level)
            top_opportunity = max(opportunities, key=lambda x: x.impact_level)
            
            strategy = TOWSStrategy(
                strategy_type=StrategyType.SO,
                title=f"Growth Strategy: Maximize {company_name}'s Competitive Advantages",
                description=f"Leverage {top_strength.description.lower()} to pursue {top_opportunity.description.lower()}. Focus on growth and market expansion.",
                priority='high',
                implementation_complexity='medium',
                expected_impact='high',
                timeline='medium_term',
                resources_required=['Strategic planning', 'Investment', 'Market research'],
                success_metrics=['Revenue growth', 'Market expansion', 'Brand strengthening'],
                risk_factors=['Market conditions', 'Resource constraints'],
                contributing_factors={
                    'strengths': [top_strength.description],
                    'opportunities': [top_opportunity.description]
                }
            )
            strategies.append(strategy)
        
        return strategies[:2]  # Top 2 SO strategies
    
    async def _generate_st_strategies(self, strengths: List[SWOTFactor], threats: List[SWOTFactor], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Generate Strengths-Threats (Defensive) strategies"""
        strategies = []
        
        company_name = business_context.get('business_name', 'Company')
        
        for strength in strengths[:2]:  # Top 2 strengths
            for threat in threats[:2]:  # Top 2 threats
                strategy = TOWSStrategy(
                    strategy_type=StrategyType.ST,
                    title=f"Defend with {strength.description.split()[0]} Against {threat.description.split()[0]} Risks",
                    description=f"Use {company_name}'s {strength.description.lower()} to mitigate risks from {threat.description.lower()}. This defensive strategy protects market position.",
                    priority='high' if threat.impact_level >= 7 else 'medium',
                    implementation_complexity='medium',
                    expected_impact='medium',
                    timeline='immediate' if threat.impact_level >= 8 else 'short_term',
                    resources_required=['Risk management', 'Strategic response team', 'Monitoring systems'],
                    success_metrics=['Risk reduction', 'Market position maintenance', 'Competitive defense'],
                    risk_factors=['Threat escalation', 'Insufficient response', 'Resource allocation'],
                    contributing_factors={
                        'strengths': [strength.description],
                        'threats': [threat.description]
                    }
                )
                strategies.append(strategy)
                break  # One strategy per strength-threat pair
        
        return strategies[:2]  # Top 2 ST strategies
    
    async def _generate_wo_strategies(self, weaknesses: List[SWOTFactor], opportunities: List[SWOTFactor], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Generate Weaknesses-Opportunities (Improvement) strategies"""
        strategies = []
        
        company_name = business_context.get('business_name', 'Company')
        
        for weakness in weaknesses[:2]:  # Top 2 weaknesses
            for opportunity in opportunities[:2]:  # Top 2 opportunities
                strategy = TOWSStrategy(
                    strategy_type=StrategyType.WO,
                    title=f"Improve {weakness.description.split()[0]} Through {opportunity.description.split()[0]} Leverage",
                    description=f"Address {company_name}'s {weakness.description.lower()} by leveraging {opportunity.description.lower()}. This improvement strategy builds capabilities.",
                    priority='medium',
                    implementation_complexity='high' if weakness.impact_level >= 7 else 'medium',
                    expected_impact='medium',
                    timeline='medium_term',
                    resources_required=['Development investment', 'Training programs', 'External partnerships'],
                    success_metrics=['Capability improvement', 'Weakness mitigation', 'Opportunity capture'],
                    risk_factors=['Implementation delays', 'Resource constraints', 'Market timing'],
                    contributing_factors={
                        'weaknesses': [weakness.description],
                        'opportunities': [opportunity.description]
                    }
                )
                strategies.append(strategy)
                break  # One strategy per weakness-opportunity pair
        
        return strategies[:2]  # Top 2 WO strategies
    
    async def _generate_wt_strategies(self, weaknesses: List[SWOTFactor], threats: List[SWOTFactor], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Generate Weaknesses-Threats (Survival/Mitigation) strategies"""
        strategies = []
        
        company_name = business_context.get('business_name', 'Company')
        
        for weakness in weaknesses[:2]:  # Top 2 weaknesses
            for threat in threats[:2]:  # Top 2 threats
                strategy = TOWSStrategy(
                    strategy_type=StrategyType.WT,
                    title=f"Mitigate {weakness.description.split()[0]} and {threat.description.split()[0]} Risks",
                    description=f"Minimize {company_name}'s {weakness.description.lower()} while avoiding {threat.description.lower()}. This survival strategy reduces overall risk exposure.",
                    priority='high' if (weakness.impact_level + threat.impact_level) > 13 else 'medium',
                    implementation_complexity='medium',
                    expected_impact='medium',
                    timeline='immediate' if (weakness.impact_level + threat.impact_level) > 14 else 'short_term',
                    resources_required=['Risk mitigation', 'Cost reduction', 'Efficiency improvement'],
                    success_metrics=['Risk reduction', 'Cost savings', 'Operational efficiency'],
                    risk_factors=['Continued exposure', 'Limited resources', 'Market pressures'],
                    contributing_factors={
                        'weaknesses': [weakness.description],
                        'threats': [threat.description]
                    }
                )
                strategies.append(strategy)
                break  # One strategy per weakness-threat pair
        
        return strategies[:2]  # Top 2 WT strategies
    
    async def _prioritize_strategies(self, strategies: List[TOWSStrategy], business_context: Dict[str, Any]) -> List[TOWSStrategy]:
        """Prioritize strategies based on impact, feasibility, and strategic fit"""
        
        def priority_score(strategy: TOWSStrategy) -> float:
            score = 0
            
            # Priority weight
            if strategy.priority == 'high':
                score += 3
            elif strategy.priority == 'medium':
                score += 2
            else:
                score += 1
            
            # Expected impact weight
            if strategy.expected_impact == 'high':
                score += 3
            elif strategy.expected_impact == 'medium':
                score += 2
            else:
                score += 1
            
            # Implementation complexity (inverse weight)
            if strategy.implementation_complexity == 'low':
                score += 2
            elif strategy.implementation_complexity == 'medium':
                score += 1
            # High complexity gets 0 additional points
            
            # Timeline urgency
            if strategy.timeline == 'immediate':
                score += 2
            elif strategy.timeline == 'short_term':
                score += 1.5
            elif strategy.timeline == 'medium_term':
                score += 1
            # Long term gets 0.5 additional points
            else:
                score += 0.5
            
            return score
        
        # Sort strategies by priority score
        prioritized = sorted(strategies, key=priority_score, reverse=True)
        
        # Ensure balanced representation across strategy types
        balanced_strategies = []
        strategy_counts = {StrategyType.SO: 0, StrategyType.ST: 0, StrategyType.WO: 0, StrategyType.WT: 0}
        
        for strategy in prioritized:
            if strategy_counts[strategy.strategy_type] < 2:  # Max 2 per type
                balanced_strategies.append(strategy)
                strategy_counts[strategy.strategy_type] += 1
        
        return balanced_strategies[:8]  # Top 8 strategies total
    
    async def _create_implementation_roadmap(self, strategies: List[TOWSStrategy]) -> Dict[str, Any]:
        """Create implementation roadmap for prioritized strategies"""
        
        roadmap = {
            "immediate_actions": [],
            "short_term_initiatives": [],
            "medium_term_projects": [],
            "long_term_goals": [],
            "resource_allocation": {},
            "success_milestones": {},
            "risk_mitigation": {}
        }
        
        # Categorize strategies by timeline
        for strategy in strategies:
            timeline_key = f"{strategy.timeline}_actions" if strategy.timeline == "immediate" else f"{strategy.timeline}_initiatives" if strategy.timeline == "short_term" else f"{strategy.timeline}_projects" if strategy.timeline == "medium_term" else "long_term_goals"
            
            if timeline_key in roadmap:
                roadmap[timeline_key].append({
                    "strategy_type": strategy.strategy_type.value,
                    "title": strategy.title,
                    "priority": strategy.priority,
                    "expected_impact": strategy.expected_impact,
                    "resources_required": strategy.resources_required,
                    "success_metrics": strategy.success_metrics
                })
        
        # Aggregate resource requirements
        all_resources = []
        for strategy in strategies:
            all_resources.extend(strategy.resources_required)
        
        from collections import Counter
        resource_counts = Counter(all_resources)
        roadmap["resource_allocation"] = {
            "critical_resources": [resource for resource, count in resource_counts.most_common(5)],
            "resource_intensity": dict(resource_counts.most_common(10))
        }
        
        return roadmap
    
    async def _generate_strategic_insights(self, 
                                         swot_factors: List[SWOTFactor], 
                                         strategies: List[TOWSStrategy], 
                                         business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level strategic insights from SWOT-TOWS analysis"""
        
        company_name = business_context.get('business_name', 'Company')
        industry = business_context.get('industry', 'Technology')
        
        # Calculate strategic position
        strength_score = sum(f.impact_level for f in swot_factors if f.category == 'strength') / len([f for f in swot_factors if f.category == 'strength']) if [f for f in swot_factors if f.category == 'strength'] else 0
        weakness_score = sum(f.impact_level for f in swot_factors if f.category == 'weakness') / len([f for f in swot_factors if f.category == 'weakness']) if [f for f in swot_factors if f.category == 'weakness'] else 0
        opportunity_score = sum(f.impact_level for f in swot_factors if f.category == 'opportunity') / len([f for f in swot_factors if f.category == 'opportunity']) if [f for f in swot_factors if f.category == 'opportunity'] else 0
        threat_score = sum(f.impact_level for f in swot_factors if f.category == 'threat') / len([f for f in swot_factors if f.category == 'threat']) if [f for f in swot_factors if f.category == 'threat'] else 0
        
        # Determine strategic position
        internal_strength = strength_score - weakness_score
        external_favorability = opportunity_score - threat_score
        
        if internal_strength > 0 and external_favorability > 0:
            strategic_position = "Star Position: Strong internal capabilities in favorable market"
            recommended_focus = "SO strategies - Aggressive growth and market expansion"
        elif internal_strength > 0 and external_favorability <= 0:
            strategic_position = "Defensive Position: Strong capabilities facing market challenges"
            recommended_focus = "ST strategies - Defensive positioning and threat mitigation"
        elif internal_strength <= 0 and external_favorability > 0:
            strategic_position = "Improvement Position: Building capabilities in favorable market"
            recommended_focus = "WO strategies - Capability building and market capture"
        else:
            strategic_position = "Survival Position: Addressing weaknesses in challenging market"
            recommended_focus = "WT strategies - Risk mitigation and efficiency improvement"
        
        # Strategy distribution analysis
        strategy_distribution = {strategy_type.value: len([s for s in strategies if s.strategy_type == strategy_type]) for strategy_type in StrategyType}
        
        insights = {
            "strategic_position": strategic_position,
            "recommended_focus": recommended_focus,
            "strategic_scores": {
                "internal_strength": round(internal_strength, 2),
                "external_favorability": round(external_favorability, 2),
                "overall_position": round((internal_strength + external_favorability) / 2, 2)
            },
            "factor_summary": {
                "strengths_count": len([f for f in swot_factors if f.category == 'strength']),
                "weaknesses_count": len([f for f in swot_factors if f.category == 'weakness']),
                "opportunities_count": len([f for f in swot_factors if f.category == 'opportunity']),
                "threats_count": len([f for f in swot_factors if f.category == 'threat']),
                "avg_strength_impact": round(strength_score, 2),
                "avg_opportunity_impact": round(opportunity_score, 2)
            },
            "strategy_distribution": strategy_distribution,
            "top_strategic_priorities": [s.title for s in strategies[:3]],
            "critical_success_factors": list(set([metric for strategy in strategies for metric in strategy.success_metrics]))[:5],
            "key_risk_factors": list(set([risk for strategy in strategies for risk in strategy.risk_factors]))[:5],
            "competitive_context": f"{company_name} in {industry} sector strategic analysis",
            "implementation_complexity": "High" if sum(1 for s in strategies if s.implementation_complexity == 'high') > 2 else "Medium"
        }
        
        return insights
    
    def _calculate_overall_confidence(self, swot_factors: List[SWOTFactor]) -> float:
        """Calculate overall confidence score for the analysis"""
        if not swot_factors:
            return 0.0
        
        total_confidence = sum(factor.confidence for factor in swot_factors)
        avg_confidence = total_confidence / len(swot_factors)
        
        # Adjust for data source diversity
        unique_sources = len(set(factor.source for factor in swot_factors))
        source_bonus = min(0.1, unique_sources * 0.02)  # Up to 10% bonus for diverse sources
        
        return min(1.0, avg_confidence + source_bonus)
    
    def get_shared_intelligence(self, company_name: str = None) -> Dict[str, Any]:
        """Get shared SWOT-TOWS intelligence for use by other agents"""
        if company_name:
            return self.shared_intelligence.get(company_name, {})
        return self.shared_intelligence
    
    def get_strategic_recommendations(self, company_name: str) -> Dict[str, Any]:
        """Get condensed strategic recommendations for agent consumption"""
        analysis = self.shared_intelligence.get(company_name, {})
        if not analysis:
            return {}
        
        tows_matrix = analysis.get('tows_matrix', {})
        insights = analysis.get('strategic_insights', {})
        
        return {
            "strategic_position": insights.get('strategic_position', 'Unknown'),
            "recommended_focus": insights.get('recommended_focus', 'Balanced approach'),
            "top_so_strategies": [s['title'] for s in tows_matrix.get('SO_strategies', [])[:2]],
            "top_st_strategies": [s['title'] for s in tows_matrix.get('ST_strategies', [])[:2]],
            "top_wo_strategies": [s['title'] for s in tows_matrix.get('WO_strategies', [])[:2]],
            "top_wt_strategies": [s['title'] for s in tows_matrix.get('WT_strategies', [])[:2]],
            "immediate_priorities": analysis.get('implementation_roadmap', {}).get('immediate_actions', []),
            "confidence_score": analysis.get('confidence_score', 0),
            "last_updated": analysis.get('analysis_timestamp', '')
        }

# Global SWOT-TOWS analyzer instance for use across agents
swot_tows_analyzer = SWOTTOWSAnalyzer()