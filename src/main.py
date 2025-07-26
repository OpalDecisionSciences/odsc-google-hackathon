#!/usr/bin/env python3
"""
Main Application Entry Point
AI Agent Orchestration System for Business Success
"""

import asyncio
import logging
import os
import sys
import json
from typing import Dict, Any, Optional
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our modules
from .core.base_agent import BaseAgent, AgentRole
from .agents.business_agents import (
    CustomerSupportAgent, SalesQualificationAgent, BusinessIntelligenceAgent,
    CustomerOperationsManager, SequentialAgent, LoopAgent, ParallelAgent, RouterAgent
)
from .agents.marketing_agents import (
    BrandManagerAgent, SocialMediaManagerAgent, ContentCreatorAgent,
    MarketingExcellenceManager
)
from .communication.a2a_system import global_message_broker, global_workflow_orchestrator
from .tools.gemini_integration import GeminiAnalyzer, BusinessIntelligenceEngine

class BusinessAgentSystem:
    """Main orchestration system for business agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.managers: Dict[str, BaseAgent] = {}
        self.router_agent: Optional[RouterAgent] = None
        self.gemini_analyzer: Optional[GeminiAnalyzer] = None
        self.bi_engine: Optional[BusinessIntelligenceEngine] = None
        
        # System status
        self.is_running = False
        self.startup_time: Optional[datetime] = None
    
    async def initialize_system(self):
        """Initialize the complete agent system"""
        logger.info("🚀 Initializing AI Agent Orchestration System...")
        
        try:
            # Initialize Gemini integration
            await self._initialize_gemini()
            
            # Start message broker
            await global_message_broker.start()
            
            # Create and register agents
            await self._create_agents()
            
            # Initialize router agent
            await self._initialize_router()
            
            # Start agent listeners
            await self._start_agent_listeners()
            
            self.is_running = True
            self.startup_time = datetime.now()
            
            logger.info("✅ System initialized successfully!")
            logger.info(f"📊 Active agents: {len(self.agents)}")
            logger.info(f"👥 Managers: {len(self.managers)}")
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            raise
    
    async def _initialize_gemini(self):
        """Initialize Gemini AI integration"""
        try:
            self.gemini_analyzer = GeminiAnalyzer()
            self.bi_engine = BusinessIntelligenceEngine(self.gemini_analyzer)
            logger.info("🧠 Gemini AI integration initialized")
        except Exception as e:
            logger.warning(f"⚠️ Gemini initialization failed: {e}")
            logger.warning("System will continue without AI capabilities")
    
    async def _create_agents(self):
        """Create and register all business agents"""
        
        # Create managers first
        customer_ops_manager = CustomerOperationsManager("mgr_customer_ops")
        marketing_manager = MarketingExcellenceManager("mgr_marketing")
        
        self.managers["customer_ops"] = customer_ops_manager
        self.managers["marketing"] = marketing_manager
        
        # Register managers with broker
        global_message_broker.register_agent(customer_ops_manager)
        global_message_broker.register_agent(marketing_manager)
        
        # Create specialist agents
        agents_to_create = [
            ("support_agent", CustomerSupportAgent, "mgr_customer_ops"),
            ("sales_agent", SalesQualificationAgent, "mgr_customer_ops"),
            ("bi_agent", BusinessIntelligenceAgent, "mgr_customer_ops"),
            ("brand_agent", BrandManagerAgent, "mgr_marketing"),
            ("social_agent", SocialMediaManagerAgent, "mgr_marketing"),
            ("content_agent", ContentCreatorAgent, "mgr_marketing")
        ]
        
        for agent_id, agent_class, manager_id in agents_to_create:
            agent = agent_class(agent_id, manager_id)
            self.agents[agent_id] = agent
            
            # Register with message broker
            global_message_broker.register_agent(agent)
            
            # Add to manager's team
            if manager_id in self.managers:
                self.managers[manager_id].add_team_member(agent_id)
        
        logger.info(f"👥 Created {len(self.agents)} specialist agents")
    
    async def _initialize_router(self):
        """Initialize the master router agent"""
        self.router_agent = RouterAgent("master_router")
        
        # Register all agents with router
        for agent in list(self.agents.values()) + list(self.managers.values()):
            self.router_agent.register_agent(agent)
        
        # Register router with broker
        global_message_broker.register_agent(self.router_agent)
        
        logger.info("🧭 Master router agent initialized")
    
    async def _start_agent_listeners(self):
        """Start message listeners for all agents"""
        tasks = []
        
        # Start listeners for all agents
        for agent in list(self.agents.values()) + list(self.managers.values()):
            if self.router_agent:
                tasks.append(asyncio.create_task(agent.listen_for_messages()))
        
        if self.router_agent:
            tasks.append(asyncio.create_task(self.router_agent.listen_for_messages()))
        
        logger.info(f"👂 Started {len(tasks)} agent listeners")
    
    async def process_business_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a business request through the agent system"""
        if not self.is_running:
            raise RuntimeError("System not initialized")
        
        logger.info(f"📥 Processing business request: {request.get('type', 'unknown')}")
        
        try:
            # Route through master router
            if self.router_agent:
                result = await self.router_agent.process_task(request)
                logger.info("✅ Request processed successfully")
                return result
            else:
                # Fallback: direct routing
                return await self._direct_process_request(request)
                
        except Exception as e:
            logger.error(f"❌ Request processing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _direct_process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Direct request processing fallback"""
        request_type = request.get("type", "general")
        
        # Simple routing logic
        if "customer" in request_type or "support" in request_type:
            agent = self.agents.get("support_agent")
        elif "sales" in request_type or "lead" in request_type:
            agent = self.agents.get("sales_agent")
        elif "marketing" in request_type or "content" in request_type:
            agent = self.agents.get("content_agent")
        elif "social" in request_type:
            agent = self.agents.get("social_agent")
        else:
            agent = self.agents.get("bi_agent")
        
        if agent:
            return await agent.process_task(request)
        else:
            return {"status": "error", "message": "No suitable agent found"}
    
    async def demonstrate_advanced_workflows(self):
        """Demonstrate advanced agent workflow patterns"""
        logger.info("🎭 Demonstrating Advanced Agent Workflows...")
        
        # Demo data
        demo_data = {
            "business_scenario": "startup_growth_analysis",
            "company": "TechStart Inc",
            "challenge": "Need comprehensive business analysis for growth planning"
        }
        
        demonstrations = []
        
        # 1. Sequential Workflow Demo
        logger.info("🔄 Demo 1: Sequential Agent Pipeline")
        sequential_agents = [
            self.agents["bi_agent"],
            self.agents["content_agent"],
            self.agents["social_agent"]
        ]
        
        if all(sequential_agents):
            sequential_agent = SequentialAgent("demo_sequential", sequential_agents)
            sequential_result = await sequential_agent.process_task(demo_data)
            demonstrations.append({
                "workflow": "Sequential Pipeline",
                "description": "BI Analysis → Content Creation → Social Strategy",
                "result": sequential_result
            })
        
        # 2. Parallel Workflow Demo
        logger.info("⚡ Demo 2: Parallel Agent Processing")
        parallel_agents = [
            self.agents["support_agent"],
            self.agents["sales_agent"],
            self.agents["brand_agent"]
        ]
        
        if all(parallel_agents):
            parallel_agent = ParallelAgent("demo_parallel", parallel_agents)
            parallel_result = await parallel_agent.process_task(demo_data)
            demonstrations.append({
                "workflow": "Parallel Processing",
                "description": "Simultaneous analysis from multiple perspectives",
                "result": parallel_result
            })
        
        # 3. Loop/Iterative Demo
        logger.info("🔁 Demo 3: Iterative Refinement Loop")
        if self.agents.get("content_agent"):
            loop_agent = LoopAgent("demo_loop", self.agents["content_agent"], max_iterations=3)
            loop_result = await loop_agent.process_task({
                **demo_data,
                "task": "Create high-quality marketing content"
            })
            demonstrations.append({
                "workflow": "Iterative Loop",
                "description": "Continuous refinement until quality threshold met",
                "result": loop_result
            })
        
        return {
            "demo_title": "Advanced Agent Workflow Patterns",
            "demonstrations": demonstrations,
            "timestamp": datetime.now().isoformat()
        }
    
    async def run_comprehensive_business_analysis(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run comprehensive business analysis using Gemini AI"""
        if not self.bi_engine:
            return {"error": "Business Intelligence engine not available"}
        
        logger.info("📊 Running comprehensive business analysis...")
        
        try:
            # Perform multi-dimensional analysis
            analyses = await self.bi_engine.comprehensive_business_analysis(business_data)
            
            # Generate executive summary
            executive_summary = await self.bi_engine.generate_executive_summary(analyses)
            
            return {
                "analysis_type": "comprehensive_business_analysis",
                "individual_analyses": {name: {
                    "type": result.analysis_type,
                    "confidence": result.confidence,
                    "recommendations_count": len(result.recommendations),
                    "timestamp": result.timestamp.isoformat()
                } for name, result in analyses.items()},
                "executive_summary": executive_summary,
                "system_metadata": {
                    "total_analyses": len(analyses),
                    "processing_time": "estimated_30_seconds",
                    "gemini_integration": "active"
                }
            }
        except Exception as e:
            logger.error(f"Business analysis failed: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        broker_metrics = global_message_broker.get_metrics()
        agent_status = global_message_broker.get_agent_status()
        
        return {
            "system_status": "running" if self.is_running else "stopped",
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "agents": {
                "total_agents": len(self.agents),
                "managers": len(self.managers),
                "router_active": self.router_agent is not None,
                "gemini_active": self.gemini_analyzer is not None
            },
            "communication": broker_metrics,
            "agent_details": agent_status
        }
    
    async def shutdown(self):
        """Gracefully shutdown the system"""
        logger.info("🛑 Shutting down system...")
        
        self.is_running = False
        
        # Shutdown all agents
        for agent in list(self.agents.values()) + list(self.managers.values()):
            await agent.shutdown()
        
        if self.router_agent:
            await self.router_agent.shutdown()
        
        # Stop message broker
        await global_message_broker.stop()
        
        logger.info("✅ System shutdown complete")

async def run_demo_scenarios():
    """Run demonstration scenarios"""
    system = BusinessAgentSystem()
    
    try:
        # Initialize system
        await system.initialize_system()
        
        print("\n" + "="*60)
        print("🎯 AI AGENT ORCHESTRATION SYSTEM DEMO")
        print("="*60)
        
        # Demo 1: System Status
        print("\n📊 SYSTEM STATUS:")
        status = system.get_system_status()
        print(f"   Agents: {status['agents']['total_agents']} specialists + {status['agents']['managers']} managers")
        print(f"   Router: {'✅ Active' if status['agents']['router_active'] else '❌ Inactive'}")
        print(f"   Gemini AI: {'✅ Active' if status['agents']['gemini_active'] else '❌ Inactive'}")
        print(f"   Messages: {status['communication']['messages_sent']} sent, {status['communication']['success_rate']:.1f}% success")
        
        # Demo 2: Business Request Processing  
        print("\n💼 DEMO: Customer Support Request")
        customer_request = {
            "type": "customer_support",
            "inquiry_text": "I'm having trouble with my account login and need immediate help",
            "customer_id": "CUST_12345",
            "channel": "email",
            "priority": "high"
        }
        
        result = await system.process_business_request(customer_request)
        print(f"   ✅ Support request processed")
        print(f"   📋 Status: {result.get('execution_result', {}).get('status', 'completed')}")
        
        # Demo 3: Advanced Workflows
        print("\n🎭 DEMO: Advanced Agent Workflows")
        workflow_demo = await system.demonstrate_advanced_workflows()
        print(f"   🔄 Sequential Pipeline: {'✅ Completed' if workflow_demo else '❌ Failed'}")
        print(f"   ⚡ Parallel Processing: {'✅ Completed' if workflow_demo else '❌ Failed'}")
        print(f"   🔁 Iterative Refinement: {'✅ Completed' if workflow_demo else '❌ Failed'}")
        
        # Demo 4: Business Intelligence
        if system.gemini_analyzer:
            print("\n🧠 DEMO: AI-Powered Business Analysis")
            business_data = {
                "company": {
                    "name": "TechStart Inc",
                    "industry": "SaaS",
                    "stage": "growth",
                    "business_model": {"type": "subscription", "mrr": 50000}
                },
                "market": {
                    "size": "large",
                    "growth_rate": 0.15,
                    "competition": "moderate"
                }
            }
            
            analysis_result = await system.run_comprehensive_business_analysis(business_data)
            if "error" not in analysis_result:
                print(f"   📈 Analyses completed: {analysis_result.get('system_metadata', {}).get('total_analyses', 0)}")
                print(f"   🎯 Executive summary: {'✅ Generated' if analysis_result.get('executive_summary') else '❌ Failed'}")
            else:
                print(f"   ❌ Analysis failed: {analysis_result['error']}")
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    finally:
        await system.shutdown()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Agent Orchestration System")
    parser.add_argument("--demo", action="store_true", help="Run demonstration scenarios")
    parser.add_argument("--api-key", help="Gemini API key (or set GEMINI_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Set API key if provided
    if args.api_key:
        os.environ['GEMINI_API_KEY'] = args.api_key
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️ Warning: GEMINI_API_KEY not set. AI features will be limited.")
        print("Set it with: export GEMINI_API_KEY='your_key_here'")
    
    try:
        if args.demo:
            asyncio.run(run_demo_scenarios())
        else:
            print("🚀 AI Agent Orchestration System")
            print("Use --demo to run demonstration scenarios")
            print("Use --help for more options")
    
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()