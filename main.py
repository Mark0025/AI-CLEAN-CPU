#!/usr/bin/env python3
"""Directory Cleanup Application"""

import logging
from pathlib import Path
from colorama import init, Fore, Style
from utils.logging_utils import setup_logging
from core.chat_interface import CleanupAssistant

# Initialize colorama
init()

def main():
    """Main entry point."""
    setup_logging()
    assistant = CleanupAssistant()
    
    print(f"""
{Fore.GREEN}Directory Navigation Assistant{Style.RESET_ALL}
You can:
- Navigate directories (cd, ls, go to)
- Delete empty files/folders (delete empty)
- Search for files (find, search)
- Get help (help, ?)
    """)
    
    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}{assistant.current_path}{Style.RESET_ALL}> ").strip()
            
            if not user_input:
                continue
                
            response = assistant.handle_command(user_input)
            
            if response == "exit":
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
                
            if response:  # Only print if there's a response
                print(response)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
