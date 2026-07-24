import os
import pathspec
from loguru import logger
from typing import List

class RepositoryScanner:
    """Scans the repository and yields files ignoring binary and .gitignore matches."""
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.ignore_spec = self._load_gitignore()

        # Binary/unsupported extensions to skip
        self.skip_extensions = {
            ".exe", ".dll", ".so", ".dylib", ".png", ".jpg", ".jpeg", ".gif", 
            ".ico", ".pdf", ".zip", ".tar", ".gz", ".pyc", ".db", ".sqlite3"
        }
        
        # Directories to skip regardless of gitignore
        self.skip_dirs = {
            ".git", ".venv", "venv", "node_modules", "__pycache__", ".chroma", "dist", "build"
        }

    def _load_gitignore(self) -> pathspec.PathSpec:
        """Parse .gitignore to skip unneeded files."""
        gitignore_path = os.path.join(self.root_path, ".gitignore")
        lines = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, lines)

    def scan(self) -> List[str]:
        """Walks the directory, yielding valid file paths."""
        valid_files = []
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            # Mutate dirnames to avoid walking skipped dirs
            dirnames[:] = [d for d in dirnames if d not in self.skip_dirs]

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, self.root_path)

                # Check extensions
                _, ext = os.path.splitext(filename)
                if ext.lower() in self.skip_extensions:
                    continue

                # Check gitignore
                if self.ignore_spec.match_file(rel_path):
                    continue

                valid_files.append(file_path)
                
        logger.info(f"Scanned {len(valid_files)} valid files in repository.")
        return valid_files

    def read_file_content(self, filepath: str) -> str:
        """Safely read a file, ignoring encoding errors."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            return ""
