# modules/Providers/OpenAI/OA_gen_response.py

from openai import AsyncOpenAI
from model_manager import ModelManager

from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List, Dict, Union, AsyncIterator
from config import ConfigManager
from modules.logging.logger import setup_logger
from Tools.ToolManager import (
    load_function_map_from_current_persona,
    load_functions_from_json,
    use_tool
)

class OpenAIGenerator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = setup_logger(__name__) 
        self.api_key = self.config_manager.get_openai_api_key()
        if not self.api_key:
            self.logger.error("OpenAI API key not found in configuration")
            raise ValueError("OpenAI API key not found in configuration")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model_manager = ModelManager(config_manager)  

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        max_tokens: int = 4000,
        temperature: float = 0.0,
        stream: bool = True,
        current_persona=None,
        conversation_manager=None,
        user=None,
        conversation_id=None,
        functions=None
    ) -> Union[str, AsyncIterator[str]]:
        try:
            current_model = self.model_manager.get_current_model()
            
            if model and model != current_model:
                self.model_manager.set_model(model, "OpenAI")
                current_model = model
                self.logger.info(f"Model changed to {model}")
            elif not model:
                model = current_model
                self.logger.info(f"Using current model: {model}")

            self.logger.info(f"Starting API call to OpenAI with model {model}")
            self.logger.info(f"Current persona: {current_persona}")

            # Load functions if not provided
            if functions is None and current_persona:
                self.logger.info("No functions provided; attempting to load from current persona.")
                functions = load_functions_from_json(current_persona)
                if functions:
                    self.logger.info(f"Functions loaded from JSON: {functions}")
                else:
                    self.logger.warning("No functions loaded from JSON.")
            elif functions:
                self.logger.info(f"Using provided functions: {functions}")
            else:
                self.logger.warning("No functions to load or provide.")

            # Load function map
            function_map = load_function_map_from_current_persona(current_persona) if current_persona else None
            if function_map:
                self.logger.info(f"Function map loaded: {function_map}")
            else:
                self.logger.warning("No function map loaded.")

            # Ensure functions and function_map are sent for all models
            if not functions and not function_map:
                self.logger.warning("Neither functions nor function map available to send to the model.")

            # Log what is being sent to the API
            self.logger.info(f"Sending functions to OpenAI API: {functions}")
            self.logger.info(f"Sending function map to OpenAI API: {function_map}")

            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=temperature,
                stream=stream,
                functions=functions,
                function_call="auto" if functions else None  # Always include if functions exist
            )
            
            self.logger.info("Received response from OpenAI API.")

            if stream:
                self.logger.info("Processing streaming response.")
                return self.process_streaming_response(
                    response,
                    user,
                    conversation_id,
                    function_map,
                    functions,
                    current_persona,
                    temperature,
                    conversation_manager
                )
            else:
                message = response.choices[0].message
                if hasattr(message, 'function_call') and message.function_call:
                    self.logger.info(f"Function call detected in response: {message.function_call}")
                    return await self.handle_function_call(
                        user,
                        conversation_id,
                        message,
                        conversation_manager,
                        function_map,
                        functions,
                        current_persona,
                        temperature,
                        model
                    )
                self.logger.info("No function call detected in response.")
                return message.content

        except Exception as e:
            self.logger.error(f"Error in OpenAI API call: {str(e)}", exc_info=True)
            raise

    async def process_streaming_response(
        self,
        response: AsyncIterator[Dict],
        user,
        conversation_id,
        function_map,
        functions,
        current_persona,
        temperature,
        conversation_manager
    ):
        full_response = ""
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                full_response += chunk.choices[0].delta.content
            elif chunk.choices[0].delta.function_call:
                function_call = chunk.choices[0].delta.function_call
                self.logger.info(f"Function call detected during streaming: {function_call}")
                result = await self.handle_function_call(
                    user,
                    conversation_id,
                    {"function_call": function_call},
                    conversation_manager,
                    function_map,
                    functions,
                    current_persona,
                    temperature,
                    response.model
                )
                yield result
                full_response += result

        if conversation_manager:
            conversation_manager.add_message(user, conversation_id, "assistant", full_response)
            self.logger.info("Full streaming response added to conversation history.")

    async def handle_function_call(
        self,
        user,
        conversation_id,
        message,
        conversation_manager,
        function_map,
        functions,
        current_persona,
        temperature,
        model
    ):
        self.logger.info(f"Handling function call: {message.get('function_call')}")
        tool_response = await use_tool(
            user,
            conversation_id,
            message,
            conversation_manager,
            function_map,
            functions,
            current_persona,
            temperature,
            1.0,  # Assuming top_p_var is 1.0
            conversation_manager,
            self.config_manager
        )
        
        if tool_response:
            self.logger.info(f"Tool response generated: {tool_response}")
            return tool_response

        self.logger.warning("No tool response generated; sending default message.")
        return "Sorry, I couldn't process the function call. Please try again or provide more context."

async def generate_response(
    config_manager: ConfigManager,
    messages: List[Dict[str, str]],
    model: str = None,
    max_tokens: int = 4000,
    temperature: float = 0.0,
    stream: bool = True,
    current_persona=None,
    conversation_manager=None,
    user=None,
    conversation_id=None,
    functions=None
) -> Union[str, AsyncIterator[str]]:
    generator = OpenAIGenerator(config_manager)
    return await generator.generate_response(
        messages,
        model,
        max_tokens,
        temperature,
        stream,
        current_persona,
        conversation_manager,
        user,
        conversation_id,
        functions
    )

async def process_streaming_response(response: AsyncIterator[Dict]) -> str:
    content = ""
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content += chunk.choices[0].delta.content
    return content
