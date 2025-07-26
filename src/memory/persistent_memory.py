"""
Persistent Memory System for AI Agent Orchestration
Enables cross-session memory persistence using JSON storage
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging

class PersistentMemoryManager:
    """Manages persistent memory across agent sessions using JSON storage"""
    
    def __init__(self, memory_dir: str = None):
        # Docker-compatible path setup
        if memory_dir is None:
            # Use relative path from project root in Docker
            project_root = Path(__file__).parent.parent.parent
            memory_dir = project_root / "memory_data"
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        
        # Memory file paths
        self.customer_memory_file = self.memory_dir / "customer_interactions.json"
        self.swot_intelligence_file = self.memory_dir / "swot_intelligence.json"
        self.agent_interactions_file = self.memory_dir / "agent_interactions.json"
        self.business_context_file = self.memory_dir / "business_contexts.json"
        
        self.logger = logging.getLogger(__name__)
        
        # Load existing memory on initialization
        self._load_all_memory()
    
    def _load_all_memory(self):
        """Load all persistent memory files"""
        self.customer_memory = self._load_json_file(self.customer_memory_file, {})
        self.swot_intelligence = self._load_json_file(self.swot_intelligence_file, {})
        self.agent_interactions = self._load_json_file(self.agent_interactions_file, {})
        self.business_contexts = self._load_json_file(self.business_context_file, {})
        
        print(f"✅ Persistent memory loaded: {len(self.customer_memory)} customers, {len(self.swot_intelligence)} SWOT analyses")
    
    def _load_json_file(self, file_path: Path, default: Any) -> Any:
        """Load JSON file with error handling"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Error loading {file_path}: {e}")
        return default
    
    def _save_json_file(self, file_path: Path, data: Any):
        """Save data to JSON file with error handling"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error saving {file_path}: {e}")
    
    # Customer Memory Management
    def store_customer_interaction(self, customer_id: str, interaction_data: Dict[str, Any]):
        """Store customer interaction with timestamp"""
        timestamp = datetime.now().isoformat()
        
        if customer_id not in self.customer_memory:
            self.customer_memory[customer_id] = {
                "customer_id": customer_id,
                "first_interaction": timestamp,
                "interactions": [],
                "preferences": {},
                "satisfaction_scores": [],
                "escalation_history": [],
                "customer_profile": {}
            }
        
        # Store interaction
        interaction_record = {
            "timestamp": timestamp,
            "inquiry_type": interaction_data.get("inquiry_classification", {}).get("type", "general"),
            "inquiry_text": interaction_data.get("inquiry_text", ""),
            "response": interaction_data.get("response", ""),
            "satisfaction_score": interaction_data.get("satisfaction_tracking", {}).get("current_score"),
            "escalated": interaction_data.get("needs_escalation", False),
            "resolution_status": interaction_data.get("resolution_status", "pending"),
            "channel": interaction_data.get("channel", "unknown")
        }
        
        self.customer_memory[customer_id]["interactions"].append(interaction_record)
        
        # Update customer profile
        if "customer_name" in interaction_data:
            self.customer_memory[customer_id]["customer_profile"]["name"] = interaction_data["customer_name"]
        
        # Track satisfaction scores
        if interaction_record["satisfaction_score"]:
            self.customer_memory[customer_id]["satisfaction_scores"].append({
                "score": interaction_record["satisfaction_score"],
                "timestamp": timestamp
            })
        
        # Track escalations
        if interaction_record["escalated"]:
            self.customer_memory[customer_id]["escalation_history"].append({
                "reason": interaction_data.get("escalation_reason", "Complex inquiry"),
                "timestamp": timestamp
            })
        
        self._save_json_file(self.customer_memory_file, self.customer_memory)
        print(f"💾 Customer memory saved: {customer_id}")
    
    def get_customer_history(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve complete customer history"""
        return self.customer_memory.get(customer_id, {})
    
    def get_customer_context(self, customer_id: str) -> str:
        """Get formatted customer context for agent prompts"""
        customer_data = self.get_customer_history(customer_id)
        
        if not customer_data:
            return f"New customer (ID: {customer_id}) - no previous interaction history."
        
        # Calculate metrics
        total_interactions = len(customer_data.get("interactions", []))
        avg_satisfaction = None
        if customer_data.get("satisfaction_scores"):
            scores = [s["score"] for s in customer_data["satisfaction_scores"] if s["score"]]
            avg_satisfaction = sum(scores) / len(scores) if scores else None
        
        escalation_count = len(customer_data.get("escalation_history", []))
        
        # Get customer name if available
        customer_name = customer_data.get("customer_profile", {}).get("name", "Unknown")
        
        # Recent interactions
        recent_interactions = customer_data.get("interactions", [])[-3:]  # Last 3
        
        satisfaction_text = f"{avg_satisfaction:.1f}/5.0" if avg_satisfaction else "No ratings"
        
        context = f"""
**CUSTOMER MEMORY CONTEXT for {customer_id}:**
Customer Name: {customer_name}
First Interaction: {customer_data.get('first_interaction', 'Unknown')}
Total Interactions: {total_interactions}
Average Satisfaction: {satisfaction_text}
Escalations: {escalation_count}

**Recent Interaction History:**
"""
        
        for interaction in recent_interactions:
            context += f"- {interaction['timestamp'][:10]}: {interaction['inquiry_type']} - {interaction['inquiry_text'][:100]}...\n"
        
        if customer_data.get("preferences"):
            context += f"\n**Customer Preferences:** {customer_data['preferences']}"
        
        return context.strip()
    
    # SWOT Intelligence Persistence
    def store_swot_intelligence(self, company_name: str, analysis_data: Dict[str, Any]):
        """Store SWOT-TOWS analysis results"""
        self.swot_intelligence[company_name] = {
            **analysis_data,
            "last_updated": datetime.now().isoformat()
        }
        self._save_json_file(self.swot_intelligence_file, self.swot_intelligence)
        print(f"💾 SWOT intelligence saved: {company_name}")
    
    def get_swot_intelligence(self, company_name: str) -> Dict[str, Any]:
        """Retrieve SWOT intelligence for company"""
        return self.swot_intelligence.get(company_name, {})
    
    def has_swot_intelligence(self, company_name: str) -> bool:
        """Check if SWOT intelligence exists for company"""
        return company_name in self.swot_intelligence
    
    # Business Context Persistence  
    def store_business_context(self, company_name: str, context_data: Dict[str, Any]):
        """Store business research context"""
        self.business_contexts[company_name] = {
            **context_data,
            "last_updated": datetime.now().isoformat()
        }
        self._save_json_file(self.business_context_file, self.business_contexts)
        print(f"💾 Business context saved: {company_name}")
    
    def get_business_context(self, company_name: str) -> Dict[str, Any]:
        """Retrieve business context for company"""
        return self.business_contexts.get(company_name, {})
    
    # Agent Interaction Tracking
    def store_agent_interaction(self, agent_name: str, interaction_data: Dict[str, Any]):
        """Store agent interaction for cross-session learning"""
        timestamp = datetime.now().isoformat()
        
        if agent_name not in self.agent_interactions:
            self.agent_interactions[agent_name] = {
                "agent_name": agent_name,
                "first_interaction": timestamp,
                "interactions": [],
                "performance_metrics": {},
                "learning_patterns": {}
            }
        
        interaction_record = {
            "timestamp": timestamp,
            "task_type": interaction_data.get("task_type", "unknown"),
            "input_data": interaction_data.get("input_summary", ""),
            "success": interaction_data.get("success", True),
            "processing_time": interaction_data.get("processing_time", 0),
            "output_summary": interaction_data.get("output_summary", "")
        }
        
        self.agent_interactions[agent_name]["interactions"].append(interaction_record)
        self._save_json_file(self.agent_interactions_file, self.agent_interactions)
    
    def get_agent_history(self, agent_name: str) -> Dict[str, Any]:
        """Get agent interaction history"""
        return self.agent_interactions.get(agent_name, {})
    
    # Memory Cleanup and Maintenance
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Remove data older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_iso = cutoff_date.isoformat()
        
        # Clean customer interactions
        for customer_id, data in self.customer_memory.items():
            if "interactions" in data:
                data["interactions"] = [
                    interaction for interaction in data["interactions"]
                    if interaction.get("timestamp", "") > cutoff_iso
                ]
        
        # Clean agent interactions
        for agent_name, data in self.agent_interactions.items():
            if "interactions" in data:
                data["interactions"] = [
                    interaction for interaction in data["interactions"]
                    if interaction.get("timestamp", "") > cutoff_iso
                ]
        
        # Save cleaned data
        self._save_json_file(self.customer_memory_file, self.customer_memory)
        self._save_json_file(self.agent_interactions_file, self.agent_interactions)
        
        print(f"🧹 Memory cleanup completed: data older than {days_to_keep} days removed")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        return {
            "customers_tracked": len(self.customer_memory),
            "total_customer_interactions": sum(len(data.get("interactions", [])) for data in self.customer_memory.values()),
            "companies_analyzed": len(self.swot_intelligence),
            "business_contexts": len(self.business_contexts),
            "agents_tracked": len(self.agent_interactions),
            "memory_files": [
                str(self.customer_memory_file),
                str(self.swot_intelligence_file),
                str(self.agent_interactions_file),
                str(self.business_context_file)
            ]
        }
    
    def export_customer_data(self, customer_id: str) -> str:
        """Export customer data for analysis (GDPR compliance)"""
        customer_data = self.get_customer_history(customer_id)
        if customer_data:
            export_path = self.memory_dir / f"customer_export_{customer_id}_{datetime.now().strftime('%Y%m%d')}.json"
            self._save_json_file(export_path, customer_data)
            return str(export_path)
        return ""

# Global persistent memory manager instance
persistent_memory = PersistentMemoryManager()