# HP SDLC Agentic AI - AAVA AI Framework

<div align="center">

**An intelligent orchestration framework for automatic code repository ingestion and contextualization**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## 🎯 What is AAVA AI?

**AAVA AI** (Automated Analysis and Validation Architecture) is a multi-agent orchestration framework that automatically ingests any code repository and builds comprehensive context understanding through specialized AI agents.

### The Problem
- New developers take days to understand codebases
- Technical debt is hard to quantify
- Architecture documentation becomes outdated
- Manual code audits are time-consuming
- SDLC artifacts are scattered and hard to track

### The Solution
Point AAVA AI at any repository and get:
- ✅ Complete project analysis in minutes
- ✅ Automated insights and recommendations
- ✅ Unified context map of your codebase
- ✅ SDLC artifact tracking
- ✅ Semantic search capabilities

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd aava-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Analyze a repository
python main.py --repo-path /path/to/your/repo

# 4. Check results
ls output/
# → context_map.json
# → analysis_report.md
# → vector_store/
```

**That's it!** See [QUICKSTART.md](QUICKSTART.md) for more details.

---

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Repository Scanner**: Identifies all files and structure
- **Dependency Analyzer**: Extracts dependencies across languages
- **Structure Analyzer**: Maps classes, functions, and modules
- **Semantic Analyzer**: Creates embeddings for semantic search
- **SDLC Detector**: Finds tests, docs, CI/CD configs
- **Context Synthesizer**: Aggregates everything into unified context

### 🌍 Multi-Language Support
Python • JavaScript • TypeScript • Java • C++ • Go • Rust • Ruby • PHP • and more

### 🔍 Comprehensive Analysis
- **Dependencies**: All project dependencies with versions
- **Code Structure**: Classes, functions, imports, relationships
- **Architecture Patterns**: MVC, Repository, Service Layer, etc.
- **SDLC Artifacts**: Tests, docs, requirements, CI/CD
- **Test Coverage**: Automated test coverage analysis
- **Documentation**: Doc coverage metrics

### 💡 Intelligent Insights
- Automated insights generation
- Actionable recommendations
- Architecture pattern detection
- Technical debt identification
- Security and compliance checks

### 🔌 Flexible Deployment
- **CLI**: Command-line interface
- **REST API**: HTTP API for integration
- **Docker**: Containerized deployment
- **SDK**: Programmatic Python API

---

## 📊 Architecture

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

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical architecture.

---

## 📁 Project Structure

```
aava-ai/
├── agents/                  # Specialized AI agents
│   ├── dependency_analyzer.py
│   ├── structure_analyzer.py
│   ├── semantic_analyzer.py
│   ├── sdlc_detector.py
│   └── context_synthesizer.py
├── ingestion/              # Repository ingestion
│   ├── repository_scanner.py
│   └── file_parser.py
├── orchestration/          # Orchestration engine
│   └── orchestrator.py
├── storage/                # Data storage
│   ├── context_store.py
│   └── vector_store.py
├── main.py                 # CLI entry point
├── api_server.py          # REST API server
└── config.yaml            # Configuration
```

---

## 💻 Usage Examples

### CLI Usage
```bash
# Basic analysis
python main.py --repo-path /path/to/repo

# Custom output directory
python main.py --repo-path /path/to/repo --output ./results

# Verbose logging
python main.py --repo-path /path/to/repo --verbose
```

### API Usage
```bash
# Start API server
python api_server.py

# Submit repository for analysis
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/path/to/repo"}'

# Check job status
curl http://localhost:8000/jobs/{job_id}

# Get results
curl http://localhost:8000/context/{job_id}
```

### Programmatic Usage
```python
from orchestration.orchestrator import Orchestrator
from utils.config import load_config

config = load_config('config.yaml')
orchestrator = Orchestrator(config, output_path)
result = await orchestrator.process_repository(repo_path)

print(f"Analyzed {result['files_analyzed']} files")
print(f"Found {result['dependencies_count']} dependencies")
```

### Docker Usage
```bash
# Build and run
docker-compose up

# Or use Makefile
make docker-build
make docker-run
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [USAGE.md](USAGE.md) | Detailed usage instructions |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical architecture |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Comprehensive project overview |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## 🎯 Use Cases

### 👨‍💻 Developer Onboarding
```bash
python main.py --repo-path /company/project
# Share analysis_report.md with new developers
```

### 🔍 Technical Debt Assessment
```bash
python main.py --repo-path /legacy/codebase
# Review recommendations for refactoring priorities
```

### 📚 Architecture Documentation
```bash
python main.py --repo-path /project
# Use structure analysis for up-to-date architecture docs
```

### 🔐 Security & Compliance Audit
```bash
python main.py --repo-path /project
# Check dependencies and SDLC artifacts for compliance
```

### 📊 Code Quality Monitoring
```yaml
# .github/workflows/analyze.yml
- name: Analyze Code
  run: python main.py --repo-path .
```

---

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
ingestion:
  ignore_patterns:
    - "node_modules/**"
    - "venv/**"
    - "*.log"
  max_file_size_mb: 10

contextualization:
  embedding_model: "text-embedding-3-small"
  chunk_size: 1000
  chunk_overlap: 200
```

Environment variables (`.env`):
```bash
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
AI_PROVIDER=anthropic
AI_MODEL=claude-sonnet-4.5
```

---

## 📊 Example Output

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

---

## 🛠️ Development

```bash
# Setup development environment
make install-dev

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean generated files
make clean
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - REST API framework
- [Tree-sitter](https://tree-sitter.github.io/) - Code parsing
- [ChromaDB](https://www.trychroma.com/) - Vector storage
- [Rich](https://rich.readthedocs.io/) - Beautiful CLI output
- [Click](https://click.palletsprojects.com/) - CLI framework

---

## 📞 Support

- 📖 **Documentation**: See docs in this repository
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-org/aava-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-org/aava-ai/discussions)

---

## 🗺️ Roadmap

- [x] Core multi-agent orchestration
- [x] Multi-language support
- [x] CLI and API interfaces
- [ ] LLM-powered insights (Q2 2026)
- [ ] Real-time analysis mode (Q2 2026)
- [ ] IDE plugins (Q3 2026)
- [ ] Distributed processing (Q4 2026)

---

<div align="center">

**Built with ❤️ for the HP SDLC Agentic AI Initiative**

[Get Started](QUICKSTART.md) • [Documentation](USAGE.md) • [Architecture](ARCHITECTURE.md)

</div>
