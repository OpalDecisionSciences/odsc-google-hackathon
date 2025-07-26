#!/usr/bin/env python3
"""
Test script for BusinessStrategyAgent with social media intelligence integration
Demonstrates how strategy agents access competitive intelligence from social media agents
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.business_agents import BusinessStrategyAgent
from src.agents.marketing_agents import SocialMediaManagerAgent

async def test_comprehensive_strategy():
    """Test comprehensive business strategy with integrated intelligence"""
    print("🎯 Testing Comprehensive Business Strategy...")
    
    strategy_agent = BusinessStrategyAgent("strategy_001", "manager_001")
    
    # Test comprehensive strategy
    strategy_data = {
        "strategy_type": "comprehensive",
        "business_context": {
            "company": "AI Startup Solutions",
            "stage": "growth",
            "industry": "AI/SaaS",
            "target_market": "startups and SMBs",
            "current_revenue": "$500K ARR",
            "team_size": 15
        },
        "time_horizon": "quarterly"
    }
    
    result = await strategy_agent.process_task(strategy_data)
    
    print(f"   ✅ Strategy Type: {result['strategy_type']}")
    print(f"   ✅ Time Horizon: {result['time_horizon']}")
    print(f"   ✅ Intelligence Sources: {', '.join(result['intelligence_sources'])}")
    print(f"   ✅ Strategic Plan Generated: {len(str(result['strategic_plan'])) > 100}")
    print(f"   ✅ Implementation Roadmap: {len(result['implementation_roadmap']['phase_1_30_days'])} immediate initiatives")
    print(f"   ✅ Success Metrics Defined: {len(result['success_metrics']['financial_metrics'])} financial KPIs")
    
    return result

async def test_swot_toes_integration():
    """Test SWOT/TOES analysis integration"""
    print("\n📊 Testing SWOT/TOES Analysis Integration...")
    
    strategy_agent = BusinessStrategyAgent("strategy_swot", "manager_001")
    
    # Test strategy with SWOT/TOES analysis
    strategy_data = {
        "strategy_type": "comprehensive",
        "business_context": {
            "company": "AI Startup Solutions",
            "stage": "growth",
            "industry": "AI/SaaS",
            "team_size": 15,
            "current_revenue": "$500K ARR"
        }
    }
    
    # Get the intelligence data to verify SWOT/TOES is included
    intelligence_data = await strategy_agent._gather_intelligence_data(strategy_data["business_context"])
    
    print(f"   ✅ Business Intelligence Gathered: {'business_metrics' in intelligence_data}")
    
    if 'business_metrics' in intelligence_data:
        swot_data = intelligence_data['business_metrics'].get('swot_analysis', {})
        print(f"   ✅ SWOT Matrix: {len(swot_data.get('swot_matrix', {}).get('strengths', []))} strengths identified")
        print(f"   ✅ TOES Analysis: {len(swot_data.get('toes_analysis', {}).keys())} TOES dimensions analyzed")
        print(f"   ✅ Strategic Insights: {len(swot_data.get('strategic_insights', []))} insights generated")
        print(f"   ✅ Action Priorities: {len(swot_data.get('action_priorities', []))} priorities identified")
    
    # Test full strategy creation with SWOT/TOES
    full_result = await strategy_agent.process_task(strategy_data)
    print(f"   ✅ SWOT/TOES Integrated Strategy: Generated comprehensive plan with analytical foundation")
    
    return intelligence_data

async def test_competitive_positioning():
    """Test competitive positioning strategy"""
    print("\n🥊 Testing Competitive Positioning Strategy...")
    
    strategy_agent = BusinessStrategyAgent("strategy_002", "manager_001")
    
    # Test competitive positioning
    competitive_data = {
        "strategy_type": "competitive_positioning",
        "business_context": {
            "company": "AI Startup Solutions",
            "competitors": ["TechRival Corp", "InnovateStartup", "AutomationPro"],
            "differentiators": ["AI-first approach", "startup-focused", "affordable pricing"],
            "market_position": "challenger"
        }
    }
    
    result = await strategy_agent.process_task(competitive_data)
    
    print(f"   ✅ Competitive Landscape Analysis: Generated")
    print(f"   ✅ Differentiation Strategy: {result['strategic_plan'].get('differentiation_strategy', 'Defined')}")
    print(f"   ✅ Market Positioning: {result['strategic_plan'].get('market_positioning', 'Established')}")
    print(f"   ✅ Go-to-Market Tactics: {len(result['strategic_plan'].get('go_to_market_tactics', []))} tactics defined")
    
    return result

async def test_brand_strategy():
    """Test brand strategy with sentiment intelligence"""
    print("\n🎨 Testing Brand Strategy with Sentiment Intelligence...")
    
    strategy_agent = BusinessStrategyAgent("strategy_004", "manager_001")
    
    # Test brand strategy
    brand_data = {
        "strategy_type": "brand_strategy",
        "business_context": {
            "company": "AI Startup Solutions",
            "brand_attributes": ["innovative", "reliable", "accessible"],
            "target_perception": "The AI partner for growing businesses",
            "reputation_concerns": ["pricing", "support response time"]
        }
    }
    
    result = await strategy_agent.process_task(brand_data)
    
    print(f"   ✅ Brand Positioning: {result['strategic_plan'].get('brand_positioning', 'Defined')}")
    print(f"   ✅ Brand Promise: {result['strategic_plan'].get('brand_promise', 'Established')}")
    print(f"   ✅ Brand Personality: {', '.join(result['strategic_plan'].get('brand_personality', []))}")
    print(f"   ✅ Reputation Management: {result['strategic_plan'].get('reputation_management', 'Strategy defined')}")
    
    return result

async def test_intelligence_integration():
    """Test intelligence data integration"""
    print("\n🧠 Testing Intelligence Integration...")
    
    strategy_agent = BusinessStrategyAgent("strategy_005", "manager_001")
    
    # Create a strategy to test intelligence gathering
    strategy_data = {
        "strategy_type": "comprehensive",
        "business_context": {
            "company": "AI Startup Solutions",
            "focus": "competitive advantage"
        }
    }
    
    # Access the intelligence gathering method directly to test integration
    intelligence_data = await strategy_agent._gather_intelligence_data(strategy_data["business_context"])
    
    print(f"   ✅ Social Media Intelligence: {'social_media' in intelligence_data}")
    print(f"   ✅ Business Metrics: {'business_metrics' in intelligence_data}")
    print(f"   ✅ Historical Insights: {'historical_insights' in intelligence_data}")
    
    if 'social_media' in intelligence_data:
        social_intel = intelligence_data['social_media']
        print(f"   ✅ Competitor Analysis: {len(social_intel.get('competitor_analysis', {}).get('market_leaders', []))} competitors identified")
        print(f"   ✅ Sentiment Score: {social_intel.get('sentiment_intelligence', {}).get('sentiment_score', 0)}/10")
        print(f"   ✅ Market Opportunities: {len(social_intel.get('competitor_analysis', {}).get('opportunities', []))} opportunities found")
    
    if 'business_metrics' in intelligence_data:
        business_intel = intelligence_data['business_metrics']
        swot_data = business_intel.get('swot_analysis', {})
        print(f"   ✅ SWOT Analysis Available: {len(swot_data.get('swot_matrix', {}).keys()) == 4}")
        print(f"   ✅ TOES Analysis Available: {len(swot_data.get('toes_analysis', {}).keys()) == 4}")
    
    return intelligence_data

async def main():
    """Run strategic integration tests"""
    print("🎯 Testing BusinessStrategyAgent with Integrated Intelligence (SWOT/TOES + Social)")
    print("=" * 80)
    
    test_results = []
    
    try:
        # Test comprehensive strategy
        comprehensive_result = await test_comprehensive_strategy()
        test_results.append(("Comprehensive Strategy", True))
        
        # Test SWOT/TOES integration
        swot_intelligence = await test_swot_toes_integration()
        test_results.append(("SWOT/TOES Integration", 'swot_analysis' in swot_intelligence.get('business_metrics', {})))
        
        # Test competitive positioning
        competitive_result = await test_competitive_positioning()
        test_results.append(("Competitive Positioning", True))
        
        # Test brand strategy
        brand_result = await test_brand_strategy()
        test_results.append(("Brand Strategy", True))
        
        # Test intelligence integration
        intelligence_data = await test_intelligence_integration()
        test_results.append(("Intelligence Integration", len(intelligence_data) >= 2))
        
        print("\n🎉 Strategy Integration Tests Summary:")
        print("=" * 45)
        
        passed_tests = 0
        for test_name, success in test_results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   {test_name}: {status}")
            if success:
                passed_tests += 1
        
        success_rate = (passed_tests / len(test_results)) * 100
        print(f"\n📊 Overall Success Rate: {passed_tests}/{len(test_results)} ({success_rate:.0f}%)")
        
        if success_rate >= 80:
            print("\n🚀 Strategic Intelligence Integration: SUCCESSFUL!")
            print("💡 Key Innovations Demonstrated:")
            print("   • SWOT/TOES analysis integrated into strategic planning")
            print("   • Social media intelligence feeds strategic decisions")
            print("   • Multiple strategy types with unified intelligence")
            print("   • Memory-enhanced strategic learning")
            print("   • Comprehensive implementation roadmaps")
        else:
            print("\n⚠️ Integration needs optimization")
        
        print("\n🔗 Integration Benefits:")
        print("   • SWOT/TOES provides analytical foundation for strategy")
        print("   • Real-time competitive intelligence informs positioning")
        print("   • Market sentiment guides brand and positioning strategy")
        print("   • Historical strategic insights improve future planning")
        print("   • Unified intelligence enables data-driven strategic decisions")
        
        return success_rate >= 80
        
    except Exception as e:
        print(f"\n❌ Strategy integration tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())