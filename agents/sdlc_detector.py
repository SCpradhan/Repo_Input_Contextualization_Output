"""SDLC Artifact Detector Agent"""

from typing import Dict, Any, List
from pathlib import Path
from agents.base_agent import BaseAgent


class SDLCDetector(BaseAgent):
    """Detects SDLC artifacts: requirements, design, tests, docs"""
    
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Main analysis method - delegates to detect"""
        if isinstance(data, tuple) and len(data) == 2:
            return await self.detect(data[0], data[1])
        return await self.detect(data, {})
    
    ARTIFACT_PATTERNS = {
        'requirements': {
            'files': ['requirements.md', 'requirements.txt', 'REQUIREMENTS', 'specs.md'],
            'dirs': ['requirements', 'specs', 'specifications']
        },
        'design': {
            'files': ['design.md', 'architecture.md', 'DESIGN', 'ADR'],
            'dirs': ['design', 'architecture', 'docs/design', 'adr']
        },
        'tests': {
            'files': ['test_*.py', '*_test.py', '*.test.js', '*.spec.js', '*.test.ts'],
            'dirs': ['tests', 'test', '__tests__', 'spec']
        },
        'documentation': {
            'files': ['README.md', 'CONTRIBUTING.md', 'CHANGELOG.md', 'docs.md'],
            'dirs': ['docs', 'documentation', 'wiki']
        },
        'ci_cd': {
            'files': ['.gitlab-ci.yml', '.travis.yml', 'Jenkinsfile', 'azure-pipelines.yml'],
            'dirs': ['.github/workflows', '.circleci']
        },
        'configuration': {
            'files': ['config.yaml', 'config.json', '.env.example', 'settings.py'],
            'dirs': ['config', 'configuration', 'settings']
        }
    }
    
    async def detect(self, parsed_files: List[Dict], scan_result: Dict) -> Dict[str, List[Dict]]:
        """Detect SDLC artifacts in the repository"""
        
        artifacts = {
            'requirements': [],
            'design': [],
            'tests': [],
            'documentation': [],
            'ci_cd': [],
            'configuration': []
        }
        
        all_paths = [f['path'] for f in parsed_files]
        
        for artifact_type, patterns in self.ARTIFACT_PATTERNS.items():
            # Check files
            for file_pattern in patterns.get('files', []):
                matching_files = self._match_pattern(all_paths, file_pattern)
                for file_path in matching_files:
                    file_data = next((f for f in parsed_files if f['path'] == file_path), None)
                    if file_data:
                        artifacts[artifact_type].append({
                            'name': Path(file_path).name,
                            'path': file_path,
                            'type': 'file',
                            'size': len(file_data.get('content', ''))
                        })
            
            # Check directories
            for dir_pattern in patterns.get('dirs', []):
                matching_dirs = self._match_dir_pattern(all_paths, dir_pattern)
                for dir_path in matching_dirs:
                    artifacts[artifact_type].append({
                        'name': dir_path,
                        'path': dir_path,
                        'type': 'directory'
                    })
        
        # Analyze test coverage
        artifacts['test_coverage'] = self._analyze_test_coverage(artifacts['tests'], parsed_files)
        
        return artifacts
    
    def _match_pattern(self, paths: List[str], pattern: str) -> List[str]:
        """Match file pattern"""
        import fnmatch
        return [p for p in paths if fnmatch.fnmatch(Path(p).name, pattern)]
    
    def _match_dir_pattern(self, paths: List[str], pattern: str) -> List[str]:
        """Match directory pattern"""
        matching = set()
        for path in paths:
            parts = Path(path).parts
            for part in parts:
                if pattern in str(Path(*parts[:parts.index(part)+1])):
                    matching.add(str(Path(*parts[:parts.index(part)+1])))
        return list(matching)
    
    def _analyze_test_coverage(self, test_files: List[Dict], all_files: List[Dict]) -> Dict:
        """Analyze test coverage metrics"""
        
        total_code_files = len([f for f in all_files if f.get('type') in 
                               ['python', 'javascript', 'typescript', 'java']])
        total_test_files = len(test_files)
        
        return {
            'total_test_files': total_test_files,
            'total_code_files': total_code_files,
            'test_ratio': total_test_files / total_code_files if total_code_files > 0 else 0,
            'has_tests': total_test_files > 0
        }
