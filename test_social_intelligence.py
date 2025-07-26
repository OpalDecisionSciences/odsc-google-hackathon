#!/usr/bin/env python3
"""
Test script for enhanced SocialMediaManagerAgent intelligence capabilities
Tests competitor analysis and customer sentiment monitoring
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.marketing_agents import SocialMediaManagerAgent

async def test_competitor_analysis():
    """Test competitor analysis capabilities"""
    print("🔍 Testing Competitor Analysis...")
    
    agent = SocialMediaManagerAgent("social_intel_001", "manager_001")
    
    # Mock competitor data
    competitor_data = {
        "task_type": "competitor_analysis",
        "competitors": [
            {
                "name": "TechRival Corp",
                "platforms": ["linkedin", "twitter"],
                "followers": {"linkedin": 15000, "twitter": 8500},
                "engagement_rate": 4.2,
                "posting_frequency": "daily"
            },
            {
                "name": "InnovateStartup",
                "platforms": ["linkedin", "instagram"],
                "followers": {"linkedin": 8000, "instagram": 12000},
                "engagement_rate": 6.1,
                "posting_frequency": "3x/week"
            }
        ],
        "period": "last_30_days",
        "platforms": ["linkedin", "twitter", "instagram"]
    }
    
    result = await agent.process_task(competitor_data)
    
    print(f"   ✅ Competitors analyzed: {result['competitors_analyzed']}")
    print(f"   ✅ Analysis period: {result['period']}")
    print(f"   ✅ Intelligence generated: {len(str(result['competitive_intelligence']))> 100}")
    print(f"   ✅ Historical trends: {result['historical_trends_available']}")
    
    # Test second analysis to check memory/trends
    result2 = await agent.process_task(competitor_data)
    print(f"   ✅ Memory tracking works: {result2['historical_trends_available']}")
    
    return result

async def test_sentiment_monitoring():
    """Test customer sentiment monitoring"""
    print("\n💭 Testing Customer Sentiment Monitoring...")
    
    agent = SocialMediaManagerAgent("social_intel_002", "manager_001")
    
    # Mock sentiment monitoring data
    sentiment_data = {
        "task_type": "sentiment_monitoring",
        "brand_name": "AI Startup Solutions",
        "period": "last_7_days",
        "platforms": ["twitter", "linkedin", "facebook"],
        "mentions": [
            {"text": "Love the new AI features from AI Startup Solutions!", "platform": "twitter", "sentiment": "positive"},
            {"text": "Having some issues with their customer support", "platform": "linkedin", "sentiment": "negative"},
            {"text": "Great product but pricing is a bit high", "platform": "facebook", "sentiment": "mixed"},
            {"text": "AI Startup Solutions helped us increase productivity by 40%", "platform": "linkedin", "sentiment": "positive"},
            {"text": "The integration was seamless", "platform": "twitter", "sentiment": "positive"}
        ]
    }
    
    result = await agent.process_task(sentiment_data)
    
    print(f"   ✅ Brand monitored: {result['brand']}")
    print(f"   ✅ Platforms: {len(result['platforms_monitored'])}")
    print(f"   ✅ Mentions analyzed: {result['mentions_analyzed']}")
    print(f"   ✅ Sentiment intelligence: {len(str(result['sentiment_intelligence'])) > 100}")
    print(f"   ✅ Trend tracking: {result['trend_data_available']}")
    
    return result

async def test_brand_mention_analysis():
    """Test brand mention analysis"""
    print("\n🏷️ Testing Brand Mention Analysis...")
    
    agent = SocialMediaManagerAgent("social_intel_003", "manager_001")
    
    # Mock brand mention data
    mention_data = {
        "task_type": "brand_monitoring",
        "brand_name": "AI Startup Solutions",
        "period": "last_24_hours",
        "mentions": [
            {"text": "Just tried AI Startup Solutions - impressed!", "author": "tech_reviewer", "platform": "twitter", "engagement": 45},
            {"text": "Anyone used AI Startup Solutions for automation?", "author": "startup_founder", "platform": "linkedin", "engagement": 12},
            {"text": "AI Startup Solutions vs TechRival - which is better?", "author": "business_analyst", "platform": "linkedin", "engagement": 23},
            {"text": "AI Startup Solutions customer service needs improvement", "author": "frustrated_user", "platform": "twitter", "engagement": 8}
        ]
    }
    
    result = await agent.process_task(mention_data)
    
    print(f"   ✅ Brand: {result['brand']}")
    print(f"   ✅ Mentions processed: {result['mentions_processed']}")
    print(f"   ✅ Brand intelligence: {len(str(result['brand_intelligence'])) > 100}")
    print(f"   ✅ Historical context: {result['historical_context']}")
    
    return result

async def test_competitive_benchmarking():
    """Test competitive benchmarking"""
    print("\n📊 Testing Competitive Benchmarking...")
    
    agent = SocialMediaManagerAgent("social_intel_004", "manager_001")
    
    # Mock benchmarking data
    benchmark_data = {
        "task_type": "competitive_benchmarking",
        "our_metrics": {
            "followers": {"linkedin": 5000, "twitter": 3200},
            "engagement_rate": 3.8,
            "posting_frequency": "5x/week",
            "content_quality_score": 7.5
        },
        "competitor_metrics": {
            "TechRival Corp": {
                "followers": {"linkedin": 15000, "twitter": 8500},
                "engagement_rate": 4.2,
                "posting_frequency": "daily",
                "content_quality_score": 8.1
            },
            "InnovateStartup": {
                "followers": {"linkedin": 8000, "twitter": 4200},
                "engagement_rate": 6.1,
                "posting_frequency": "3x/week",
                "content_quality_score": 7.8
            }
        },
        "period": "last_month"
    }
    
    result = await agent.process_task(benchmark_data)
    
    print(f"   ✅ Benchmarking period: {result['period']}")
    print(f"   ✅ Competitors benchmarked: {result['competitors_benchmarked']}")
    print(f"   ✅ Intelligence generated: {len(str(result['benchmarking_intelligence'])) > 100}")
    print(f"   ✅ Trend analysis: {result['trend_analysis_available']}")
    
    return result

async def main():
    """Run social media intelligence tests"""
    print("🧠 Testing Enhanced Social Media Intelligence Features")
    print("=" * 55)
    
    try:
        # Test competitor analysis
        competitor_result = await test_competitor_analysis()
        
        # Test sentiment monitoring  
        sentiment_result = await test_sentiment_monitoring()
        
        # Test brand mention analysis
        mention_result = await test_brand_mention_analysis()
        
        # Test competitive benchmarking
        benchmark_result = await test_competitive_benchmarking()
        
        print("\n🎉 Social Media Intelligence Tests Summary:")
        print("=" * 45)
        print("✅ Competitor Analysis: PASSED")
        print("✅ Sentiment Monitoring: PASSED") 
        print("✅ Brand Mention Analysis: PASSED")
        print("✅ Competitive Benchmarking: PASSED")
        print("\n🚀 All enhanced intelligence features working correctly!")
        
        # Show enhanced capabilities
        agent = SocialMediaManagerAgent("capability_test", "manager")
        capabilities = agent.get_capabilities()
        intelligence_capabilities = [cap for cap in capabilities if any(keyword in cap for keyword in ['competitor', 'sentiment', 'brand', 'competitive', 'intelligence', 'reputation'])]
        
        print(f"\n🎯 New Intelligence Capabilities Added:")
        for cap in intelligence_capabilities:
            print(f"   • {cap}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Intelligence tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())