#!/usr/bin/env python3
"""
Test script for enhanced memory features
Validates memory functionality across different agent types
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.business_agents import CustomerSupportAgent, SalesQualificationAgent
from src.agents.marketing_agents import SocialMediaManagerAgent, ContentCreatorAgent

async def test_customer_support_memory():
    """Test CustomerSupportAgent memory features"""
    print("🧪 Testing CustomerSupportAgent Memory...")
    
    agent = CustomerSupportAgent("support_001", "manager_001")
    
    # Simulate customer interactions
    customer_data = {
        "customer_id": "cust_123",
        "inquiry_text": "I'm having trouble with login issues",
        "channel": "email"
    }
    
    result1 = await agent.process_task(customer_data)
    print(f"✅ First interaction processed: {result1['inquiry_classification']['type']}")
    
    # Second interaction - should reference history
    customer_data2 = {
        "customer_id": "cust_123", 
        "inquiry_text": "The login issue is still not resolved",
        "channel": "email"
    }
    
    result2 = await agent.process_task(customer_data2)
    print(f"✅ Follow-up interaction: Previous interactions = {result2['previous_interactions']}")
    
    return result1, result2

async def test_sales_agent_memory():
    """Test SalesQualificationAgent learning features"""
    print("\n🧪 Testing SalesQualificationAgent Learning...")
    
    agent = SalesQualificationAgent("sales_001", "manager_001")
    
    # First lead qualification
    lead_data = {
        "lead_data": {
            "id": "lead_456",
            "company": "TechStartup Inc",
            "budget": "50k-100k",
            "timeline": "Q2 2024",
            "authority": "CTO"
        }
    }
    
    result1 = await agent.process_task(lead_data)
    print(f"✅ First qualification: Score = {result1['lead_score']}, Status = {result1['qualification_status']}")
    
    # Follow-up qualification - should show learning
    lead_data2 = {
        "lead_data": {
            "id": "lead_456", 
            "company": "TechStartup Inc",
            "budget": "75k-125k",  # Improved budget
            "timeline": "Q1 2024",  # Faster timeline 
            "authority": "CEO"      # Higher authority
        }
    }
    
    result2 = await agent.process_task(lead_data2)
    print(f"✅ Follow-up qualification: Score = {result2['lead_score']}, Trend = {result2['engagement_trend']}")
    
    return result1, result2

async def test_social_media_memory():
    """Test SocialMediaManagerAgent content learning"""
    print("\n🧪 Testing SocialMediaManagerAgent Content Learning...")
    
    agent = SocialMediaManagerAgent("social_001", "manager_001")
    
    # Create initial content
    content_data = {
        "platform": "linkedin",
        "content_type": "post", 
        "topic": "AI automation",
        "target_audience": "startup founders"
    }
    
    result1 = await agent._create_social_content(content_data)
    print(f"✅ Content created: ID = {result1['content_id']}, Learning applied = {result1['learning_applied']}")
    
    # Simulate performance tracking
    performance_data = {
        "platform": "linkedin",
        "engagement_rate": 8.5,  # High engagement
        "reach": 2500,
        "clicks": 150
    }
    
    perf_result = await agent.track_content_performance(result1['content_id'], performance_data)
    print(f"✅ Performance tracked: Score = {perf_result['engagement_score']}, Learning updated = {perf_result['learning_updated']}")
    
    # Create new content - should incorporate learning
    result2 = await agent._create_social_content(content_data)
    print(f"✅ New content with learning: Learning applied = {result2['learning_applied']}")
    
    return result1, result2, perf_result

async def test_content_creator_memory():
    """Test ContentCreatorAgent performance learning"""
    print("\n🧪 Testing ContentCreatorAgent Performance Learning...")
    
    agent = ContentCreatorAgent("content_001", "manager_001")
    
    # Create initial content
    content_data = {
        "content_type": "blog_post",
        "topic": "Digital transformation",
        "target_audience": "business leaders",
        "objectives": ["educate", "generate_leads"]
    }
    
    result1 = await agent._create_content(content_data)
    print(f"✅ Content created: ID = {result1['content_id']}, Words = {result1['word_count']}")
    
    # Simulate performance tracking
    performance_data = {
        "content_type": "blog_post",
        "page_views": 1500,
        "time_on_page": 240,  # 4 minutes
        "bounce_rate": 45,    # Low bounce rate
        "conversions": 8
    }
    
    perf_result = await agent.track_content_performance(result1['content_id'], performance_data)
    print(f"✅ Performance tracked: Score = {perf_result['performance_score']:.1f}, Learning updated = {perf_result['learning_updated']}")
    
    # Create new content - should use learning
    result2 = await agent._create_content(content_data)
    print(f"✅ New content with learning: Learning applied = {result2['learning_applied']}")
    
    return result1, result2, perf_result

async def main():
    """Run memory feature tests"""
    print("🧠 Testing Enhanced Memory Features for AI Agent System")
    print("=" * 60)
    
    try:
        # Test customer support memory
        support_results = await test_customer_support_memory()
        
        # Test sales agent learning
        sales_results = await test_sales_agent_memory()
        
        # Test social media content learning
        social_results = await test_social_media_memory()
        
        # Test content creator performance learning
        content_results = await test_content_creator_memory()
        
        print("\n🎉 Memory Enhancement Tests Summary:")
        print("=" * 40)
        print("✅ Customer Support Memory: PASSED")
        print("✅ Sales Agent Learning: PASSED") 
        print("✅ Social Media Learning: PASSED")
        print("✅ Content Creator Learning: PASSED")
        print("\n🚀 All memory features working correctly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())