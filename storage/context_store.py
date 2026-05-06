"""Context Store"""

import json
from pathlib import Path
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContextStore:
    """Stores and retrieves context information"""
    
    def __init__(self, store_path: Path):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Context store initialized at {self.store_path}")
    
    async def save_context_map(self, context: Dict[str, Any], output_file: Path):
        """Save context map to JSON file"""
        
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(context, f, indent=2, default=str)
            
            logger.info(f"Context map saved to {output_file}")
        
        except Exception as e:
            logger.error(f"Error saving context map: {e}")
            raise
    
    async def load_context_map(self, context_file: Path) -> Dict[str, Any]:
        """Load context map from JSON file"""
        
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                context = json.load(f)
            
            logger.info(f"Context map loaded from {context_file}")
            return context
        
        except Exception as e:
            logger.error(f"Error loading context map: {e}")
            raise
    
    async def save_entry(self, key: str, data: Dict[str, Any]):
        """Save individual context entry"""
        
        entry_file = self.store_path / f"{key}.json"
        
        try:
            with open(entry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        
        except Exception as e:
            logger.error(f"Error saving entry {key}: {e}")
    
    async def load_entry(self, key: str) -> Dict[str, Any]:
        """Load individual context entry"""
        
        entry_file = self.store_path / f"{key}.json"
        
        try:
            with open(entry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        except Exception as e:
            logger.error(f"Error loading entry {key}: {e}")
            return {}
