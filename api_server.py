#!/usr/bin/env python3
"""
REST API Server for AAVA AI
Provides HTTP endpoints for repository ingestion and analysis
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio
import uuid

from orchestration.orchestrator import Orchestrator
from utils.config import load_config
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="AAVA AI API",
    description="Automatic Repository Contextualization API",
    version="1.0.0"
)

# Store for tracking jobs
jobs: Dict[str, Dict[str, Any]] = {}

# Configuration
config = load_config('config.yaml')


class IngestionRequest(BaseModel):
    """Request model for repository ingestion"""
    repo_path: str
    output_path: Optional[str] = "./output"


class JobStatus(BaseModel):
    """Job status response"""
    job_id: str
    status: str
    progress: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AAVA AI",
        "version": "1.0.0",
        "description": "HP SDLC Agentic AI Framework"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/ingest", response_model=JobStatus)
async def ingest_repository(
    request: IngestionRequest,
    background_tasks: BackgroundTasks
):
    """
    Start repository ingestion and analysis
    
    Returns a job ID that can be used to track progress
    """
    
    # Validate repository path
    repo_path = Path(request.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail=f"Repository path does not exist: {request.repo_path}")
    
    # Create job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "repo_path": request.repo_path,
        "output_path": request.output_path
    }
    
    # Start background task
    background_tasks.add_task(
        process_repository_job,
        job_id,
        request.repo_path,
        request.output_path
    )
    
    logger.info(f"Created ingestion job {job_id} for {request.repo_path}")
    
    return JobStatus(
        job_id=job_id,
        status="pending"
    )


@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get status of an ingestion job"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
    
    job = jobs[job_id]
    
    return JobStatus(
        job_id=job_id,
        status=job.get("status"),
        progress=job.get("progress"),
        result=job.get("result"),
        error=job.get("error")
    )


@app.get("/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "jobs": [
            {
                "job_id": job_id,
                "status": job.get("status"),
                "repo_path": job.get("repo_path")
            }
            for job_id, job in jobs.items()
        ]
    }


@app.get("/context/{job_id}")
async def get_context(job_id: str):
    """Get the generated context for a completed job"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
    
    job = jobs[job_id]
    
    if job.get("status") != "completed":
        raise HTTPException(status_code=400, detail=f"Job not completed: {job_id}")
    
    # Load context from file
    output_path = Path(job.get("output_path"))
    context_file = output_path / "context_map.json"
    
    if not context_file.exists():
        raise HTTPException(status_code=404, detail="Context file not found")
    
    import json
    with open(context_file, 'r') as f:
        context = json.load(f)
    
    return context


async def process_repository_job(job_id: str, repo_path: str, output_path: str):
    """Background task to process repository"""
    
    try:
        jobs[job_id]["status"] = "running"
        logger.info(f"Starting job {job_id}")
        
        # Initialize orchestrator
        output_dir = Path(output_path) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        orchestrator = Orchestrator(config, output_dir)
        
        # Process repository
        result = await orchestrator.process_repository(repo_path)
        
        # Update job status
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
        jobs[job_id]["output_path"] = str(output_dir)
        
        logger.info(f"Completed job {job_id}")
    
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
