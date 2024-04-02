import asyncio
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import time

logger = logging.getLogger('TerminalCommand')

log_filename = 'SCOUT.log'
log_max_size = 10 * 1024 * 1024  # 10 MB
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

# Define a list of applications that are expected to run indefinitely
indefinite_apps = ["chrome", "main.py", "taskmgr"]

async def TerminalCommand(command: str, timeout: int = 60, encoding: str = 'utf-8', verbose: bool = False, output_limit: int = 1024 * 1024, max_retries: int = 3):
    retry_count = 0
    while retry_count <= max_retries:
        process = None
        start_time = time.time()
        try:
            if verbose:
                logger.info(f"Executing command (attempt {retry_count + 1}): {command} - Verbose mode enabled")
            else:
                logger.info(f"Executing command (attempt {retry_count + 1}): {command}")
                
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                limit=output_limit 
            )

            # Log if the command is an indefinite application
            if any(app in command for app in indefinite_apps):
                logger.info(f"Launched application/script (expected to run indefinitely): {command}")

            feedback_interval = 10  # seconds
            last_feedback_time = start_time

            while True:
                if verbose and time.time() - last_feedback_time >= feedback_interval:
                    logger.info(f"Command is still running: {command}")
                    last_feedback_time = time.time()
                if process.returncode is not None:
                    break
                await asyncio.sleep(1)

            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout - (time.time() - start_time))
            result_stdout = stdout.decode(encoding).strip()
            result_stderr = stderr.decode(encoding).strip()
            execution_time = time.time() - start_time
            if verbose:
                logger.info(f"Command executed successfully: {command}")
            command_history.append((command, "Success", result_stdout, execution_time))
            return {"output": result_stdout, "error": result_stderr, "status_code": process.returncode}
        except asyncio.TimeoutError:
            logger.error(f"Command timed out after {timeout} seconds: {command}")
            process.terminate()
            await process.wait()
            command_history.append((command, "Timeout", "", timeout))
            retry_count += 1
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
        except Exception as e:
            logger.error(f"Error executing command: {command} - {str(e)}")
            if process:
                await process.wait()
            command_history.append((command, "Error", str(e), time.time() - start_time))
            retry_count += 1
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
        finally:
            if process is not None and process.returncode is None:
                try:
                    process.terminate()
                    await process.wait()
                except ProcessLookupError:
                    pass
    
    logger.error(f"Command failed after {max_retries} retries: {command}")
    return {"output": "", "error": f"Command failed after {max_retries} retries.", "status_code": -1}

def get_command_history():
    enhanced_history = []
    for entry in command_history:
        command, status, output, execution_time = entry
        enhanced_history.append({
            "command": command,
            "status": status,
            "output": output,
            "execution_time": execution_time
        })
    return enhanced_history