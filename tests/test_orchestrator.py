"""Tests for orchestrator"""

import pytest
from pathlib import Path
from orchestration.orchestrator import Orchestrator


@pytest.fixture
def config():
    return {
        'ingestion': {
            'ignore_patterns': ['*.pyc', '__pycache__'],
            'max_file_size_mb': 10
        },
        'contextualization': {
            'chunk_size': 1000,
            'chunk_overlap': 200
        }
    }


@pytest.fixture
def output_path(tmp_path):
    return tmp_path / "output"


def test_orchestrator_initialization(config, output_path):
    """Test orchestrator can be initialized"""
    orchestrator = Orchestrator(config, output_path)
    assert orchestrator is not None
    assert orchestrator.config == config


@pytest.mark.asyncio
async def test_orchestrator_process_empty_repo(config, output_path, tmp_path):
    """Test processing an empty repository"""
    empty_repo = tmp_path / "empty_repo"
    empty_repo.mkdir()
    
    orchestrator = Orchestrator(config, output_path)
    result = await orchestrator.process_repository(str(empty_repo))
    
    assert result['files_analyzed'] == 0
    assert isinstance(result['duration_seconds'], float)
