#MODULES/Personas/CodeGenius/Toolbox/Tools/TerminalCommand.py

import asyncio
import subprocess
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('TerminalCommand')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024
log_backup_count = 5

rotating_handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=log_backup_count, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(rotating_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def adjust_logging_level(level):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logger.setLevel(levels.get(level, logging.WARNING))

async def TerminalCommand(command: str, timeout: int = 60):
    process = None
    try:
        logger.info(f"Executing command: {command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=1024 * 1024  # Limit output to 1MB
        )

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            result_stdout = stdout.decode().strip()
            result_stderr = stderr.decode().strip()
            logger.info(f"Command executed successfully: {command}")
            return {"output": result_stdout, "error": result_stderr, "status_code": process.returncode}
        except asyncio.TimeoutError:
            logger.error(f"Command timed out after {timeout} seconds: {command}")
            process.terminate()
            return {"output": "", "error": f"Command timed out after {timeout} seconds", "status_code": -1}
    except Exception as e:
        logger.error(f"Error executing command: {command} - {str(e)}")
        return {"output": "", "error": str(e), "status_code": -1}
    finally:
        if process is not None:
            try:
                process.terminate()
                await process.wait()
            except ProcessLookupError:
                pass