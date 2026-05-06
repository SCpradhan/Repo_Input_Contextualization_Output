"""Base agent class for all specialized agents"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Main analysis method - must be implemented by subclasses"""
        pass
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
