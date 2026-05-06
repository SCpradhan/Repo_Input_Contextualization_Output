"""Structure Analyzer Agent"""

import re
from typing import Dict, Any, List
from collections import defaultdict
from agents.base_agent import BaseAgent


class StructureAnalyzer(BaseAgent):
    """Analyzes code structure - classes, functions, modules"""
    
    async def analyze(self, parsed_files: List[Dict]) -> Dict[str, Any]:
        """Analyze code structure"""
        
        structure = {
            'modules': [],
            'classes': [],
            'functions': [],
            'imports': [],
            'statistics': defaultdict(int),
            'architecture_patterns': []
        }
        
        for file_data in parsed_files:
            file_type = file_data.get('type', '')
            content = file_data.get('content', '')
            path = file_data.get('path', '')
            
            if file_type == 'python':
                self._analyze_python_structure(content, path, structure)
            elif file_type in ['javascript', 'typescript']:
                self._analyze_javascript_structure(content, path, structure)
            elif file_type == 'java':
                self._analyze_java_structure(content, path, structure)
        
        # Detect architecture patterns
        structure['architecture_patterns'] = self._detect_patterns(structure)
        
        return structure
    
    def _analyze_python_structure(self, content: str, path: str, structure: Dict):
        """Analyze Python file structure"""
        
        # Find classes
        class_pattern = r'class\s+(\w+)(?:\(([^)]*)\))?:'
        for match in re.finditer(class_pattern, content):
            structure['classes'].append({
                'name': match.group(1),
                'parent': match.group(2) if match.group(2) else None,
                'file': path,
                'language': 'python'
            })
            structure['statistics']['total_classes'] += 1
        
        # Find functions
        func_pattern = r'def\s+(\w+)\s*\('
        for match in re.finditer(func_pattern, content):
            structure['functions'].append({
                'name': match.group(1),
                'file': path,
                'language': 'python'
            })
            structure['statistics']['total_functions'] += 1
        
        # Find imports
        import_pattern = r'(?:from\s+(\S+)\s+)?import\s+([^#\n]+)'
        for match in re.finditer(import_pattern, content):
            structure['imports'].append({
                'module': match.group(1) if match.group(1) else match.group(2).split()[0],
                'file': path,
                'language': 'python'
            })
    
    def _analyze_javascript_structure(self, content: str, path: str, structure: Dict):
        """Analyze JavaScript/TypeScript structure"""
        
        # Find classes
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        for match in re.finditer(class_pattern, content):
            structure['classes'].append({
                'name': match.group(1),
                'parent': match.group(2) if match.group(2) else None,
                'file': path,
                'language': 'javascript'
            })
            structure['statistics']['total_classes'] += 1
        
        # Find functions
        func_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*(?:async\s+)?function\s*\('
        ]
        
        for pattern in func_patterns:
            for match in re.finditer(pattern, content):
                structure['functions'].append({
                    'name': match.group(1),
                    'file': path,
                    'language': 'javascript'
                })
                structure['statistics']['total_functions'] += 1
        
        # Find imports
        import_patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                structure['imports'].append({
                    'module': match.group(1),
                    'file': path,
                    'language': 'javascript'
                })
    
    def _analyze_java_structure(self, content: str, path: str, structure: Dict):
        """Analyze Java structure"""
        
        # Find classes
        class_pattern = r'(?:public\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?'
        for match in re.finditer(class_pattern, content):
            structure['classes'].append({
                'name': match.group(1),
                'parent': match.group(2) if match.group(2) else None,
                'file': path,
                'language': 'java'
            })
            structure['statistics']['total_classes'] += 1
        
        # Find methods
        method_pattern = r'(?:public|private|protected)\s+(?:static\s+)?(?:\w+)\s+(\w+)\s*\('
        for match in re.finditer(method_pattern, content):
            structure['functions'].append({
                'name': match.group(1),
                'file': path,
                'language': 'java'
            })
            structure['statistics']['total_functions'] += 1
        
        # Find imports
        import_pattern = r'import\s+([^;]+);'
        for match in re.finditer(import_pattern, content):
            structure['imports'].append({
                'module': match.group(1),
                'file': path,
                'language': 'java'
            })
    
    def _detect_patterns(self, structure: Dict) -> List[str]:
        """Detect common architecture patterns"""
        patterns = []
        
        # Check for MVC pattern
        files_str = ' '.join([c['file'].lower() for c in structure['classes']])
        if 'controller' in files_str and 'model' in files_str and 'view' in files_str:
            patterns.append('MVC')
        
        # Check for Repository pattern
        if any('repository' in c['name'].lower() for c in structure['classes']):
            patterns.append('Repository Pattern')
        
        # Check for Service layer
        if any('service' in c['name'].lower() for c in structure['classes']):
            patterns.append('Service Layer')
        
        # Check for Factory pattern
        if any('factory' in c['name'].lower() for c in structure['classes']):
            patterns.append('Factory Pattern')
        
        return patterns
