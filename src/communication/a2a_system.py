"""
Agent-to-Agent (A2A) Communication System
Advanced messaging, coordination, and workflow orchestration
"""

from typing import Dict, Any, List, Optional, Callable, Set
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
from collections import defaultdict, deque

from ..core.base_agent import BaseAgent, AgentMessage, MessageType

class MessagePriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RoutingStrategy(Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    ROUND_ROBIN = "round_robin"
    LOAD_BALANCED = "load_balanced"
    SKILL_BASED = "skill_based"

@dataclass
class MessageRoute:
    sender_id: str
    recipient_id: str
    message_id: str
    route_hops: List[str] = field(default_factory=list)
    delivery_timestamp: Optional[datetime] = None
    delivery_status: str = "pending"  # pending, delivered, failed

@dataclass
class CommunicationMetrics:
    messages_sent: int = 0
    messages_delivered: int = 0
    messages_failed: int = 0
    average_delivery_time: float = 0.0
    active_connections: int = 0
    throughput_per_second: float = 0.0

class MessageBroker:
    """Central message broker for A2A communication"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.routing_table: Dict[str, List[str]] = defaultdict(list)
        self.message_history: deque = deque(maxlen=10000)
        self.active_routes: Dict[str, MessageRoute] = {}
        self.metrics = CommunicationMetrics()
        
        # Message delivery tracking
        self.delivery_confirmations: Dict[str, bool] = {}
        self.retry_queues: Dict[str, List[AgentMessage]] = defaultdict(list)
        
        # Load balancing
        self.agent_loads: Dict[str, int] = defaultdict(int)
        self.skill_registry: Dict[str, Set[str]] = defaultdict(set)
        
        self.is_running = False
        self.broker_tasks: List[asyncio.Task] = []
    
    async def start(self):
        """Start the message broker"""
        self.is_running = True
        
        # Start broker tasks
        self.broker_tasks = [
            asyncio.create_task(self._message_processor()),
            asyncio.create_task(self._retry_processor()),
            asyncio.create_task(self._metrics_updater()),
            asyncio.create_task(self._health_monitor())
        ]
        
        logging.info("A2A Message Broker started")
    
    async def stop(self):
        """Stop the message broker"""
        self.is_running = False
        
        # Cancel all broker tasks
        for task in self.broker_tasks:
            task.cancel()
        
        await asyncio.gather(*self.broker_tasks, return_exceptions=True)
        logging.info("A2A Message Broker stopped")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the broker"""
        self.agents[agent.agent_id] = agent
        self.message_queues[agent.agent_id] = asyncio.Queue()
        self.agent_loads[agent.agent_id] = 0
        
        # Register agent capabilities/skills
        capabilities = agent.get_capabilities()
        self.skill_registry[agent.agent_id].update(capabilities)
        
        self.metrics.active_connections += 1
        logging.info(f"Agent {agent.name} registered with broker")
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the broker"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.message_queues[agent_id]
            del self.agent_loads[agent_id]
            del self.skill_registry[agent_id]
            
            self.metrics.active_connections -= 1
            logging.info(f"Agent {agent_id} unregistered from broker")
    
    async def send_message(self, 
                          sender_id: str, 
                          recipient_id: str, 
                          message_type: MessageType,
                          content: Dict[str, Any],
                          priority: MessagePriority = MessagePriority.MEDIUM,
                          routing_strategy: RoutingStrategy = RoutingStrategy.DIRECT) -> str:
        """Send message between agents"""
        
        message = AgentMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            priority=priority.name.lower()
        )
        
        # Create routing record
        route = MessageRoute(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_id=message.id
        )
        self.active_routes[message.id] = route
        
        # Route message based on strategy
        success = await self._route_message(message, routing_strategy)
        
        if success:
            self.metrics.messages_sent += 1
            route.delivery_status = "sent"
        else:
            route.delivery_status = "failed"
            self.metrics.messages_failed += 1
        
        # Store in history
        self.message_history.append({
            "message_id": message.id,
            "sender": sender_id,
            "recipient": recipient_id,
            "timestamp": datetime.now().isoformat(),
            "success": success
        })
        
        return message.id
    
    async def _route_message(self, message: AgentMessage, strategy: RoutingStrategy) -> bool:
        """Route message based on routing strategy"""
        
        if strategy == RoutingStrategy.DIRECT:
            return await self._route_direct(message)
        elif strategy == RoutingStrategy.BROADCAST:
            return await self._route_broadcast(message)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            return await self._route_round_robin(message)
        elif strategy == RoutingStrategy.LOAD_BALANCED:
            return await self._route_load_balanced(message)
        elif strategy == RoutingStrategy.SKILL_BASED:
            return await self._route_skill_based(message)
        else:
            return await self._route_direct(message)
    
    async def _route_direct(self, message: AgentMessage) -> bool:
        """Direct routing to specific agent"""
        recipient_id = message.recipient_id
        
        if recipient_id not in self.message_queues:
            logging.error(f"Recipient {recipient_id} not found")
            return False
        
        try:
            await self.message_queues[recipient_id].put(message)
            self.agent_loads[recipient_id] += 1
            return True
        except Exception as e:
            logging.error(f"Failed to route message to {recipient_id}: {e}")
            return False
    
    async def _route_broadcast(self, message: AgentMessage) -> bool:
        """Broadcast message to all agents in department/category"""
        # Parse recipient as department or category
        department = message.recipient_id
        target_agents = []
        
        for agent_id, agent in self.agents.items():
            if agent.department == department or department == "all":
                target_agents.append(agent_id)
        
        success_count = 0
        for agent_id in target_agents:
            try:
                broadcast_message = AgentMessage(
                    id=f"{message.id}_{agent_id}",
                    sender_id=message.sender_id,
                    recipient_id=agent_id,
                    message_type=message.message_type,
                    content=message.content,
                    priority=message.priority
                )
                await self.message_queues[agent_id].put(broadcast_message)
                success_count += 1
            except Exception as e:
                logging.error(f"Failed to broadcast to {agent_id}: {e}")
        
        return success_count > 0
    
    async def _route_round_robin(self, message: AgentMessage) -> bool:
        """Round-robin routing among available agents"""
        # Get agents in target department
        department = message.recipient_id
        available_agents = [
            agent_id for agent_id, agent in self.agents.items()
            if agent.department == department
        ]
        
        if not available_agents:
            return False
        
        # Simple round-robin selection
        selected_agent = available_agents[self.metrics.messages_sent % len(available_agents)]
        message.recipient_id = selected_agent
        
        return await self._route_direct(message)
    
    async def _route_load_balanced(self, message: AgentMessage) -> bool:
        """Load-balanced routing to least loaded agent"""
        department = message.recipient_id
        available_agents = [
            agent_id for agent_id, agent in self.agents.items()
            if agent.department == department
        ]
        
        if not available_agents:
            return False
        
        # Select agent with lowest load
        selected_agent = min(available_agents, key=lambda aid: self.agent_loads[aid])
        message.recipient_id = selected_agent
        
        return await self._route_direct(message)
    
    async def _route_skill_based(self, message: AgentMessage) -> bool:
        """Route based on required skills/capabilities"""
        required_skills = message.content.get("required_skills", [])
        
        if not required_skills:
            return await self._route_direct(message)
        
        # Find agents with matching skills
        matching_agents = []
        for agent_id, skills in self.skill_registry.items():
            if any(skill in skills for skill in required_skills):
                matching_agents.append(agent_id)
        
        if not matching_agents:
            return False
        
        # Select best matching agent (most skills in common)
        best_agent = max(
            matching_agents,
            key=lambda aid: len(set(required_skills) & self.skill_registry[aid])
        )
        
        message.recipient_id = best_agent
        return await self._route_direct(message)
    
    async def _message_processor(self):
        """Process messages from queues to agents"""
        while self.is_running:
            try:
                # Process messages for each agent
                for agent_id, queue in self.message_queues.items():
                    if not queue.empty() and agent_id in self.agents:
                        try:
                            message = await asyncio.wait_for(queue.get(), timeout=0.1)
                            agent = self.agents[agent_id]
                            
                            # Deliver message to agent
                            await self._deliver_to_agent(agent, message)
                            
                            # Update metrics
                            self.metrics.messages_delivered += 1
                            self.agent_loads[agent_id] = max(0, self.agent_loads[agent_id] - 1)
                            
                            # Update route status
                            if message.id in self.active_routes:
                                route = self.active_routes[message.id]
                                route.delivery_timestamp = datetime.now()
                                route.delivery_status = "delivered"
                            
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            logging.error(f"Error processing message for {agent_id}: {e}")
                            self.metrics.messages_failed += 1
                
                await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logging.error(f"Error in message processor: {e}")
                await asyncio.sleep(0.1)
    
    async def _deliver_to_agent(self, agent: BaseAgent, message: AgentMessage):
        """Deliver message to specific agent"""
        try:
            # Put message in agent's message queue
            await agent.message_queue.put(message)
        except Exception as e:
            # Add to retry queue if delivery fails
            self.retry_queues[agent.agent_id].append(message)
            raise e
    
    async def _retry_processor(self):
        """Process failed message retries"""
        while self.is_running:
            try:
                for agent_id, retry_queue in self.retry_queues.items():
                    if retry_queue and agent_id in self.agents:
                        message = retry_queue.pop(0)
                        try:
                            agent = self.agents[agent_id]
                            await self._deliver_to_agent(agent, message)
                            logging.info(f"Retry successful for message {message.id}")
                        except Exception as e:
                            # Re-add to retry queue with limit
                            if len(retry_queue) < 100:  # Limit retry queue size
                                retry_queue.append(message)
                            logging.error(f"Retry failed for {agent_id}: {e}")
                
                await asyncio.sleep(1)  # Retry every second
                
            except Exception as e:
                logging.error(f"Error in retry processor: {e}")
                await asyncio.sleep(1)
    
    async def _metrics_updater(self):
        """Update communication metrics"""
        last_message_count = 0
        
        while self.is_running:
            try:
                # Calculate throughput
                current_messages = self.metrics.messages_delivered
                messages_per_second = (current_messages - last_message_count) / 10.0  # 10 second interval
                self.metrics.throughput_per_second = messages_per_second
                last_message_count = current_messages
                
                # Calculate average delivery time
                delivered_routes = [
                    route for route in self.active_routes.values()
                    if route.delivery_status == "delivered" and route.delivery_timestamp
                ]
                
                if delivered_routes:
                    delivery_times = [
                        (route.delivery_timestamp - datetime.fromisoformat(route.delivery_timestamp.isoformat())).total_seconds()
                        for route in delivered_routes[-100:]  # Last 100 deliveries
                    ]
                    self.metrics.average_delivery_time = sum(delivery_times) / len(delivery_times)
                
                await asyncio.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                logging.error(f"Error updating metrics: {e}")
                await asyncio.sleep(10)
    
    async def _health_monitor(self):
        """Monitor broker health and performance"""
        while self.is_running:
            try:
                # Check for stuck messages
                stuck_routes = [
                    route for route in self.active_routes.values()
                    if (route.delivery_status == "pending" and 
                        datetime.now() - datetime.fromisoformat(route.message_id.split('_')[0]) > timedelta(minutes=5))
                ]
                
                if stuck_routes:
                    logging.warning(f"Found {len(stuck_routes)} stuck messages")
                
                # Check agent health
                unresponsive_agents = []
                for agent_id, load in self.agent_loads.items():
                    if load > 1000:  # High load threshold
                        unresponsive_agents.append(agent_id)
                
                if unresponsive_agents:
                    logging.warning(f"High load agents: {unresponsive_agents}")
                
                # Clean up old routes
                cutoff_time = datetime.now() - timedelta(hours=1)
                old_routes = [
                    route_id for route_id, route in self.active_routes.items()
                    if (route.delivery_timestamp and route.delivery_timestamp < cutoff_time)
                ]
                
                for route_id in old_routes:
                    del self.active_routes[route_id]
                
                await asyncio.sleep(60)  # Health check every minute
                
            except Exception as e:
                logging.error(f"Error in health monitor: {e}")
                await asyncio.sleep(60)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current communication metrics"""
        return {
            "messages_sent": self.metrics.messages_sent,
            "messages_delivered": self.metrics.messages_delivered,
            "messages_failed": self.metrics.messages_failed,
            "success_rate": (
                self.metrics.messages_delivered / max(1, self.metrics.messages_sent) * 100
            ),
            "average_delivery_time": self.metrics.average_delivery_time,
            "active_connections": self.metrics.active_connections,
            "throughput_per_second": self.metrics.throughput_per_second,
            "active_routes": len(self.active_routes),
            "pending_retries": sum(len(queue) for queue in self.retry_queues.values())
        }
    
    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered agents"""
        return {
            agent_id: {
                "name": agent.name,
                "department": agent.department,
                "current_load": self.agent_loads[agent_id],
                "queue_size": self.message_queues[agent_id].qsize(),
                "capabilities": list(self.skill_registry[agent_id]),
                "is_active": agent.is_active
            }
            for agent_id, agent in self.agents.items()
        }

class WorkflowOrchestrator:
    """Orchestrates complex multi-agent workflows"""
    
    def __init__(self, message_broker: MessageBroker):
        self.broker = message_broker
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.workflow_templates: Dict[str, Callable] = {}
    
    def register_workflow_template(self, name: str, workflow_func: Callable):
        """Register a workflow template"""
        self.workflow_templates[name] = workflow_func
    
    async def execute_workflow(self, 
                              workflow_name: str, 
                              workflow_data: Dict[str, Any],
                              participating_agents: List[str]) -> str:
        """Execute a complex workflow"""
        workflow_id = str(uuid.uuid4())
        
        workflow_instance = {
            "id": workflow_id,
            "name": workflow_name,
            "data": workflow_data,
            "agents": participating_agents,
            "status": "running",
            "start_time": datetime.now(),
            "steps_completed": [],
            "current_step": 0
        }
        
        self.active_workflows[workflow_id] = workflow_instance
        
        try:
            if workflow_name in self.workflow_templates:
                # Execute custom workflow template
                result = await self.workflow_templates[workflow_name](
                    workflow_data, participating_agents, self.broker
                )
            else:
                # Execute default workflow
                result = await self._execute_default_workflow(workflow_instance)
            
            workflow_instance["status"] = "completed"
            workflow_instance["result"] = result
            workflow_instance["end_time"] = datetime.now()
            
        except Exception as e:
            workflow_instance["status"] = "failed"
            workflow_instance["error"] = str(e)
            workflow_instance["end_time"] = datetime.now()
            logging.error(f"Workflow {workflow_id} failed: {e}")
        
        return workflow_id
    
    async def _execute_default_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute default sequential workflow"""
        results = []
        
        for i, agent_id in enumerate(workflow["agents"]):
            step_data = workflow["data"].copy()
            step_data["workflow_step"] = i + 1
            step_data["previous_results"] = results
            
            # Send task to agent
            message_id = await self.broker.send_message(
                sender_id="workflow_orchestrator",
                recipient_id=agent_id,
                message_type=MessageType.TASK_REQUEST,
                content=step_data,
                priority=MessagePriority.HIGH
            )
            
            # Wait for response (simplified - in real implementation would use proper response handling)
            await asyncio.sleep(2)  # Simulate processing time
            
            # Record step completion
            workflow["steps_completed"].append({
                "step": i + 1,
                "agent_id": agent_id,
                "message_id": message_id,
                "timestamp": datetime.now().isoformat()
            })
            
            results.append(f"Step {i+1} completed by {agent_id}")
        
        return {
            "workflow_id": workflow["id"],
            "steps_completed": len(workflow["steps_completed"]),
            "results": results
        }
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of specific workflow"""
        return self.active_workflows.get(workflow_id)
    
    def get_all_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all workflows"""
        return self.active_workflows.copy()

# Global broker instance
global_message_broker = MessageBroker()
global_workflow_orchestrator = WorkflowOrchestrator(global_message_broker)