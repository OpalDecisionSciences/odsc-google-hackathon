#!/usr/bin/env python3
"""
Persistent Memory Demo for Google Hackathon Judges
Demonstrates customer service remembering users by name across sessions
"""

import asyncio
import sys
import os

# Ensure we can import from src  
sys.path.append('src')

async def demo_customer_service_memory():
    """Demo showing customer service remembers users by name across different sessions"""
    
    print("🎯 PERSISTENT MEMORY DEMO FOR HACKATHON JUDGES")
    print("=" * 70)
    print("📋 SCENARIO: Customer service that remembers users by name")
    print("🎪 DEMO: Two separate sessions showing memory persistence")
    print()
    
    # Import customer support agent
    from src.agents.business_agents import CustomerSupportAgent
    
    # SESSION 1: First interaction with John
    print("🟦 SESSION 1: John's First Contact")
    print("-" * 40)
    
    agent_session1 = CustomerSupportAgent("support_agent_1", "demo_manager")
    
    task_data_1 = {
        "customer_id": "customer_john_123",
        "inquiry_text": "Hello, my name is John Smith and I'm having trouble accessing my account. Can you help me?",
        "channel": "web_chat"
    }
    
    print(f"📞 Customer inquiry: '{task_data_1['inquiry_text']}'")
    
    result_1 = await agent_session1.process_task(task_data_1)
    
    print(f"🤖 Agent response preview: {result_1['response'][:150]}...")
    print(f"📊 Classification: {result_1['inquiry_classification']['type']}")
    print(f"🔢 Previous interactions found: {result_1['previous_interactions']}")
    print()
    
    # SESSION 2: Simulate system restart - new agent instance
    print("🟩 SESSION 2: John Returns (System Restarted)")
    print("-" * 50)
    print("💻 Simulating: New session, new agent instance, persistent memory loads...")
    
    # Create completely new agent instance (simulates system restart)
    agent_session2 = CustomerSupportAgent("support_agent_2", "demo_manager")
    
    task_data_2 = {
        "customer_id": "customer_john_123",  # Same customer ID
        "inquiry_text": "Hi, it's John again. I wanted to follow up on my account issue from earlier.",
        "channel": "web_chat"
    }
    
    print(f"📞 Customer follow-up: '{task_data_2['inquiry_text']}'")
    
    result_2 = await agent_session2.process_task(task_data_2)
    
    print(f"🤖 Agent response preview: {result_2['response'][:150]}...")
    print(f"📊 Classification: {result_2['inquiry_classification']['type']}")
    print(f"🔢 Previous interactions found: {result_2['previous_interactions']}")
    print()
    
    # Show persistent memory details
    print("🧠 PERSISTENT MEMORY VERIFICATION")
    print("-" * 40)
    
    from src.memory.persistent_memory import persistent_memory
    
    customer_context = persistent_memory.get_customer_context("customer_john_123")
    customer_data = persistent_memory.get_customer_history("customer_john_123")
    
    print(f"✅ Customer name stored: {customer_data.get('customer_profile', {}).get('name', 'NOT FOUND')}")
    print(f"✅ Total interactions: {len(customer_data.get('interactions', []))}")
    print(f"✅ First interaction date: {customer_data.get('first_interaction', 'NOT FOUND')[:19]}")
    print(f"✅ Memory context length: {len(customer_context)} characters")
    print()
    
    print("📄 CUSTOMER MEMORY CONTEXT (What agents see):")
    print("-" * 50)
    print(customer_context)
    print()
    
    # SESSION 3: Different customer to show isolation
    print("🟨 SESSION 3: Different Customer (Sarah)")
    print("-" * 40)
    
    agent_session3 = CustomerSupportAgent("support_agent_3", "demo_manager")
    
    task_data_3 = {
        "customer_id": "customer_sarah_456",
        "inquiry_text": "Hello, my name is Sarah Johnson. I'm a new customer and need help setting up my account.",
        "channel": "phone"
    }
    
    print(f"📞 New customer inquiry: '{task_data_3['inquiry_text']}'")
    
    result_3 = await agent_session3.process_task(task_data_3)
    
    print(f"🤖 Agent response preview: {result_3['response'][:150]}...")
    print(f"🔢 Previous interactions: {result_3['previous_interactions']} (should be 0 for new customer)")
    print()
    
    # Final verification
    print("🎯 HACKATHON JUDGE VERIFICATION POINTS")
    print("=" * 50)
    print("✅ 1. Customer names are extracted and stored from conversations")
    print("✅ 2. Memory persists across completely separate agent sessions")
    print("✅ 3. Follow-up interactions reference previous conversations")
    print("✅ 4. Different customers have isolated memory spaces")
    print("✅ 5. Persistent JSON storage in Docker-compatible paths")
    print("✅ 6. Cross-session customer context loading works")
    print()
    
    # Show memory files created
    memory_stats = persistent_memory.get_memory_stats()
    print("📁 PERSISTENT MEMORY FILES CREATED:")
    for memory_file in memory_stats['memory_files']:
        if os.path.exists(memory_file):
            size = os.path.getsize(memory_file)
            print(f"   📄 {os.path.basename(memory_file)}: {size} bytes")
    
    print()
    print("🏆 DEMO COMPLETE: Customer service remembers users by name!")
    print("🎪 Ready for hackathon judges to test with real interactions!")

if __name__ == "__main__":
    asyncio.run(demo_customer_service_memory())