import subprocess
from typing import Optional, Tuple, List, Dict, Any
import shlex
from rich.console import Console
from langchain_openai import OpenAI
import os
import logging
from utils.logger import logger
import re
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import json

console = Console()

class CommandError(Exception):
    """Base exception for command execution errors"""
    pass

class CommandExecutionError(CommandError):
    """Raised when command execution fails"""
    pass

class CommandInterpretationError(CommandError):
    """Raised when AI fails to interpret command"""
    pass

class SmartCommandExecutor:
    # Common command mappings and shortcuts
    COMMON_SHORTCUTS = {
        # Directory shortcuts (case-insensitive)
        'desktop': 'cd ~/Desktop',
        'dsktp': 'cd ~/Desktop',
        'dt': 'cd ~/Desktop',
        'downloads': 'cd ~/Downloads',
        'dl': 'cd ~/Downloads',
        'docs': 'cd ~/Documents',
        'documents': 'cd ~/Documents',
        'pics': 'cd ~/Pictures',
        'pictures': 'cd ~/Pictures',
        'music': 'cd ~/Music',
        'videos': 'cd ~/Videos',
        # Common typos
        'cd..': 'cd ..',
        'sl': 'ls',
        'lls': 'ls',
        'la': 'ls -la',
        'll': 'ls -l',
        'gti': 'git',
        'pythno': 'python',
        'pyhton': 'python',
    }

    # Direct commands that don't need AI
    DIRECT_COMMANDS = {
        'ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'grep',
        'find', 'du', 'df', 'ps', 'top', 'clear', 'history', 'touch',
        'chmod', 'chown', 'tar', 'zip', 'unzip', 'ssh', 'scp', 'ping'
    }

    def __init__(self, api_key: str, user_config: dict):
        self.api_key = api_key
        self.user_config = user_config
        self.command_history = []
        self.error_history = []
        self.llm = OpenAI(api_key=self.api_key, model="gpt-3.5-turbo")
        
    def execute_command(self, command: str) -> Tuple[bool, str, Optional[str]]:
        """Execute a command and return success status, output, and error"""
        try:
            if not command.strip():
                return False, "Empty command", "Please enter a command"
            
            # Check for dangerous commands first
            if self._is_dangerous_command(command):
                return False, "This operation has been identified as dangerous", "Operation blocked for safety"
            
            # Try direct command execution first
            if command.split()[0] in self.DIRECT_COMMANDS:
                success, output = self._run_command(command)
                return success, output, None
            
            # Handle shortcuts
            if command.lower() in self.COMMON_SHORTCUTS:
                actual_command = self.COMMON_SHORTCUTS[command.lower()]
                success, output = self._run_command(actual_command)
                return success, output, f"Using shortcut: {command} → {actual_command}"
            
            # If not a direct command or shortcut, use AI interpretation
            return self._handle_ai_command(command)
            
        except IndexError:
            return False, "Invalid command format", "Please provide a valid command"
        except FileNotFoundError as e:
            return False, f"Command not found: {str(e)}", None
        except PermissionError as e:
            return False, f"Permission denied: {str(e)}", None
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return False, f"Error: {str(e)}", None

    def _run_command(self, command: str) -> Tuple[bool, str]:
        """Execute a shell command safely"""
        try:
            if not command.strip():
                return False, "Empty command"
            
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            self.command_history.append(command)
            
            if process.returncode == 0:
                return True, process.stdout
            else:
                return False, process.stderr or "Command failed"
            
        except FileNotFoundError:
            return False, "Command not found"
        except PermissionError:
            return False, "Permission denied"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def _is_dangerous_command(self, command: str) -> bool:
        dangerous_patterns = [
            r"rm\s+-rf\s+/",
            r"rm\s+-rf\s+~/",
            r"mkfs",
            r"dd\s+if=",
            r">\s+/dev/"
        ]
        return any(re.search(pattern, command) for pattern in dangerous_patterns)

    def _handle_ai_command(self, command: str) -> Tuple[bool, str, Optional[str]]:
        """Use AI to interpret and handle natural language commands"""
        try:
            response = self.llm.invoke(
                f"""
                As a command-line expert, help with this request:
                
                User input: {command}
                Current directory: {os.getcwd()}
                Recent commands: {', '.join(self.command_history[-3:])}
                
                If this is a question about system administration, networking, or general computing,
                provide a helpful explanation.
                
                If this is a command that needs to be fixed or a task that can be done with commands,
                suggest the correct command(s).
                
                Return format:
                TYPE: <command|explanation>
                RESPONSE: <your response>
                COMMAND: <if type is command, provide the command to execute>
                """
            )
            # Process response here
            return False, "Command not found", None
            
        except Exception as e:
            logger.error(f"AI interpretation error: {str(e)}")
            return False, f"Command not found: {str(e)}", None