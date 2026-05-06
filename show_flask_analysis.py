#!/usr/bin/env python3
"""Display Flask analysis results"""

import json

# Load the analysis
with open('flask-analysis/context_map.json', 'r') as f:
    data = json.load(f)

print("=" * 70)
print("🔍 FLASK WEB FRAMEWORK - AAVA AI ANALYSIS RESULTS")
print("=" * 70)

print(f"\n📊 OVERVIEW")
print(f"  Repository: {data['repository_name']}")
print(f"  Total Files: {data['total_files']}")
print(f"  Languages: {', '.join(data['languages'])}")
print(f"  Analysis Date: {data['timestamp']}")

print(f"\n📦 DEPENDENCIES ({len(data['dependencies'])} found)")
for dep in data['dependencies'][:10]:
    print(f"  • {dep['name']} ({dep.get('version', 'latest')}) - {dep['type']}")
if len(data['dependencies']) > 10:
    print(f"  ... and {len(data['dependencies']) - 10} more")

print(f"\n🏗️  CODE STRUCTURE")
stats = data['structure']['statistics']
print(f"  Classes: {stats.get('total_classes', 0)}")
print(f"  Functions: {stats.get('total_functions', 0)}")
print(f"  Total Imports: {len(data['structure'].get('imports', []))}")

print(f"\n🎯 ARCHITECTURE PATTERNS")
patterns = data['structure'].get('architecture_patterns', [])
if patterns:
    for pattern in patterns:
        print(f"  ✓ {pattern}")
else:
    print("  No specific patterns detected")

print(f"\n📋 SDLC ARTIFACTS")
artifacts = data['sdlc_artifacts']
print(f"  Requirements: {len(artifacts.get('requirements', []))} files")
print(f"  Tests: {len(artifacts.get('tests', []))} files")
print(f"  Documentation: {len(artifacts.get('documentation', []))} files")
print(f"  CI/CD: {len(artifacts.get('ci_cd', []))} files")
print(f"  Configuration: {len(artifacts.get('configuration', []))} files")

test_cov = artifacts.get('test_coverage', {})
if test_cov:
    print(f"\n  Test Coverage:")
    print(f"    Total test files: {test_cov.get('total_test_files', 0)}")
    print(f"    Total code files: {test_cov.get('total_code_files', 0)}")
    print(f"    Test ratio: {test_cov.get('test_ratio', 0):.1%}")

print(f"\n💡 KEY INSIGHTS")
for insight in data['insights']:
    print(f"  • {insight}")

print(f"\n✅ RECOMMENDATIONS")
for idx, rec in enumerate(data['recommendations'], 1):
    print(f"  {idx}. {rec}")

print(f"\n📁 SAMPLE FILES ANALYZED")
for entry in data['entries'][:5]:
    print(f"  • {entry['file']} ({entry['type']}) - {entry['size']} bytes")

print("\n" + "=" * 70)
print("✨ Analysis complete! Full details in flask-analysis/")
print("=" * 70)
