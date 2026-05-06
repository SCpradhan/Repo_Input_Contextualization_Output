"""Context Synthesizer Agent"""

from typing import Dict, Any, List
from datetime import datetime
from agents.base_agent import BaseAgent


class ContextSynthesizer(BaseAgent):
    """Synthesizes all analysis into unified context"""
    
    def __init__(self, config: Dict[str, Any], context_store):
        super().__init__(config)
        self.context_store = context_store
    
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Main analysis method - delegates to synthesize"""
        return await self.synthesize(data)
    
    async def synthesize(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all analysis into unified context"""
        
        scan_result = analysis_data.get('scan_result', {})
        parsed_files = analysis_data.get('parsed_files', [])
        analysis = analysis_data.get('analysis', {})
        sdlc_artifacts = analysis_data.get('sdlc_artifacts', {})
        
        context = {
            'timestamp': datetime.now().isoformat(),
            'repository_name': scan_result.get('repository_name', 'Unknown'),
            'total_files': len(parsed_files),
            'languages': scan_result.get('languages', []),
            'total_loc': scan_result.get('total_loc', 0),
            'entries': [],
            'dependencies': analysis.get('dependencies', []) if isinstance(analysis.get('dependencies'), list) else [],
            'structure': analysis.get('structure', {}),
            'semantics': analysis.get('semantics', {}),
            'sdlc_artifacts': sdlc_artifacts,
            'insights': [],
            'recommendations': [],
            'structure_summary': ''
        }
        
        # Generate insights
        context['insights'] = self._generate_insights(context)
        
        # Generate recommendations
        context['recommendations'] = self._generate_recommendations(context)
        
        # Create structure summary
        context['structure_summary'] = self._create_structure_summary(context)
        
        # Create context entries for each file
        for file_data in parsed_files:
            entry = {
                'file': file_data.get('path'),
                'type': file_data.get('type'),
                'size': len(file_data.get('content', '')),
                'summary': self._summarize_file(file_data, analysis)
            }
            context['entries'].append(entry)
        
        return context
    
    def _generate_insights(self, context: Dict) -> List[str]:
        """Generate insights from analysis"""
        insights = []
        
        # Language insights
        languages = context.get('languages', [])
        if len(languages) > 1:
            insights.append(f"Multi-language project using {', '.join(languages)}")
        elif languages:
            insights.append(f"Single-language project using {languages[0]}")
        
        # Dependency insights
        deps = context.get('dependencies', [])
        if len(deps) > 50:
            insights.append(f"Large dependency footprint with {len(deps)} dependencies")
        elif len(deps) > 0:
            insights.append(f"Moderate dependency footprint with {len(deps)} dependencies")
        
        # Test coverage insights
        test_coverage = context.get('sdlc_artifacts', {}).get('test_coverage', {})
        if test_coverage.get('has_tests'):
            ratio = test_coverage.get('test_ratio', 0)
            if ratio > 0.3:
                insights.append(f"Good test coverage with {ratio:.1%} test-to-code ratio")
            else:
                insights.append(f"Limited test coverage with {ratio:.1%} test-to-code ratio")
        else:
            insights.append("No automated tests detected")
        
        # Architecture insights
        patterns = context.get('structure', {}).get('architecture_patterns', [])
        if patterns:
            insights.append(f"Uses architectural patterns: {', '.join(patterns)}")
        
        # Documentation insights
        doc_coverage = context.get('semantics', {}).get('documentation_coverage', 0)
        if doc_coverage > 0.5:
            insights.append(f"Well-documented codebase ({doc_coverage:.1%} coverage)")
        elif doc_coverage > 0:
            insights.append(f"Partially documented codebase ({doc_coverage:.1%} coverage)")
        
        return insights
    
    def _generate_recommendations(self, context: Dict) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        # Test recommendations
        test_coverage = context.get('sdlc_artifacts', {}).get('test_coverage', {})
        if not test_coverage.get('has_tests'):
            recommendations.append("Add automated testing framework and write unit tests")
        elif test_coverage.get('test_ratio', 0) < 0.3:
            recommendations.append("Increase test coverage to improve code reliability")
        
        # Documentation recommendations
        doc_coverage = context.get('semantics', {}).get('documentation_coverage', 0)
        if doc_coverage < 0.3:
            recommendations.append("Add inline documentation and docstrings to improve maintainability")
        
        # CI/CD recommendations
        ci_cd_artifacts = context.get('sdlc_artifacts', {}).get('ci_cd', [])
        if not ci_cd_artifacts:
            recommendations.append("Set up CI/CD pipeline for automated testing and deployment")
        
        # Dependency recommendations
        deps = context.get('dependencies', [])
        if len(deps) > 100:
            recommendations.append("Review and consolidate dependencies to reduce complexity")
        
        # Architecture recommendations
        structure = context.get('structure', {})
        total_functions = structure.get('statistics', {}).get('total_functions', 0)
        total_classes = structure.get('statistics', {}).get('total_classes', 0)
        
        if total_functions > 500 and total_classes < 50:
            recommendations.append("Consider refactoring into more modular, object-oriented structure")
        
        return recommendations
    
    def _create_structure_summary(self, context: Dict) -> str:
        """Create human-readable structure summary"""
        structure = context.get('structure', {})
        stats = structure.get('statistics', {})
        
        lines = [
            f"- Total Classes: {stats.get('total_classes', 0)}",
            f"- Total Functions: {stats.get('total_functions', 0)}",
            f"- Total Imports: {len(structure.get('imports', []))}",
        ]
        
        patterns = structure.get('architecture_patterns', [])
        if patterns:
            lines.append(f"- Architecture Patterns: {', '.join(patterns)}")
        
        return '\n'.join(lines)
    
    def _summarize_file(self, file_data: Dict, analysis: Dict) -> str:
        """Create summary for a single file"""
        file_type = file_data.get('type', 'unknown')
        path = file_data.get('path', '')
        
        # Find relevant structure info
        structure = analysis.get('structure', {})
        classes = [c for c in structure.get('classes', []) if c['file'] == path]
        functions = [f for f in structure.get('functions', []) if f['file'] == path]
        
        summary_parts = []
        if classes:
            summary_parts.append(f"{len(classes)} classes")
        if functions:
            summary_parts.append(f"{len(functions)} functions")
        
        if summary_parts:
            return f"{file_type} file with {', '.join(summary_parts)}"
        else:
            return f"{file_type} file"
