"""File Parser"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FileParser:
    """Parses files and extracts content"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.batch_size = config.get('ingestion', {}).get('batch_size', 100)
    
    async def parse_files(self, files: List[Dict]) -> List[Dict]:
        """Parse all files in batches"""
        
        logger.info(f"Parsing {len(files)} files")
        
        parsed_files = []
        
        # Process in batches
        for i in range(0, len(files), self.batch_size):
            batch = files[i:i + self.batch_size]
            batch_results = await asyncio.gather(
                *[self._parse_file(file_info) for file_info in batch],
                return_exceptions=True
            )
            
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Error parsing file: {result}")
                elif result:
                    parsed_files.append(result)
        
        logger.info(f"Parsed {len(parsed_files)} files successfully")
        
        return parsed_files
    
    async def _parse_file(self, file_info: Dict) -> Dict[str, Any]:
        """Parse a single file"""
        
        file_path = Path(file_info['absolute_path'])
        
        try:
            # Read file content
            content = await self._read_file(file_path)
            
            # Count lines of code
            loc = len([line for line in content.split('\n') if line.strip()])
            
            return {
                'path': file_info['path'],
                'type': file_info['type'],
                'content': content,
                'size': file_info['size'],
                'loc': loc,
                'extension': file_info['extension']
            }
        
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None
    
    async def _read_file(self, file_path: Path) -> str:
        """Read file content with encoding detection"""
        
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                return file_path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")
                return ""
        
        # If all encodings fail, try binary mode
        try:
            return file_path.read_bytes().decode('utf-8', errors='ignore')
        except Exception:
            return ""
