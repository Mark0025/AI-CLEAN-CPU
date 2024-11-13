"""Smart chat interface for interacting with the cleanup assistant."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import os
import mimetypes
from datetime import datetime
import json
import subprocess
import shlex
from colorama import init, Fore, Style
from tqdm import tqdm
import sys
from send2trash import send2trash

# Initialize colorama
init()

class CleanupAssistant:
    def __init__(self):
        self.current_path = Path.cwd()
        self.logger = logging.getLogger(__name__)
        self.file_index: Dict[str, Dict] = {}
        self.history: List[str] = []
        
    def handle_command(self, user_input: str) -> str:
        """Process user input with natural language understanding."""
        try:
            self.history.append(user_input)
            command = user_input.lower().strip()
            
            # First try to parse as natural language
            nl_response = self._natural_to_cli(command)
            if nl_response:
                return nl_response  # Return the response directly, don't execute as command
            
            # If not a natural language command, process normally
            return self._process_command(command)
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"
    
    def _natural_to_cli(self, text: str) -> Optional[str]:
        """Convert natural language to CLI command."""
        try:
            # Directory listing commands - return the actual method result, not a command string
            if any(x in text.lower() for x in [
                "what's in", "show directory", "show me what's",
                "list", "contents", "show contents"
            ]):
                return self.list_contents()  # Return the actual method result
            
            # Empty file/directory commands
            if any(x in text.lower() for x in ["show empty files", "show me empty files"]):
                return self._find_empty_files()  # Return the actual method result
            if any(x in text.lower() for x in ["show empty directories", "show me empty directories"]):
                return self._find_empty_directories()  # Return the actual method result
            
            # Navigation commands
            if text.strip() == "..":
                return self.change_directory("..")  # Return the actual method result
            if text.startswith("go to"):
                path = text[5:].strip()
                return self.change_directory(path)  # Return the actual method result
            
            # Handle deletion commands
            if any(word in text.lower() for word in ["delete", "remove", "clean"]):
                if "empty" in text:
                    empty_items = self._find_empty_items()
                    if not empty_items['files'] and not empty_items['dirs']:
                        return f"{Fore.GREEN}No empty files or folders found.{Style.RESET_ALL}"
                    
                    return self._delete_empty_items(empty_items)
            
            return None
        except Exception as e:
            self.logger.error(f"Error in natural language processing: {e}")
            return self._generate_helpful_response(text)  # Return helpful message instead of None

    def _extract_size(self, text: str) -> str:
        """Extract size specification from text."""
        words = text.split()
        for i, word in enumerate(words):
            if word.isdigit():
                unit = words[i+1] if i+1 < len(words) else "b"
                return f"{word}{unit[0]}"
        return "1M"  # default to 1MB

    def _extract_days(self, text: str) -> str:
        """Extract day specification from text."""
        words = text.split()
        for i, word in enumerate(words):
            if word.isdigit():
                return f"-{word}"  # negative for "newer than"
        return "-1"  # default to 1 day

    def _extract_pattern(self, text: str) -> str:
        """Extract search pattern from text."""
        if '"' in text:
            return text.split('"')[1]
        if "named" in text:
            words = text.split("named")
            if len(words) > 1:
                return words[1].strip().split()[0]
        return "*"

    def _process_command(self, command: str) -> str:
        """Process command after natural language parsing."""
        try:
            # Direct terminal command execution
            if command.startswith("!"):
                return self._execute_system_command(command[1:])
            
            # Smart directory navigation
            if command.lower() in ["desktop", "downloads", "documents", "home"]:
                return self.change_directory(command)
            
            # Basic commands
            if command in ["help", "what can i do?", "?"]:
                return self.show_help()
            elif command.startswith("cd") or command.startswith("go to"):
                # Extract path from command
                if command.startswith("cd"):
                    path = command[2:].strip()
                else:  # go to
                    path = " ".join(command.split()[2:])  # Skip "go" and "to"
                return self.change_directory(path)
            elif command in ["ls", "show directories", "list", "show directory contents"]:
                return self.list_contents()
            elif command == "exit":
                return "exit"
            
            # Try natural language processing
            nl_response = self._natural_to_cli(command)
            if nl_response:
                return nl_response
            
            return self._generate_helpful_response(command)
        except Exception as e:
            self.logger.error(f"Error in command processing: {e}")
            return f"{Fore.RED}Error processing command: {str(e)}{Style.RESET_ALL}"

    def _execute_system_command(self, command: str) -> str:
        """Execute system command and return output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.current_path)
            )
            
            if result.returncode == 0:
                # Always return the actual output if available
                if result.stdout.strip():
                    return result.stdout.strip()
                if result.stderr.strip():
                    return result.stderr.strip()
                return f"{Fore.GREEN}Command executed successfully{Style.RESET_ALL}"
            return f"{Fore.RED}Error: {result.stderr}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}Failed to execute command: {e}{Style.RESET_ALL}"

    def analyze_directory(self, directory: Path) -> str:
        """Analyze directory contents with detailed information."""
        try:
            stats = {
                "total_files": 0,
                "total_size": 0,
                "file_types": {},
            }
            
            files = []
            for item in directory.rglob("*"):
                if item.is_file():
                    stats["total_files"] += 1
                    size = item.stat().st_size
                    modified = datetime.fromtimestamp(item.stat().st_mtime)
                    mime_type = mimetypes.guess_type(item.name)[0] or "unknown"
                    
                    files.append({
                        "path": str(item),
                        "size": size,
                        "modified": modified.isoformat(),
                        "type": mime_type
                    })
                    
                    stats["total_size"] += size
                    stats["file_types"][mime_type] = stats["file_types"].get(mime_type, 0) + 1
            
            # Sort by most recent
            files.sort(key=lambda x: x["modified"], reverse=True)
            
            output = [
                f"\n{Fore.GREEN}Directory Analysis for: {directory}{Style.RESET_ALL}",
                f"Total Files: {stats['total_files']}",
                f"Total Size: {self._format_size(stats['total_size'])}",
                f"\n{Fore.YELLOW}Most Recent Files:{Style.RESET_ALL}"
            ]
            
            for f in files[:10]:  # Show 10 most recent files
                name = Path(f["path"]).name
                size = self._format_size(f["size"])
                date = f["modified"].split("T")[0]
                output.append(f"  {name} ({size}, {date})")
            
            return "\n".join(output)
            
        except Exception as e:
            return f"{Fore.RED}Error analyzing directory: {str(e)}{Style.RESET_ALL}"

    def search_files(self, term: str) -> str:
        """Search for files matching the given term."""
        try:
            results = []
            for item in self.current_path.rglob("*"):
                if term.lower() in item.name.lower():
                    results.append(str(item))
            
            if not results:
                return f"No files found matching '{term}'"
            
            return f"{Fore.GREEN}Found matches:{Style.RESET_ALL}\n" + "\n".join(f"- {r}" for r in results)
        except Exception as e:
            return f"{Fore.RED}Error searching files: {str(e)}{Style.RESET_ALL}"

    def show_file_content(self, file_name: str) -> str:
        """Show content of a file with smart handling of different file types."""
        try:
            file_path = self.current_path / file_name
            if not file_path.exists():
                return f"{Fore.RED}File not found: {file_name}{Style.RESET_ALL}"
            
            if file_path.is_dir():
                return f"{Fore.YELLOW}{file_name} is a directory{Style.RESET_ALL}"
            
            if file_path.stat().st_size > 1_000_000:  # 1MB
                response = input(f"{Fore.YELLOW}File is large. View anyway? (y/N): {Style.RESET_ALL}")
                if response.lower() != 'y':
                    return "Operation cancelled"
            
            if file_path.stat().st_size > 1000:
                pager = os.environ.get('PAGER', 'less' if os.name != 'nt' else 'more')
                subprocess.run([pager, str(file_path)])
                return ""
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return f"{Fore.CYAN}=== {file_name} ==={Style.RESET_ALL}\n{content}"
                
        except Exception as e:
            return f"{Fore.RED}Error reading file: {str(e)}{Style.RESET_ALL}"

    def change_directory(self, new_path: str) -> str:
        """Change current working directory with smart path handling."""
        try:
            # Handle common directory names
            path_aliases = {
                "desktop": Path.home() / "Desktop",
                "downloads": Path.home() / "Downloads",
                "documents": Path.home() / "Documents",
                "home": Path.home(),
                "~": Path.home(),
                ".": self.current_path,
                "..": self.current_path.parent
            }
            
            # Clean up the path input
            clean_path = new_path.lower().strip()
            
            # Check if it's a common directory name
            if clean_path in path_aliases:
                new_path = path_aliases[clean_path]
            else:
                # Handle regular path
                new_path = Path(new_path).expanduser()
                if not new_path.is_absolute():
                    new_path = self.current_path / new_path
            
            if new_path.exists() and new_path.is_dir():
                self.current_path = new_path
                return f"{Fore.GREEN}Changed directory to: {self.current_path}{Style.RESET_ALL}\n\n{self.list_contents()}"
            else:
                # Try to be helpful with suggestions
                suggestions = []
                if clean_path in ["desktop", "downloads", "documents"]:
                    suggestions.append(f"Did you mean: '{clean_path.capitalize()}'?")
                return f"{Fore.RED}Directory does not exist: {new_path}\n{Style.RESET_ALL}" + \
                       ("\n".join(suggestions) if suggestions else "")
        except Exception as e:
            self.logger.error(f"Error changing directory: {e}")
            return f"{Fore.RED}Could not change directory: {str(e)}{Style.RESET_ALL}"

    def list_contents(self) -> str:
        """List contents with enhanced information."""
        try:
            contents = list(self.current_path.iterdir())
            
            dirs = []
            files = []
            
            for p in contents:
                if p.is_dir():
                    dirs.append(f"{Fore.BLUE}📁 {p.name}/{Style.RESET_ALL}")
                else:
                    size = self._format_size(p.stat().st_size)
                    modified = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    files.append(f"📄 {p.name} ({size}, modified: {modified})")
            
            return f"{Fore.YELLOW}Current directory contents:{Style.RESET_ALL}\n" + "\n".join(sorted(dirs) + sorted(files))
        except Exception as e:
            self.logger.error(f"Error listing contents: {e}")
            return f"{Fore.RED}Could not list directory contents: {str(e)}{Style.RESET_ALL}"

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def _generate_helpful_response(self, command: str) -> str:
        """Generate contextual helpful response."""
        return (
            f"{Fore.YELLOW}Not sure what you want to do. Try:{Style.RESET_ALL}\n"
            "- A terminal command directly (ls, cd, grep, etc.)\n"
            "- Ask 'What's in <location>?'\n"
            "- Type 'help' for more options"
        )

    def _find_empty_items(self) -> Dict[str, List[Path]]:
        """Find empty files and directories with extra safety checks."""
        empty_files = []
        empty_dirs = []
        
        # Skip patterns for safety
        SKIP_PATTERNS = {
            'venv', '__pycache__', '.git', 
            'py.typed', '__init__.py', '.pytest_cache',
            'REQUESTED', 'dist-info', '$RECYCLE.BIN'  # Added recycle bin to skip
        }
        
        print(f"{Fore.CYAN}Analyzing directory contents...{Style.RESET_ALL}")
        total_items = sum(1 for _ in self.current_path.rglob("*"))
        
        with tqdm(total=total_items, desc="Scanning", unit="items") as pbar:
            for item in self.current_path.rglob("*"):
                try:
                    # Skip system and configuration files
                    if any(pattern in str(item) for pattern in SKIP_PATTERNS):
                        pbar.update(1)
                        continue
                    
                    if item.is_file():
                        # Double check file is truly empty
                        try:
                            if item.stat().st_size == 0:
                                empty_files.append(item)
                        except (OSError, IOError):
                            # Skip if can't access file
                            pass
                    elif item.is_dir():
                        try:
                            # Check if directory is truly empty (no hidden files)
                            if not any(item.iterdir()):
                                empty_dirs.append(item)
                        except (OSError, IOError):
                            # Skip if can't access directory
                            pass
                    pbar.update(1)
                except Exception as e:
                    self.logger.error(f"Error checking {item}: {e}")
                    pbar.update(1)
        
        return {
            'files': sorted(empty_files),
            'dirs': sorted(empty_dirs, reverse=True)
        }

    def _format_path_for_display(self, path: Path) -> str:
        """Format path for user-friendly display."""
        try:
            # Get relative path if possible
            try:
                rel_path = path.relative_to(self.current_path)
            except ValueError:
                rel_path = path.relative_to(Path.home())
            
            # Get file size and modified time
            stats = path.stat()
            size = self._format_size(stats.st_size)
            modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M")
            
            # Format name with just the final component and parent dir if not in current dir
            if len(path.parts) > 1:
                display_name = f"{path.parts[-2]}/{path.name}"
            else:
                display_name = path.name
            
            return f"{display_name:<50} {size:>8} (modified: {modified})"
        except Exception:
            return str(path.name)

    def _analyze_files_for_safety(self, items: Dict[str, List[Path]]) -> Tuple[bool, str]:
        """Analyze files for potential safety concerns."""
        try:
            # Group files by risk level
            safe_files = []
            caution_files = []
            unsafe_files = []
            
            for file in items['files']:
                name_lower = file.name.lower()
                parent_lower = file.parent.name.lower()
                
                # Completely safe files
                if ('node_modules' in str(file) and 
                    (file.suffix in ['.js', '.d.ts', '.txt'])):
                    safe_files.append(file)
                # Files that need caution
                elif any(x in parent_lower for x in ['test', 'tests', 'examples']):
                    caution_files.append(file)
                # Files that might be risky
                else:
                    unsafe_files.append(file)
            
            print(f"\n{Fore.GREEN}Safe to delete:{Style.RESET_ALL}")
            for f in safe_files:
                print(f"  ✓ {f.name} (in {f.parent.name})")
            
            print(f"\n{Fore.YELLOW}Proceed with caution:{Style.RESET_ALL}")
            for f in caution_files:
                print(f"  ⚠️  {f.name} (in {f.parent.name})")
            
            print(f"\n{Fore.RED}Review carefully:{Style.RESET_ALL}")
            for f in unsafe_files:
                print(f"  ❌ {f.name} (in {f.parent.name})")
            
            return True, "Files have been categorized by safety level"
            
        except Exception as e:
            self.logger.error(f"Error in safety analysis: {e}")
            return False, f"Could not complete safety analysis: {e}"

    def _format_empty_item(self, item: Path, is_dir: bool = False) -> str:
        """Format empty item display with size."""
        try:
            if is_dir:
                # For directories, count total size of directory (should be 0)
                size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                return f"  - {item.name}/ ({self._format_size(size)})"
            else:
                # For files, just get the file size (should be 0)
                size = item.stat().st_size
                return f"  - {item.name} ({self._format_size(size)})"
        except Exception:
            return f"  - {item.name} (size unknown)"

    def _create_cleanup_directory(self) -> Path:
        """Create a dated cleanup directory."""
        # Create base name based on OS
        base_name = "mac-clean" if os.name == "posix" else "pc-clean"
        
        # Add date
        date_str = datetime.now().strftime("%d-%m-%Y")
        dir_name = f"{base_name}-{date_str}"
        
        # Create in current directory
        cleanup_dir = self.current_path / dir_name
        cleanup_dir.mkdir(exist_ok=True)
        
        return cleanup_dir

    def _move_to_cleanup_dir(self, items: Dict[str, List[Path]], cleanup_dir: Path) -> Tuple[List[str], List[str]]:
        """Move items to cleanup directory with size in name."""
        moved_files = []
        moved_dirs = []
        
        # Move files
        for file in items['files']:
            try:
                size = self._format_size(file.stat().st_size)
                new_name = f"{file.stem}-{size}{file.suffix}"
                new_path = cleanup_dir / new_name
                file.rename(new_path)
                moved_files.append(f"{file.name} -> {new_name}")
            except Exception as e:
                self.logger.error(f"Error moving file {file}: {e}")
        
        # Move directories
        for directory in items['dirs']:
            try:
                # Calculate total size (should be 0 for empty dirs)
                size = self._format_size(sum(f.stat().st_size for f in directory.rglob('*') if f.is_file()))
                new_name = f"{directory.name}-{size}"
                new_path = cleanup_dir / new_name
                directory.rename(new_path)
                moved_dirs.append(f"{directory.name} -> {new_name}")
            except Exception as e:
                self.logger.error(f"Error moving directory {directory}: {e}")
        
        return moved_files, moved_dirs

    def _delete_empty_items(self, items: Dict[str, List[Path]]) -> str:
        """Delete empty files and directories with safety options."""
        # First show summary and educational message
        print(f"\n{Fore.CYAN}About Empty Files and Directories:{Style.RESET_ALL}")
        print("- Empty files (0 bytes) are safe to delete and won't harm your system")
        print("- Empty directories contain no files or hidden files")
        print("- Deletion can't be undone, but empty files have no content to lose")
        
        if items['files']:
            print(f"\n{Fore.CYAN}Empty files found ({len(items['files'])}):{Style.RESET_ALL}")
            for f in items['files']:
                print(self._format_empty_item(f))
        
        if items['dirs']:
            print(f"\n{Fore.CYAN}Empty directories found ({len(items['dirs'])}):{Style.RESET_ALL}")
            for d in items['dirs']:
                print(self._format_empty_item(d, is_dir=True))
        
        # Perform safety analysis
        is_safe, safety_message = self._analyze_files_for_safety(items)
        
        if not is_safe:
            print(f"\n{Fore.RED}Safety Warning:{Style.RESET_ALL}")
            print(safety_message)
        
        # Ask for deletion method
        print(f"\n{Fore.YELLOW}How would you like to proceed?{Style.RESET_ALL}")
        print("1. Move to Trash/Recycle Bin (safer)")
        print("2. Delete permanently")
        print("3. Cancel operation")
        
        choice = input(f"\nEnter your choice (1-3): ")
        
        if choice == "3":
            return f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}"
        
        if choice not in ["1", "2"]:
            return f"{Fore.RED}Invalid choice. Operation cancelled.{Style.RESET_ALL}"
        
        # Extra confirmation for permanent deletion
        if choice == "2":
            confirm = input(f"\n{Fore.RED}Are you sure you want to permanently delete these items? (type 'yes' to confirm): {Style.RESET_ALL}")
            if confirm.lower() != 'yes':
                return f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}"
        
        if choice == "1":  # Move to Trash/Recycle Bin
            try:
                # Create cleanup directory
                cleanup_dir = self._create_cleanup_directory()
                print(f"\n{Fore.CYAN}Creating cleanup directory: {cleanup_dir.name}{Style.RESET_ALL}")
                
                # Move items to cleanup directory
                moved_files, moved_dirs = self._move_to_cleanup_dir(items, cleanup_dir)
                
                # Send entire cleanup directory to trash
                send2trash(str(cleanup_dir))
                
                # Prepare result message
                result = []
                if moved_files:
                    result.append(f"\n{Fore.GREEN}Moved files to trash:{Style.RESET_ALL}")
                    result.extend(f"  - {f}" for f in moved_files)
                if moved_dirs:
                    result.append(f"\n{Fore.GREEN}Moved directories to trash:{Style.RESET_ALL}")
                    result.extend(f"  - {d}" for d in moved_dirs)
                
                result.append(f"\n{Fore.GREEN}All items have been organized in {cleanup_dir.name} and moved to trash{Style.RESET_ALL}")
                result.append("You can restore them if needed.")
                
                return "\n".join(result)
                
            except Exception as e:
                return f"{Fore.RED}Error organizing items: {str(e)}{Style.RESET_ALL}"
        
        deleted_files = []
        deleted_dirs = []
        errors = []
        
        # Delete files first
        if items['files']:
            with tqdm(total=len(items['files']), desc="Processing files", unit="files") as pbar:
                for file in items['files']:
                    try:
                        # One final check before deletion
                        if file.stat().st_size == 0:
                            if choice == "1":
                                send2trash(str(file))
                                deleted_files.append(f"{self._format_path_for_display(file)} (moved to trash)")
                            else:
                                file.unlink()
                                deleted_files.append(f"{self._format_path_for_display(file)} (deleted)")
                        pbar.update(1)
                    except Exception as e:
                        errors.append(f"{file.name}: {e}")
                        pbar.update(1)
        
        # Then delete directories
        if items['dirs']:
            with tqdm(total=len(items['dirs']), desc="Processing directories", unit="dirs") as pbar:
                for directory in items['dirs']:
                    try:
                        # One final check before deletion
                        if not any(directory.iterdir()):
                            if choice == "1":
                                send2trash(str(directory))
                                deleted_dirs.append(f"{directory.name}/ (moved to trash)")
                            else:
                                directory.rmdir()
                                deleted_dirs.append(f"{directory.name}/ (deleted)")
                        pbar.update(1)
                    except Exception as e:
                        errors.append(f"{directory.name}: {e}")
                        pbar.update(1)
        
        # Prepare result message
        result = []
        if deleted_files:
            result.append(f"\n{Fore.GREEN}Processed files:{Style.RESET_ALL}")
            result.extend(f"  - {f}" for f in deleted_files)
        if deleted_dirs:
            result.append(f"\n{Fore.GREEN}Processed directories:{Style.RESET_ALL}")
            result.extend(f"  - {d}" for d in deleted_dirs)
        if errors:
            result.append(f"\n{Fore.RED}Errors:{Style.RESET_ALL}")
            result.extend(f"  - {e}" for e in errors)
        
        # Add summary message
        if choice == "1":
            result.append(f"\n{Fore.GREEN}Items have been moved to your Trash/Recycle Bin{Style.RESET_ALL}")
            result.append("You can restore them if needed.")
        else:
            result.append(f"\n{Fore.YELLOW}Items have been permanently deleted{Style.RESET_ALL}")
        
        return "\n".join(result) if result else f"{Fore.YELLOW}No items were processed.{Style.RESET_ALL}"

    def show_help(self) -> str:
        """Show enhanced help message."""
        return f"""
{Fore.GREEN}Available Commands:{Style.RESET_ALL}
1. Navigation:
   - cd <path>, go to <path>: Change directory
   - ls, list: Show directory contents
   - desktop, downloads, home: Quick navigation
   
2. File Operations:
   - find empty: Find empty files and directories
   - delete empty: Remove empty files/folders
   - cat, show content <file>: View file contents
   
3. System Commands:
   - !<command>: Execute system command (e.g., !echo test)
   
4. Natural Language:
   - "What's in this directory?"
   - "Show me empty files"
   - "Clean up empty folders"

Type 'exit' to quit
"""

    def _find_empty_files(self) -> str:
        """Find empty files in current directory."""
        try:
            empty_files = [f for f in self.current_path.rglob("*") 
                          if f.is_file() and f.stat().st_size == 0]
            
            if not empty_files:
                return f"{Fore.GREEN}No empty files found.{Style.RESET_ALL}"
            
            return f"{Fore.CYAN}Found empty files:{Style.RESET_ALL}\n" + \
                   "\n".join(f"  - {f.name} (0 B)" for f in empty_files)
        except Exception as e:
            return f"{Fore.RED}Error finding empty files: {str(e)}{Style.RESET_ALL}"

    def _find_empty_directories(self) -> str:
        """Find empty directories in current directory."""
        try:
            empty_dirs = [d for d in self.current_path.rglob("*") 
                         if d.is_dir() and not any(d.iterdir())]
            
            if not empty_dirs:
                return f"{Fore.GREEN}No empty directories found.{Style.RESET_ALL}"
            
            return f"{Fore.CYAN}Found empty directories:{Style.RESET_ALL}\n" + \
                   "\n".join(f"  - {d.name}/ (0 B)" for d in empty_dirs)
        except Exception as e:
            return f"{Fore.RED}Error finding empty directories: {str(e)}{Style.RESET_ALL}"
