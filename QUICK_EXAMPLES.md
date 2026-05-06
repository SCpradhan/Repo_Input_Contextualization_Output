# 🚀 Quick Examples - AAVA AI

Ready-to-run examples for analyzing popular repositories.

---

## 📋 Table of Contents

1. [Flask - Python Web Framework](#flask)
2. [Django - Python Web Framework](#django)
3. [React - JavaScript Library](#react)
4. [Express - Node.js Framework](#express)
5. [Your Own Repository](#your-own-repository)

---

## <a name="flask"></a>🐍 Example 1: Flask (Python Web Framework)

### Clone & Analyze
```bash
git clone --depth 1 https://github.com/pallets/flask.git flask-repo
python main.py --repo-path flask-repo --output flask-analysis
```

### Expected Results
- **Files**: ~264
- **Languages**: Python, Markdown, YAML, JSON
- **Dependencies**: ~21
- **Test Coverage**: Excellent (256%+)
- **Duration**: ~0.3 seconds

### View Results
```bash
cat flask-analysis/analysis_report.md
```

---

## <a name="django"></a>🎸 Example 2: Django (Python Web Framework)

### Clone & Analyze
```bash
git clone --depth 1 https://github.com/django/django.git django-repo
python main.py --repo-path django-repo --output django-analysis
```

### Expected Results
- **Files**: ~1000+
- **Languages**: Python, JavaScript, HTML, CSS
- **Dependencies**: Multiple
- **Test Coverage**: Comprehensive
- **Duration**: ~2-3 seconds

### View Results
```bash
cat django-analysis/analysis_report.md
```

---

## <a name="react"></a>⚛️ Example 3: React (JavaScript Library)

### Clone & Analyze
```bash
git clone --depth 1 https://github.com/facebook/react.git react-repo
python main.py --repo-path react-repo --output react-analysis
```

### Expected Results
- **Files**: ~500+
- **Languages**: JavaScript, TypeScript, HTML
- **Dependencies**: npm packages
- **Test Coverage**: Good
- **Duration**: ~1-2 seconds

### View Results
```bash
cat react-analysis/analysis_report.md
```

---

## <a name="express"></a>🚂 Example 4: Express (Node.js Framework)

### Clone & Analyze
```bash
git clone --depth 1 https://github.com/expressjs/express.git express-repo
python main.py --repo-path express-repo --output express-analysis
```

### Expected Results
- **Files**: ~200+
- **Languages**: JavaScript, Markdown
- **Dependencies**: npm packages
- **Test Coverage**: Good
- **Duration**: ~0.5 seconds

### View Results
```bash
cat express-analysis/analysis_report.md
```

---

## <a name="your-own-repository"></a>💼 Example 5: Your Own Repository

### Local Repository
```bash
python main.py --repo-path /path/to/your/project --output my-analysis
```

### Remote Repository
```bash
# Clone first
git clone https://github.com/yourusername/yourproject.git my-project

# Then analyze
python main.py --repo-path my-project --output my-analysis
```

### View Results
```bash
cat my-analysis/analysis_report.md
```

---

## 🎯 Quick Command Reference

### Basic Analysis
```bash
python main.py --repo-path <path> --output <output-dir>
```

### With Verbose Logging
```bash
python main.py --repo-path <path> --output <output-dir> --verbose
```

### Using API
```bash
# Start server
python api_server.py

# Submit analysis (in another terminal)
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/path/to/repo"}'
```

---

## 📊 What You Get

After each analysis, you'll find:

```
<output-dir>/
├── context_map.json          # Complete structured data
├── analysis_report.md        # Human-readable report
├── context_store/            # Individual file contexts
└── vector_store/             # Semantic embeddings
```

---

## 🔍 Viewing Results

### View Full Report
```bash
cat <output-dir>/analysis_report.md
```

### View Context Map (JSON)
```bash
cat <output-dir>/context_map.json | jq '.'
```

### View Specific Sections
```bash
# Dependencies
cat <output-dir>/context_map.json | jq '.dependencies'

# Insights
cat <output-dir>/context_map.json | jq '.insights'

# Recommendations
cat <output-dir>/context_map.json | jq '.recommendations'
```

---

## ⚡ Performance Benchmarks

| Repository | Files | Duration | Dependencies | Classes | Functions |
|------------|-------|----------|--------------|---------|-----------|
| Flask | 264 | 0.31s | 21 | 166 | 1,491 |
| Express | ~200 | ~0.5s | ~30 | ~50 | ~300 |
| React | ~500 | ~1.5s | ~50 | ~200 | ~800 |
| Django | ~1000 | ~3s | ~40 | ~500 | ~2000 |

*Actual times may vary based on system performance*

---

## 🎓 Tips & Tricks

### 1. Analyze Multiple Repositories
```bash
for repo in flask django express; do
  git clone --depth 1 https://github.com/example/$repo.git
  python main.py --repo-path $repo --output ${repo}-analysis
done
```

### 2. Compare Projects
```bash
# Analyze two projects
python main.py --repo-path project-a --output analysis-a
python main.py --repo-path project-b --output analysis-b

# Compare results
diff analysis-a/analysis_report.md analysis-b/analysis_report.md
```

### 3. Track Changes Over Time
```bash
# Initial analysis
python main.py --repo-path myproject --output analysis-v1

# After changes
python main.py --repo-path myproject --output analysis-v2

# Compare
diff analysis-v1/context_map.json analysis-v2/context_map.json
```

### 4. Extract Specific Data
```bash
# Get all dependencies
cat analysis/context_map.json | jq '.dependencies[].name'

# Get test coverage
cat analysis/context_map.json | jq '.sdlc_artifacts.test_coverage'

# Get insights
cat analysis/context_map.json | jq '.insights[]'
```

---

## 🐛 Troubleshooting

### Issue: "Repository path does not exist"
```bash
# Make sure the path is correct
ls -la /path/to/repo

# Use absolute path
python main.py --repo-path $(pwd)/myrepo --output analysis
```

### Issue: "Permission denied"
```bash
# Check file permissions
chmod -R 755 /path/to/repo
```

### Issue: "Out of memory"
```bash
# For very large repos, adjust batch size in config.yaml
ingestion:
  batch_size: 50  # Reduce from 100
```

---

## 📚 More Examples

### Analyze Current Directory
```bash
python main.py --repo-path . --output self-analysis
```

### Analyze with Custom Config
```bash
# Edit config.yaml first
python main.py --repo-path myrepo --output analysis --config custom-config.yaml
```

### Use Docker
```bash
docker-compose run aava-cli python main.py --repo-path /app/repo --output /app/output
```

---

## 🎉 Success Indicators

After running analysis, you should see:

✅ "Analysis Complete!" message  
✅ Summary with file count and languages  
✅ Output files created  
✅ No error messages  
✅ Duration under a few seconds (for small-medium repos)  

---

## 🚀 Next Steps

1. **Try the Flask example** (fastest to run)
2. **Analyze your own project**
3. **Compare different projects**
4. **Integrate into CI/CD**
5. **Build custom agents**

---

<div align="center">

**Ready to start?**

```bash
git clone --depth 1 https://github.com/pallets/flask.git flask-repo
python main.py --repo-path flask-repo --output flask-analysis
cat flask-analysis/analysis_report.md
```

**That's it! 🎉**

</div>
