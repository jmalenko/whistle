#!/usr/bin/env python3
"""File watcher to auto-run whistle.py on save"""
import sys
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CodeReloader(FileSystemEventHandler):
    def __init__(self, script_path, python_path):
        self.script_path = script_path
        self.python_path = python_path
        self.last_run = 0
        
    def on_modified(self, event):
        if event.src_path.endswith('whistle.py'):
            # Debounce: prevent multiple runs
            current_time = time.time()
            if current_time - self.last_run < 0.5:
                return
            self.last_run = current_time
            
            print(f"\n{'='*60}")
            print(f"File changed: {event.src_path}")
            print(f"Running {self.script_path}...")
            print(f"{'='*60}\n")
            
            try:
                result = subprocess.run(
                    [self.python_path, self.script_path],
                    capture_output=False,
                    text=True
                )
                if result.returncode == 0:
                    print(f"\n✓ Success!")
                else:
                    print(f"\n✗ Exit code: {result.returncode}")
            except Exception as e:
                print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    script_path = Path(__file__).parent / "whistle.py"
    python_path = sys.executable
    
    print(f"Watching: {script_path}")
    print(f"Python: {python_path}")
    print("Press Ctrl+C to stop\n")
    
    event_handler = CodeReloader(script_path, python_path)
    observer = Observer()
    observer.schedule(event_handler, path=str(script_path.parent), recursive=False)
    observer.start()
    
    # Run once at start
    subprocess.run([python_path, script_path])
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching.")
    observer.join()
