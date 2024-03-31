import sys
import os
import unittest
import logging
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from TerminalCommand import TerminalCommand, adjust_logging_level

class TestTerminalCommand(unittest.IsolatedAsyncioTestCase):
    async def test_successful_command(self):
        command = "echo 'Hello, World!'"
        result = await TerminalCommand(command)
        self.assertIn("Hello, World!", result["output"])
        self.assertEqual(result["error"], "")
        self.assertEqual(result["status_code"], 0)

    async def test_command_with_error(self):
        command = "non_existent_command"
        result = await TerminalCommand(command)
        self.assertEqual(result["output"], "")
        self.assertNotEqual(result["error"], "")
        self.assertNotEqual(result["status_code"], 0)

    async def test_command_timeout(self):
        command = "timeout 5"
        timeout = 2
        result = await TerminalCommand(command, timeout=timeout)
        self.assertEqual(result["output"], "")
        self.assertEqual(result["error"], f"Command timed out after {timeout} seconds")
        self.assertEqual(result["status_code"], -1)

    def test_adjust_logging_level(self):
        adjust_logging_level("DEBUG")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.DEBUG)

        adjust_logging_level("INFO")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.INFO)

        adjust_logging_level("WARNING")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.WARNING)

        adjust_logging_level("ERROR")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.ERROR)

        adjust_logging_level("CRITICAL")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.CRITICAL)

        adjust_logging_level("INVALID_LEVEL")
        self.assertEqual(logging.getLogger("TerminalCommand").level, logging.WARNING)

if __name__ == "__main__":
    unittest.main()