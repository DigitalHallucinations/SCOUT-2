import asyncio
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import time

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


command_history = []

async def TerminalCommand(command: str, timeout: int = 60, encoding: str = 'utf-8'):
    process = None
    start_time = time.time()
    try:
        logger.info(f"Executing command: {command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=1024 * 1024  # Limit output to 1MB
        )

        feedback_interval = 10  # seconds
        last_feedback_time = start_time

        try:
            while True:
                if time.time() - last_feedback_time >= feedback_interval:
                    logger.info(f"Command is still running: {command}")
                    last_feedback_time = time.time()
                if process.returncode is not None:
                    break
                await asyncio.sleep(1)

            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout - (time.time() - start_time))
            result_stdout = stdout.decode(encoding).strip()
            result_stderr = stderr.decode(encoding).strip()
            logger.info(f"Command executed successfully: {command}")
            command_history.append((command, "Success"))
            return {"output": result_stdout, "error": result_stderr, "status_code": process.returncode}
        except asyncio.TimeoutError:
            logger.error(f"Command timed out after {timeout} seconds: {command}")
            process.terminate()
            command_history.append((command, "Timeout"))
            return {"output": "", "error": f"Command timed out after {timeout} seconds", "status_code": -1}
    except Exception as e:
        logger.error(f"Error executing command: {command} - {str(e)}")
        command_history.append((command, "Error"))
        return {"output": "", "error": str(e), "status_code": -1}
    finally:
        if process is not None:
            try:
                process.terminate()
                await process.wait()
            except ProcessLookupError:
                pass

def get_command_history():
    return command_history