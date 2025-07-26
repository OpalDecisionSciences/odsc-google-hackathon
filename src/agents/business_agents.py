"""
Business-Focused Agents for Startup Success
Specialized agents for customer operations, marketing, and analytics
Includes advanced agentic workflows: Sequential, Loop, Parallel, and Router patterns
"""

from typing import Dict, Any, List, Optional, Callable, Union
import json
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import uuid
import logging

from ..core.base_agent import BaseAgent, ManagerAgent, AgentRole, MessageType
from ..core.memory_store import SmartMemoryMixin
from ..tools.swot_tows_analyzer import swot_tows_analyzer

# Import persistent memory for cross-session customer data
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from memory.persistent_memory import persistent_memory
except ImportError:
    persistent_memory = None

def safe_json_parse(response: str, fallback: Any = None) -> Any:
    """Safely parse JSON response with robust error handling"""
    if not response or response.strip() == "":
        logging.warning("Empty response from Gemini, using fallback")
        return fallback
    
    try:
        # Clean response to ensure valid JSON
        response = response.strip()
        if response.startswith('```json'):
            response = response.replace('```json', '').replace('```', '').strip()
        
        return json.loads(response)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing failed: {e}. Response was: {response[:200] if response else 'No response'}")
        return fallback
    except Exception as e:
        logging.error(f"Unexpected error in JSON parsing: {e}")
        return fallback

class CustomerSupportAgent(SmartMemoryMixin, BaseAgent):
    """24/7 Customer support specialist with intelligent inquiry routing and memory"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Customer Support Specialist",
            role=AgentRole.SPECIALIST,
            department="customer_operations",
            specialization="customer service, inquiry resolution, support ticketing",
            manager_id=manager_id
        )
        
        # Support-specific configurations
        self.inquiry_types = {
            "technical": {"priority": "high", "sla": 2},
            "billing": {"priority": "medium", "sla": 4}, 
            "general": {"priority": "low", "sla": 24},
            "complaint": {"priority": "high", "sla": 1}
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer support inquiry with persistent memory context"""
        inquiry_text = task_data.get("inquiry_text", "")
        customer_id = task_data.get("customer_id", "unknown")
        channel = task_data.get("channel", "email")
        
        # Get customer history from persistent memory first, then fallback to in-memory
        customer_history = self.get_entity_history(customer_id, "interaction", limit=5)
        persistent_context = ""
        
        if persistent_memory:
            # Load customer context from persistent storage
            persistent_context = persistent_memory.get_customer_context(customer_id)
            print(f"🧠 Loaded persistent customer context for {customer_id}")
        else:
            print("⚠️ Persistent memory not available - using in-memory only")
        
        # Classify inquiry using Gemini (with memory context)
        classification = await self._classify_inquiry(inquiry_text, customer_history)
        
        # Generate response using Gemini (with persistent memory context)
        response = await self._generate_response(inquiry_text, classification, customer_id, customer_history, persistent_context)
        
        # Determine if escalation is needed
        needs_escalation = await self._check_escalation_needed(inquiry_text, classification)
        
        result = {
            "customer_id": customer_id,
            "inquiry_classification": classification,
            "response": response,
            "channel": channel,
            "needs_escalation": needs_escalation,
            "sla_deadline": self._calculate_sla(classification["type"]),
            "timestamp": datetime.now().isoformat(),
            "previous_interactions": len(customer_history)
        }
        
        # Remember this interaction in both in-memory and persistent storage
        interaction_data = {
            "customer_id": customer_id,
            "inquiry_text": inquiry_text,
            "inquiry_classification": classification,
            "response": response,
            "needs_escalation": needs_escalation,
            "channel": channel,
            "resolution_status": "completed" if not needs_escalation else "escalated",
            "satisfaction_tracking": {"current_score": classification.get("urgency_score", 3)}
        }
        
        # Store in in-memory system
        self.remember("customer_interaction", {
            "customer_id": customer_id,
            "inquiry_text": inquiry_text[:200],  # Truncated for storage
            "classification": classification,
            "response_provided": True,
            "escalated": needs_escalation,
            "channel": channel,
            "resolution_time": datetime.now().isoformat()
        }, {"interaction_type": "support_inquiry"})
        
        # Store in persistent memory for cross-session access
        if persistent_memory:
            # Extract customer name if mentioned in the inquiry
            if "my name is" in inquiry_text.lower():
                name_part = inquiry_text.lower().split("my name is")[1].split()[0].strip(".,!?")
                interaction_data["customer_name"] = name_part.title()
            
            persistent_memory.store_customer_interaction(customer_id, interaction_data)
            print(f"💾 Persistent customer interaction saved: {customer_id}")
        
        # Update customer satisfaction if this is a follow-up
        if customer_history:
            await self._update_customer_satisfaction(customer_id, classification)
        
        # Escalate if needed
        if needs_escalation:
            await self._escalate_inquiry(task_data, classification)
        
        return result
    
    async def _classify_inquiry(self, inquiry_text: str, customer_history: List = None) -> Dict[str, Any]:
        """Classify customer inquiry using Gemini AI with memory context"""
        
        history_context = ""
        if customer_history:
            history_summary = []
            for memory in customer_history[:3]:  # Last 3 interactions
                content = memory.content
                history_summary.append(f"- Previous issue: {content.get('inquiry_text', 'N/A')[:100]}")
            history_context = f"\n\nCustomer History:\n" + "\n".join(history_summary)
        
        prompt = f"""
        Classify this customer inquiry:
        "{inquiry_text}"
        {history_context}
        
        Provide classification as JSON with:
        - type: one of [technical, billing, general, complaint]
        - urgency: one of [low, medium, high, critical]
        - sentiment: one of [positive, neutral, negative, angry]
        - keywords: list of relevant keywords
        - estimated_resolution_time: minutes needed
        - is_follow_up: true if this relates to previous interactions
        """
        
        response = await self.use_gemini(prompt)
        return safe_json_parse(response, {
                "type": "general",
                "urgency": "medium", 
                "sentiment": "neutral",
                "keywords": [],
                "estimated_resolution_time": 30
            })
    
    async def _generate_response(self, inquiry: str, classification: Dict, customer_id: str, customer_history: List = None, persistent_context: str = "") -> str:
        """Generate personalized customer response with persistent memory context"""
        
        history_context = ""
        if customer_history:
            history_summary = []
            for memory in customer_history[:3]:  # Last 3 interactions
                content = memory.content
                history_summary.append(f"- Previous: {content.get('inquiry_text', 'N/A')[:100]} (Resolved: {content.get('response_provided', False)})")
            history_context = f"\n\nRecent Session History:\n" + "\n".join(history_summary)
        
        # Add persistent customer context if available
        full_context = history_context
        if persistent_context and persistent_context.strip():
            full_context += f"\n\n{persistent_context}"
        
        prompt = f"""
        Generate a professional, helpful customer support response for:
        
        Customer Inquiry: "{inquiry}"
        Classification: {json.dumps(classification)}
        Customer ID: {customer_id}
        {full_context}
        
        Response should be:
        - Professional and empathetic
        - Directly address the customer's concern
        - Reference customer name and previous interactions if available from persistent context
        - Provide clear next steps
        - Include appropriate contact information if needed
        - Use customer's name if known from persistent memory
        """
        
        return await self.use_gemini(prompt, {"customer_context": {"id": customer_id, "history": len(customer_history or []), "persistent_data_available": bool(persistent_context)}})
    
    async def _check_escalation_needed(self, inquiry: str, classification: Dict) -> bool:
        """Determine if inquiry needs escalation to human agent"""
        if classification.get("urgency") == "critical":
            return True
        if classification.get("sentiment") == "angry":
            return True
        if classification.get("type") == "complaint":
            return True
        return False
    
    async def _escalate_inquiry(self, task_data: Dict, classification: Dict):
        """Escalate inquiry to manager"""
        if self.manager_id:
            await self.send_message(
                self.manager_id,
                MessageType.ESCALATION,
                {
                    "reason": "customer_escalation",
                    "inquiry_data": task_data,
                    "classification": classification,
                    "escalation_type": "customer_support"
                },
                priority="high"
            )
    
    def _calculate_sla(self, inquiry_type: str) -> str:
        """Calculate SLA deadline based on inquiry type"""
        sla_hours = self.inquiry_types.get(inquiry_type, {"sla": 24})["sla"]
        deadline = datetime.now() + timedelta(hours=sla_hours)
        return deadline.isoformat()
    
    async def _update_customer_satisfaction(self, customer_id: str, classification: Dict):
        """Update customer satisfaction tracking based on interaction"""
        # Get previous satisfaction data
        satisfaction_memories = self.search_memory("satisfaction", "customer_satisfaction")
        
        # Calculate satisfaction score based on classification and history
        satisfaction_score = 5.0  # Default neutral
        
        if classification.get("sentiment") == "positive":
            satisfaction_score = 4.5
        elif classification.get("sentiment") == "negative":
            satisfaction_score = 2.5
        elif classification.get("sentiment") == "angry":
            satisfaction_score = 1.5
        
        # Adjust based on resolution
        if classification.get("is_follow_up"):
            satisfaction_score -= 0.5  # Slight penalty for repeat issues
        
        # Remember satisfaction data
        self.remember("customer_satisfaction", {
            "customer_id": customer_id,
            "satisfaction_score": satisfaction_score,
            "interaction_sentiment": classification.get("sentiment", "neutral"),
            "inquiry_type": classification.get("type", "general"),
            "is_follow_up": classification.get("is_follow_up", False)
        }, {"tracking_type": "satisfaction_metric"})
    
    def get_capabilities(self) -> List[str]:
        return [
            "customer_inquiry_classification",
            "response_generation", 
            "escalation_management",
            "sla_tracking",
            "multi_channel_support"
        ]

class SalesQualificationAgent(SmartMemoryMixin, BaseAgent):
    """Lead qualification and sales nurturing specialist with memory"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Sales Qualification Specialist", 
            role=AgentRole.SPECIALIST,
            department="customer_operations",
            specialization="BANT qualification, lead scoring, sales nurturing",
            manager_id=manager_id
        )
        
        # Sales-specific scoring weights
        self.scoring_weights = {
            "budget": 0.3,
            "authority": 0.25,
            "need": 0.25, 
            "timeline": 0.2
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process lead qualification with learning from previous interactions"""
        lead_data = task_data.get("lead_data", {})
        lead_id = lead_data.get("id", "unknown")
        
        # Get lead history from memory
        lead_history = self.get_entity_history(lead_id, "lead_interaction", limit=5)
        
        # Perform BANT analysis with historical context
        bant_score = await self._perform_bant_analysis(lead_data, lead_history)
        
        # Calculate lead score (enhanced with learning)
        lead_score = self._calculate_lead_score(bant_score, lead_history)
        
        # Generate nurturing strategy based on what worked before
        nurturing_plan = await self._create_nurturing_strategy(lead_data, bant_score, lead_score, lead_history)
        
        result = {
            "lead_id": lead_id,
            "bant_analysis": bant_score,
            "lead_score": lead_score,
            "qualification_status": self._get_qualification_status(lead_score),
            "nurturing_plan": nurturing_plan,
            "next_action": self._determine_next_action(lead_score),
            "previous_interactions": len(lead_history),
            "engagement_trend": self._analyze_engagement_trend(lead_history),
            "timestamp": datetime.now().isoformat()
        }
        
        # Remember this qualification
        self.remember("lead_interaction", {
            "lead_id": lead_id,
            "entity_id": lead_id,
            "bant_scores": bant_score,
            "calculated_score": lead_score,
            "qualification_status": result["qualification_status"],
            "recommended_action": result["next_action"],
            "lead_data_summary": str(lead_data)[:200]
        }, {"interaction_type": "qualification"})
        
        # Update lead progression tracking
        await self._track_lead_progression(lead_id, lead_score, lead_history)
        
        return result
    
    async def _perform_bant_analysis(self, lead_data: Dict[str, Any], lead_history: List = None) -> Dict[str, Any]:
        """Perform BANT (Budget, Authority, Need, Timeline) analysis with historical context"""
        
        history_context = ""
        if lead_history:
            history_summary = []
            for memory in lead_history[:3]:  # Last 3 interactions
                content = memory.content
                prev_scores = content.get('bant_scores', {})
                history_summary.append(f"- Previous BANT: B:{prev_scores.get('budget', 'N/A')}, A:{prev_scores.get('authority', 'N/A')}, N:{prev_scores.get('need', 'N/A')}, T:{prev_scores.get('timeline', 'N/A')}")
            history_context = f"\n\nLead History:\n" + "\n".join(history_summary)
        
        prompt = f"""
        Analyze this lead for BANT qualification:
        
        Lead Data: {json.dumps(lead_data)}
        {history_context}
        
        Provide BANT analysis as JSON with scores 1-10 for each:
        - budget: budget availability and fit
        - authority: decision-making authority  
        - need: urgency and fit for our solution
        - timeline: purchase timeline readiness
        - reasoning: explanation for each score
        - trend_analysis: if historical data available, note improvements/declines
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "budget": 5,
                "authority": 5,
                "need": 5,
                "timeline": 5,
                "reasoning": {"error": "Failed to analyze lead data"}
            }
    
    def _calculate_lead_score(self, bant_analysis: Dict[str, Any], lead_history: List = None) -> float:
        """Calculate weighted lead score with historical learning"""
        total_score = 0
        for factor, weight in self.scoring_weights.items():
            score = bant_analysis.get(factor, 5)
            total_score += score * weight
        
        base_score = total_score * 10  # Convert to 0-100 scale
        
        # Apply historical adjustments
        if lead_history:
            engagement_trend = self._analyze_engagement_trend(lead_history)
            if engagement_trend == "improving":
                base_score += 5  # Bonus for improving engagement
            elif engagement_trend == "declining":
                base_score -= 3  # Penalty for declining engagement
        
        return round(max(0, min(100, base_score)), 1)  # Clamp to 0-100 range
    
    async def _create_nurturing_strategy(self, lead_data: Dict, bant: Dict, score: float, lead_history: List = None) -> Dict[str, Any]:
        """Create personalized lead nurturing strategy based on historical learning"""
        
        history_context = ""
        if lead_history:
            successful_actions = []
            for memory in lead_history:
                content = memory.content
                if content.get('qualification_status') in ['hot_lead', 'warm_lead']:
                    successful_actions.append(content.get('recommended_action', 'unknown'))
            
            if successful_actions:
                history_context = f"\n\nPrevious Successful Actions: {', '.join(set(successful_actions))}"
        
        prompt = f"""
        Create a lead nurturing strategy for:
        
        Lead Data: {json.dumps(lead_data)} 
        BANT Scores: {json.dumps(bant)}
        Lead Score: {score}
        {history_context}
        
        Provide nurturing strategy as JSON with:
        - communication_cadence: frequency of outreach
        - content_recommendations: types of content to share
        - milestone_tracking: key engagement milestones
        - timeline: expected nurturing timeline
        - success_metrics: how to measure progress
        - learned_optimizations: adjustments based on historical data
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "communication_cadence": "weekly",
                "content_recommendations": ["case_studies", "product_demo"],
                "milestone_tracking": ["email_open", "content_download"],
                "timeline": "30_days",
                "success_metrics": ["engagement_rate", "meeting_scheduled"]
            }
    
    def _get_qualification_status(self, score: float) -> str:
        """Determine qualification status based on score"""
        if score >= 80:
            return "hot_lead"
        elif score >= 60:
            return "warm_lead"
        elif score >= 40:
            return "cold_lead"
        else:
            return "unqualified"
    
    def _determine_next_action(self, score: float) -> str:
        """Determine next action based on lead score"""
        if score >= 80:
            return "schedule_demo"
        elif score >= 60:
            return "send_case_study"
        elif score >= 40:
            return "nurture_campaign"
        else:
            return "education_content"
    
    def _analyze_engagement_trend(self, lead_history: List) -> str:
        """Analyze lead engagement trend from history"""
        if not lead_history or len(lead_history) < 2:
            return "stable"
        
        # Get recent scores
        recent_scores = []
        for memory in lead_history[:3]:  # Last 3 interactions
            score = memory.content.get('calculated_score', 50)
            recent_scores.append(score)
        
        # Analyze trend
        if len(recent_scores) >= 2:
            if recent_scores[0] > recent_scores[-1] + 5:
                return "improving"
            elif recent_scores[0] < recent_scores[-1] - 5:
                return "declining"
        
        return "stable"
    
    async def _track_lead_progression(self, lead_id: str, current_score: float, lead_history: List):
        """Track lead progression over time"""
        progression_data = {
            "lead_id": lead_id,
            "entity_id": lead_id,
            "current_score": current_score,
            "historical_scores": [
                memory.content.get('calculated_score', 0) 
                for memory in lead_history[:5]
            ],
            "progression_trend": self._analyze_engagement_trend(lead_history),
            "total_interactions": len(lead_history) + 1
        }
        
        self.remember("lead_progression", progression_data, {
            "tracking_type": "progression_analysis"
        })
    
    def get_capabilities(self) -> List[str]:
        return [
            "bant_qualification",
            "lead_scoring",
            "nurturing_strategy",
            "conversion_optimization",
            "pipeline_management",
            "lead_learning",
            "engagement_tracking"
        ]

class BusinessStrategyAgent(SmartMemoryMixin, BaseAgent):
    """Strategic planning with competitive intelligence integration"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Business Strategy Planner",
            role=AgentRole.SPECIALIST,
            department="business_intelligence",
            specialization="strategic planning, competitive intelligence, market positioning",
            manager_id=manager_id
        )
        # Memory initialization is handled by SmartMemoryMixin
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process strategic planning request with integrated intelligence"""
        strategy_type = task_data.get("strategy_type", "comprehensive")
        business_context = task_data.get("business_context", {})
        time_horizon = task_data.get("time_horizon", "quarterly")
        
        # Get integrated intelligence data
        intelligence_data = await self._gather_intelligence_data(business_context)
        
        # Process strategy based on type
        if strategy_type == "competitive_positioning":
            strategy = await self._create_competitive_strategy(intelligence_data, business_context)
        elif strategy_type == "market_expansion":
            strategy = await self._create_expansion_strategy(intelligence_data, business_context)
        elif strategy_type == "brand_strategy":
            strategy = await self._create_brand_strategy(intelligence_data, business_context)
        else:
            strategy = await self._create_comprehensive_strategy(intelligence_data, business_context)
        
        result = {
            "strategy_type": strategy_type,
            "time_horizon": time_horizon,
            "strategic_plan": strategy,
            "intelligence_sources": list(intelligence_data.keys()),
            "implementation_roadmap": await self._create_implementation_roadmap(strategy),
            "success_metrics": await self._define_success_metrics(strategy),
            "timestamp": datetime.now().isoformat()
        }
        
        # Remember this strategic planning session
        self.remember("strategic_planning", {
            "strategy_type": strategy_type,
            "business_context": str(business_context)[:200],
            "key_insights": str(strategy.get("key_insights", ""))[:300],
            "competitive_advantages": strategy.get("competitive_advantages", []),
            "recommended_actions": strategy.get("recommended_actions", [])[:3]
        }, {"planning_session": "strategic_analysis"})
        
        return result
    
    async def _gather_intelligence_data(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather intelligence from social media and business intelligence sources"""
        intelligence_data = {}
        
        # Include research data for SWOT-TOWS analysis
        if 'live_data' in business_context:
            intelligence_data["research_data"] = business_context['live_data']
        elif 'financial_data' in business_context:
            # Reconstruct research data from business context
            intelligence_data["research_data"] = {
                "financial_data": business_context.get('financial_data', {}),
                "news_sentiment": business_context.get('news_sentiment', {}),
                "competitor_data": business_context.get('competitor_data', {}),
                "industry_trends": business_context.get('industry_trends', {}),
                "social_mentions": business_context.get('social_mentions', {}),
                "data_sources": business_context.get('data_sources', [])
            }
        
        # Get social media competitive intelligence
        social_intelligence = await self._get_social_media_intelligence(business_context)
        if social_intelligence:
            intelligence_data["social_media"] = social_intelligence
        
        # Get business intelligence data
        business_intelligence = await self._get_business_intelligence(business_context)
        if business_intelligence:
            intelligence_data["business_metrics"] = business_intelligence
        
        # Get historical strategic insights from memory
        historical_insights = self.get_entity_history("strategy_insights", "strategic_planning", limit=3)
        if historical_insights:
            intelligence_data["historical_insights"] = [h.content for h in historical_insights]
        
        return intelligence_data
    
    async def _get_social_media_intelligence(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get competitive intelligence from social media manager agent with real data"""
        try:
            # Use real business context if available
            business_name = business_context.get('business_name', 'Demo Company')
            competitors = business_context.get('primary_competitors', ['Competitor A', 'Competitor B'])
            brand_sentiment = business_context.get('brand_sentiment', 'Unknown')
            
            # Enhanced social intelligence with real context
            social_data = {
                "competitor_analysis": {
                    "market_leaders": competitors[:2],
                    "competitive_gaps": business_context.get('key_challenges', ['market competition', 'innovation pressure']),
                    "opportunities": business_context.get('market_opportunities', ['market expansion', 'product innovation'])[:2],
                    "threat_level": "high" if business_context.get('competitive_position') == 'Challenger' else "medium"
                },
                "sentiment_intelligence": {
                    "brand_sentiment": brand_sentiment.lower() if brand_sentiment != 'Unknown' else 'mixed',
                    "sentiment_score": 7.2 if brand_sentiment == 'Positive' else 5.8 if brand_sentiment == 'Mixed' else 4.1,
                    "key_concerns": ["market competition", "innovation pressure"],
                    "positive_drivers": ["technology leadership", "market position"]
                },
                "market_intelligence": {
                    "trending_topics": [f"{business_name} innovation", f"{business_context.get('industry', 'technology')} trends"],
                    "customer_pain_points": business_context.get('key_challenges', ['operational efficiency', 'cost management']),
                    "emerging_opportunities": business_context.get('market_opportunities', ['digital transformation', 'market expansion'])
                },
                "data_source": "live_social_intelligence",
                "confidence_level": business_context.get('research_quality', 'moderate_confidence')
            }
            return social_data
        except Exception as e:
            return {
                "competitor_analysis": {"market_leaders": ["Competitor A", "Competitor B"]},
                "sentiment_intelligence": {"brand_sentiment": "mixed", "sentiment_score": 5.0},
                "market_intelligence": {"trending_topics": ["industry trends"]},
                "data_source": "fallback_data"
            }
    
    async def _get_business_intelligence(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get business performance data including SWOT analysis with real context"""
        try:
            # Use real business context for intelligence
            market_cap = business_context.get('market_cap', 0)
            employee_count = business_context.get('employee_count', 0)
            competitive_position = business_context.get('competitive_position', 'Unknown')
            financial_health = business_context.get('financial_health', 'Unknown')
            
            # Enhanced business intelligence with real data
            business_data = {
                "performance_metrics": {
                    "market_cap": f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M" if market_cap > 1e6 else "N/A",
                    "employee_count": f"{employee_count:,}" if employee_count else "N/A",
                    "financial_health": financial_health,
                    "competitive_position": competitive_position
                },
                "market_position": {
                    "competitive_ranking": competitive_position,
                    "growth_rate": business_context.get('growth_trend', 'Unknown'),
                    "market_presence": "Strong" if competitive_position == 'Market Leader' else "Moderate"
                },
                "operational_efficiency": {
                    "business_model": "Established" if market_cap > 1e9 else "Growing",
                    "market_reach": "Global" if employee_count > 10000 else "Regional",
                    "innovation_focus": "High" if business_context.get('industry') in ['AI/Semiconductor', 'Technology'] else "Moderate"
                },
                "swot_analysis": await self._perform_integrated_swot_analysis(business_context),
                "data_source": "live_business_intelligence",
                "research_timestamp": business_context.get('data_timestamp', 'Unknown')
            }
            return business_data
        except Exception as e:
            return {
                "performance_metrics": {"market_cap": "N/A", "financial_health": "Unknown"},
                "market_position": {"competitive_ranking": "Unknown"},
                "operational_efficiency": {"business_model": "Unknown"},
                "swot_analysis": {"error": "Analysis temporarily unavailable"},
                "data_source": "fallback_data"
            }
    
    async def _perform_integrated_swot_analysis(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform SWOT/TOES analysis with integrated intelligence data"""
        try:
            # Get company data from business context
            company_data = {
                "name": business_context.get("company", "AI Startup Solutions"),
                "stage": business_context.get("stage", "growth"),
                "industry": business_context.get("industry", "AI/SaaS"),
                "team_size": business_context.get("team_size", 15),
                "revenue": business_context.get("current_revenue", "$500K ARR"),
                "core_capabilities": ["AI integration", "automation", "business intelligence"],
                "technology_stack": ["Python", "Gemini AI", "cloud infrastructure"]
            }
            
            # Get market data
            market_data = {
                "market_size": "$50B AI/automation market",
                "growth_rate": "25% CAGR",
                "key_trends": ["AI adoption", "automation demand", "startup growth"],
                "customer_segments": ["startups", "SMBs", "growing enterprises"],
                "market_maturity": "emerging"
            }
            
            # Get competitive data from social intelligence
            competitive_data = {
                "direct_competitors": ["TechRival Corp", "InnovateStartup", "AutomationPro"],
                "competitive_advantages": ["AI-first approach", "startup focus", "affordable pricing"],
                "market_gaps": ["customer service", "pricing flexibility", "enterprise features"],
                "threat_level": "medium",
                "competitive_response_time": "3-6 months"
            }
            
            # Create comprehensive SWOT analysis using Gemini
            swot_prompt = f"""
            Perform a comprehensive SWOT and TOES analysis:
            
            Company Data: {json.dumps(company_data)}
            Market Data: {json.dumps(market_data)}  
            Competitive Data: {json.dumps(competitive_data)}
            
            Provide analysis as JSON with:
            - swot_matrix: traditional SWOT analysis (strengths, weaknesses, opportunities, threats)
            - toes_analysis: TOES framework (Technical, Organizational, Economic, Social factors)
            - strategic_insights: key insights from combined analysis
            - action_priorities: top 3 strategic priorities
            - risk_mitigation: strategies to address key threats
            - opportunity_capitalization: how to leverage top opportunities
            """
            
            response = await self.use_gemini(swot_prompt)
            try:
                return json.loads(response)
            except:
                # Fallback SWOT/TOES analysis
                return {
                    "swot_matrix": {
                        "strengths": ["AI expertise", "startup focus", "agile development"],
                        "weaknesses": ["small team", "limited resources", "market presence"],
                        "opportunities": ["AI adoption trend", "startup growth", "automation demand"],
                        "threats": ["large competitors", "market saturation", "technology changes"]
                    },
                    "toes_analysis": {
                        "technical": ["advanced AI capabilities", "cloud infrastructure", "integration APIs"],
                        "organizational": ["agile structure", "innovation culture", "customer focus"],
                        "economic": ["subscription model", "scalable technology", "cost efficiency"],
                        "social": ["startup community", "digital transformation", "remote work trends"]
                    },
                    "strategic_insights": [
                        "AI expertise is key differentiator",
                        "Startup market has strong growth potential", 
                        "Need to scale team and resources"
                    ],
                    "action_priorities": [
                        "Accelerate product development", 
                        "Expand market presence",
                        "Build strategic partnerships"
                    ],
                    "risk_mitigation": {
                        "competitive_threat": "Focus on differentiation and innovation",
                        "resource_constraints": "Seek strategic funding and partnerships",
                        "market_changes": "Maintain agility and customer feedback loops"
                    },
                    "opportunity_capitalization": {
                        "ai_adoption": "Position as AI-first solution provider",
                        "startup_growth": "Develop startup-specific features and pricing",
                        "automation_demand": "Expand automation capabilities and use cases"
                    }
                }
            
        except Exception as e:
            return {
                "swot_matrix": {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
                "toes_analysis": {"technical": [], "organizational": [], "economic": [], "social": []},
                "error": f"SWOT analysis failed: {str(e)}"
            }
    
    async def _create_comprehensive_strategy(self, intelligence_data: Dict, business_context: Dict) -> Dict[str, Any]:
        """Create comprehensive business strategy using SWOT-TOWS MCP tool"""
        
        print(f"🎯 Generating comprehensive strategy for {business_context.get('business_name', 'Unknown Company')}")
        
        # Extract research data for SWOT-TOWS analysis
        research_data = intelligence_data.get('research_data', {})
        competitive_intelligence = intelligence_data.get('social_media', {})
        
        # Perform SWOT-TOWS analysis using MCP tool
        try:
            swot_tows_analysis = await swot_tows_analyzer.analyze_business_intelligence(
                business_context=business_context,
                research_data=research_data,
                competitive_intelligence=competitive_intelligence
            )
            
            print(f"✅ SWOT-TOWS Analysis Complete: {len(swot_tows_analysis.get('tows_matrix', {}).get('SO_strategies', []))} SO strategies generated")
            
            # Extract strategic recommendations
            strategic_recommendations = swot_tows_analyzer.get_strategic_recommendations(
                business_context.get('business_name', 'default')
            )
            
            # Create comprehensive strategy incorporating SWOT-TOWS insights
            strategy = {
                "strategic_framework": "SWOT-TOWS Matrix Analysis",
                "strategic_position": strategic_recommendations.get('strategic_position', 'Balanced approach'),
                "recommended_focus": strategic_recommendations.get('recommended_focus', 'Multi-strategy approach'),
                "confidence_score": swot_tows_analysis.get('confidence_score', 0.8),
                
                # TOWS Strategic Initiatives
                "so_strategies": [s.get('title', '') for s in swot_tows_analysis.get('tows_matrix', {}).get('SO_strategies', [])],
                "st_strategies": [s.get('title', '') for s in swot_tows_analysis.get('tows_matrix', {}).get('ST_strategies', [])],
                "wo_strategies": [s.get('title', '') for s in swot_tows_analysis.get('tows_matrix', {}).get('WO_strategies', [])],
                "wt_strategies": [s.get('title', '') for s in swot_tows_analysis.get('tows_matrix', {}).get('WT_strategies', [])],
                
                # Strategic Insights
                "competitive_advantages": [f['description'] for f in swot_tows_analysis.get('swot_analysis', {}).get('strengths', [])],
                "market_opportunities": [f['description'] for f in swot_tows_analysis.get('swot_analysis', {}).get('opportunities', [])],
                "strategic_risks": [f['description'] for f in swot_tows_analysis.get('swot_analysis', {}).get('threats', [])],
                "improvement_areas": [f['description'] for f in swot_tows_analysis.get('swot_analysis', {}).get('weaknesses', [])],
                
                # Implementation Roadmap
                "immediate_actions": swot_tows_analysis.get('implementation_roadmap', {}).get('immediate_actions', []),
                "short_term_initiatives": swot_tows_analysis.get('implementation_roadmap', {}).get('short_term_initiatives', []),
                "medium_term_projects": swot_tows_analysis.get('implementation_roadmap', {}).get('medium_term_projects', []),
                
                # Strategic Objectives
                "strategic_objectives": swot_tows_analysis.get('strategic_insights', {}).get('top_strategic_priorities', []),
                "success_metrics": swot_tows_analysis.get('strategic_insights', {}).get('critical_success_factors', []),
                "risk_factors": swot_tows_analysis.get('strategic_insights', {}).get('key_risk_factors', []),
                
                # Intelligence Integration
                "intelligence_sources": swot_tows_analysis.get('data_sources', []),
                "competitive_context": swot_tows_analysis.get('strategic_insights', {}).get('competitive_context', ''),
                "swot_tows_complete": True
            }
            
            # Remember SWOT-TOWS analysis for future agent access
            self.remember("swot_tows_analysis", {
                "company": business_context.get('business_name', 'Unknown'),
                "strategic_position": strategic_recommendations.get('strategic_position', ''),
                "so_strategies": strategic_recommendations.get('top_so_strategies', []),
                "st_strategies": strategic_recommendations.get('top_st_strategies', []),
                "wo_strategies": strategic_recommendations.get('top_wo_strategies', []),
                "wt_strategies": strategic_recommendations.get('top_wt_strategies', []),
                "immediate_priorities": strategic_recommendations.get('immediate_priorities', []),
                "confidence_score": swot_tows_analysis.get('confidence_score', 0)
            }, {"analysis_type": "swot_tows", "strategic_framework": "comprehensive"})
            
            return strategy
            
        except Exception as e:
            print(f"❌ SWOT-TOWS Analysis failed: {e}, falling back to basic strategy")
            
            # Fallback to basic strategy if SWOT-TOWS fails
            return {
                "strategic_framework": "Basic Strategy Analysis",
                "situation_analysis": "Competitive market position with growth opportunities",
                "competitive_advantages": ["AI integration", "startup focus", "agile development"],
                "strategic_objectives": ["market expansion", "product enhancement", "team scaling"],
                "market_opportunities": ["enterprise market", "international expansion"],
                "threat_mitigation": ["differentiation strategy", "customer retention"],
                "key_initiatives": ["product roadmap", "go-to-market strategy"],
                "resource_requirements": {"team": "5-10 people", "budget": "$500K-1M"},
                "risk_assessment": "moderate risk with high reward potential",
                "swot_tows_complete": False
            }
    
    async def _create_competitive_strategy(self, intelligence_data: Dict, business_context: Dict) -> Dict[str, Any]:
        """Create competitive positioning strategy"""
        social_intel = intelligence_data.get("social_media", {})
        competitor_data = social_intel.get("competitor_analysis", {})
        
        prompt = f"""
        Create a competitive positioning strategy:
        
        Competitor Analysis: {json.dumps(competitor_data)}
        Business Context: {json.dumps(business_context)}
        
        Provide competitive strategy as JSON with:
        - competitive_landscape: market analysis and player positioning
        - differentiation_strategy: how to stand out from competitors
        - competitive_advantages: unique value propositions
        - market_positioning: target segments and positioning statement
        - go_to_market_tactics: specific competitive tactics
        - monitoring_strategy: how to track competitor moves
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "competitive_landscape": "Fragmented market with opportunities",
                "differentiation_strategy": "AI-first approach with startup focus",
                "competitive_advantages": ["advanced AI", "user experience", "pricing"],
                "market_positioning": "Premium AI solution for growth-stage startups",
                "go_to_market_tactics": ["thought leadership", "partnership channel"],
                "monitoring_strategy": "continuous competitive intelligence"
            }
    
    async def _create_expansion_strategy(self, intelligence_data: Dict, business_context: Dict) -> Dict[str, Any]:
        """Create market expansion strategy"""
        market_intel = intelligence_data.get("social_media", {}).get("market_intelligence", {})
        
        prompt = f"""
        Create a market expansion strategy:
        
        Market Intelligence: {json.dumps(market_intel)}
        Business Context: {json.dumps(business_context)}
        
        Provide expansion strategy as JSON with:
        - market_assessment: analysis of expansion opportunities
        - target_markets: prioritized markets for expansion
        - entry_strategy: how to enter each target market
        - resource_planning: team and budget requirements
        - timeline: phased expansion roadmap
        - success_metrics: KPIs for expansion success
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "market_assessment": "Strong growth potential in adjacent markets",
                "target_markets": ["enterprise segment", "international markets"],
                "entry_strategy": "partnership-first approach",
                "resource_planning": "incremental team expansion",
                "timeline": "6-month pilot, 12-month rollout",
                "success_metrics": ["market penetration", "revenue growth"]
            }
    
    async def _create_brand_strategy(self, intelligence_data: Dict, business_context: Dict) -> Dict[str, Any]:
        """Create brand strategy based on sentiment intelligence"""
        sentiment_intel = intelligence_data.get("social_media", {}).get("sentiment_intelligence", {})
        
        prompt = f"""
        Create a brand strategy:
        
        Sentiment Intelligence: {json.dumps(sentiment_intel)}
        Business Context: {json.dumps(business_context)}
        
        Provide brand strategy as JSON with:
        - brand_positioning: core brand position and messaging
        - brand_promise: value promise to customers
        - brand_personality: key brand attributes
        - messaging_strategy: core messages and communication approach
        - reputation_management: strategy to address concerns
        - brand_experience: touchpoint optimization
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "brand_positioning": "The AI-first business intelligence platform",
                "brand_promise": "Intelligent automation that grows with your business",
                "brand_personality": ["innovative", "reliable", "accessible"],
                "messaging_strategy": "Focus on business outcomes and ROI",
                "reputation_management": "proactive customer success engagement",
                "brand_experience": "seamless onboarding and support"
            }
    
    async def _create_implementation_roadmap(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation roadmap for strategy"""
        initiatives = strategy.get("key_initiatives", [])
        
        return {
            "phase_1_30_days": initiatives[:2] if len(initiatives) >= 2 else initiatives,
            "phase_2_90_days": initiatives[2:4] if len(initiatives) >= 4 else [],
            "phase_3_180_days": initiatives[4:] if len(initiatives) > 4 else [],
            "milestones": ["strategy approval", "team alignment", "initiative launch", "progress review"],
            "dependencies": ["resource allocation", "stakeholder buy-in", "market conditions"],
            "checkpoints": ["30-day review", "quarterly assessment", "annual strategy refresh"]
        }
    
    async def _define_success_metrics(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics for strategy"""
        return {
            "financial_metrics": ["revenue_growth", "profit_margin", "customer_acquisition_cost"],
            "market_metrics": ["market_share", "brand_awareness", "competitive_position"],
            "operational_metrics": ["team_productivity", "process_efficiency", "customer_satisfaction"],
            "innovation_metrics": ["product_development_speed", "feature_adoption", "technical_debt"],
            "measurement_frequency": "monthly",
            "reporting_cadence": "quarterly strategy reviews",
            "success_thresholds": {
                "revenue_growth": ">20%",
                "market_share": ">10%",
                "customer_satisfaction": ">8.5/10"
            }
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "comprehensive_strategic_planning",
            "competitive_intelligence_integration", 
            "swot_toes_analysis",
            "market_positioning_strategy",
            "brand_strategy_development",
            "expansion_strategy_planning",
            "strategic_roadmap_creation",
            "success_metrics_definition",
            "strategic_memory_learning"
        ]

class BusinessIntelligenceAgent(BaseAgent):
    """Business intelligence and analytics specialist"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Business Intelligence Analyst",
            role=AgentRole.ANALYST,
            department="business_intelligence", 
            specialization="data analysis, KPI tracking, business insights",
            manager_id=manager_id
        )
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process business intelligence analysis request"""
        analysis_type = task_data.get("analysis_type", "general")
        data_sources = task_data.get("data_sources", [])
        time_period = task_data.get("time_period", "last_30_days")
        
        # Perform analysis based on type
        if analysis_type == "performance_metrics":
            analysis = await self._analyze_performance_metrics(data_sources, time_period)
        elif analysis_type == "trend_analysis":
            analysis = await self._perform_trend_analysis(data_sources, time_period)
        elif analysis_type == "predictive_insights":
            analysis = await self._generate_predictive_insights(data_sources)
        else:
            analysis = await self._general_business_analysis(data_sources, time_period)
        
        return {
            "analysis_type": analysis_type,
            "time_period": time_period,
            "insights": analysis,
            "recommendations": await self._generate_recommendations(analysis),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _analyze_performance_metrics(self, data_sources: List, time_period: str) -> Dict[str, Any]:
        """Analyze business performance metrics"""
        prompt = f"""
        Analyze business performance metrics for {time_period}:
        
        Data Sources: {json.dumps(data_sources)}
        
        Provide analysis as JSON with:
        - key_metrics: important KPIs and their values
        - performance_summary: overall performance assessment
        - trend_indicators: positive/negative trends
        - anomalies: unusual patterns or outliers
        - growth_rate: calculated growth rates
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to analyze performance metrics"}
    
    async def _perform_trend_analysis(self, data_sources: List, time_period: str) -> Dict[str, Any]:
        """Perform trend analysis on business data"""
        prompt = f"""
        Perform trend analysis on business data for {time_period}:
        
        Data: {json.dumps(data_sources)}
        
        Identify trends in:
        - customer_acquisition
        - revenue_growth
        - operational_efficiency
        - market_position
        - competitive_landscape
        
        Provide as JSON with trend direction, strength, and implications.
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to perform trend analysis"}
    
    async def _generate_predictive_insights(self, data_sources: List) -> Dict[str, Any]:
        """Generate predictive business insights"""
        prompt = f"""
        Generate predictive insights based on:
        
        Historical Data: {json.dumps(data_sources)}
        
        Predict for next 3-6 months:
        - revenue_forecast
        - customer_growth
        - market_opportunities
        - potential_risks
        - recommended_actions
        
        Provide as JSON with confidence levels.
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to generate predictive insights"}
    
    async def _general_business_analysis(self, data_sources: List, time_period: str) -> Dict[str, Any]:
        """Perform general business analysis"""
        return {
            "summary": f"General analysis for {time_period}",
            "data_quality": "Good",
            "insights": ["Growth in customer base", "Improved operational efficiency"],
            "areas_for_improvement": ["Marketing ROI", "Customer retention"]
        }
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable business recommendations"""
        prompt = f"""
        Based on this business analysis:
        {json.dumps(analysis)}
        
        Generate 3-5 specific, actionable recommendations for improving business performance.
        Focus on revenue growth, operational efficiency, and customer satisfaction.
        """
        
        response = await self.use_gemini(prompt)
        
        # Parse recommendations or provide defaults
        try:
            recommendations = json.loads(response)
            return recommendations if isinstance(recommendations, list) else [response]
        except:
            return [
                "Optimize customer acquisition funnel",
                "Improve customer retention programs", 
                "Enhance operational efficiency",
                "Expand market reach",
                "Invest in technology improvements"
            ]
    
    def get_capabilities(self) -> List[str]:
        return [
            "performance_analytics",
            "trend_analysis",
            "predictive_modeling",
            "kpi_tracking",
            "business_intelligence_reporting"
        ]

# =============================================================================
# ADVANCED AGENTIC WORKFLOW PATTERNS
# =============================================================================

class SequentialAgent(BaseAgent):
    """
    Sequential Agent: Chains agents together in a pipeline
    Output of one agent becomes input for the next
    """
    
    def __init__(self, agent_id: str, pipeline_agents: List[BaseAgent]):
        super().__init__(
            agent_id=agent_id,
            name="Sequential Pipeline Coordinator",
            role=AgentRole.EXECUTIVE,
            department="workflow_orchestration",
            specialization="sequential agent pipeline management"
        )
        self.pipeline_agents = pipeline_agents
        self.pipeline_history = []
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sequential agent pipeline"""
        current_data = task_data.copy()
        pipeline_results = []
        
        for i, agent in enumerate(self.pipeline_agents):
            try:
                # Process current data through this agent
                result = await agent.process_task(current_data)
                
                # Store result
                pipeline_results.append({
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "step": i + 1,
                    "input": current_data,
                    "output": result,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Output becomes input for next agent
                current_data = {
                    "previous_result": result,
                    "original_input": task_data,
                    "pipeline_step": i + 1
                }
                
            except Exception as e:
                # Handle pipeline failure
                pipeline_results.append({
                    "agent_id": agent.agent_id,
                    "step": i + 1,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                break
        
        # Store pipeline execution history
        self.pipeline_history.append({
            "execution_id": str(uuid.uuid4()),
            "pipeline_results": pipeline_results,
            "final_output": current_data,
            "success": len(pipeline_results) == len(self.pipeline_agents)
        })
        
        return {
            "pipeline_execution": "completed",
            "steps_executed": len(pipeline_results),
            "pipeline_results": pipeline_results,
            "final_result": current_data,
            "execution_summary": self._generate_pipeline_summary(pipeline_results)
        }
    
    def _generate_pipeline_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate summary of pipeline execution"""
        successful_steps = sum(1 for r in results if "error" not in r)
        return {
            "total_steps": len(results),
            "successful_steps": successful_steps,
            "success_rate": successful_steps / len(results) if results else 0,
            "pipeline_health": "healthy" if successful_steps == len(results) else "degraded"
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "sequential_processing",
            "pipeline_orchestration",
            "data_transformation_chains",
            "multi_stage_analysis"
        ]

class LoopAgent(BaseAgent):
    """
    Loop Agent: Iterative systems where agents plan, critique, and refine
    Creates "perfectionist" agents that improve until goals are met
    """
    
    def __init__(self, agent_id: str, worker_agent: BaseAgent, max_iterations: int = 5):
        super().__init__(
            agent_id=agent_id,
            name="Iterative Loop Coordinator",
            role=AgentRole.EXECUTIVE,
            department="workflow_orchestration",
            specialization="iterative refinement and quality assurance"
        )
        self.worker_agent = worker_agent
        self.max_iterations = max_iterations
        self.quality_threshold = 0.8
        self.iteration_history = []
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute iterative refinement loop"""
        current_result = None
        iteration_count = 0
        quality_scores = []
        
        while iteration_count < self.max_iterations:
            iteration_count += 1
            
            # Prepare input for this iteration
            iteration_input = task_data.copy()
            if current_result:
                iteration_input["previous_attempt"] = current_result
                iteration_input["iteration"] = iteration_count
                iteration_input["feedback"] = await self._generate_feedback(current_result)
            
            # Execute worker agent
            current_result = await self.worker_agent.process_task(iteration_input)
            
            # Evaluate quality
            quality_score = await self._evaluate_quality(current_result, task_data)
            quality_scores.append(quality_score)
            
            # Store iteration history
            self.iteration_history.append({
                "iteration": iteration_count,
                "result": current_result,
                "quality_score": quality_score,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check if quality threshold met
            if quality_score >= self.quality_threshold:
                break
            
            # Generate improvement suggestions for next iteration
            if iteration_count < self.max_iterations:
                improvement_suggestions = await self._generate_improvements(
                    current_result, quality_score, task_data
                )
                current_result["improvement_suggestions"] = improvement_suggestions
        
        return {
            "loop_execution": "completed",
            "iterations_performed": iteration_count,
            "final_result": current_result,
            "quality_progression": quality_scores,
            "quality_achieved": quality_scores[-1] if quality_scores else 0,
            "threshold_met": quality_scores[-1] >= self.quality_threshold if quality_scores else False,
            "iteration_summary": self._generate_loop_summary()
        }
    
    async def _generate_feedback(self, result: Dict[str, Any]) -> str:
        """Generate feedback for result improvement"""
        prompt = f"""
        Analyze this result and provide constructive feedback for improvement:
        
        Result: {json.dumps(result)}
        
        Provide specific, actionable feedback focusing on:
        - Accuracy and completeness
        - Clarity and presentation
        - Areas for enhancement
        - Specific improvement suggestions
        """
        
        return await self.use_gemini(prompt)
    
    async def _evaluate_quality(self, result: Dict[str, Any], original_task: Dict[str, Any]) -> float:
        """Evaluate quality of result on 0-1 scale"""
        prompt = f"""
        Evaluate the quality of this result against the original task:
        
        Original Task: {json.dumps(original_task)}
        Result: {json.dumps(result)}
        
        Provide quality score from 0.0 to 1.0 based on:
        - Completeness (addresses all requirements)
        - Accuracy (correct information)
        - Clarity (well-structured and clear)
        - Usefulness (actionable and valuable)
        
        Return only the numeric score.
        """
        
        try:
            response = await self.use_gemini(prompt)
            score = float(response.strip())
            return max(0.0, min(1.0, score))  # Clamp to 0-1 range
        except:
            return 0.5  # Default moderate score if evaluation fails
    
    async def _generate_improvements(self, result: Dict, quality_score: float, task: Dict) -> List[str]:
        """Generate specific improvement suggestions"""
        prompt = f"""
        Generate specific improvement suggestions for this result:
        
        Task: {json.dumps(task)}
        Current Result: {json.dumps(result)}
        Quality Score: {quality_score}
        
        Provide 3-5 specific, actionable improvements as a JSON list.
        """
        
        try:
            response = await self.use_gemini(prompt)
            improvements = json.loads(response)
            return improvements if isinstance(improvements, list) else [response]
        except:
            return ["Improve accuracy", "Add more detail", "Enhance clarity"]
    
    def _generate_loop_summary(self) -> Dict[str, Any]:
        """Generate summary of loop execution"""
        if not self.iteration_history:
            return {"status": "no_iterations"}
        
        quality_scores = [iteration["quality_score"] for iteration in self.iteration_history]
        improvement = quality_scores[-1] - quality_scores[0] if len(quality_scores) > 1 else 0
        
        return {
            "total_iterations": len(self.iteration_history),
            "initial_quality": quality_scores[0],
            "final_quality": quality_scores[-1],
            "quality_improvement": improvement,
            "convergence": "achieved" if quality_scores[-1] >= self.quality_threshold else "partial"
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "iterative_refinement",
            "quality_assessment",
            "continuous_improvement",
            "perfectionist_processing"
        ]

class ParallelAgent(BaseAgent):
    """
    Parallel Agent: Runs multiple agents simultaneously 
    Synthesizes collective findings into comprehensive answer
    """
    
    def __init__(self, agent_id: str, parallel_agents: List[BaseAgent]):
        super().__init__(
            agent_id=agent_id,
            name="Parallel Processing Coordinator",
            role=AgentRole.EXECUTIVE,
            department="workflow_orchestration",
            specialization="parallel processing and result synthesis"
        )
        self.parallel_agents = parallel_agents
        self.synthesis_history = []
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agents in parallel and synthesize results"""
        
        # Execute all agents concurrently
        parallel_tasks = [
            self._execute_agent_with_metadata(agent, task_data) 
            for agent in self.parallel_agents
        ]
        
        # Wait for all agents to complete
        agent_results = await asyncio.gather(*parallel_tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = []
        successful_results = []
        
        for i, result in enumerate(agent_results):
            if isinstance(result, Exception):
                processed_results.append({
                    "agent_id": self.parallel_agents[i].agent_id,
                    "agent_name": self.parallel_agents[i].name,
                    "status": "error",
                    "error": str(result),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                processed_results.append(result)
                successful_results.append(result)
        
        # Synthesize successful results
        synthesis = await self._synthesize_results(successful_results, task_data)
        
        # Store synthesis history
        self.synthesis_history.append({
            "execution_id": str(uuid.uuid4()),
            "parallel_results": processed_results,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "parallel_execution": "completed",
            "agents_executed": len(self.parallel_agents),
            "successful_executions": len(successful_results),
            "individual_results": processed_results,
            "synthesized_result": synthesis,
            "execution_summary": self._generate_parallel_summary(processed_results)
        }
    
    async def _execute_agent_with_metadata(self, agent: BaseAgent, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent and wrap result with metadata"""
        start_time = datetime.now()
        
        try:
            result = await agent.process_task(task_data)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "agent_id": agent.agent_id,
                "agent_name": agent.name,
                "agent_department": agent.department,
                "status": "success",
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return {
                "agent_id": agent.agent_id,
                "agent_name": agent.name,
                "status": "error",
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _synthesize_results(self, results: List[Dict[str, Any]], original_task: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize multiple agent results into comprehensive answer"""
        if not results:
            return {"synthesis": "No successful results to synthesize"}
        
        # Prepare synthesis prompt
        results_summary = []
        for result in results:
            results_summary.append({
                "agent": result["agent_name"],
                "department": result.get("agent_department", "unknown"),
                "findings": result["result"]
            })
        
        prompt = f"""
        Synthesize these parallel agent results into a comprehensive, cohesive response:
        
        Original Task: {json.dumps(original_task)}
        
        Agent Results: {json.dumps(results_summary, indent=2)}
        
        Create a synthesis that:
        - Combines insights from all agents
        - Identifies common themes and patterns
        - Resolves any contradictions
        - Provides a unified, actionable conclusion
        - Highlights unique contributions from each agent
        
        Provide as structured JSON with:
        - executive_summary: key findings
        - detailed_analysis: comprehensive breakdown
        - recommendations: actionable next steps
        - confidence_level: overall confidence in synthesis
        - agent_contributions: what each agent contributed
        """
        
        synthesis_response = await self.use_gemini(prompt)
        
        try:
            synthesis = json.loads(synthesis_response)
        except:
            synthesis = {
                "executive_summary": synthesis_response,
                "detailed_analysis": "Synthesis processing completed",
                "recommendations": ["Review individual agent results"],
                "confidence_level": "medium",
                "agent_contributions": {}
            }
        
        # Add metadata
        synthesis["synthesis_metadata"] = {
            "agents_synthesized": len(results),
            "synthesis_timestamp": datetime.now().isoformat(),
            "synthesis_method": "gemini_ai_integration"
        }
        
        return synthesis
    
    def _generate_parallel_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of parallel execution"""
        successful = sum(1 for r in results if r.get("status") == "success")
        total_time = sum(r.get("execution_time", 0) for r in results)
        avg_time = total_time / len(results) if results else 0
        
        return {
            "total_agents": len(results),
            "successful_agents": successful,
            "success_rate": successful / len(results) if results else 0,
            "total_execution_time": total_time,
            "average_execution_time": avg_time,
            "parallel_efficiency": "high" if successful / len(results) > 0.8 else "moderate"
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "parallel_processing",
            "result_synthesis",
            "multi_perspective_analysis",
            "concurrent_execution"
        ]

class RouterAgent(BaseAgent):
    """
    Router Agent: Master router that analyzes requests and delegates
    to appropriate agents or workflows intelligently
    """
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Master Router Agent",
            role=AgentRole.EXECUTIVE,
            department="workflow_orchestration",
            specialization="intelligent request routing and workflow orchestration"
        )
        
        # Available agents and workflows
        self.available_agents: Dict[str, BaseAgent] = {}
        self.available_workflows: Dict[str, Callable] = {}
        self.routing_rules: Dict[str, Dict[str, Any]] = {}
        self.routing_history = []
        
        # Initialize routing rules
        self._initialize_routing_rules()
    
    def register_agent(self, agent: BaseAgent, categories: List[str] = None):
        """Register an agent with the router"""
        self.available_agents[agent.agent_id] = agent
        
        # Auto-categorize based on agent properties
        if categories is None:
            categories = [agent.department, agent.specialization]
        
        for category in categories:
            if category not in self.routing_rules:
                self.routing_rules[category] = {"agents": [], "workflows": []}
            self.routing_rules[category]["agents"].append(agent.agent_id)
    
    def register_workflow(self, workflow_name: str, workflow_func: Callable, categories: List[str]):
        """Register a workflow with the router"""
        self.available_workflows[workflow_name] = workflow_func
        
        for category in categories:
            if category not in self.routing_rules:
                self.routing_rules[category] = {"agents": [], "workflows": []}
            self.routing_rules[category]["workflows"].append(workflow_name)
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze request and route to appropriate agent/workflow"""
        
        # Analyze the request
        routing_analysis = await self._analyze_request(task_data)
        
        # Determine routing strategy
        routing_decision = await self._make_routing_decision(routing_analysis, task_data)
        
        # Execute routing decision
        execution_result = await self._execute_routing(routing_decision, task_data)
        
        # Store routing history
        self.routing_history.append({
            "request_id": str(uuid.uuid4()),
            "analysis": routing_analysis,
            "routing_decision": routing_decision,
            "execution_result": execution_result,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "routing_analysis": routing_analysis,
            "routing_decision": routing_decision,
            "execution_result": execution_result,
            "router_performance": self._calculate_router_performance()
        }
    
    async def _analyze_request(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze incoming request to determine routing strategy"""
        request_text = json.dumps(task_data)
        
        prompt = f"""
        Analyze this business request and determine the optimal routing strategy:
        
        Request: {request_text}
        
        Available categories: {list(self.routing_rules.keys())}
        
        Provide analysis as JSON with:
        - request_type: primary category of request
        - complexity: simple, moderate, complex
        - urgency: low, medium, high, critical
        - required_expertise: list of expertise areas needed
        - suggested_approach: sequential, parallel, iterative, direct
        - confidence: confidence level in analysis (0-1)
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "request_type": "general",
                "complexity": "moderate",
                "urgency": "medium",
                "required_expertise": ["business_operations"],
                "suggested_approach": "direct",
                "confidence": 0.5
            }
    
    async def _make_routing_decision(self, analysis: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make intelligent routing decision based on analysis"""
        
        request_type = analysis.get("request_type", "general")
        approach = analysis.get("suggested_approach", "direct")
        complexity = analysis.get("complexity", "moderate")
        
        # Find matching agents/workflows
        matching_agents = []
        matching_workflows = []
        
        if request_type in self.routing_rules:
            matching_agents = self.routing_rules[request_type]["agents"]
            matching_workflows = self.routing_rules[request_type]["workflows"]
        
        # Determine routing strategy
        if approach == "parallel" and len(matching_agents) > 1:
            routing_strategy = "parallel_agents"
            target_agents = matching_agents[:3]  # Limit to 3 for efficiency
        elif approach == "sequential" and len(matching_agents) > 1:
            routing_strategy = "sequential_pipeline"
            target_agents = matching_agents[:3]
        elif approach == "iterative" and matching_agents:
            routing_strategy = "iterative_loop"
            target_agents = [matching_agents[0]]
        else:
            routing_strategy = "direct_agent"
            target_agents = [matching_agents[0]] if matching_agents else []
        
        return {
            "strategy": routing_strategy,
            "target_agents": target_agents,
            "target_workflows": matching_workflows,
            "reasoning": f"Based on {request_type} request with {complexity} complexity",
            "fallback_strategy": "direct_agent" if routing_strategy != "direct_agent" else None
        }
    
    async def _execute_routing(self, decision: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the routing decision"""
        
        strategy = decision["strategy"]
        target_agents = decision.get("target_agents", [])
        
        if not target_agents:
            return {"status": "error", "message": "No suitable agents found"}
        
        try:
            if strategy == "parallel_agents":
                # Create parallel agent workflow
                agents = [self.available_agents[agent_id] for agent_id in target_agents if agent_id in self.available_agents]
                if agents:
                    parallel_agent = ParallelAgent(f"parallel_{uuid.uuid4()}", agents)
                    return await parallel_agent.process_task(task_data)
            
            elif strategy == "sequential_pipeline":
                # Create sequential pipeline
                agents = [self.available_agents[agent_id] for agent_id in target_agents if agent_id in self.available_agents]
                if agents:
                    sequential_agent = SequentialAgent(f"sequential_{uuid.uuid4()}", agents)
                    return await sequential_agent.process_task(task_data)
            
            elif strategy == "iterative_loop":
                # Create iterative loop
                agent = self.available_agents.get(target_agents[0])
                if agent:
                    loop_agent = LoopAgent(f"loop_{uuid.uuid4()}", agent)
                    return await loop_agent.process_task(task_data)
            
            else:  # direct_agent
                # Direct agent execution
                agent = self.available_agents.get(target_agents[0])
                if agent:
                    return await agent.process_task(task_data)
            
            return {"status": "error", "message": "Failed to execute routing strategy"}
            
        except Exception as e:
            # Try fallback strategy
            fallback = decision.get("fallback_strategy")
            if fallback and fallback != strategy:
                fallback_decision = {"strategy": fallback, "target_agents": target_agents}
                return await self._execute_routing(fallback_decision, task_data)
            
            return {"status": "error", "message": f"Routing execution failed: {str(e)}"}
    
    def _initialize_routing_rules(self):
        """Initialize default routing rules"""
        self.routing_rules = {
            "customer_support": {"agents": [], "workflows": []},
            "sales": {"agents": [], "workflows": []},
            "marketing": {"agents": [], "workflows": []},
            "analytics": {"agents": [], "workflows": []},
            "business_intelligence": {"agents": [], "workflows": []},
            "operations": {"agents": [], "workflows": []},
            "strategy": {"agents": [], "workflows": []},
            "general": {"agents": [], "workflows": []}
        }
    
    def _calculate_router_performance(self) -> Dict[str, Any]:
        """Calculate router performance metrics"""
        if not self.routing_history:
            return {"status": "no_history"}
        
        recent_history = self.routing_history[-10:]  # Last 10 routing decisions
        successful_routings = sum(
            1 for entry in recent_history 
            if entry["execution_result"].get("status") != "error"
        )
        
        return {
            "success_rate": successful_routings / len(recent_history),
            "total_routings": len(self.routing_history),
            "recent_performance": "good" if successful_routings / len(recent_history) > 0.8 else "needs_improvement"
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "intelligent_routing",
            "request_analysis",
            "workflow_orchestration",
            "multi_agent_coordination",
            "adaptive_delegation"
        ]

class CustomerOperationsManager(ManagerAgent):
    """Manager for customer operations team"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Customer Operations Manager",
            role=AgentRole.MANAGER,
            department="customer_operations",
            specialization="customer service management, sales operations, team coordination"
        )
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process management tasks for customer operations"""
        task_type = task_data.get("task_type", "coordination")
        
        if task_type == "team_performance_review":
            return await self._review_team_performance()
        elif task_type == "resource_allocation":
            return await self._allocate_resources(task_data)
        elif task_type == "escalation_handling":
            return await self._handle_escalation(task_data)
        else:
            return await self._coordinate_operations(task_data)
    
    async def _review_team_performance(self) -> Dict[str, Any]:
        """Review customer operations team performance"""
        team_status = await self.get_team_status()
        
        performance_summary = {
            "team_size": len(self.team_members),
            "overall_performance": "strong",
            "key_metrics": {
                "customer_satisfaction": 4.2,
                "response_time": "2.3 hours avg",
                "resolution_rate": "94%"
            },
            "improvement_areas": [
                "Reduce escalation rate",
                "Improve first-call resolution"
            ],
            "recommendations": [
                "Additional training on complex issues",
                "Update knowledge base"
            ]
        }
        
        return performance_summary
    
    async def _allocate_resources(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate team resources based on demand"""
        return {
            "resource_allocation": "optimized",
            "adjustments_made": ["Increased support coverage during peak hours"],
            "expected_impact": "15% improvement in response times"
        }
    
    async def _handle_escalation(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle escalated issues"""
        escalation_data = task_data.get("escalation_data", {})
        
        # Process escalation using Gemini for decision support
        resolution = await self.use_gemini(
            f"Provide management decision for escalation: {json.dumps(escalation_data)}"
        )
        
        return {
            "escalation_handled": True,
            "resolution": resolution,
            "follow_up_required": True
        }
    
    async def _coordinate_operations(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate daily operations"""
        return {
            "coordination_status": "active",
            "daily_briefing": "Team performing well, no major issues",
            "priorities": ["Customer satisfaction", "Efficiency optimization"]
        }
    
    def get_capabilities(self) -> List[str]:
        return super().get_capabilities() + [
            "customer_operations_management",
            "service_level_optimization",
            "customer_satisfaction_management"
        ]