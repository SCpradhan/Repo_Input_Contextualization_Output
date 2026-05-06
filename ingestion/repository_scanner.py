"""Repository Scanner"""

import os
from pathlib import Path
from typing import Dict, Any, List
import fnmatch
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RepositoryScanner:
    """Scans repository structure and identifies files"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ignore_patterns = config.get('ingestion', {}).get('ignore_patterns', [])
        self.max_file_size = config.get('ingestion', {}).get('max_file_size_mb', 10) * 1024 * 1024
    
    async def scan(self, repo_path: str) -> Dict[str, Any]:
        """Scan repository and return file inventory"""
        
        repo_path = Path(repo_path).resolve()
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        logger.info(f"Scanning repository: {repo_path}")
        
        files = []
        languages = set()
        total_size = 0
        total_loc = 0
        
        for root, dirs, filenames in os.walk(repo_path):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Skip ignored files
                if self._should_ignore(str(file_path)):
                    continue
                
                # Skip files that are too large
                try:
                    file_size = file_path.stat().st_size
                    if file_size > self.max_file_size:
                        logger.warning(f"Skipping large file: {file_path} ({file_size} bytes)")
                        continue
                except OSError:
                    continue
                
                # Determine file type
                file_type = self._detect_file_type(filename)
                
                if file_type:
                    languages.add(file_type)
                
                relative_path = file_path.relative_to(repo_path)
                
                files.append({
                    'path': str(relative_path),
                    'absolute_path': str(file_path),
                    'type': file_type,
                    'size': file_size,
                    'extension': file_path.suffix
                })
                
                total_size += file_size
        
        logger.info(f"Scan complete: {len(files)} files, {len(languages)} languages")
        
        return {
            'repository_path': str(repo_path),
            'repository_name': repo_path.name,
            'files': files,
            'total_files': len(files),
            'languages': sorted(list(languages)),
            'total_size': total_size,
            'total_loc': total_loc
        }
    
    def _should_ignore(self, path: str) -> bool:
        """Check if path should be ignored"""
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(Path(path).name, pattern):
                return True
        return False
    
    def _detect_file_type(self, filename: str) -> str:
        """Detect programming language from filename"""
        
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'shell',
            '.bash': 'shell',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.md': 'markdown',
            '.txt': 'text',
            '.sql': 'sql',
        }
        
        ext = Path(filename).suffix.lower()
        return extension_map.get(ext, 'unknown')
