# AAVA AI Usage Guide

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd aava-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
```

## Quick Start

### CLI Usage

```bash
# Basic usage
python main.py --repo-path /path/to/your/repo

# Specify output directory
python main.py --repo-path /path/to/repo --output ./analysis_results

# Use custom configuration
python main.py --repo-path /path/to/repo --config custom_config.yaml

# Verbose logging
python main.py --repo-path /path/to/repo --verbose
```

### API Usage

Start the API server:

```bash
python api_server.py
```

The API will be available at `http://localhost:8000`

#### API Endpoints

**1. Start Ingestion**

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "repo_path": "/path/to/repo",
    "output_path": "./output"
  }'
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending"
}
```

**2. Check Job Status**

```bash
curl http://localhost:8000/jobs/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "result": {
    "files_analyzed": 150,
    "languages": ["python", "javascript"],
    "dependencies_count": 45,
    "context_entries": 150,
    "duration_seconds": 12.5
  }
}
```

**3. Get Context**

```bash
curl http://localhost:8000/context/123e4567-e89b-12d3-a456-426614174000
```

**4. List All Jobs**

```bash
curl http://localhost:8000/jobs
```

## Configuration

### config.yaml

```yaml
orchestration:
  pipeline:
    - name: "repository_scan"
      agent: "scanner"
      enabled: true
    # ... more stages

agents:
  scanner:
    description: "Scans repository structure"
    priority: 1
  # ... more agents

ingestion:
  ignore_patterns:
    - "node_modules/**"
    - "venv/**"
    - ".git/**"
  max_file_size_mb: 10
  
contextualization:
  embedding_model: "text-embedding-3-small"
  chunk_size: 1000
  chunk_overlap: 200
```

### Environment Variables

```bash
# AI Provider
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
AI_PROVIDER=anthropic
AI_MODEL=claude-sonnet-4.5

# Storage
VECTOR_STORE_PATH=./data/vector_store
CONTEXT_STORE_PATH=./data/context_store

# Orchestration
MAX_CONCURRENT_AGENTS=5
INGESTION_BATCH_SIZE=100
```

## Output Files

After analysis, you'll find:

```
output/
├── context_map.json          # Complete context data
├── analysis_report.md        # Human-readable report
├── context_store/            # Individual context entries
│   ├── file1.json
│   └── file2.json
└── vector_store/             # Embeddings database
    └── chroma.sqlite3
```

### context_map.json

Contains:
- Repository metadata
- File inventory
- Dependencies
- Code structure
- SDLC artifacts
- Insights and recommendations

### analysis_report.md

Human-readable report with:
- Project overview
- Structure summary
- Dependency list
- SDLC artifacts
- Key insights
- Recommendations

## Use Cases

### 1. Onboarding New Developers

```bash
# Generate comprehensive project overview
python main.py --repo-path /path/to/project

# Share analysis_report.md with new team members
```

### 2. Code Review Preparation

```bash
# Analyze before major refactoring
python main.py --repo-path /path/to/project --output ./pre-refactor

# Compare with post-refactor analysis
python main.py --repo-path /path/to/project --output ./post-refactor
```

### 3. Technical Debt Assessment

```bash
# Analyze project to identify issues
python main.py --repo-path /path/to/legacy-project

# Review recommendations in analysis_report.md
```

### 4. Dependency Audit

```bash
# Extract all dependencies
python main.py --repo-path /path/to/project

# Check context_map.json for dependency list
```

### 5. Architecture Documentation

```bash
# Generate architecture insights
python main.py --repo-path /path/to/project

# Use structure analysis for documentation
```

## Advanced Usage

### Custom Agents

Create a custom agent:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    async def analyze(self, data):
        # Your analysis logic
        return results
```

Register in config.yaml:

```yaml
agents:
  custom_agent:
    description: "My custom analyzer"
    priority: 7
```

### Filtering Files

Modify `config.yaml`:

```yaml
ingestion:
  ignore_patterns:
    - "*.log"
    - "temp/**"
    - "build/**"
  
  include_patterns:
    - "src/**/*.py"
    - "lib/**/*.js"
```

### Custom Embeddings

Modify `config.yaml`:

```yaml
contextualization:
  embedding_model: "your-model-name"
  chunk_size: 2000
  chunk_overlap: 400
  similarity_threshold: 0.8
```

## Troubleshooting

### Large Repositories

For very large repos (>10k files):

```yaml
ingestion:
  max_file_size_mb: 5
  batch_size: 50
```

### Memory Issues

Reduce batch size:

```yaml
ingestion:
  batch_size: 25
```

### Encoding Errors

The parser tries multiple encodings automatically. If issues persist, check file encodings.

### API Timeout

For long-running jobs, use the job status endpoint to poll:

```bash
# Start job
JOB_ID=$(curl -X POST http://localhost:8000/ingest -d '{"repo_path": "/path"}' | jq -r '.job_id')

# Poll status
while true; do
  STATUS=$(curl http://localhost:8000/jobs/$JOB_ID | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" = "completed" ] && break
  sleep 5
done
```

## Best Practices

1. **Start Small**: Test on a small repo first
2. **Review Config**: Adjust ignore patterns for your needs
3. **Monitor Resources**: Watch memory usage on large repos
4. **Incremental Analysis**: Analyze specific directories first
5. **Version Control**: Keep analysis results in version control
6. **Regular Updates**: Re-analyze after major changes

## Integration Examples

### CI/CD Integration

```yaml
# .github/workflows/analyze.yml
name: Code Analysis
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run AAVA AI
        run: |
          pip install -r requirements.txt
          python main.py --repo-path .
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: analysis-results
          path: output/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python main.py --repo-path . --output .analysis
```

## Support

For issues and questions:
- Check ARCHITECTURE.md for technical details
- Review logs in `./logs/aava.log`
- Enable verbose mode for debugging
