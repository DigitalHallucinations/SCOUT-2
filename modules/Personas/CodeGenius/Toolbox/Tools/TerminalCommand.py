import asyncio
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import time
import ctypes
import sys
import os

# Function to check if the script is running with administrative privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to relaunch the script with administrative privileges if not already running as admin
def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Ensure the script is running with administrative privileges
run_as_admin()

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
indefinite_apps = ["main.py", "taskmgr"]

async def TerminalCommand(command: str, timeout: int = 60, encoding: str = 'utf-8', verbose: bool = False, output_limit: int = 1024 * 1024, max_retries: int = 3, wait_for_indefinite_app: int = 10):
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

            # Check if the command is an indefinite application
            if any(app in command for app in indefinite_apps):
                logger.info(f"Launched application/script (expected to run indefinitely): {command}")
                await asyncio.sleep(wait_for_indefinite_app)  # Wait for the application to fully launch and stabilize
                # Check if the process is still running
                if process.returncode is None:
                    logger.info(f"Application is running: {command}")
                    command_history.append((command, "Running", "", time.time() - start_time))
                    return {"output": "", "error": "", "status_code": 0}  # Consider successful launch
                else:
                    logger.info(f"Application terminated unexpectedly: {command}")

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