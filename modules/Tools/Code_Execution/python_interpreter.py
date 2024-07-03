# modules/Tools/Code_Execution/python_interpreter.py

import asyncio
import copy
import io
import logging
import textwrap
import inspect
from contextlib import redirect_stdout
from typing import Any, Optional
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger('python_interpreter.py')

class GenericRuntime:
    GLOBAL_DICT = {}
    LOCAL_DICT = None
    HEADERS = []

    def __init__(self):
        self._global_vars = copy.copy(self.GLOBAL_DICT)
        self._local_vars = copy.copy(self.LOCAL_DICT) if self.LOCAL_DICT else None
        for c in self.HEADERS:
            self.exec_code(c)
        logger.debug("GenericRuntime initialized")

    def exec_code(self, code_piece: str) -> None:
        exec(code_piece, self._global_vars)
        logger.debug(f"Executed code: {code_piece[:50]}...")

    def eval_code(self, expr: str) -> Any:
        result = eval(expr, self._global_vars)
        logger.debug(f"Evaluated expression: {expr}")
        return result

class PythonInterpreter(QObject):
    code_executed = Signal(str, dict)

    def __init__(self, description: str = "", answer_symbol: Optional[str] = None, answer_expr: Optional[str] = None, answer_from_stdout: bool = True, name: Optional[str] = None, enable: bool = True, disable_description: Optional[str] = None, timeout: int = 20) -> None:
        super().__init__()
        self.description = description
        self.answer_symbol = answer_symbol
        self.answer_expr = answer_expr
        self.answer_from_stdout = answer_from_stdout
        self.name = name or self.__class__.__name__
        self.enable = enable
        self.disable_description = disable_description
        self.timeout = timeout
        logger.info(f"PythonInterpreter initialized with name: {self.name}")

    def run(self, command: str) -> dict:
        logger.info(f"Running command in {self.name}")
        logger.debug(f"Full command: {command}")
        self.runtime = GenericRuntime()
        try:
            if self._is_async_code(command):
                result = self._run_async(command)
            else:
                result = self._run_sync(command)
            logger.info(f"Command execution result: {result}")
            self.code_executed.emit(command, result)
            return result
        except Exception as e:
            logger.error(f"Error executing command: {repr(e)}")
            error_result = {
                "success": False,
                "error": repr(e),
                "result": None
            }
            self.code_executed.emit(command, error_result)
            return error_result

    def _is_async_code(self, command: str) -> bool:
        return 'async def' in command or 'await ' in command

    def _run_sync(self, command: str) -> dict:
        try:
            logger.info("Processing synchronous command")
            
            # Replace asterisk with underscore in the range() function
            command = command.replace("for * in range", "for _ in range")
            
            # Capture stdout
            captured_output = io.StringIO()
            with redirect_stdout(captured_output):
                exec(command, self.runtime._global_vars)
            
            output = captured_output.getvalue().strip()
            
            logger.info("Command executed successfully")
            logger.debug(f"Execution result: {output}")
            return {
                "success": True,
                "result": output,
                "error": None
            }
        except Exception as e:
            logger.error(f"Error executing command: {repr(e)}")
            return {
                "success": False,
                "result": None,
                "error": repr(e)
            }

    def _run_async(self, command: str) -> dict:
        try:
            logger.info("Processing asynchronous command")
            
            # Replace asterisk with underscore in the range() function
            command = command.replace("for * in range", "for _ in range")
            
            # Capture stdout
            captured_output = io.StringIO()
            
            # Prepare the global namespace with asyncio and inspect
            global_vars = {**self.runtime._global_vars, 'asyncio': asyncio, 'inspect': inspect}
            
            # Wrap the command in an async function, preserving indentation
            wrapped_command = f"""
async def __temp_async_func():
{textwrap.indent(command, '    ')}

async def run_async_code():
    result = await __temp_async_func()
    if inspect.iscoroutine(result):
        result = await result
    return result

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    __temp_result = loop.run_until_complete(run_async_code())
finally:
    loop.close()
"""
            
            # Execute the async code
            with redirect_stdout(captured_output):
                exec(wrapped_command, global_vars)
            
            output = captured_output.getvalue().strip()
            result = global_vars.get('__temp_result', None)
            
            logger.info("Asynchronous command executed successfully")
            logger.debug(f"Execution result: {output}")
            logger.debug(f"Returned result: {result}")
            
            # Format the result for display
            formatted_result = output + "\n" if output else ""
            if result is not None:
                formatted_result += f"Result: {result}\n"
            
            return {
                "success": True,
                "result": formatted_result.strip(),
                "error": None
            }
        except Exception as e:
            logger.error(f"Error executing asynchronous command: {repr(e)}")
            return {
                "success": False,
                "result": None,
                "error": repr(e)
            }