"""Semantic Analyzer Agent"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class SemanticAnalyzer(BaseAgent):
    """Performs semantic analysis using embeddings and LLM"""
    
    def __init__(self, config: Dict[str, Any], vector_store):
        super().__init__(config)
        self.vector_store = vector_store
    
    async def analyze(self, parsed_files: List[Dict]) -> Dict[str, Any]:
        """Perform semantic analysis on code"""
        
        semantic_data = {
            'code_chunks': [],
            'embeddings_created': 0,
            'key_concepts': [],
            'documentation_coverage': 0.0
        }
        
        total_files = len(parsed_files)
        documented_files = 0
        
        for file_data in parsed_files:
            content = file_data.get('content', '')
            path = file_data.get('path', '')
            
            # Check for documentation
            if self._has_documentation(content):
                documented_files += 1
            
            # Create chunks for embedding
            chunks = self._create_chunks(content, path)
            semantic_data['code_chunks'].extend(chunks)
            
            # Store embeddings (async operation)
            await self._store_embeddings(chunks)
            semantic_data['embeddings_created'] += len(chunks)
        
        # Calculate documentation coverage
        if total_files > 0:
            semantic_data['documentation_coverage'] = documented_files / total_files
        
        # Extract key concepts
        semantic_data['key_concepts'] = self._extract_concepts(parsed_files)
        
        return semantic_data
    
    def _has_documentation(self, content: str) -> bool:
        """Check if file has documentation"""
        doc_indicators = ['"""', "'''", '/**', '///', '##']
        return any(indicator in content for indicator in doc_indicators)
    
    def _create_chunks(self, content: str, path: str) -> List[Dict]:
        """Create semantic chunks from content"""
        chunk_size = self.config.get('contextualization', {}).get('chunk_size', 1000)
        chunk_overlap = self.config.get('contextualization', {}).get('chunk_overlap', 200)
        
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        
        for line in lines:
            current_chunk.append(line)
            current_size += len(line)
            
            if current_size >= chunk_size:
                chunks.append({
                    'content': '\n'.join(current_chunk),
                    'file': path,
                    'size': current_size
                })
                
                # Keep overlap
                overlap_lines = int(len(current_chunk) * (chunk_overlap / chunk_size))
                current_chunk = current_chunk[-overlap_lines:] if overlap_lines > 0 else []
                current_size = sum(len(line) for line in current_chunk)
        
        # Add remaining chunk
        if current_chunk:
            chunks.append({
                'content': '\n'.join(current_chunk),
                'file': path,
                'size': current_size
            })
        
        return chunks
    
    async def _store_embeddings(self, chunks: List[Dict]):
        """Store chunks in vector store"""
        # This would integrate with actual vector store
        # For now, just pass through
        await self.vector_store.add_chunks(chunks)
    
    def _extract_concepts(self, parsed_files: List[Dict]) -> List[str]:
        """Extract key concepts from code"""
        concepts = set()
        
        # Simple keyword-based extraction
        keywords = ['authentication', 'authorization', 'database', 'api', 'service',
                   'controller', 'model', 'view', 'repository', 'cache', 'queue',
                   'payment', 'user', 'admin', 'security', 'logging', 'monitoring']
        
        for file_data in parsed_files:
            content = file_data.get('content', '').lower()
            for keyword in keywords:
                if keyword in content:
                    concepts.add(keyword)
        
        return sorted(list(concepts))
