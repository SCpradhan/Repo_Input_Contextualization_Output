.PHONY: help install test lint format clean run api docker-build docker-run

help:
	@echo "AAVA AI - Available Commands"
	@echo "=============================="
	@echo "install       - Install dependencies"
	@echo "test          - Run tests"
	@echo "lint          - Run linters"
	@echo "format        - Format code"
	@echo "clean         - Clean generated files"
	@echo "run           - Run CLI (set REPO_PATH)"
	@echo "api           - Start API server"
	@echo "docker-build  - Build Docker image"
	@echo "docker-run    - Run in Docker"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8 mypy

test:
	pytest tests/ -v

test-cov:
	pytest --cov=. --cov-report=html tests/

lint:
	flake8 . --exclude=venv,env,.venv
	mypy . --exclude=venv --exclude=env --exclude=.venv

format:
	black . --exclude=venv --exclude=env --exclude=.venv

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

run:
	@if [ -z "$(REPO_PATH)" ]; then \
		echo "Error: REPO_PATH not set. Usage: make run REPO_PATH=/path/to/repo"; \
		exit 1; \
	fi
	python main.py --repo-path $(REPO_PATH)

api:
	python api_server.py

docker-build:
	docker-compose build

docker-run:
	docker-compose up

docker-cli:
	docker-compose run --rm aava-cli

example:
	python examples/example_usage.py

setup:
	@echo "Setting up AAVA AI..."
	python -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"
	@echo "Then run: make install"
