"""
scripts/watch_jupytext.py
Watches for changes to .py and .ipynb files and runs `jupytext --sync`.
"""
import time
import subprocess
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Debounce window in seconds
DEBOUNCE_SECONDS = 1.0

class JupytextSyncHandler(FileSystemEventHandler):
    def __init__(self, root_dir: Path):
        super().__init__()
        self.root_dir = root_dir
        self.last_sync_times: dict[str, float] = {}

    def is_target(self, path: Path) -> bool:
        if path.suffix not in ('.py', '.ipynb'):
            return False
        # Ignore checkpoints, git, venv, caches
        parts = path.parts
        ignored = {'.ipynb_checkpoints', '.git', '__pycache__', '.venv', '.idea', '.vscode'}
        return not any(part in ignored for part in parts)

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path).resolve()
        if not self.is_target(file_path):
            return

        now = time.time()
        file_stem_key = str(file_path.with_suffix(''))

        # Prevent ping-pong loop: skip if paired leg was synced within DEBOUNCE_SECONDS
        if now - self.last_sync_times.get(file_stem_key, 0) < DEBOUNCE_SECONDS:
            return

        self.last_sync_times[file_stem_key] = now
        print(f"[Watcher] Change detected in {file_path.name}. Syncing pair...")

        try:
            # jupytext uses the existing jupytext.toml pairing configuration
            cmd = [sys.executable, "-m", "jupytext", "--sync", str(file_path)]
            result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[Watcher] Synced: {file_path.name}")
            else:
                print(f"[Watcher Error] {result.stderr.strip()}", file=sys.stderr)
        except Exception as e:
            print(f"[Watcher Exception] {e}", file=sys.stderr)

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    print(f"Starting Jupytext watcher on {project_root}...")
    event_handler = JupytextSyncHandler(project_root)
    observer = Observer()
    observer.schedule(event_handler, path=str(project_root), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
