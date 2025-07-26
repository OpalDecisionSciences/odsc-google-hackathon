"""
Base Agent Framework for Google ADK/A2A Implementation
Hierarchical Business AI Agent System for Startup Success
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
import asyncio
from datetime import datetime
import json
import google.generativeai as genai
import os

class AgentRole(Enum):
    EXECUTIVE = "executive"
    MANAGER = "manager" 
    SPECIALIST = "specialist"
    ANALYST = "analyst"

class MessageType(Enum):
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    COORDINATION = "coordination"
    ESCALATION = "escalation"
    STATUS_UPDATE = "status_update"
    ANALYSIS_REQUEST = "analysis_request"

@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_id: str = ""
    message_type: MessageType = MessageType.TASK_REQUEST
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: str = "medium"
    requires_response: bool = True

@dataclass
class AgentMetrics:
    tasks_completed: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    escalation_rate: float = 0.0
    customer_satisfaction: float = 0.0

class BaseAgent(ABC):
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 role: AgentRole,
                 department: str,
                 specialization: str,
                 manager_id: Optional[str] = None):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.department = department
        self.specialization = specialization
        self.manager_id = manager_id
        
        # Communication system
        self.message_queue = asyncio.Queue()
        self.subscribers = set()
        self.message_handlers: Dict[MessageType, Callable] = {}
        
        # Performance tracking
        self.metrics = AgentMetrics()
        self.is_active = True
        self.current_tasks = []
        
        # Gemini integration
        self.gemini_model = None
        self._initialize_gemini()
        
        # Register default message handlers
        self._register_handlers()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI model for this agent"""
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            print(f"Failed to initialize Gemini for {self.name}: {e}")
    
    def _register_handlers(self):
        """Register default message handlers"""
        self.message_handlers[MessageType.TASK_REQUEST] = self.handle_task_request
        self.message_handlers[MessageType.COORDINATION] = self.handle_coordination
        self.message_handlers[MessageType.ESCALATION] = self.handle_escalation
        self.message_handlers[MessageType.STATUS_UPDATE] = self.handle_status_update
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific task - must be implemented by each agent"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    async def send_message(self, recipient_id: str, message_type: MessageType, 
                          content: Dict[str, Any], priority: str = "medium") -> str:
        """Send message to another agent via A2A communication"""
        message = AgentMessage(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            priority=priority
        )
        
        # In real implementation, this would go through A2A system
        # For now, simulate with direct delivery
        await self._deliver_message(message)
        return message.id
    
    async def _deliver_message(self, message: AgentMessage):
        """Simulate message delivery - replace with actual A2A implementation"""
        # This would be handled by the A2A communication system
        await self.message_queue.put(message)
    
    async def listen_for_messages(self):
        """Listen for incoming messages and process them"""
        while self.is_active:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._process_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing message in {self.name}: {e}")
    
    async def _process_message(self, message: AgentMessage):
        """Process incoming message based on type"""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                print(f"Error in message handler for {self.name}: {e}")
                if message.requires_response:
                    await self._send_error_response(message, str(e))
    
    async def handle_task_request(self, message: AgentMessage):
        """Handle incoming task request"""
        try:
            result = await self.process_task(message.content)
            
            if message.requires_response:
                await self.send_message(
                    message.sender_id,
                    MessageType.TASK_RESPONSE,
                    {"result": result, "status": "completed"},
                    message.priority
                )
            
            self.metrics.tasks_completed += 1
        except Exception as e:
            await self._send_error_response(message, str(e))
    
    async def handle_coordination(self, message: AgentMessage):
        """Handle coordination messages from other agents"""
        coordination_type = message.content.get("type")
        
        if coordination_type == "status_check":
            await self.send_message(
                message.sender_id,
                MessageType.STATUS_UPDATE,
                {
                    "status": "active" if self.is_active else "inactive",
                    "current_tasks": len(self.current_tasks),
                    "metrics": self.metrics.__dict__
                }
            )
    
    async def handle_escalation(self, message: AgentMessage):
        """Handle escalations - forward to manager if available"""
        if self.manager_id:
            await self.send_message(
                self.manager_id,
                MessageType.ESCALATION,
                {
                    "original_sender": message.sender_id,
                    "escalation_reason": message.content.get("reason"),
                    "original_content": message.content
                },
                priority="high"
            )
        else:
            print(f"No manager available for escalation from {self.name}")
    
    async def handle_status_update(self, message: AgentMessage):
        """Handle status updates from other agents"""
        # Log status update for monitoring
        print(f"{self.name} received status update from {message.sender_id}")
    
    async def _send_error_response(self, original_message: AgentMessage, error: str):
        """Send error response back to sender"""
        await self.send_message(
            original_message.sender_id,
            MessageType.TASK_RESPONSE,
            {
                "status": "error",
                "error": error,
                "original_task": original_message.content
            },
            priority="high"
        )
    
    async def use_gemini(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Use Gemini AI for intelligent processing with conversation context"""
        if not self.gemini_model:
            return "Gemini AI not available"
        
        try:
            # Get conversation context if available (for agents with memory)
            conversation_context = ""
            if hasattr(self, 'recall'):
                recent_conversations = self.recall("conversation", limit=3)
                if recent_conversations:
                    conv_summary = []
                    for conv in recent_conversations:
                        conv_data = conv.content
                        conv_summary.append(f"- Previous: {conv_data.get('summary', 'N/A')[:100]}")
                    conversation_context = f"\n\nRecent Conversations:\n" + "\n".join(conv_summary)
            
            # Enhance prompt with agent context
            enhanced_prompt = f"""
            You are {self.name}, a {self.role.value} in the {self.department} department.
            Your specialization is: {self.specialization}
            
            Context: {json.dumps(context) if context else 'None'}
            {conversation_context}
            
            Task: {prompt}
            
            Please provide a professional response that aligns with your role and expertise.
            If conversation history is available, maintain continuity and reference relevant past interactions.
            """
            
            response = await asyncio.to_thread(
                self.gemini_model.generate_content, enhanced_prompt
            )
            
            # Remember this conversation if agent has memory
            if hasattr(self, 'remember'):
                self.remember("conversation", {
                    "prompt": prompt[:200],  # Truncated
                    "response": response.text[:200],  # Truncated
                    "summary": f"Discussed {prompt[:50]}...",
                    "context_provided": context is not None,
                    "conversation_length": len(response.text)
                }, {"interaction_type": "ai_conversation"})
            
            return response.text
        except Exception as e:
            return f"Gemini processing error: {e}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "department": self.department,
            "is_active": self.is_active,
            "current_tasks": len(self.current_tasks),
            "metrics": self.metrics.__dict__,
            "capabilities": self.get_capabilities()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        self.is_active = False
        print(f"Agent {self.name} shutting down...")

class ManagerAgent(BaseAgent):
    """Base class for manager agents with team oversight capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_members: List[str] = []
        self.delegation_rules: Dict[str, List[str]] = {}
    
    def add_team_member(self, agent_id: str):
        """Add agent to this manager's team"""
        if agent_id not in self.team_members:
            self.team_members.append(agent_id)
    
    async def delegate_task(self, task_data: Dict[str, Any], preferred_agent: str = None) -> str:
        """Delegate task to appropriate team member"""
        if not self.team_members:
            raise Exception("No team members available for delegation")
        
        # Simple delegation logic - enhance with more sophisticated routing
        target_agent = preferred_agent if preferred_agent in self.team_members else self.team_members[0]
        
        message_id = await self.send_message(
            target_agent,
            MessageType.TASK_REQUEST,
            task_data,
            priority=task_data.get("priority", "medium")
        )
        
        return message_id
    
    async def get_team_status(self) -> Dict[str, Any]:
        """Get status of all team members"""
        team_status = {}
        for member_id in self.team_members:
            await self.send_message(
                member_id,
                MessageType.COORDINATION,
                {"type": "status_check"}
            )
        return team_status
    
    def get_capabilities(self) -> List[str]:
        return [
            "team_management",
            "task_delegation", 
            "performance_monitoring",
            "strategic_coordination",
            "escalation_handling"
        ]