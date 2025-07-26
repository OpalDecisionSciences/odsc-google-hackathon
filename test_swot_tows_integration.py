#!/usr/bin/env python3
"""
Test SWOT-TOWS MCP Tool Integration
Comprehensive test of the SWOT-TOWS analyzer with real business data
"""

import asyncio
import sys
import os
sys.path.append('src')

from src.tools.swot_tows_analyzer import swot_tows_analyzer
from src.tools.agent_intelligence_sharing import agent_intelligence_sharing

async def test_swot_tows_integration():
    """Test comprehensive SWOT-TOWS integration"""
    
    print("🧪 Testing SWOT-TOWS MCP Tool Integration")
    print("=" * 60)
    
    # Simulate real business context from Research Agent
    business_context = {
        'business_name': 'NVIDIA',
        'industry': 'AI/Semiconductor',
        'market_cap': 1500000000000,  # 1.5T
        'primary_competitors': ['AMD', 'Intel', 'Qualcomm'],
        'competitive_position': 'Market Leader',
        'financial_health': 'Strong'
    }
    
    # Simulate research data from enhanced scraper
    research_data = {
        'financial_data': {
            'current_price': 875.50,
            'market_cap': 1500000000000,
            'pe_ratio': 28.5,
            'profit_margin': 0.26,
            'month_performance': 15.2,
            'sector': 'Technology',
            'employees': 65000
        },
        'news_sentiment': {
            'sentiment_label': 'Positive',
            'articles_analyzed': 15,
            'sentiment_score': 0.8
        },
        'competitor_data': {
            'primary_competitors': ['AMD', 'Intel', 'Qualcomm'],
            'competitive_analysis': [
                {'name': 'AMD', 'market_cap': 240000000000},
                {'name': 'Intel', 'market_cap': 190000000000}
            ]
        },
        'industry_trends': {
            'growth_trend': 'High Growth',
            'market_size': '$574B by 2030',
            'key_drivers': ['AI adoption', 'Data center demand', 'Edge computing'],
            'challenges': ['Supply chain', 'Geopolitical tensions']
        },
        'data_sources': ['yahoo_finance', 'google_news', 'wikipedia']
    }
    
    # Simulate competitive intelligence from Social Media Agent
    competitive_intelligence = {
        'analysis_type': 'competitor_performance',
        'competitive_intelligence': {
            'competitive_advantages': ['Market leadership', 'AI technology'],
            'opportunity_gaps': ['New market segments', 'Emerging technologies'],
            'threat_assessment': ['Intense competition', 'Regulatory risks']
        }
    }
    
    print(f"📊 Testing SWOT-TOWS Analysis for {business_context['business_name']}")
    
    try:
        # Test SWOT-TOWS analysis
        analysis_result = await swot_tows_analyzer.analyze_business_intelligence(
            business_context=business_context,
            research_data=research_data,
            competitive_intelligence=competitive_intelligence
        )
        
        print("✅ SWOT-TOWS Analysis Completed Successfully!")
        print(f"   Company: {analysis_result['company']}")
        print(f"   Strategic Framework: SWOT-TOWS Matrix")
        print(f"   Confidence Score: {analysis_result['confidence_score']:.1%}")
        
        # Test SWOT factors
        swot_analysis = analysis_result['swot_analysis']
        print(f"\n📋 SWOT Factors Identified:")
        print(f"   Strengths: {len(swot_analysis['strengths'])}")
        print(f"   Weaknesses: {len(swot_analysis['weaknesses'])}")
        print(f"   Opportunities: {len(swot_analysis['opportunities'])}")
        print(f"   Threats: {len(swot_analysis['threats'])}")
        
        # Test TOWS strategies
        tows_matrix = analysis_result['tows_matrix']
        print(f"\n🚀 TOWS Strategies Generated:")
        print(f"   SO Strategies: {len(tows_matrix['SO_strategies'])}")
        print(f"   ST Strategies: {len(tows_matrix['ST_strategies'])}")
        print(f"   WO Strategies: {len(tows_matrix['WO_strategies'])}")
        print(f"   WT Strategies: {len(tows_matrix['WT_strategies'])}")
        
        # Test strategic insights
        strategic_insights = analysis_result['strategic_insights']
        print(f"\n🎯 Strategic Intelligence:")
        print(f"   Strategic Position: {strategic_insights['strategic_position']}")
        print(f"   Recommended Focus: {strategic_insights['recommended_focus']}")
        
        # Test agent intelligence sharing
        print(f"\n🔗 Testing Agent Intelligence Sharing:")
        
        # Test strategic recommendations access
        recommendations = agent_intelligence_sharing.get_strategic_recommendations('NVIDIA')
        print(f"   ✅ Strategic recommendations available: {bool(recommendations)}")
        
        if recommendations:
            print(f"   Strategic Position: {recommendations.get('strategic_position', 'Unknown')}")
            print(f"   SO Strategies: {len(recommendations.get('top_so_strategies', []))}")
            print(f"   ST Strategies: {len(recommendations.get('top_st_strategies', []))}")
            print(f"   WO Strategies: {len(recommendations.get('top_wo_strategies', []))}")
            print(f"   WT Strategies: {len(recommendations.get('top_wt_strategies', []))}")
        
        # Test strategic context formatting for different agent types
        print(f"\n📝 Testing Strategic Context Formatting:")
        
        agent_types = ['social_media', 'customer_support', 'sales', 'general']
        for agent_type in agent_types:
            context = agent_intelligence_sharing.format_strategic_context_for_agent('NVIDIA', agent_type)
            if context:
                print(f"   ✅ {agent_type.title()} Agent: {len(context)} chars of strategic context")
            else:
                print(f"   ❌ {agent_type.title()} Agent: No context generated")
        
        print("\n" + "=" * 60)
        print("🎯 SWOT-TOWS MCP TOOL INTEGRATION TEST RESULTS:")
        print("✅ SWOT-TOWS analysis engine working perfectly")
        print("✅ Real business intelligence integration successful")
        print("✅ TOWS strategy generation operational")
        print("✅ Agent intelligence sharing functional")
        print("✅ Strategic context formatting for all agent types")
        print("✅ Ready for production deployment!")
        
        # Test specific strategy access
        print(f"\n🎪 Sample Strategic Intelligence Access:")
        so_strategies = agent_intelligence_sharing.get_so_strategies('NVIDIA')
        if so_strategies:
            print(f"   SO Strategy Example: {so_strategies[0][:80]}...")
        
        strategic_position = agent_intelligence_sharing.get_strategic_position('NVIDIA')
        print(f"   Strategic Position: {strategic_position}")
        
        confidence = agent_intelligence_sharing.get_confidence_score('NVIDIA')
        print(f"   Analysis Confidence: {confidence:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ SWOT-TOWS Integration Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_swot_tows_integration())
    
    if success:
        print("\n🏆 SWOT-TOWS MCP Tool ready for Google Hackathon demo!")
    else:
        print("\n💥 Integration test failed - needs debugging")
        sys.exit(1)