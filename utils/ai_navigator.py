"""AI-powered directory navigation and interaction module."""

import os
import logging
from pathlib import Path
from typing import Tuple, Optional, List
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class AINavigator:
    """Interactive AI assistant for directory navigation and cleanup."""
    
    def __init__(self):
        self.current_dir = Path.cwd()
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai.api_key:
            raise ValueError("OpenAI API key is required")
    
    async def chat(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Process user input and return AI response and directory if applicable."""
        try:
            # Provide context about current directory
            context = f"""
            Current directory: {self.current_dir}
            Parent directory: {self.current_dir.parent}
            Available directories: {[d.name for d in self.current_dir.iterdir() if d.is_dir()]}
            """
            
            prompt = f"""
            User is navigating directories for cleanup. Current context:
            {context}
            
            User input: {user_input}
            
            If the user is:
            1. Asking to navigate (cd, back, up, ls, etc.) - provide directory info
            2. Asking about directory safety - assess the risks
            3. Asking for cleanup recommendations - provide specific advice
            4. Asking for general help - explain available commands
            
            Respond conversationally but include a COMMAND: prefix if action needed:
            - COMMAND:CD:{path} for directory change
            - COMMAND:LS for directory listing
            - COMMAND:CLEAN to start cleanup
            - COMMAND:HELP for help
            """
            
            response = await self.openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful directory navigation assistant. Keep responses friendly but concise."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            ai_response = response.choices[0].message.content
            command = self._extract_command(ai_response)
            
            return ai_response, command
            
        except Exception as e:
            logging.error(f"Error in AI chat: {e}")
            return "Sorry, I encountered an error. Please try again.", None
    
    def _extract_command(self, response: str) -> Optional[str]:
        """Extract command from AI response if present."""
        if "COMMAND:" in response:
            command_line = [line for line in response.split('\n') if "COMMAND:" in line][0]
            return command_line.split("COMMAND:")[1].strip()
        return None
    
    async def process_command(self, command: str) -> bool:
        """Process navigation command."""
        try:
            if command.startswith("CD:"):
                new_dir = command[3:].strip()
                if new_dir == "..":
                    self.current_dir = self.current_dir.parent
                else:
                    new_path = (self.current_dir / new_dir).resolve()
                    if new_path.is_dir():
                        self.current_dir = new_path
                return True
                
            elif command == "LS":
                return True
                
            elif command == "CLEAN":
                return True
                
            return False
            
        except Exception as e:
            logging.error(f"Error processing command: {e}")
            return False 