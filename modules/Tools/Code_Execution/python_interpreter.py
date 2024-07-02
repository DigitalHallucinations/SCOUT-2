import copy
import io
import logging
from contextlib import redirect_stdout
from typing import Any, Optional

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

class PythonInterpreter:
    def __init__(self, description: str = "", answer_symbol: Optional[str] = None, answer_expr: Optional[str] = None, answer_from_stdout: bool = True, name: Optional[str] = None, enable: bool = True, disable_description: Optional[str] = None, timeout: int = 20) -> None:
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
            result = self._run(command)
            logger.info(f"Command execution result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing command: {repr(e)}")
            return {
                "success": False,
                "error": repr(e),
                "result": None
            }

    def _run(self, command: str) -> dict:
        try:
            logger.info("Processing command")
            
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