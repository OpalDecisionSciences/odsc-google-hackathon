"""
Advanced Memory Store System
Provides persistent memory capabilities for agents
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import asyncio
from pathlib import Path

@dataclass
class MemoryEntry:
    id: str
    agent_id: str
    memory_type: str
    content: Dict[str, Any]
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

class MemoryStore:
    """Persistent memory store for agents"""
    
    def __init__(self, storage_path: str = "memory_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # In-memory caches for performance
        self.memory_cache: Dict[str, List[MemoryEntry]] = {}
        self.load_all_memories()
    
    def _get_agent_file_path(self, agent_id: str) -> Path:
        """Get file path for agent's memory"""
        return self.storage_path / f"{agent_id}_memory.json"
    
    def load_all_memories(self):
        """Load all agent memories from disk into cache"""
        if not self.storage_path.exists():
            return
            
        for memory_file in self.storage_path.glob("*_memory.json"):
            agent_id = memory_file.stem.replace("_memory", "")
            self.memory_cache[agent_id] = self._load_agent_memories(agent_id)
    
    def _load_agent_memories(self, agent_id: str) -> List[MemoryEntry]:
        """Load memories for specific agent from disk"""
        file_path = self._get_agent_file_path(agent_id)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return [MemoryEntry.from_dict(entry) for entry in data.get('memories', [])]
        except Exception as e:
            print(f"Error loading memories for {agent_id}: {e}")
            return []
    
    def _save_agent_memories(self, agent_id: str):
        """Save agent memories to disk"""
        file_path = self._get_agent_file_path(agent_id)
        memories = self.memory_cache.get(agent_id, [])
        
        data = {
            'agent_id': agent_id,
            'last_updated': datetime.now().isoformat(), 
            'memory_count': len(memories),
            'memories': [memory.to_dict() for memory in memories]
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memories for {agent_id}: {e}")
    
    def add_memory(self, agent_id: str, memory_type: str, content: Dict[str, Any], 
                   metadata: Dict[str, Any] = None) -> str:
        """Add new memory entry for agent"""
        
        memory_id = f"{agent_id}_{memory_type}_{int(datetime.now().timestamp())}"
        
        memory_entry = MemoryEntry(
            id=memory_id,
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        if agent_id not in self.memory_cache:
            self.memory_cache[agent_id] = []
        
        self.memory_cache[agent_id].append(memory_entry)
        
        # Keep only last 1000 memories per agent to prevent unlimited growth
        if len(self.memory_cache[agent_id]) > 1000:
            self.memory_cache[agent_id] = self.memory_cache[agent_id][-1000:]
        
        # Save to disk
        self._save_agent_memories(agent_id)
        
        return memory_id
    
    def get_memories(self, agent_id: str, memory_type: str = None, 
                    limit: int = None) -> List[MemoryEntry]:
        """Get memories for agent, optionally filtered by type"""
        
        memories = self.memory_cache.get(agent_id, [])
        
        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]
        
        # Sort by timestamp (newest first)
        memories.sort(key=lambda x: x.timestamp, reverse=True)
        
        if limit:
            memories = memories[:limit]
        
        return memories
    
    def search_memories(self, agent_id: str, query: str, memory_type: str = None) -> List[MemoryEntry]:
        """Search memories by content (simple text search)"""
        memories = self.get_memories(agent_id, memory_type)
        query_lower = query.lower()
        
        matching_memories = []
        for memory in memories:
            # Search in content and metadata
            content_str = json.dumps(memory.content).lower()
            metadata_str = json.dumps(memory.metadata or {}).lower()
            
            if query_lower in content_str or query_lower in metadata_str:
                matching_memories.append(memory)
        
        return matching_memories
    
    def get_entity_history(self, agent_id: str, entity_id: str, 
                          interaction_type: str, limit: int = 10) -> List[MemoryEntry]:
        """Get recent interactions with specific entity (customer, lead, etc.)"""
        memories = self.get_memories(agent_id, interaction_type)
        
        # Filter by entity_id in content
        entity_memories = [
            m for m in memories 
            if m.content.get("entity_id") == entity_id or 
               m.content.get("customer_id") == entity_id or
               m.content.get("lead_id") == entity_id
        ]
        
        return entity_memories[:limit]

# Global memory store instance
global_memory_store = MemoryStore()

class SmartMemoryMixin:
    """Mixin to add smart memory capabilities to agents"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory_store = global_memory_store
    
    def remember(self, memory_type: str, content: Dict[str, Any], 
                metadata: Dict[str, Any] = None) -> str:
        """Add memory for this agent"""
        return self.memory_store.add_memory(
            self.agent_id, memory_type, content, metadata
        )
    
    def recall(self, memory_type: str = None, limit: int = 10) -> List[MemoryEntry]:
        """Recall memories for this agent"""
        return self.memory_store.get_memories(self.agent_id, memory_type, limit)
    
    def search_memory(self, query: str, memory_type: str = None) -> List[MemoryEntry]:
        """Search through agent's memories"""
        return self.memory_store.search_memories(self.agent_id, query, memory_type)
    
    def get_entity_history(self, entity_id: str, interaction_type: str, limit: int = 10) -> List[MemoryEntry]:
        """Get interaction history with specific entity"""
        return self.memory_store.get_entity_history(
            self.agent_id, entity_id, interaction_type, limit
        )
    
    async def process_with_memory(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with memory context"""
        # Get relevant memories based on task
        relevant_memories = await self._get_relevant_memories(task_data)
        
        # Add memory context to task
        if relevant_memories:
            task_data["memory_context"] = [
                {
                    "type": m.memory_type,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in relevant_memories[:5]  # Limit to 5 most relevant
            ]
        
        # Process the task
        result = await self.process_task(task_data)
        
        # Remember this interaction
        await self._remember_interaction(task_data, result)
        
        return result
    
    async def _get_relevant_memories(self, task_data: Dict[str, Any]) -> List[MemoryEntry]:
        """Get memories relevant to current task"""
        # Check for entity-specific memories (customer, lead, etc.)
        entity_id = (task_data.get("customer_id") or 
                    task_data.get("lead_id") or 
                    task_data.get("entity_id"))
        
        relevant_memories = []
        
        if entity_id:
            # Get previous interactions with this entity
            entity_memories = self.get_entity_history(entity_id, "interaction", 5)
            relevant_memories.extend(entity_memories)
        
        # Get recent general memories
        recent_memories = self.recall(limit=3)
        relevant_memories.extend(recent_memories)
        
        # Remove duplicates
        seen_ids = set()
        unique_memories = []
        for memory in relevant_memories:
            if memory.id not in seen_ids:
                unique_memories.append(memory)
                seen_ids.add(memory.id)
        
        return unique_memories[:5]  # Return top 5
    
    async def _remember_interaction(self, task_data: Dict[str, Any], result: Dict[str, Any]):
        """Remember this interaction for future reference"""
        # Extract entity ID for tracking
        entity_id = (task_data.get("customer_id") or 
                    task_data.get("lead_id") or 
                    task_data.get("entity_id"))
        
        memory_content = {
            "task_type": task_data.get("type", "unknown"),
            "entity_id": entity_id,
            "customer_id": task_data.get("customer_id"),
            "lead_id": task_data.get("lead_id"),
            "task_summary": str(task_data)[:200],  # Truncated summary
            "result_summary": str(result)[:200],   # Truncated summary
            "success": result.get("status") != "error"
        }
        
        metadata = {
            "task_category": task_data.get("type", "unknown"),
            "entity_type": "customer" if task_data.get("customer_id") else "lead" if task_data.get("lead_id") else "unknown"
        }
        
        self.remember("interaction", memory_content, metadata)