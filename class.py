import os
from pathlib import Path
import sys
import logging
from typing import List, Set, Dict, Tuple
from datetime import datetime, timedelta
import shutil
from colorama import init, Fore, Style
import json
import time

# Initialize colorama for cross-platform colored output
init()
start_dir = input("Enter the starting directory: ")
# Configure file logging
log_filename = f"file_operations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

# Directories to skip
SKIP_DIRS = {
    '.Trash',
    'Library',
    'node_modules',
    '.git',
    'venv',
    '.venv',
    '__pycache__',
    'empty-dirs'  # Skip our own empty-dirs folder
}

class DirectoryAnalyzer:
    def __init__(self):
        self.start_time = datetime.now()
        self.dirs_processed = 0
        self.total_dirs = 0
        self.last_status_time = time.time()
        self.start_dir = start_dir  # Initialize with the input directory
        self.target_dir = os.path.join(os.getcwd(), 'empty-dirs')  # Create target directory in current working directory
        
        # Create target directory if it doesn't exist
        os.makedirs(self.target_dir, exist_ok=True)
        logging.info(f"Initialized DirectoryAnalyzer with start_dir: {self.start_dir}")
        logging.info(f"Target directory for empty dirs: {self.target_dir}")

    def count_and_create_directories(self):
        """First phase: Count and create all directories"""
        print("\nPhase 1: Creating Directory Structure...")
        
        try:
            # First pass: Count total directories
            print("Counting directories...")
            for root, dirs, _ in os.walk(self.start_dir):
                if any(skip_dir in root for skip_dir in SKIP_DIRS):
                    continue
                self.total_dirs += len(dirs)
            
            print(f"Found {self.total_dirs:,} directories to process")
            
            # Second pass: Create directories
            for root, dirs, _ in os.walk(self.start_dir):
                if any(skip_dir in root for skip_dir in SKIP_DIRS):
                    continue
                
                for dir_name in dirs:
                    self.dirs_processed += 1
                    source_path = os.path.join(root, dir_name)
                    target_path = os.path.join(
                        self.target_dir, 
                        os.path.relpath(source_path, self.start_dir)
                    )
                    
                    try:
                        os.makedirs(target_path, exist_ok=True)
                    except OSError as e:
                        print(f"Error creating directory {target_path}: {e}")
                    
                    # Log progress every 5 seconds
                    self.log_directory_status()
            
            print("\nDirectory structure created successfully!")
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Directory creation cancelled by user.{Style.RESET_ALL}")
            return False

    def log_directory_status(self):
        """Log directory creation progress every 5 seconds"""
        current_time = time.time()
        if current_time - self.last_status_time >= 5:
            percent_complete = (self.dirs_processed / self.total_dirs * 100) if self.total_dirs > 0 else 0
            print(f"\rCreating Directories: {self.dirs_processed:,} / {self.total_dirs:,} ({percent_complete:.1f}%)", end="")
            self.last_status_time = current_time

    def analyze_directories(self):
        """Main method that coordinates the two phases"""
        try:
            # Phase 1: Create directory structure
            if not self.count_and_create_directories():
                return None, None

            # Phase 2: Process files (existing code)
            print("\nPhase 2: Processing Files...")
            # ... rest of your existing analyze_directories code ...
            
        except Exception as e:
            logging.error(f"Error during directory analysis: {e}")
            return None, None

    def move_empty_dirs(self):
        """Move empty directories to the target location"""
        try:
            logging.info("Starting to move empty directories...")
            empty_dirs_moved = 0
            
            for root, dirs, files in os.walk(self.start_dir, topdown=False):
                if any(skip_dir in root for skip_dir in SKIP_DIRS):
                    continue
                    
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    # Check if directory is empty (no files and no subdirectories)
                    if not os.listdir(dir_path):
                        try:
                            # Create relative path to maintain directory structure
                            rel_path = os.path.relpath(dir_path, self.start_dir)
                            target_path = os.path.join(self.target_dir, rel_path)
                            
                            # Create parent directories if they don't exist
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            
                            # Move the empty directory
                            shutil.move(dir_path, target_path)
                            empty_dirs_moved += 1
                            logging.info(f"Moved empty directory: {dir_path} -> {target_path}")
                            
                        except (OSError, shutil.Error) as e:
                            logging.error(f"Error moving directory {dir_path}: {e}")
            
            logging.info(f"Finished moving {empty_dirs_moved} empty directories")
            return empty_dirs_moved
            
        except Exception as e:
            logging.error(f"Error in move_empty_dirs: {e}")
            return 0

    def print_summary(self):
        """Print a summary of the operations performed"""
        try:
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            print(f"\n{'='*80}")
            print(f"Directory Analysis Summary")
            print(f"{'='*80}")
            print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Duration: {duration}")
            print(f"Total directories processed: {self.dirs_processed:,}")
            print(f"Results written to: all_dirs.txt and directory_stats.json")
            print(f"Log file: {log_filename}")
            print(f"{'='*80}\n")
            
        except Exception as e:
            logging.error(f"Error printing summary: {e}")

def main():
    try:
        print(f"\n{'='*80}")
        print(f"Directory Analysis Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        analyzer = DirectoryAnalyzer()
        all_files, dir_stats = analyzer.analyze_directories()
        
        if all_files is None:  # Early exit if directory creation failed
            return
            
        # Write results to files
        with open('all_dirs.txt', 'w', encoding='utf-8') as f:
            for item in sorted(all_files):
                f.write(f"{item}\n")
        
        # Save detailed statistics to JSON
        with open('directory_stats.json', 'w', encoding='utf-8') as f:
            json.dump(dir_stats, f, indent=2)
        
        # Move empty directories
        analyzer.move_empty_dirs()
        
        # Print summary
        analyzer.print_summary()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        logging.error(f"Program terminated with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
