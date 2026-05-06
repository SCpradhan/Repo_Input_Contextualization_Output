"""Dependency Analyzer Agent"""

import re
from pathlib import Path
from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class DependencyAnalyzer(BaseAgent):
    """Analyzes project dependencies across different languages"""
    
    DEPENDENCY_FILES = {
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'javascript': ['package.json', 'yarn.lock', 'package-lock.json'],
        'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
        'ruby': ['Gemfile', 'Gemfile.lock'],
        'go': ['go.mod', 'go.sum'],
        'rust': ['Cargo.toml', 'Cargo.lock'],
        'php': ['composer.json', 'composer.lock'],
    }
    
    async def analyze(self, parsed_files: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze dependencies from parsed files"""
        
        dependencies = []
        
        for file_data in parsed_files:
            file_path = Path(file_data['path'])
            
            # Check if this is a dependency file
            for lang, dep_files in self.DEPENDENCY_FILES.items():
                if file_path.name in dep_files:
                    deps = await self._parse_dependency_file(
                        file_path, 
                        file_data.get('content', ''),
                        lang
                    )
                    dependencies.extend(deps)
        
        # Deduplicate and enrich
        unique_deps = self._deduplicate_dependencies(dependencies)
        
        return unique_deps
    
    async def _parse_dependency_file(self, file_path: Path, content: str, lang: str) -> List[Dict]:
        """Parse specific dependency file format"""
        
        if lang == 'python':
            return self._parse_python_deps(content, file_path.name)
        elif lang == 'javascript':
            return self._parse_javascript_deps(content, file_path.name)
        elif lang == 'java':
            return self._parse_java_deps(content, file_path.name)
        elif lang == 'go':
            return self._parse_go_deps(content)
        elif lang == 'rust':
            return self._parse_rust_deps(content)
        
        return []
    
    def _parse_python_deps(self, content: str, filename: str) -> List[Dict]:
        """Parse Python dependencies"""
        deps = []
        
        if filename == 'requirements.txt':
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    match = re.match(r'^([a-zA-Z0-9\-_]+)([>=<~!]+)?(.+)?', line)
                    if match:
                        deps.append({
                            'name': match.group(1),
                            'version': match.group(3) if match.group(3) else 'latest',
                            'type': 'python',
                            'source': filename
                        })
        
        elif 'pyproject.toml' in filename:
            # Simple regex-based parsing for dependencies section
            in_deps = False
            for line in content.split('\n'):
                if '[tool.poetry.dependencies]' in line or '[project.dependencies]' in line:
                    in_deps = True
                elif line.startswith('[') and in_deps:
                    in_deps = False
                elif in_deps and '=' in line:
                    match = re.match(r'^([a-zA-Z0-9\-_]+)\s*=', line)
                    if match:
                        deps.append({
                            'name': match.group(1),
                            'version': 'specified',
                            'type': 'python',
                            'source': filename
                        })
        
        return deps
    
    def _parse_javascript_deps(self, content: str, filename: str) -> List[Dict]:
        """Parse JavaScript/Node dependencies"""
        deps = []
        
        if filename == 'package.json':
            import json
            try:
                data = json.loads(content)
                for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                    if dep_type in data:
                        for name, version in data[dep_type].items():
                            deps.append({
                                'name': name,
                                'version': version,
                                'type': 'javascript',
                                'category': dep_type,
                                'source': filename
                            })
            except json.JSONDecodeError:
                pass
        
        return deps
    
    def _parse_java_deps(self, content: str, filename: str) -> List[Dict]:
        """Parse Java dependencies"""
        deps = []
        
        if 'pom.xml' in filename:
            # Simple regex for Maven dependencies
            pattern = r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>.*?<version>(.*?)</version>'
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                deps.append({
                    'name': f"{match[0]}:{match[1]}",
                    'version': match[2],
                    'type': 'java',
                    'source': filename
                })
        
        elif 'build.gradle' in filename:
            # Simple regex for Gradle dependencies
            pattern = r"implementation\s+['\"]([^:]+):([^:]+):([^'\"]+)['\"]"
            matches = re.findall(pattern, content)
            for match in matches:
                deps.append({
                    'name': f"{match[0]}:{match[1]}",
                    'version': match[2],
                    'type': 'java',
                    'source': filename
                })
        
        return deps
    
    def _parse_go_deps(self, content: str) -> List[Dict]:
        """Parse Go dependencies"""
        deps = []
        pattern = r'require\s+([^\s]+)\s+([^\s]+)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            deps.append({
                'name': match[0],
                'version': match[1],
                'type': 'go',
                'source': 'go.mod'
            })
        
        return deps
    
    def _parse_rust_deps(self, content: str) -> List[Dict]:
        """Parse Rust dependencies"""
        deps = []
        in_deps = False
        
        for line in content.split('\n'):
            if line.strip() == '[dependencies]':
                in_deps = True
            elif line.startswith('[') and in_deps:
                in_deps = False
            elif in_deps and '=' in line:
                match = re.match(r'^([a-zA-Z0-9\-_]+)\s*=\s*["\']([^"\']+)["\']', line)
                if match:
                    deps.append({
                        'name': match.group(1),
                        'version': match.group(2),
                        'type': 'rust',
                        'source': 'Cargo.toml'
                    })
        
        return deps
    
    def _deduplicate_dependencies(self, dependencies: List[Dict]) -> List[Dict]:
        """Remove duplicate dependencies"""
        seen = set()
        unique = []
        
        for dep in dependencies:
            key = (dep['name'], dep['type'])
            if key not in seen:
                seen.add(key)
                unique.append(dep)
        
        return unique
