---
generated: 2025-07-26T00:00:00Z
directory: SuperClaude_Framework/SuperClaude/Commands/IA
total_files: 26
total_directories: 1
depth: 2
---

# Site Map for Information Architecture (IA) Commands

## Overview
This directory contains a comprehensive collection of information architecture tools and commands for analyzing, organizing, and optimizing document structures. The tools follow Rosenfeld & Morville's Information Architecture principles and are designed to help LLMs better understand and process complex document repositories.

## Structure

IA/
├── [DOC] info-arch.md <- [HIGH] foundational concepts and LLM optimization strategies
├── [DOC] LLMS-THESAURUS.md <- referenced by: multiple tools for terminology standardization
├── [DOC] LLM-OPTIMIZED-TOOLS.md <- [HIGH] tool overview and optimization guide
├── [DOC] LLMS_20250713_1038.md <- legacy documentation file
├── [TEMPLATE] sitemap.md -> generates: LLMS-SITEMAP.md files
├── [TEMPLATE] thesaurus.md -> generates: LLMS-THESAURUS.md files
├── [TEMPLATE] taxonomy.md -> generates: classification hierarchies
├── [TEMPLATE] yaml-frontmatter.md -> standardizes: metadata schemas
├── Analysis Tools/
│   ├── [DOC] concept-extractor.md -> processes: document content for key concepts
│   ├── [DOC] content-audit.md -> evaluates: document quality and gaps
│   ├── [DOC] content-inventory.md -> catalogs: all document assets
│   ├── [DOC] content-relationships.md -> maps: document interconnections
│   ├── [DOC] cross-reference.md -> identifies: document reference patterns
│   ├── [DOC] dependency-graph.md -> visualizes: content dependencies
│   ├── [DOC] document-clustering.md -> groups: related documents
│   ├── [DOC] document-embeddings.md -> creates: semantic representations
│   ├── [DOC] gap-analysis.md -> identifies: missing content areas
│   └── [DOC] metadata-schema.md -> defines: structured metadata templates
├── Classification Tools/
│   ├── [DOC] faceted-classification.md -> creates: multi-dimensional taxonomies
│   └── [DOC] navigation-blueprint.md -> designs: navigation structures
├── Optimization Tools/
│   ├── [DOC] context-optimizer.md -> improves: LLM context understanding
│   ├── [DOC] context-window-optimizer.md -> manages: token limitations
│   ├── [DOC] multi-doc-synthesizer.md -> combines: related content
│   ├── [DOC] qa-generator.md -> creates: question-answer pairs
│   ├── [DOC] rag-index-builder.md -> builds: retrieval-augmented indexes
│   └── [DOC] semantic-markdown.md -> enhances: markdown semantics
├── Quality Tools/
│   ├── [DOC] ia-scorecard.md -> evaluates: information architecture quality
│   ├── [DOC] ord-mode.md <- organization and relationship documentation
│   └── reading-score/
│       ├── [DOC] reading-score.md <- [HIGH] readability overview and concepts
│       ├── [DOC] ari.md -> implements: Automated Readability Index
│       ├── [DOC] coleman-liau.md -> implements: Coleman-Liau Index
│       ├── [DOC] flesch-kincaid.md -> implements: Flesch-Kincaid Grade Level
│       ├── [DOC] flesch-reading-ease.md -> implements: Flesch Reading Ease
│       ├── [DOC] gunning-fog.md -> implements: Gunning Fog Index
│       └── [DOC] smog.md -> implements: SMOG Index

## Key Navigation Paths

### Primary Entry Points
1. **info-arch.md** - Start here for conceptual overview and LLM considerations
2. **LLM-OPTIMIZED-TOOLS.md** - Comprehensive tool guide for practitioners
3. **sitemap.md** - Template for generating site maps like this one

### Analysis Workflow
1. content-inventory.md → content-audit.md → gap-analysis.md
2. document-clustering.md → content-relationships.md → dependency-graph.md
3. concept-extractor.md → thesaurus.md → taxonomy.md

### Quality Assessment
1. reading-score/reading-score.md → specific readability metrics
2. ia-scorecard.md → overall architecture evaluation
3. metadata-schema.md → standardization assessment

### Output Generation
1. sitemap.md → LLMS-SITEMAP.md files
2. thesaurus.md → LLMS-THESAURUS.md files
3. taxonomy.md → classification hierarchies

## Content Clusters

### **Core IA Concepts** (Foundational)
- info-arch.md
- LLM-OPTIMIZED-TOOLS.md
- LLMS-THESAURUS.md

### **Document Analysis** (Discovery)
- content-inventory.md
- content-audit.md
- document-clustering.md
- concept-extractor.md

### **Relationship Mapping** (Connection)
- content-relationships.md
- cross-reference.md
- dependency-graph.md

### **Classification Systems** (Organization)
- taxonomy.md
- faceted-classification.md
- metadata-schema.md

### **Quality Metrics** (Assessment)
- reading-score/ (all files)
- ia-scorecard.md
- gap-analysis.md

### **LLM Optimization** (Enhancement)
- context-optimizer.md
- context-window-optimizer.md
- semantic-markdown.md
- rag-index-builder.md

### **Output Templates** (Generation)
- sitemap.md
- thesaurus.md
- yaml-frontmatter.md

## Cross-References

### High Interconnection Files
- **LLMS-THESAURUS.md** ← referenced by: most analysis tools for terminology
- **info-arch.md** ← referenced by: foundational concepts across tools
- **reading-score.md** ← referenced by: all readability metric tools
- **metadata-schema.md** ← referenced by: output generation tools

### Reference Patterns
- Analysis tools → reference thesaurus for consistent terminology
- Output templates → reference metadata schemas for structure
- Quality tools → reference readability metrics for assessment
- Optimization tools → reference context management strategies

## Orphaned Content

### Standalone Files
- **LLMS_20250713_1038.md** - Legacy documentation with unclear relationships
- **ord-mode.md** - Specialized tool with limited cross-references

### Integration Opportunities
- ord-mode.md could be integrated with navigation-blueprint.md
- LLMS_20250713_1038.md content should be migrated to relevant tools

## Navigation Notes

### For LLM Processing
- Start with info-arch.md for conceptual grounding
- Use LLMS-THESAURUS.md for terminology consistency
- Reference reading-score/ for accessibility assessment
- Apply templates systematically for standardized outputs

### For Human Users
- Begin with LLM-OPTIMIZED-TOOLS.md for tool overview
- Follow workflow patterns based on analysis goals
- Use quality metrics to validate outputs
- Leverage templates for consistent deliverables