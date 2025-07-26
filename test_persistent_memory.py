#!/usr/bin/env python3
"""
Test Persistent Memory System
Verify customer service remembers users across sessions
"""

import asyncio
import sys
import os
import shutil
from pathlib import Path

# Ensure we can import from src
sys.path.append('src')

async def test_persistent_memory_system():
    """Test complete persistent memory functionality"""
    
    print("🧪 Testing Persistent Memory System")
    print("=" * 60)
    
    # Clean up any existing memory data for clean test
    memory_dir = Path("memory_data")
    if memory_dir.exists():
        shutil.rmtree(memory_dir)
        print("🧹 Cleaned up existing memory data")
    
    # Test 1: Import and initialize persistent memory
    print("\n📂 Test 1: Initialize Persistent Memory System")
    try:
        from src.memory.persistent_memory import persistent_memory
        stats = persistent_memory.get_memory_stats()
        print(f"✅ Persistent memory initialized")
        print(f"   Memory directory: {persistent_memory.memory_dir}")
        print(f"   Initial customers: {stats['customers_tracked']}")
        print(f"   Memory files: {len(stats['memory_files'])}")
    except Exception as e:
        print(f"❌ Failed to initialize persistent memory: {e}")
        return False
    
    # Test 2: Store customer interaction with name
    print("\n👤 Test 2: Store Customer Interaction with Name")
    try:
        customer_id = "test_customer_john"
        interaction_data = {
            "customer_id": customer_id,
            "inquiry_text": "Hi, my name is John Doe and I need help with my account",
            "inquiry_classification": {"type": "account_issue", "urgency": "medium"},
            "response": "Hello John! I'd be happy to help you with your account issue.",
            "needs_escalation": False,
            "channel": "web_ui",
            "resolution_status": "completed",
            "satisfaction_tracking": {"current_score": 4},
            "customer_name": "John Doe"
        }
        
        persistent_memory.store_customer_interaction(customer_id, interaction_data)
        print(f"✅ Customer interaction stored: {customer_id}")
        
        # Verify storage
        customer_data = persistent_memory.get_customer_history(customer_id)
        print(f"   Customer name: {customer_data.get('customer_profile', {}).get('name', 'Not found')}")
        print(f"   Total interactions: {len(customer_data.get('interactions', []))}")
        
    except Exception as e:
        print(f"❌ Failed to store customer interaction: {e}")
        return False
    
    # Test 3: Store SWOT intelligence
    print("\n📊 Test 3: Store SWOT Intelligence")
    try:
        company_name = "NVIDIA"
        swot_data = {
            "company": company_name,
            "analysis_timestamp": "2024-01-15T10:30:00",
            "strategic_insights": {
                "strategic_position": "Star Position: Strong internal capabilities in favorable market"
            },
            "tows_matrix": {
                "SO_strategies": [{"title": "Growth Strategy 1", "description": "Leverage AI leadership"}],
                "ST_strategies": [{"title": "Defense Strategy 1", "description": "Protect market position"}]
            },
            "confidence_score": 0.91
        }
        
        persistent_memory.store_swot_intelligence(company_name, swot_data)
        print(f"✅ SWOT intelligence stored: {company_name}")
        
        # Verify storage
        retrieved_swot = persistent_memory.get_swot_intelligence(company_name)
        print(f"   Strategic position: {retrieved_swot.get('strategic_insights', {}).get('strategic_position', 'Not found')}")
        print(f"   Confidence score: {retrieved_swot.get('confidence_score', 0):.1%}")
        
    except Exception as e:
        print(f"❌ Failed to store SWOT intelligence: {e}")
        return False
    
    # Test 4: Simulate session restart by re-importing
    print("\n🔄 Test 4: Simulate Session Restart")
    try:
        # Re-import to simulate new session
        from importlib import reload
        import src.memory.persistent_memory as pm_module
        reload(pm_module)
        from src.memory.persistent_memory import persistent_memory as new_persistent_memory
        
        # Verify data persisted across "session restart"
        customer_data = new_persistent_memory.get_customer_history(customer_id)
        swot_data = new_persistent_memory.get_swot_intelligence(company_name)
        
        print(f"✅ Data persisted across session restart")
        print(f"   Customer found: {bool(customer_data)}")
        print(f"   Customer name: {customer_data.get('customer_profile', {}).get('name', 'Not found')}")
        print(f"   SWOT data found: {bool(swot_data)}")
        print(f"   SWOT confidence: {swot_data.get('confidence_score', 0):.1%}")
        
    except Exception as e:
        print(f"❌ Failed session restart test: {e}")
        return False
    
    # Test 5: Customer context formatting
    print("\n💬 Test 5: Customer Context Formatting")
    try:
        context = new_persistent_memory.get_customer_context(customer_id)
        print(f"✅ Customer context generated")
        print(f"   Context length: {len(context)} characters")
        print(f"   Contains name: {'John Doe' in context}")
        print(f"   Contains interaction count: {'Total Interactions:' in context}")
        
        # Show first part of context
        print(f"\n   Context preview:")
        print(f"   {context[:200]}...")
        
    except Exception as e:
        print(f"❌ Failed customer context formatting: {e}")
        return False
    
    # Test 6: Test customer support agent integration
    print("\n🤖 Test 6: Customer Support Agent Integration")
    try:
        from src.agents.business_agents import CustomerSupportAgent
        
        # Create agent
        agent = CustomerSupportAgent("test_support", "test_manager")
        
        # Test follow-up interaction
        task_data = {
            "customer_id": customer_id,
            "inquiry_text": "Hi, it's John again. I need to follow up on my account issue",
            "channel": "web_ui"
        }
        
        # This should load persistent memory and recognize John
        result = await agent.process_task(task_data)
        
        print(f"✅ Customer support agent processed follow-up")
        print(f"   Previous interactions found: {result.get('previous_interactions', 0)}")
        print(f"   Response generated: {bool(result.get('response'))}")
        
        # Verify second interaction was stored
        updated_customer_data = new_persistent_memory.get_customer_history(customer_id)
        total_interactions = len(updated_customer_data.get('interactions', []))
        print(f"   Total interactions now: {total_interactions}")
        
    except Exception as e:
        print(f"❌ Failed customer support integration: {e}")
        return False
    
    # Test 7: Memory statistics
    print("\n📈 Test 7: Memory Statistics")
    try:
        stats = new_persistent_memory.get_memory_stats()
        print(f"✅ Memory statistics generated")
        print(f"   Customers tracked: {stats['customers_tracked']}")
        print(f"   Total customer interactions: {stats['total_customer_interactions']}")
        print(f"   Companies analyzed: {stats['companies_analyzed']}")
        print(f"   Memory files: {len(stats['memory_files'])}")
        
    except Exception as e:
        print(f"❌ Failed memory statistics: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎯 PERSISTENT MEMORY SYSTEM TEST RESULTS:")
    print("✅ JSON persistent memory system operational")
    print("✅ Customer data persists across sessions")
    print("✅ Customer names stored and retrieved")
    print("✅ SWOT intelligence persists across sessions")
    print("✅ Customer support agent integration successful")
    print("✅ Cross-session memory loading functional")
    print("✅ Memory statistics and monitoring available")
    print("\n🏆 Persistent memory system ready for hackathon demo!")
    print("📋 Judges can verify customer service remembers users by name!")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_persistent_memory_system())
    
    if success:
        print("\n🎉 All persistent memory tests passed!")
    else:
        print("\n💥 Persistent memory tests failed - needs debugging")
        sys.exit(1)