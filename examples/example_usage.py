#!/usr/bin/env python3
"""
Example usage of AAVA AI programmatically
"""

import asyncio
from pathlib import Path
from orchestration.orchestrator import Orchestrator
from utils.config import load_config


async def main():
    """Example: Analyze a repository programmatically"""
    
    # Load configuration
    config = load_config('config.yaml')
    
    # Setup paths
    repo_path = "/path/to/your/repository"
    output_path = Path("./example_output")
    output_path.mkdir(exist_ok=True)
    
    # Initialize orchestrator
    orchestrator = Orchestrator(config, output_path)
    
    # Process repository
    print(f"Analyzing repository: {repo_path}")
    result = await orchestrator.process_repository(repo_path)
    
    # Display results
    print("\n=== Analysis Complete ===")
    print(f"Files analyzed: {result['files_analyzed']}")
    print(f"Languages: {', '.join(result['languages'])}")
    print(f"Dependencies: {result['dependencies_count']}")
    print(f"Duration: {result['duration_seconds']:.2f}s")
    print(f"\nResults saved to: {output_path}")
    
    # Access context data
    import json
    context_file = output_path / "context_map.json"
    with open(context_file, 'r') as f:
        context = json.load(f)
    
    # Print insights
    print("\n=== Key Insights ===")
    for insight in context.get('insights', []):
        print(f"- {insight}")
    
    # Print recommendations
    print("\n=== Recommendations ===")
    for i, rec in enumerate(context.get('recommendations', []), 1):
        print(f"{i}. {rec}")


if __name__ == '__main__':
    asyncio.run(main())
