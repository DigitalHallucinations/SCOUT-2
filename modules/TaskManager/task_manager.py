# modules/Tasks/task_manager.py

import asyncio
from collections import deque
from modules.logging.logger import setup_logger
import gui.send_message as send_message_module

logger = setup_logger('task_manager.py')

class TaskPlanner:
    def __init__(self, personas):
        self.personas = personas

    def plan_tasks(self, user_request):
        # TODO: Implement NLP logic to break down user_request into tasks
        # For now, we'll just return the request as a single task
        return [user_request]

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task, priority=0):
        self.queue.append((priority, task))
        self.queue = deque(sorted(self.queue, key=lambda x: x[0], reverse=True))

    def get_next_task(self):
        if self.queue:
            return self.queue.popleft()[1]
        return None

class TaskExecutor:
    def __init__(self):
        self.send_message = send_message_module.send_message

    async def execute_task(self, chat_component, user, task, session_id, conversation_id, conversation_manager, model_manager, provider_manager):
        try:
            result = await self.send_message(chat_component, user, task, session_id, conversation_id, conversation_manager, model_manager, provider_manager)
            return result
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return f"Error: {str(e)}"

class Task:
    def __init__(self, task_id, user_id, content):
        self.task_id = task_id
        self.user_id = user_id
        self.content = content
        self.status = "created"

class TaskManager:
    def __init__(self, personas):
        self.task_planner = TaskPlanner(personas)
        self.task_queue = TaskQueue()
        self.task_executor = TaskExecutor()
        self.personas = personas
        self.task_id_counter = 0

    def plan_tasks(self, user_request):
        return self.task_planner.plan_tasks(user_request)

    def add_task(self, task, priority=0):
        self.task_queue.add_task(task, priority)

    def create_task(self, user_id, content):
        self.task_id_counter += 1
        return Task(self.task_id_counter, user_id, content)    

    async def execute_next_task(self, chat_component, user, session_id, conversation_id, conversation_manager, model_manager, provider_manager):
        task = self.task_queue.get_next_task()
        if task:
            return await self.task_executor.execute_task(chat_component, user, task, session_id, conversation_id, conversation_manager, model_manager, provider_manager)
        return None

    async def process_user_input(self, chat_component, user, user_input, session_id, conversation_id, conversation_manager, model_manager, provider_manager):
        tasks = self.plan_tasks(user_input)
        results = []
        for task in tasks:
            self.add_task(task)
            result = await self.execute_next_task(chat_component, user, session_id, conversation_id, conversation_manager, model_manager, provider_manager)
            if result:
                results.append(result)
        return results