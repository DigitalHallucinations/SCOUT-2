# TerminalCommand Tool for AI Agents

The TerminalCommand tool is a Python utility designed for AI agents to execute terminal commands asynchronously. It provides advanced features such as timeout handling, output limiting, retry mechanisms, and verbose logging to enhance the agent's interaction with the terminal.

## Configuration

The TerminalCommand tool offers several configuration options:

- `log_filename`: The name of the log file (default: 'SCOUT.log').
- `log_max_size`: The maximum size of the log file in bytes (default: 10 MB).
- `log_backup_count`: The number of backup log files to keep (default: 5).

These options can be modified in the code to suit the AI agent's requirements.

## Usage

To integrate the TerminalCommand tool into an AI agent, follow these steps:

1. Import the necessary functions and classes:
   ```python
   from terminal_command import TerminalCommand, adjust_logging_level, get_command_history
   ```

2. Execute a command using the `TerminalCommand` function:
   ```python
   result = await TerminalCommand(command, timeout=60, encoding='utf-8', verbose=False, output_limit=1024*1024, max_retries=3)
   ```
   - `command`: The terminal command to execute (required).
   - `timeout`: The maximum time (in seconds) to wait for the command to complete (default: 60).
   - `encoding`: The encoding to use for decoding the command output (default: 'utf-8').
   - `verbose`: Enable verbose logging mode (default: False).
   - `output_limit`: The maximum size (in bytes) of the command output to capture (default: 1 MB).
   - `max_retries`: The maximum number of retries if the command fails (default: 3).

3. The `TerminalCommand` function returns a dictionary with the following keys:
   - `output`: The captured stdout output of the command.
   - `error`: The captured stderr output of the command.
   - `status_code`: The exit code of the command process.

4. Adjust the logging level using the `adjust_logging_level` function:
   ```python
   adjust_logging_level('DEBUG')
   ```
   Available logging levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

5. Retrieve the command execution history using the `get_command_history` function:
   ```python
   history = get_command_history()
   ```
   The function returns a list of dictionaries, each containing information about an executed command, including the command itself, status, output, and execution time.

## Error Handling

- If the command fails to execute, the AI agent should check the error message in the returned dictionary or the log file for more information.
- The AI agent should ensure that the command is valid and accessible from the system's terminal.
- The AI agent should verify that it has the necessary permissions to execute the command.
- If the command times out, the AI agent can consider increasing the `timeout` parameter or optimizing the command for faster execution.

## Example Use Cases

1. Executing system commands:
   ```python
   result = await TerminalCommand('systeminfo')
   ai_agent.process_output(result['output'])
   ```

2. Performing file operations:
   ```python
   result = await TerminalCommand('dir /s /b')
   files = result['output'].split('\n')
   ai_agent.analyze_files(files)
   ```

3. Monitoring system resources:
   ```python
   result = await TerminalCommand('top -b -n 1')
   ai_agent.monitor_system_resources(result['output'])
   ```

4. Executing scripts or batch files:
   ```python
   result = await TerminalCommand('python script.py')
   ai_agent.process_script_output(result['output'])
   ```

The AI agent can leverage the TerminalCommand tool to interact with the terminal, execute commands, and retrieve output for further processing and decision-making. The tool provides a convenient and reliable way for the AI agent to perform system-level operations and gather information from the terminal.