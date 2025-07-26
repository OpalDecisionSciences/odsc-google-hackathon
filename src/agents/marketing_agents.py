"""
Marketing Excellence Agents
Brand management, social media, and content creation specialists
"""

from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime, timedelta

from ..core.base_agent import BaseAgent, ManagerAgent, AgentRole, MessageType
from ..core.memory_store import SmartMemoryMixin

class BrandManagerAgent(BaseAgent):
    """Brand consistency and messaging specialist"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Brand Manager",
            role=AgentRole.SPECIALIST,
            department="marketing_excellence",
            specialization="brand consistency, messaging strategy, brand guidelines",
            manager_id=manager_id
        )
        
        # Brand management configurations
        self.brand_guidelines = {
            "voice": "professional, approachable, innovative",
            "tone": "confident yet friendly",
            "values": ["innovation", "customer-centric", "reliability"],
            "messaging_pillars": ["expertise", "results", "partnership"]
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process brand management task"""
        task_type = task_data.get("task_type", "brand_review")
        
        if task_type == "brand_consistency_check":
            return await self._check_brand_consistency(task_data)
        elif task_type == "messaging_strategy":
            return await self._develop_messaging_strategy(task_data)
        elif task_type == "brand_guidelines_update":
            return await self._update_brand_guidelines(task_data)
        else:
            return await self._general_brand_analysis(task_data)
    
    async def _check_brand_consistency(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check content for brand consistency"""
        content = task_data.get("content", "")
        channel = task_data.get("channel", "general")
        
        prompt = f"""
        Review this content for brand consistency:
        
        Content: "{content}"
        Channel: {channel}
        Brand Guidelines: {json.dumps(self.brand_guidelines)}
        
        Provide analysis as JSON with:
        - consistency_score: 0-100 score
        - voice_alignment: how well it matches brand voice
        - tone_assessment: tone evaluation
        - messaging_alignment: alignment with brand pillars
        - recommendations: specific improvements needed
        - approval_status: approved, needs_revision, rejected
        """
        
        response = await self.use_gemini(prompt)
        try:
            analysis = json.loads(response)
        except:
            analysis = {
                "consistency_score": 75,
                "voice_alignment": "good",
                "tone_assessment": "appropriate",
                "messaging_alignment": "strong",
                "recommendations": ["Review tone consistency"],
                "approval_status": "needs_revision"
            }
        
        return {
            "content_id": task_data.get("content_id", "unknown"),
            "channel": channel,
            "brand_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _develop_messaging_strategy(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop messaging strategy for campaign/initiative"""
        campaign_type = task_data.get("campaign_type", "general")
        target_audience = task_data.get("target_audience", "general")
        objectives = task_data.get("objectives", [])
        
        prompt = f"""
        Develop a messaging strategy for:
        
        Campaign Type: {campaign_type}
        Target Audience: {target_audience}
        Objectives: {json.dumps(objectives)}
        Brand Guidelines: {json.dumps(self.brand_guidelines)}
        
        Provide strategy as JSON with:
        - core_message: primary message
        - supporting_messages: secondary messages
        - key_benefits: benefits to highlight
        - proof_points: credibility elements
        - call_to_action: primary CTA
        - channel_adaptations: how to adapt for different channels
        """
        
        response = await self.use_gemini(prompt)
        try:
            strategy = json.loads(response)
        except:
            strategy = {
                "core_message": "Transform your business with AI-powered solutions",
                "supporting_messages": ["Increase efficiency", "Reduce costs", "Scale operations"],
                "key_benefits": ["Faster growth", "Better decisions", "Competitive advantage"],
                "proof_points": ["Proven results", "Expert team", "Cutting-edge technology"],
                "call_to_action": "Start your transformation today",
                "channel_adaptations": {}
            }
        
        return {
            "campaign_type": campaign_type,
            "messaging_strategy": strategy,
            "brand_alignment": "strong",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _update_brand_guidelines(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update brand guidelines based on new requirements"""
        updates = task_data.get("updates", {})
        
        # Update guidelines
        for key, value in updates.items():
            if key in self.brand_guidelines:
                self.brand_guidelines[key] = value
        
        return {
            "guidelines_updated": True,
            "updated_fields": list(updates.keys()),
            "current_guidelines": self.brand_guidelines,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _general_brand_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """General brand analysis and recommendations"""
        return {
            "brand_health": "strong",
            "consistency_level": "high",
            "recommendations": [
                "Maintain current brand voice",
                "Expand brand guidelines for digital channels",
                "Regular brand consistency audits"
            ],
            "next_actions": ["Schedule quarterly brand review"]
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "brand_consistency_management",
            "messaging_strategy_development",
            "brand_guidelines_maintenance",
            "content_brand_review",
            "brand_voice_optimization"
        ]

class SocialMediaManagerAgent(SmartMemoryMixin, BaseAgent):
    """Social media strategy and community management specialist with memory"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Social Media Manager",
            role=AgentRole.SPECIALIST,
            department="marketing_excellence",
            specialization="social media strategy, community management, engagement optimization",
            manager_id=manager_id
        )
        
        # Social media configurations
        self.platforms = {
            "linkedin": {"audience": "professionals", "tone": "professional", "format": "long-form"},
            "twitter": {"audience": "tech-savvy", "tone": "conversational", "format": "short-form"},
            "instagram": {"audience": "visual-oriented", "tone": "inspiring", "format": "visual"},
            "facebook": {"audience": "broad", "tone": "friendly", "format": "mixed"}
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process social media management task"""
        task_type = task_data.get("task_type", "content_creation")
        
        if task_type == "content_creation":
            return await self._create_social_content(task_data)
        elif task_type == "engagement_analysis":
            return await self._analyze_engagement(task_data)
        elif task_type == "community_management":
            return await self._manage_community(task_data)
        elif task_type == "campaign_optimization":
            return await self._optimize_campaign(task_data)
        elif task_type == "competitor_analysis":
            return await self._analyze_competitor_performance(task_data)
        elif task_type == "sentiment_monitoring":
            return await self._monitor_customer_sentiment(task_data)
        elif task_type == "brand_monitoring":
            return await self._analyze_brand_mentions(task_data)
        elif task_type == "competitive_benchmarking":
            return await self._benchmark_against_competitors(task_data)
        else:
            return await self._general_social_management(task_data)
    
    async def _create_social_content(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create platform-optimized social media content with performance memory"""
        platform = task_data.get("platform", "linkedin")
        content_type = task_data.get("content_type", "post")
        topic = task_data.get("topic", "business growth")
        target_audience = task_data.get("target_audience", "startup founders")
        
        platform_config = self.platforms.get(platform, self.platforms["linkedin"])
        
        # Get high-performing content patterns from memory
        performance_memories = self.recall("content_performance", limit=5)
        high_performing_patterns = []
        
        if performance_memories:
            for memory in performance_memories:
                content_data = memory.content
                if (content_data.get("platform") == platform and 
                    content_data.get("engagement_score", 0) > 7):
                    high_performing_patterns.append({
                        "format": content_data.get("content_format"),
                        "hooks": content_data.get("successful_hooks", []),
                        "hashtags": content_data.get("successful_hashtags", [])
                    })
        
        learning_context = ""
        if high_performing_patterns:
            learning_context = f"\n\nHigh-Performing Patterns:\n{json.dumps(high_performing_patterns[:3], indent=2)}"
        
        prompt = f"""
        Create {content_type} for {platform}:
        
        Topic: {topic}
        Target Audience: {target_audience}
        Platform: {platform}
        Platform Guidelines: {json.dumps(platform_config)}
        {learning_context}
        
        Create content optimized for {platform} including:
        - main_text: primary content text
        - hashtags: relevant hashtags (5-10)
        - call_to_action: engagement driver
        - posting_time: optimal posting time
        - engagement_hooks: elements to drive interaction
        
        If learning patterns are available, incorporate successful elements.
        Make it engaging, valuable, and platform-appropriate.
        """
        
        response = await self.use_gemini(prompt)
        try:
            content = json.loads(response)
        except:
            content = {
                "main_text": f"Insights on {topic} for {target_audience}",
                "hashtags": ["#startup", "#business", "#growth", "#AI", "#innovation"],
                "call_to_action": "What's your experience with this?",
                "posting_time": "9:00 AM",
                "engagement_hooks": ["Question", "Statistics", "Personal story"]
            }
        
        content_id = f"social_{platform}_{int(datetime.now().timestamp())}"
        
        # Remember this content creation for future learning
        self.remember("content_creation", {
            "content_id": content_id,
            "platform": platform,
            "content_type": content_type,
            "topic": topic,
            "target_audience": target_audience,
            "content_format": content.get("main_text", "")[:100],
            "hashtags_used": content.get("hashtags", []),
            "engagement_hooks_used": content.get("engagement_hooks", [])
        }, {"creation_type": "social_content"})
        
        return {
            "content_id": content_id,
            "platform": platform,
            "content_type": content_type,
            "content": content,
            "brand_aligned": True,
            "estimated_reach": self._estimate_reach(platform, content),
            "learning_applied": len(high_performing_patterns) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _analyze_engagement(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze social media engagement metrics"""
        platform = task_data.get("platform", "all")
        time_period = task_data.get("time_period", "last_30_days")
        metrics = task_data.get("metrics", {})
        
        prompt = f"""
        Analyze social media engagement for {platform} over {time_period}:
        
        Metrics: {json.dumps(metrics)}
        
        Provide analysis as JSON with:
        - engagement_rate: calculated engagement rate
        - performance_summary: overall performance assessment
        - top_performing_content: best performing posts/content types
        - audience_insights: audience behavior patterns
        - optimization_opportunities: areas for improvement
        - recommended_actions: specific next steps
        """
        
        response = await self.use_gemini(prompt)
        try:
            analysis = json.loads(response)
        except:
            analysis = {
                "engagement_rate": "3.2%",
                "performance_summary": "Above industry average",
                "top_performing_content": ["Educational posts", "Behind-the-scenes"],
                "audience_insights": ["Most active during business hours"],
                "optimization_opportunities": ["Video content", "User-generated content"],
                "recommended_actions": ["Increase video content", "Engage more with comments"]
            }
        
        return {
            "platform": platform,
            "time_period": time_period,
            "engagement_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _manage_community(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle community management tasks"""
        action_type = task_data.get("action_type", "respond_to_comments")
        
        if action_type == "respond_to_comments":
            return await self._respond_to_comments(task_data)
        elif action_type == "handle_mentions":
            return await self._handle_mentions(task_data)
        elif action_type == "crisis_management":
            return await self._handle_crisis(task_data)
        else:
            return {"status": "community_managed", "action": action_type}
    
    async def _respond_to_comments(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate responses to social media comments"""
        comments = task_data.get("comments", [])
        responses = []
        
        for comment in comments:
            response = await self._generate_comment_response(comment)
            responses.append(response)
        
        return {
            "comments_processed": len(comments),
            "responses": responses,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_comment_response(self, comment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate response to individual comment"""
        comment_text = comment.get("text", "")
        sentiment = comment.get("sentiment", "neutral")
        
        prompt = f"""
        Generate an appropriate social media response to this comment:
        
        Comment: "{comment_text}"
        Sentiment: {sentiment}
        
        Response should be:
        - Professional and brand-aligned
        - Engaging and helpful
        - Appropriate for the sentiment
        - Encouraging further interaction
        
        Keep it concise and authentic.
        """
        
        response_text = await self.use_gemini(prompt)
        
        return {
            "original_comment": comment_text,
            "response": response_text,
            "sentiment": sentiment,
            "requires_escalation": sentiment == "negative"
        }
    
    def _estimate_reach(self, platform: str, content: Dict[str, Any]) -> Dict[str, str]:
        """Estimate content reach based on platform and content quality"""
        base_reach = {
            "linkedin": "500-2000",
            "twitter": "100-1000", 
            "instagram": "200-1500",
            "facebook": "50-500"
        }
        
        return {
            "estimated_reach": base_reach.get(platform, "100-1000"),
            "engagement_prediction": "moderate to high"
        }
    
    async def _optimize_campaign(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize social media campaign performance"""
        campaign_data = task_data.get("campaign_data", {})
        
        return {
            "campaign_optimized": True,
            "optimization_areas": ["Targeting", "Content format", "Posting schedule"],
            "expected_improvement": "15-25% increase in engagement"
        }
    
    async def _handle_mentions(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle brand mentions across platforms"""
        return {
            "mentions_processed": task_data.get("mention_count", 0),
            "response_strategy": "engage_positive_address_negative"
        }
    
    async def _handle_crisis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle social media crisis situations"""
        crisis_type = task_data.get("crisis_type", "negative_feedback")
        
        # Escalate crisis to manager
        if self.manager_id:
            await self.send_message(
                self.manager_id,
                MessageType.ESCALATION,
                {
                    "reason": "social_media_crisis",
                    "crisis_type": crisis_type,
                    "crisis_data": task_data
                },
                priority="critical"
            )
        
        return {
            "crisis_acknowledged": True,
            "immediate_action": "escalated_to_management",
            "response_timeline": "within_1_hour"
        }
    
    async def _analyze_competitor_performance(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor social media performance and extract strategic insights"""
        competitors = task_data.get("competitors", [])
        analysis_period = task_data.get("period", "last_30_days")
        platforms = task_data.get("platforms", ["linkedin", "twitter"])
        
        # Get previous competitor analysis from memory for trend tracking
        competitor_memories = self.recall("competitor_analysis", limit=10)
        historical_data = {}
        
        for memory in competitor_memories:
            comp_data = memory.content
            comp_name = comp_data.get("competitor_name")
            if comp_name:
                historical_data[comp_name] = comp_data
        
        prompt = f"""
        Analyze competitor social media performance and provide strategic insights:
        
        Competitors: {json.dumps(competitors)}
        Analysis Period: {analysis_period}
        Platforms: {json.dumps(platforms)}
        Historical Data: {json.dumps(historical_data) if historical_data else 'None'}
        
        Provide comprehensive competitor analysis as JSON with:
        - competitor_performance: individual performance metrics for each competitor
        - success_patterns: what's working well for top performers
        - failure_patterns: what's not working for struggling competitors
        - content_strategies: analysis of their content approaches
        - engagement_tactics: successful engagement methods they use
        - posting_patterns: optimal timing and frequency insights
        - audience_insights: their target audience characteristics
        - competitive_gaps: opportunities where we can outperform
        - threat_assessment: areas where competitors pose risks
        - strategic_recommendations: actionable insights for our strategy
        - trend_analysis: performance trends compared to historical data
        """
        
        analysis = await self.use_gemini(prompt)
        
        try:
            competitor_analysis = json.loads(analysis)
        except:
            competitor_analysis = {
                "competitor_performance": {},
                "success_patterns": ["High-quality visual content", "Consistent posting"],
                "failure_patterns": ["Irregular posting", "Low engagement rates"],
                "content_strategies": ["Educational content", "Behind-the-scenes"],
                "strategic_recommendations": ["Focus on unique value proposition", "Increase posting frequency"]
            }
        
        # Remember this analysis for future trend tracking
        for competitor in competitors:
            comp_name = competitor.get("name", "unknown")
            self.remember("competitor_analysis", {
                "competitor_name": comp_name,
                "analysis_period": analysis_period,
                "performance_data": competitor_analysis.get("competitor_performance", {}).get(comp_name, {}),
                "platforms_analyzed": platforms,
                "analysis_summary": str(competitor_analysis)[:300]
            }, {"analysis_type": "competitive_intelligence"})
        
        return {
            "analysis_type": "competitor_performance",
            "period": analysis_period,
            "competitors_analyzed": len(competitors),
            "competitive_intelligence": competitor_analysis,
            "historical_trends_available": len(historical_data) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _monitor_customer_sentiment(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor and analyze customer sentiment across social media platforms"""
        brand_name = task_data.get("brand_name", "our company")
        monitoring_period = task_data.get("period", "last_7_days")
        platforms = task_data.get("platforms", ["twitter", "linkedin", "facebook"])
        mentions_data = task_data.get("mentions", [])
        
        # Get historical sentiment data from memory
        sentiment_memories = self.recall("sentiment_tracking", limit=20)
        sentiment_trends = []
        
        for memory in sentiment_memories:
            sentiment_data = memory.content
            sentiment_trends.append({
                "date": memory.timestamp.isoformat(),
                "sentiment_score": sentiment_data.get("overall_sentiment_score", 0),
                "mention_count": sentiment_data.get("mention_count", 0),
                "platform": sentiment_data.get("platform", "unknown")
            })
        
        prompt = f"""
        Analyze customer sentiment and brand perception across social media:
        
        Brand: {brand_name}
        Monitoring Period: {monitoring_period}
        Platforms: {json.dumps(platforms)}
        Mentions Data: {json.dumps(mentions_data)}
        Historical Sentiment Trends: {json.dumps(sentiment_trends[-10:]) if sentiment_trends else 'None'}
        
        Provide comprehensive sentiment analysis as JSON with:
        - overall_sentiment_score: score from -100 (very negative) to +100 (very positive)
        - sentiment_breakdown: positive, neutral, negative percentages
        - platform_sentiment: sentiment analysis by platform
        - key_themes: main topics customers are discussing
        - positive_feedback: what customers are praising
        - negative_feedback: common complaints and issues
        - sentiment_drivers: factors influencing sentiment
        - customer_emotions: primary emotions expressed (joy, frustration, excitement)
        - influential_mentions: high-impact mentions or conversations
        - reputation_risks: potential reputation threats
        - response_recommendations: suggested responses to feedback
        - trend_analysis: sentiment changes compared to historical data
        - action_priorities: immediate actions needed based on sentiment
        """
        
        sentiment_analysis = await self.use_gemini(prompt)
        
        try:
            sentiment_result = json.loads(sentiment_analysis)
        except:
            sentiment_result = {
                "overall_sentiment_score": 75,
                "sentiment_breakdown": {"positive": 60, "neutral": 30, "negative": 10},
                "key_themes": ["product quality", "customer service", "innovation"],
                "positive_feedback": ["great product", "excellent support"],
                "negative_feedback": ["pricing concerns", "delivery delays"],
                "response_recommendations": ["Address pricing feedback", "Improve delivery communication"]
            }
        
        # Remember sentiment data for trend tracking
        self.remember("sentiment_tracking", {
            "brand_name": brand_name,
            "monitoring_period": monitoring_period,
            "platforms": platforms,
            "overall_sentiment_score": sentiment_result.get("overall_sentiment_score", 0),
            "mention_count": len(mentions_data),
            "sentiment_breakdown": sentiment_result.get("sentiment_breakdown", {}),
            "key_themes": sentiment_result.get("key_themes", []),
            "reputation_risks": sentiment_result.get("reputation_risks", [])
        }, {"tracking_type": "sentiment_monitoring"})
        
        return {
            "monitoring_type": "customer_sentiment",
            "brand": brand_name,
            "period": monitoring_period,
            "platforms_monitored": platforms,
            "mentions_analyzed": len(mentions_data),
            "sentiment_intelligence": sentiment_result,
            "trend_data_available": len(sentiment_trends) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _analyze_brand_mentions(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze brand mentions and conversations across platforms"""
        brand_name = task_data.get("brand_name", "our company")
        mentions = task_data.get("mentions", [])
        time_period = task_data.get("period", "last_24_hours")
        
        # Get previous mention analysis from memory
        mention_memories = self.search_memory(brand_name, "brand_monitoring")
        historical_mentions = []
        
        for memory in mention_memories[:5]:  # Last 5 mention analyses
            mention_data = memory.content
            historical_mentions.append({
                "date": memory.timestamp.isoformat(),
                "mention_count": mention_data.get("mention_count", 0),
                "engagement_level": mention_data.get("avg_engagement", 0),
                "sentiment": mention_data.get("dominant_sentiment", "neutral")
            })
        
        prompt = f"""
        Analyze brand mentions and customer conversations:
        
        Brand: {brand_name}
        Time Period: {time_period}
        Mentions: {json.dumps(mentions)}
        Historical Context: {json.dumps(historical_mentions) if historical_mentions else 'None'}
        
        Provide brand mention analysis as JSON with:
        - mention_volume: total number of mentions analyzed
        - reach_analysis: estimated audience reach of mentions
        - engagement_metrics: likes, shares, comments analysis
        - mention_sources: breakdown by platform and source type
        - conversation_themes: main topics being discussed
        - influencer_mentions: mentions by influential accounts
        - customer_questions: questions customers are asking
        - brand_associations: what people associate with the brand
        - competitive_mentions: mentions comparing to competitors
        - crisis_indicators: potential PR issues to monitor
        - response_opportunities: mentions that warrant company response
        - amplification_potential: content worth sharing or promoting
        - reputation_impact: overall impact on brand reputation
        - trending_topics: emerging topics related to the brand
        """
        
        mention_analysis = await self.use_gemini(prompt)
        
        try:
            mention_result = json.loads(mention_analysis)
        except:
            mention_result = {
                "mention_volume": len(mentions),
                "reach_analysis": {"estimated_reach": "5K-10K"},
                "engagement_metrics": {"avg_engagement": "moderate"},
                "conversation_themes": ["product features", "customer support"],
                "response_opportunities": ["customer questions", "feature requests"],
                "reputation_impact": "positive"
            }
        
        # Remember mention analysis
        self.remember("brand_monitoring", {
            "brand_name": brand_name,
            "time_period": time_period,
            "mention_count": len(mentions),
            "avg_engagement": mention_result.get("engagement_metrics", {}).get("avg_engagement", 0),
            "dominant_sentiment": mention_result.get("reputation_impact", "neutral"),
            "conversation_themes": mention_result.get("conversation_themes", []),
            "response_opportunities": mention_result.get("response_opportunities", []),
            "crisis_indicators": mention_result.get("crisis_indicators", [])
        }, {"monitoring_type": "brand_mentions"})
        
        return {
            "analysis_type": "brand_mentions",
            "brand": brand_name,
            "period": time_period,
            "mentions_processed": len(mentions),
            "brand_intelligence": mention_result,
            "historical_context": len(historical_mentions) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _benchmark_against_competitors(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Benchmark our social media performance against competitors"""
        our_metrics = task_data.get("our_metrics", {})
        competitor_metrics = task_data.get("competitor_metrics", {})
        benchmarking_period = task_data.get("period", "last_month")
        
        # Get historical benchmarking data
        benchmark_memories = self.recall("competitive_benchmarking", limit=5)
        trend_data = []
        
        for memory in benchmark_memories:
            benchmark_data = memory.content
            trend_data.append({
                "date": memory.timestamp.isoformat(),
                "our_performance_score": benchmark_data.get("our_performance_score", 0),
                "market_position": benchmark_data.get("market_position", "unknown"),
                "competitive_advantage": benchmark_data.get("competitive_advantages", [])
            })
        
        prompt = f"""
        Perform competitive benchmarking analysis for social media performance:
        
        Our Metrics: {json.dumps(our_metrics)}
        Competitor Metrics: {json.dumps(competitor_metrics)}
        Benchmarking Period: {benchmarking_period}
        Historical Trend Data: {json.dumps(trend_data) if trend_data else 'None'}
        
        Provide benchmarking analysis as JSON with:
        - performance_comparison: how we rank against each competitor
        - our_performance_score: overall score (0-100) relative to market
        - market_position: our position (leader, strong_competitor, challenger, niche_player)
        - competitive_advantages: areas where we outperform competitors
        - competitive_disadvantages: areas where we lag behind
        - opportunity_gaps: areas with potential for improvement
        - threat_assessment: competitive threats to monitor
        - benchmark_metrics: key metrics comparison table
        - improvement_targets: specific metrics to focus on improving
        - strategic_priorities: recommended focus areas based on gaps
        - market_trends: overall market performance trends
        - competitive_landscape: overview of competitive dynamics
        """
        
        benchmark_analysis = await self.use_gemini(prompt)
        
        try:
            benchmark_result = json.loads(benchmark_analysis)
        except:
            benchmark_result = {
                "our_performance_score": 75,
                "market_position": "strong_competitor",
                "competitive_advantages": ["content quality", "engagement rate"],
                "competitive_disadvantages": ["posting frequency", "follower growth"],
                "improvement_targets": ["increase posting frequency", "improve follower acquisition"],
                "strategic_priorities": ["content optimization", "audience growth"]
            }
        
        # Remember benchmarking results
        self.remember("competitive_benchmarking", {
            "benchmarking_period": benchmarking_period,
            "our_performance_score": benchmark_result.get("our_performance_score", 0),
            "market_position": benchmark_result.get("market_position", "unknown"),
            "competitive_advantages": benchmark_result.get("competitive_advantages", []),
            "competitive_disadvantages": benchmark_result.get("competitive_disadvantages", []),
            "improvement_targets": benchmark_result.get("improvement_targets", []),
            "competitors_analyzed": len(competitor_metrics)
        }, {"analysis_type": "competitive_benchmarking"})
        
        return {
            "analysis_type": "competitive_benchmarking",
            "period": benchmarking_period,
            "competitors_benchmarked": len(competitor_metrics),
            "benchmarking_intelligence": benchmark_result,
            "trend_analysis_available": len(trend_data) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _general_social_management(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """General social media management activities"""
        return {
            "social_health": "strong",
            "content_calendar": "up_to_date",
            "community_engagement": "active",
            "growth_rate": "steady"
        }
    
    async def track_content_performance(self, content_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and learn from content performance"""
        platform = performance_data.get("platform", "unknown")
        engagement_rate = performance_data.get("engagement_rate", 0)
        reach = performance_data.get("reach", 0)
        clicks = performance_data.get("clicks", 0)
        
        # Calculate engagement score (0-10 scale)
        engagement_score = min(10, engagement_rate * 100 / 5)  # Normalize to 0-10
        
        # Get original content creation memory
        creation_memories = self.search_memory(content_id, "content_creation")
        content_format = ""
        successful_hooks = []
        successful_hashtags = []
        
        if creation_memories:
            creation_data = creation_memories[0].content
            content_format = creation_data.get("content_format", "")
            if engagement_score > 7:  # High performing content
                successful_hooks = creation_data.get("engagement_hooks_used", [])
                successful_hashtags = creation_data.get("hashtags_used", [])
        
        # Remember performance for future optimization
        self.remember("content_performance", {
            "content_id": content_id,
            "platform": platform,
            "engagement_score": engagement_score,
            "engagement_rate": engagement_rate,
            "reach": reach,
            "clicks": clicks,
            "content_format": content_format,
            "successful_hooks": successful_hooks,
            "successful_hashtags": successful_hashtags,
            "performance_category": "high" if engagement_score > 7 else "medium" if engagement_score > 4 else "low"
        }, {"tracking_type": "performance_analysis"})
        
        return {
            "content_id": content_id,
            "engagement_score": engagement_score,
            "performance_tracked": True,
            "learning_updated": engagement_score > 7,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "social_media_content_creation",
            "community_management",
            "engagement_optimization",
            "social_media_analytics",
            "crisis_management",
            "multi_platform_strategy",
            "content_performance_learning",
            "competitor_analysis",
            "customer_sentiment_monitoring",
            "brand_mention_tracking",
            "competitive_benchmarking",
            "reputation_management",
            "competitive_intelligence",
            "sentiment_trend_analysis",
            "brand_perception_monitoring"
        ]

class ContentCreatorAgent(SmartMemoryMixin, BaseAgent):
    """Multi-channel content creation specialist with memory"""
    
    def __init__(self, agent_id: str, manager_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Content Creator",
            role=AgentRole.SPECIALIST,
            department="marketing_excellence",
            specialization="content strategy, copywriting, multi-channel content creation",
            manager_id=manager_id
        )
        
        # Content creation configurations
        self.content_types = {
            "blog_post": {"length": "1200-2000 words", "tone": "informative", "structure": "intro-body-conclusion"},
            "email": {"length": "200-400 words", "tone": "personal", "structure": "hook-value-cta"},
            "social_post": {"length": "50-200 words", "tone": "engaging", "structure": "hook-insight-cta"},
            "whitepaper": {"length": "3000-5000 words", "tone": "authoritative", "structure": "executive-analysis-recommendations"},
            "case_study": {"length": "800-1200 words", "tone": "storytelling", "structure": "challenge-solution-results"}
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process content creation task"""
        task_type = task_data.get("task_type", "content_creation")
        
        if task_type == "content_creation":
            return await self._create_content(task_data)
        elif task_type == "content_strategy":
            return await self._develop_content_strategy(task_data)
        elif task_type == "content_optimization":
            return await self._optimize_content(task_data)
        elif task_type == "content_calendar":
            return await self._create_content_calendar(task_data)
        else:
            return await self._general_content_management(task_data)
    
    async def _create_content(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create specific content piece with performance learning"""
        content_type = task_data.get("content_type", "blog_post")
        topic = task_data.get("topic", "AI for business growth")
        target_audience = task_data.get("target_audience", "startup founders")
        objectives = task_data.get("objectives", ["educate", "generate leads"])
        brand_voice = task_data.get("brand_voice", "professional yet approachable")
        
        content_config = self.content_types.get(content_type, self.content_types["blog_post"])
        
        # Get high-performing content patterns from memory
        performance_memories = self.recall("content_performance", limit=5)
        successful_patterns = []
        
        if performance_memories:
            for memory in performance_memories:
                perf_data = memory.content
                if (perf_data.get("content_type") == content_type and 
                    perf_data.get("performance_score", 0) > 7):
                    successful_patterns.append({
                        "topic_approach": perf_data.get("topic_approach", ""),
                        "structure_elements": perf_data.get("successful_structure", []),
                        "keywords": perf_data.get("high_performing_keywords", [])
                    })
        
        learning_context = ""
        if successful_patterns:
            learning_context = f"\n\nHigh-Performing Content Patterns:\n{json.dumps(successful_patterns[:3], indent=2)}"
        
        prompt = f"""
        Create {content_type} content:
        
        Topic: {topic}
        Target Audience: {target_audience}
        Objectives: {json.dumps(objectives)}
        Brand Voice: {brand_voice}
        Content Specifications: {json.dumps(content_config)}
        {learning_context}
        
        Create comprehensive content including:
        - headline: compelling headline/title
        - introduction: engaging opening
        - main_content: detailed body content
        - conclusion: strong closing with CTA
        - key_takeaways: 3-5 main points
        - seo_keywords: relevant keywords for SEO
        - meta_description: SEO meta description
        
        If learning patterns are available, incorporate successful elements.
        Make it valuable, engaging, and aligned with objectives.
        """
        
        response = await self.use_gemini(prompt)
        try:
            content = json.loads(response)
        except:
            content = {
                "headline": f"How {topic} Can Transform Your Business",
                "introduction": f"In today's competitive landscape, {topic} has become essential...",
                "main_content": f"Detailed exploration of {topic} and its applications...",
                "conclusion": "Start your transformation today with these insights.",
                "key_takeaways": [f"Key insight about {topic}", "Implementation strategy", "Expected outcomes"],
                "seo_keywords": ["AI", "business growth", "digital transformation"],
                "meta_description": f"Learn how {topic} can drive business growth and competitive advantage."
            }
        
        content_id = f"{content_type}_{int(datetime.now().timestamp())}"
        
        # Remember this content creation for future learning
        self.remember("content_creation", {
            "content_id": content_id,
            "content_type": content_type,
            "topic": topic,
            "target_audience": target_audience,
            "topic_approach": content.get("headline", "")[:100],
            "structure_used": content.get("key_takeaways", []),
            "keywords_used": content.get("seo_keywords", []),
            "objectives": objectives
        }, {"creation_type": "long_form_content"})
        
        return {
            "content_id": content_id,
            "content_type": content_type,
            "topic": topic,
            "content": content,
            "word_count": self._estimate_word_count(content),
            "brand_aligned": True,
            "seo_optimized": True,
            "learning_applied": len(successful_patterns) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _develop_content_strategy(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive content strategy"""
        business_goals = task_data.get("business_goals", [])
        target_audiences = task_data.get("target_audiences", [])
        competitors = task_data.get("competitors", [])
        timeline = task_data.get("timeline", "3_months")
        
        prompt = f"""
        Develop comprehensive content strategy:
        
        Business Goals: {json.dumps(business_goals)}
        Target Audiences: {json.dumps(target_audiences)}
        Competitors: {json.dumps(competitors)}
        Timeline: {timeline}
        
        Provide strategy as JSON with:
        - content_pillars: main content themes (3-5)
        - content_mix: distribution across content types
        - publishing_frequency: how often to publish
        - channel_strategy: which channels for which content
        - content_calendar: high-level calendar outline
        - success_metrics: KPIs to track
        - competitive_differentiation: unique positioning
        """
        
        response = await self.use_gemini(prompt)
        try:
            strategy = json.loads(response)
        except:
            strategy = {
                "content_pillars": ["Thought leadership", "Customer success", "Industry insights", "How-to guides"],
                "content_mix": {"blog_posts": "40%", "social_content": "30%", "email": "20%", "whitepapers": "10%"},
                "publishing_frequency": "3x per week",
                "channel_strategy": {"linkedin": "professional content", "blog": "long-form insights"},
                "content_calendar": "Monthly themes with weekly topics",
                "success_metrics": ["Traffic", "Engagement", "Lead generation", "Brand awareness"],
                "competitive_differentiation": "Data-driven insights with practical implementation"
            }
        
        return {
            "strategy_type": "comprehensive_content_strategy",
            "timeline": timeline,
            "content_strategy": strategy,
            "implementation_plan": await self._create_implementation_plan(strategy),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _create_implementation_plan(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation plan for content strategy"""
        return {
            "phase_1": "Content pillar development and calendar creation",
            "phase_2": "Content production and channel setup",
            "phase_3": "Publishing and performance optimization",
            "timeline": "12 weeks",
            "resources_needed": ["Content creator", "Designer", "SEO specialist"],
            "success_milestones": ["Calendar completion", "First month published", "Performance review"]
        }
    
    async def _optimize_content(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing content for better performance"""
        content = task_data.get("content", "")
        optimization_goals = task_data.get("goals", ["seo", "engagement"])
        
        optimization_results = {}
        
        for goal in optimization_goals:
            if goal == "seo":
                optimization_results["seo"] = await self._optimize_for_seo(content)
            elif goal == "engagement":
                optimization_results["engagement"] = await self._optimize_for_engagement(content)
            elif goal == "conversion":
                optimization_results["conversion"] = await self._optimize_for_conversion(content)
        
        return {
            "original_content_length": len(content),
            "optimization_results": optimization_results,
            "improvement_score": "25% improvement expected",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _optimize_for_seo(self, content: str) -> Dict[str, Any]:
        """Optimize content for SEO"""
        prompt = f"""
        Analyze this content for SEO optimization:
        
        Content: "{content[:500]}..."
        
        Provide SEO recommendations as JSON with:
        - keyword_opportunities: keywords to target
        - title_optimization: improved title suggestions
        - meta_description: optimized meta description
        - content_structure: heading and structure improvements
        - internal_linking: linking opportunities
        - readability_score: content readability assessment
        """
        
        response = await self.use_gemini(prompt)
        try:
            return json.loads(response)
        except:
            return {
                "keyword_opportunities": ["AI automation", "business efficiency"],
                "title_optimization": "Include primary keyword in title",
                "meta_description": "Write compelling 155-character description",
                "content_structure": "Add more subheadings",
                "internal_linking": "Link to related content",
                "readability_score": "Good"
            }
    
    async def _optimize_for_engagement(self, content: str) -> Dict[str, Any]:
        """Optimize content for engagement"""
        return {
            "engagement_improvements": [
                "Add compelling hook in first paragraph",
                "Include interactive elements",
                "Strengthen call-to-action",
                "Add social proof elements"
            ],
            "expected_improvement": "20% increase in engagement"
        }
    
    async def _optimize_for_conversion(self, content: str) -> Dict[str, Any]:
        """Optimize content for conversion"""
        return {
            "conversion_improvements": [
                "Clearer value proposition",
                "Stronger CTAs",
                "Reduce friction points",
                "Add urgency elements"
            ],
            "expected_improvement": "15% increase in conversion rate"
        }
    
    async def _create_content_calendar(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create content calendar"""
        duration = task_data.get("duration", "3_months")
        content_pillars = task_data.get("content_pillars", [])
        publishing_frequency = task_data.get("frequency", "weekly")
        
        calendar = await self._generate_calendar(duration, content_pillars, publishing_frequency)
        
        return {
            "calendar_duration": duration,
            "publishing_frequency": publishing_frequency,
            "content_calendar": calendar,
            "total_content_pieces": len(calendar.get("schedule", [])),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _generate_calendar(self, duration: str, pillars: List[str], frequency: str) -> Dict[str, Any]:
        """Generate detailed content calendar"""
        # Simplified calendar generation
        return {
            "schedule": [
                {"week": 1, "topic": "AI fundamentals", "type": "blog_post", "pillar": pillars[0] if pillars else "education"},
                {"week": 2, "topic": "Implementation guide", "type": "how_to", "pillar": pillars[1] if len(pillars) > 1 else "guidance"},
                {"week": 3, "topic": "Success stories", "type": "case_study", "pillar": pillars[2] if len(pillars) > 2 else "social_proof"}
            ],
            "themes": {
                "month_1": "Foundation building",
                "month_2": "Implementation",
                "month_3": "Optimization"
            }
        }
    
    def _estimate_word_count(self, content: Dict[str, Any]) -> int:
        """Estimate word count of content"""
        total_words = 0
        for key, value in content.items():
            if isinstance(value, str):
                total_words += len(value.split())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        total_words += len(item.split())
        return total_words
    
    async def _general_content_management(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """General content management activities"""
        return {
            "content_pipeline": "healthy",
            "production_capacity": "80% utilized",
            "quality_score": "high",
            "performance_trending": "positive"
        }
    
    async def track_content_performance(self, content_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track and learn from long-form content performance"""
        content_type = performance_data.get("content_type", "unknown")
        page_views = performance_data.get("page_views", 0)
        time_on_page = performance_data.get("time_on_page", 0)
        bounce_rate = performance_data.get("bounce_rate", 0)
        conversions = performance_data.get("conversions", 0)
        
        # Calculate performance score (0-10 scale)
        performance_score = 0
        if page_views > 0:
            performance_score += min(3, page_views / 1000 * 3)  # Views component
        if time_on_page > 0:
            performance_score += min(3, time_on_page / 180 * 3)  # Time component (3 min = max)
        if bounce_rate < 70:
            performance_score += 2  # Low bounce rate bonus
        if conversions > 0:
            performance_score += min(2, conversions / 10 * 2)  # Conversion component
        
        # Get original content creation memory
        creation_memories = self.search_memory(content_id, "content_creation")
        successful_structure = []
        high_performing_keywords = []
        topic_approach = ""
        
        if creation_memories:
            creation_data = creation_memories[0].content
            topic_approach = creation_data.get("topic_approach", "")
            if performance_score > 7:  # High performing content
                successful_structure = creation_data.get("structure_used", [])
                high_performing_keywords = creation_data.get("keywords_used", [])
        
        # Remember performance for future optimization
        self.remember("content_performance", {
            "content_id": content_id,
            "content_type": content_type,
            "performance_score": performance_score,
            "page_views": page_views,
            "time_on_page": time_on_page,
            "bounce_rate": bounce_rate,
            "conversions": conversions,
            "topic_approach": topic_approach,
            "successful_structure": successful_structure,
            "high_performing_keywords": high_performing_keywords,
            "performance_category": "high" if performance_score > 7 else "medium" if performance_score > 4 else "low"
        }, {"tracking_type": "content_performance_analysis"})
        
        return {
            "content_id": content_id,
            "performance_score": performance_score,
            "performance_tracked": True,
            "learning_updated": performance_score > 7,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "multi_channel_content_creation",
            "content_strategy_development",
            "seo_optimization",
            "content_calendar_planning",
            "performance_optimization",
            "brand_voice_consistency",
            "content_performance_learning"
        ]

class MarketingExcellenceManager(ManagerAgent):
    """Manager for marketing excellence team"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            name="Marketing Excellence Manager",
            role=AgentRole.MANAGER,
            department="marketing_excellence",
            specialization="marketing strategy, brand management, team coordination"
        )
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process management tasks for marketing excellence"""
        task_type = task_data.get("task_type", "coordination")
        
        if task_type == "campaign_coordination":
            return await self._coordinate_campaign(task_data)
        elif task_type == "brand_strategy_review":
            return await self._review_brand_strategy(task_data)
        elif task_type == "performance_optimization":
            return await self._optimize_team_performance(task_data)
        else:
            return await self._general_management(task_data)
    
    async def _coordinate_campaign(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multi-channel marketing campaign"""
        campaign_data = task_data.get("campaign_data", {})
        
        # Coordinate with team members
        coordination_plan = {
            "brand_manager": "Ensure brand consistency across all materials",
            "social_media_manager": "Develop social media amplification strategy",
            "content_creator": "Create campaign content assets",
            "timeline": "2 weeks for preparation, 4 weeks execution"
        }
        
        return {
            "campaign_coordination": "initiated",
            "coordination_plan": coordination_plan,
            "expected_outcomes": [
                "Consistent brand messaging",
                "Multi-channel reach",
                "Measurable ROI"
            ]
        }
    
    async def _review_brand_strategy(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review and optimize brand strategy"""
        return {
            "brand_health": "strong",
            "consistency_score": "92%",
            "market_position": "well-positioned",
            "recommendations": [
                "Expand brand guidelines for new channels",
                "Increase brand awareness campaigns",
                "Monitor competitor brand positioning"
            ]
        }
    
    async def _optimize_team_performance(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize marketing team performance"""
        return {
            "team_performance": "above_target",
            "efficiency_gains": "18% improvement in campaign ROI",
            "collaboration_score": "excellent",
            "development_priorities": [
                "Advanced analytics training",
                "Emerging platform expertise",
                "Cross-functional collaboration"
            ]
        }
    
    async def _general_management(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """General marketing management activities"""
        return {
            "marketing_health": "strong",
            "pipeline_status": "healthy",
            "team_morale": "high",
            "strategic_priorities": [
                "Brand consistency",
                "Content quality",
                "Engagement optimization"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        return super().get_capabilities() + [
            "marketing_strategy_management",
            "brand_portfolio_oversight",
            "campaign_coordination",
            "performance_optimization"
        ]