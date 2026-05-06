#!/usr/bin/env python3
"""
AAVA AI - Main Entry Point
Orchestrates the automatic repository ingestion and contextualization
"""

import asyncio
import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from orchestration.orchestrator import Orchestrator
from utils.logger import setup_logger
from utils.config import load_config

console = Console()
logger = setup_logger(__name__)


@click.command()
@click.option('--repo-path', required=True, type=click.Path(exists=True), 
              help='Path to the repository to analyze')
@click.option('--output', default='./output', type=click.Path(),
              help='Output directory for analysis results')
@click.option('--config', default='config.yaml', type=click.Path(exists=True),
              help='Configuration file path')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
def main(repo_path: str, output: str, config: str, verbose: bool):
    """
    AAVA AI - Automatic Repository Contextualization
    
    Ingests and analyzes a code repository to build comprehensive context.
    """
    console.print("[bold blue]🚀 AAVA AI - HP SDLC Agentic Framework[/bold blue]")
    console.print(f"[green]Repository:[/green] {repo_path}")
    console.print(f"[green]Output:[/green] {output}\n")
    
    # Load configuration
    cfg = load_config(config)
    
    # Setup output directory
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run orchestration
    asyncio.run(run_orchestration(repo_path, output_path, cfg, verbose))


async def run_orchestration(repo_path: str, output_path: Path, config: dict, verbose: bool):
    """Run the orchestration pipeline"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        task = progress.add_task("[cyan]Initializing orchestrator...", total=None)
        
        # Initialize orchestrator
        orchestrator = Orchestrator(config, output_path)
        
        progress.update(task, description="[cyan]Ingesting repository...")
        
        # Run the full pipeline
        result = await orchestrator.process_repository(repo_path)
        
        progress.update(task, description="[green]✓ Processing complete!")
    
    # Display results
    console.print("\n[bold green]Analysis Complete![/bold green]")
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Files analyzed: {result.get('files_analyzed', 0)}")
    console.print(f"  Languages detected: {', '.join(result.get('languages', []))}")
    console.print(f"  Dependencies found: {result.get('dependencies_count', 0)}")
    console.print(f"  Context entries: {result.get('context_entries', 0)}")
    console.print(f"\n[bold]Output saved to:[/bold] {output_path}")
    console.print(f"  - Context map: {output_path / 'context_map.json'}")
    console.print(f"  - Analysis report: {output_path / 'analysis_report.md'}")
    console.print(f"  - Vector store: {output_path / 'vector_store'}")


if __name__ == '__main__':
    main()
