import asyncio
from modules.logging.logger import setup_logger
import time
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

run_as_admin()

logger = setup_logger('TerminalCommand')

command_history = []

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

            if any(app in command for app in indefinite_apps):
                logger.info(f"Launched application/script (expected to run indefinitely): {command}")
                await asyncio.sleep(wait_for_indefinite_app)  
                if process.returncode is None:
                    logger.info(f"Application is running: {command}")
                    command_history.append((command, "Running", "", time.time() - start_time))
                    return {"output": "", "error": "", "status_code": 0}  
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
            await asyncio.sleep(2 ** retry_count)  
        except Exception as e:
            logger.error(f"Error executing command: {command} - {str(e)}")
            if process:
                await process.wait()
            command_history.append((command, "Error", str(e), time.time() - start_time))
            retry_count += 1
            await asyncio.sleep(2 ** retry_count)  
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