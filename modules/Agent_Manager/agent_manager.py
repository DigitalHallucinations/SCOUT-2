# modules/agent_manager.py

import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from modules.logging.logger import setup_logger

logger = setup_logger('agent_manager.py')

class Task:
    def __init__(self, task_id: int, user_id: str, content: str, metadata: Dict[str, Any] = None):
        self.task_id = task_id
        self.user_id = user_id
        self.content = content
        self.status = "created"
        self.metadata = metadata or {}

class Agent(ABC):
    @abstractmethod
    async def execute_task(self, task: Task, provider: Any) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        pass

    @abstractmethod
    def can_handle_task(self, task: Task) -> bool:
        pass

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def register(self, agent: Agent):
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def unregister(self, agent_name: str):
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Unregistered agent: {agent_name}")
        else:
            logger.warning(f"Attempted to unregister non-existent agent: {agent_name}")

    def get_agent(self, agent_name: str) -> Optional[Agent]:
        agent = self.agents.get(agent_name)
        if not agent:
            logger.warning(f"Attempted to retrieve non-existent agent: {agent_name}")
        return agent

    def get_all_agents(self) -> List[Agent]:
        return list(self.agents.values())

class AgentSelector:
    def __init__(self, agent_registry: AgentRegistry):
        self.agent_registry = agent_registry

    def select_agent(self, task: Task) -> Agent:
        agents = self.agent_registry.get_all_agents()
        logger.debug(f"Available agents: {[agent.name for agent in agents]}")
        
        if not agents:
            logger.error("No agents available for selection")
            raise ValueError("No agents available for selection")
        
        capable_agents = [agent for agent in agents if agent.can_handle_task(task)]
        logger.debug(f"Capable agents for task: {[agent.name for agent in capable_agents]}")
        
        if not capable_agents:
            logger.error(f"No capable agents found for task: {task.content}")
            raise ValueError(f"No capable agents found for task: {task.content}")

        selected_agent = max(capable_agents, key=lambda a: self._capability_score(a, task))
        logger.info(f"Selected agent {selected_agent.name} for task {task.task_id}")
        return selected_agent

    def _capability_score(self, agent: Agent, task: Task) -> float:
        task_keywords = set(task.content.lower().split())
        agent_capabilities = set(cap.lower() for cap in agent.capabilities)
        return len(task_keywords.intersection(agent_capabilities))

class TaskQueue:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()

    async def add_task(self, task: Task, agent: Agent, priority: int = 0):
        await self.queue.put((priority, task, agent))
        logger.info(f"Added task {task.task_id} to queue with priority {priority}")

    async def get_task(self) -> Optional[tuple]:
        if self.queue.empty():
            return None
        return await self.queue.get()

class ResultHandler:
    def __init__(self):
        self.scouts: Dict[str, Any] = {}

    def register_scout(self, scout_id: str, scout_instance: Any):
        self.scouts[scout_id] = scout_instance
        logger.info(f"Registered SCOUT instance: {scout_id}")

    async def handle_result(self, task: Task, result: str):
        scout = self.scouts.get(task.user_id)
        if scout:
            await scout.handle_task_result(task.user_id, result)
            logger.info(f"Handled result for task {task.task_id}")
        else:
            logger.warning(f"No SCOUT instance found for user {task.user_id}")

class AgentManager:
    def __init__(self, cognitive_services: Any, provider_manager: Any):
        self.cognitive_services = cognitive_services
        self.provider_manager = provider_manager
        self.agent_registry = AgentRegistry()
        self.agent_selector = AgentSelector(self.agent_registry)
        self.task_queue = TaskQueue()
        self.result_handler = ResultHandler()
        self.task_history: Dict[int, List[Dict[str, Any]]] = {}

    async def process_task(self, task: Task) -> str:
        try:
            agent = self.agent_selector.select_agent(task)
            result = await agent.execute_task(task, self.provider_manager)
            return result
        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {str(e)}")
            return f"Error: {str(e)}"

    async def _execute_task(self, task: Task, agent: Agent) -> str:
        try:
            background_provider = await self.provider_manager.get_background_provider()
            result = await agent.execute_task(task, background_provider)
            await self.result_handler.handle_result(task, result)
            self._update_task_history(task, agent, result)
            return result
        except Exception as e:
            logger.error(f"Error executing task {task.task_id}: {str(e)}")
            return f"Error: {str(e)}"

    def _update_task_history(self, task: Task, agent: Agent, result: str):
        if task.task_id not in self.task_history:
            self.task_history[task.task_id] = []
        self.task_history[task.task_id].append({
            "agent": agent.name,
            "result": result,
            "timestamp": asyncio.get_event_loop().time()
        })

    def register_agent(self, agent: Agent):
        self.agent_registry.register(agent)

    def unregister_agent(self, agent_name: str):
        self.agent_registry.unregister(agent_name)

    def register_scout(self, scout_id: str, scout_instance: Any):
        self.result_handler.register_scout(scout_id, scout_instance)

    async def run(self):
        while True:
            task_tuple = await self.task_queue.get_task()
            if task_tuple:
                _, task, agent = task_tuple
                await self._execute_task(task, agent)
            else:
                await asyncio.sleep(0.1)  # Prevent busy-waiting

    def get_task_history(self, task_id: int) -> List[Dict[str, Any]]:
        return self.task_history.get(task_id, [])

class GeneralPurposeAgent(Agent):
    def __init__(self, name: str, capabilities: List[str]):
        self._name = name
        self._capabilities = capabilities

    async def execute_task(self, task: Task, provider: Any) -> str:
        try:
            response = await provider.generate_response(
                task.user_id,
                self.name,
                task.content,
                task.metadata
            )
            return response
        except Exception as e:
            logger.error(f"Error in GeneralPurposeAgent executing task {task.task_id}: {str(e)}")
            return f"Error: {str(e)}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> List[str]:
        return self._capabilities

    def can_handle_task(self, task: Task) -> bool:
        task_keywords = set(task.content.lower().split())
        agent_capabilities = set(cap.lower() for cap in self.capabilities)
        can_handle = bool(task_keywords.intersection(agent_capabilities))
        logger.debug(f"Agent {self.name} can handle task: {can_handle}")
        return can_handle
    
def create_default_agents(agent_manager: AgentManager):
    default_agents = [
        GeneralPurposeAgent("General Assistant", ["general", "conversation", "query"]),
        GeneralPurposeAgent("Query Specialist", ["query", "search", "information"]),
        GeneralPurposeAgent("Conversation Expert", ["conversation", "dialogue", "chat"])
    ]
    for agent in default_agents:
        agent_manager.register_agent(agent)
    logger.info("Created and registered default agents")

# Helper function to create a task
def create_task(task_id: int, user_id: str, content: str, metadata: Dict[str, Any] = None) -> Task:
    return Task(task_id, user_id, content, metadata)