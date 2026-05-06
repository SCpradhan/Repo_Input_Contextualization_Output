# AAVA AI - Quick Start Guide

## What is AAVA AI?

AAVA AI (Automated Analysis and Validation Architecture) is an intelligent orchestration framework that automatically ingests any code repository and builds comprehensive context understanding through specialized AI agents.

## Key Features

✅ **Automatic Repository Ingestion** - Point to any repo and get instant analysis  
✅ **Multi-Language Support** - Python, JavaScript, Java, C++, Go, Rust, and more  
✅ **SDLC Integration** - Analyzes requirements, design, code, tests, and docs  
✅ **Intelligent Agents** - Specialized agents for different analysis tasks  
✅ **Context Synthesis** - Unified context map with insights and recommendations  
✅ **REST API** - Easy integration with existing tools  
✅ **Extensible** - Add custom agents and analyzers  

## 5-Minute Setup

```bash
# 1. Clone and setup
git clone <repo-url>
cd aava-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure (optional)
cp .env.example .env
# Edit .env with your API keys if using LLM features

# 4. Run analysis
python main.py --repo-path /path/to/your/repo

# Done! Check output/ directory for results
```

## What You Get

After running AAVA AI, you'll have:

### 1. Context Map (`context_map.json`)
Complete structured data about your repository:
- File inventory and metadata
- Dependencies and versions
- Code structure (classes, functions, modules)
- SDLC artifacts (tests, docs, CI/CD)
- Semantic embeddings for search

### 2. Analysis Report (`analysis_report.md`)
Human-readable report with:
- Project overview and statistics
- Architecture patterns detected
- Dependency analysis
- Test coverage metrics
- Key insights
- Actionable recommendations

### 3. Vector Store
Semantic embeddings enabling:
- Code similarity search
- Intelligent code navigation
- Context-aware queries

## Use Cases

### 🎯 Onboarding New Developers
```bash
python main.py --repo-path /path/to/project
# Share analysis_report.md with new team members
```

### 🔍 Technical Debt Assessment
```bash
python main.py --repo-path /path/to/legacy-project
# Review recommendations section
```

### 📊 Architecture Documentation
```bash
python main.py --repo-path /path/to/project
# Use structure analysis for documentation
```

### 🔐 Security & Compliance Audit
```bash
python main.py --repo-path /path/to/project
# Check dependencies and SDLC artifacts
```

## Architecture Overview

```
Input: Repository Path
         ↓
    [Scanner] → Identifies all files
         ↓
    [Parser] → Reads and processes content
         ↓
    [Parallel Analysis]
    ├─ Dependency Analyzer
    ├─ Structure Analyzer
    └─ Semantic Analyzer
         ↓
    [SDLC Detector] → Finds tests, docs, CI/CD
         ↓
    [Context Synthesizer] → Aggregates everything
         ↓
Output: Context Map + Reports + Embeddings
```

## API Usage

Start the server:
```bash
python api_server.py
```

Submit a repository:
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/path/to/repo"}'
```

Check status:
```bash
curl http://localhost:8000/jobs/{job_id}
```

## Configuration

Edit `config.yaml` to customize:

```yaml
ingestion:
  ignore_patterns:
    - "node_modules/**"
    - "*.log"
  max_file_size_mb: 10

contextualization:
  chunk_size: 1000
  embedding_model: "text-embedding-3-small"
```

## Docker Usage

```bash
# Build and run
docker-compose up

# Or run CLI
docker-compose run aava-cli
```

## Next Steps

1. **Read USAGE.md** - Detailed usage guide
2. **Read ARCHITECTURE.md** - Technical architecture
3. **Try examples/** - Sample code and integrations
4. **Customize config.yaml** - Adjust for your needs
5. **Add custom agents** - Extend functionality

## Troubleshooting

**Large repositories?**
```yaml
ingestion:
  batch_size: 50
  max_file_size_mb: 5
```

**Memory issues?**
- Reduce batch_size in config
- Process specific directories first

**Encoding errors?**
- Parser handles multiple encodings automatically
- Check file encodings if issues persist

## Support

- 📖 Documentation: See USAGE.md and ARCHITECTURE.md
- 🐛 Issues: Open a GitHub issue
- 💬 Questions: Check CONTRIBUTING.md

## What Makes AAVA AI Different?

Traditional tools analyze code **statically**. AAVA AI uses **agentic orchestration**:

- **Multi-Agent System**: Specialized agents work in parallel
- **Context Synthesis**: Unified understanding across all artifacts
- **SDLC Awareness**: Understands the full development lifecycle
- **Semantic Understanding**: Goes beyond syntax to meaning
- **Extensible**: Easy to add domain-specific analyzers

## Example Output

```
=== Analysis Complete ===

Files analyzed: 247
Languages: python, javascript, yaml
Dependencies: 45
Context entries: 247
Duration: 8.3s

Key Insights:
- Multi-language project using python, javascript
- Moderate dependency footprint with 45 dependencies
- Good test coverage with 35.2% test-to-code ratio
- Uses architectural patterns: MVC, Repository Pattern

Recommendations:
1. Add inline documentation to improve maintainability
2. Set up CI/CD pipeline for automated testing
3. Consider refactoring into more modular structure

Output saved to: ./output
```

## Ready to Start?

```bash
python main.py --repo-path /path/to/your/repo
```

That's it! AAVA AI will automatically analyze your repository and provide comprehensive insights.
