"""
Main Orchestrator
Coordinates all agents and manages the ingestion pipeline
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from ingestion.repository_scanner import RepositoryScanner
from ingestion.file_parser import FileParser
from agents.dependency_analyzer import DependencyAnalyzer
from agents.structure_analyzer import StructureAnalyzer
from agents.semantic_analyzer import SemanticAnalyzer
from agents.sdlc_detector import SDLCDetector
from agents.context_synthesizer import ContextSynthesizer
from storage.context_store import ContextStore
from storage.vector_store import VectorStore
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Orchestrator:
    """
    Main orchestration engine that coordinates all agents
    and manages the contextualization pipeline
    """
    
    def __init__(self, config: Dict[str, Any], output_path: Path):
        self.config = config
        self.output_path = output_path
        
        # Initialize storage
        self.context_store = ContextStore(output_path / "context_store")
        self.vector_store = VectorStore(output_path / "vector_store")
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        logger.info("Orchestrator initialized")
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents based on configuration"""
        return {
            'scanner': RepositoryScanner(self.config),
            'dependency_analyzer': DependencyAnalyzer(self.config),
            'structure_analyzer': StructureAnalyzer(self.config),
            'semantic_analyzer': SemanticAnalyzer(self.config, self.vector_store),
            'sdlc_detector': SDLCDetector(self.config),
            'context_synthesizer': ContextSynthesizer(self.config, self.context_store),
        }
    
    async def process_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Main entry point - processes entire repository through the pipeline
        """
        logger.info(f"Starting repository processing: {repo_path}")
        start_time = datetime.now()
        
        # Stage 1: Scan repository
        logger.info("Stage 1: Scanning repository structure")
        scan_result = await self.agents['scanner'].scan(repo_path)
        
        # Stage 2: Parse files
        logger.info("Stage 2: Parsing files")
        parser = FileParser(self.config)
        parsed_files = await parser.parse_files(scan_result['files'])
        
        # Stage 3: Run parallel analysis
        logger.info("Stage 3: Running parallel analysis")
        analysis_results = await self._run_parallel_analysis(parsed_files)
        
        # Stage 4: Detect SDLC artifacts
        logger.info("Stage 4: Detecting SDLC artifacts")
        sdlc_artifacts = await self.agents['sdlc_detector'].detect(
            parsed_files, 
            scan_result
        )
        
        # Stage 5: Synthesize context
        logger.info("Stage 5: Synthesizing context")
        context = await self.agents['context_synthesizer'].synthesize({
            'scan_result': scan_result,
            'parsed_files': parsed_files,
            'analysis': analysis_results,
            'sdlc_artifacts': sdlc_artifacts,
        })
        
        # Stage 6: Generate outputs
        logger.info("Stage 6: Generating outputs")
        await self._generate_outputs(context)
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Repository processing complete in {duration:.2f}s")
        
        return {
            'files_analyzed': len(parsed_files),
            'languages': scan_result.get('languages', []),
            'dependencies_count': len(analysis_results.get('dependencies', [])),
            'context_entries': len(context.get('entries', [])),
            'duration_seconds': duration,
        }
    
    async def _run_parallel_analysis(self, parsed_files: List[Dict]) -> Dict[str, Any]:
        """Run multiple analyzers in parallel"""
        
        tasks = [
            self.agents['dependency_analyzer'].analyze(parsed_files),
            self.agents['structure_analyzer'].analyze(parsed_files),
            self.agents['semantic_analyzer'].analyze(parsed_files),
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            'dependencies': results[0],
            'structure': results[1],
            'semantics': results[2],
        }
    
    async def _generate_outputs(self, context: Dict[str, Any]):
        """Generate all output artifacts"""
        
        # Save context map
        await self.context_store.save_context_map(
            context, 
            self.output_path / "context_map.json"
        )
        
        # Generate analysis report
        await self._generate_report(context, self.output_path / "analysis_report.md")
        
        logger.info("Outputs generated successfully")
    
    async def _generate_report(self, context: Dict[str, Any], output_file: Path):
        """Generate human-readable analysis report"""
        
        report_lines = [
            "# Repository Analysis Report",
            f"\nGenerated: {datetime.now().isoformat()}",
            "\n## Overview",
            f"\n- **Repository**: {context.get('repository_name', 'Unknown')}",
            f"- **Total Files**: {context.get('total_files', 0)}",
            f"- **Languages**: {', '.join(context.get('languages', []))}",
            f"- **Lines of Code**: {context.get('total_loc', 0):,}",
            "\n## Project Structure",
            f"\n{context.get('structure_summary', 'No structure information available')}",
            "\n## Dependencies",
            f"\n{self._format_dependencies(context.get('dependencies', []))}",
            "\n## SDLC Artifacts",
            f"\n{self._format_sdlc_artifacts(context.get('sdlc_artifacts', {}))}",
            "\n## Key Insights",
            f"\n{self._format_insights(context.get('insights', []))}",
            "\n## Recommendations",
            f"\n{self._format_recommendations(context.get('recommendations', []))}",
        ]
        
        output_file.write_text('\n'.join(report_lines))
    
    def _format_dependencies(self, dependencies: List[Dict]) -> str:
        """Format dependencies section"""
        if not dependencies:
            return "No dependencies detected."
        
        lines = []
        for dep in dependencies[:10]:  # Top 10
            lines.append(f"- **{dep.get('name')}** ({dep.get('type', 'unknown')})")
        
        if len(dependencies) > 10:
            lines.append(f"\n... and {len(dependencies) - 10} more")
        
        return '\n'.join(lines)
    
    def _format_sdlc_artifacts(self, artifacts: Dict) -> str:
        """Format SDLC artifacts section"""
        lines = []
        for artifact_type, items in artifacts.items():
            if artifact_type == 'test_coverage':
                continue  # Skip test_coverage as it's a dict, not a list
            lines.append(f"\n### {artifact_type.title()}")
            if items and isinstance(items, list):
                for item in items[:5]:
                    if isinstance(item, dict):
                        lines.append(f"- {item.get('name', 'Unknown')}")
                    else:
                        lines.append(f"- {item}")
            else:
                lines.append("- None detected")
        
        return '\n'.join(lines) if lines else "No SDLC artifacts detected."
    
    def _format_insights(self, insights: List[str]) -> str:
        """Format insights section"""
        if not insights:
            return "No specific insights generated."
        
        return '\n'.join([f"- {insight}" for insight in insights])
    
    def _format_recommendations(self, recommendations: List[str]) -> str:
        """Format recommendations section"""
        if not recommendations:
            return "No specific recommendations."
        
        return '\n'.join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])
