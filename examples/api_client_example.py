#!/usr/bin/env python3
"""
Example API client for AAVA AI
"""

import httpx
import asyncio
import time


async def main():
    """Example: Use AAVA AI via REST API"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        
        # 1. Start ingestion
        print("Starting repository ingestion...")
        response = await client.post(
            f"{base_url}/ingest",
            json={
                "repo_path": "/path/to/your/repository",
                "output_path": "./api_output"
            }
        )
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return
        
        job_data = response.json()
        job_id = job_data['job_id']
        print(f"Job created: {job_id}")
        
        # 2. Poll for completion
        print("\nWaiting for analysis to complete...")
        while True:
            response = await client.get(f"{base_url}/jobs/{job_id}")
            status_data = response.json()
            status = status_data['status']
            
            print(f"Status: {status}")
            
            if status == 'completed':
                print("\n=== Analysis Complete ===")
                result = status_data['result']
                print(f"Files analyzed: {result['files_analyzed']}")
                print(f"Languages: {', '.join(result['languages'])}")
                print(f"Dependencies: {result['dependencies_count']}")
                print(f"Duration: {result['duration_seconds']:.2f}s")
                break
            
            elif status == 'failed':
                print(f"\nError: {status_data.get('error')}")
                return
            
            await asyncio.sleep(2)
        
        # 3. Get context
        print("\nFetching context...")
        response = await client.get(f"{base_url}/context/{job_id}")
        context = response.json()
        
        # Display insights
        print("\n=== Key Insights ===")
        for insight in context.get('insights', []):
            print(f"- {insight}")
        
        # Display recommendations
        print("\n=== Recommendations ===")
        for i, rec in enumerate(context.get('recommendations', []), 1):
            print(f"{i}. {rec}")


if __name__ == '__main__':
    asyncio.run(main())
