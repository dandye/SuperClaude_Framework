---
title: RAG Index Builder
category: information-architecture
type: llm-tool
model: gemini-pro-2.5
platform: vertex-ai
created: 2025-07-13
---

# RAG Index Builder

Creates vector embeddings and optimally chunks documents for LLM retrieval using Gemini Pro 2.5 on Vertex AI.

## Purpose

Transforms markdown documentation into RAG-ready vector indexes with intelligent chunking strategies optimized for large language model retrieval.

## Features

- **Smart Chunking**: Preserves semantic boundaries (headers, code blocks, lists)
- **Vector Embeddings**: Uses Gemini Pro 2.5 text embeddings via Vertex AI
- **Metadata Extraction**: Preserves YAML frontmatter and document structure
- **Overlap Strategy**: Configurable chunk overlap for context preservation
- **Format Awareness**: Markdown-specific parsing and chunk boundaries

## Configuration

```yaml
rag_config:
  chunk_size: 1000        # tokens per chunk
  chunk_overlap: 200      # overlap tokens
  min_chunk_size: 100     # minimum viable chunk
  preserve_code: true     # keep code blocks intact
  preserve_headers: true  # maintain header hierarchy
  embedding_model: "textembedding-gecko@003"
  project_id: "your-gcp-project"
  location: "us-central1"
```

## Usage

```bash
# Build RAG index for entire documentation
./scripts/rag-index-builder.py --input docs/ --output rag_index/

# Build with custom chunking
./scripts/rag-index-builder.py --chunk-size 800 --overlap 150 --input docs/

# Update existing index
./scripts/rag-index-builder.py --update --index rag_index/
```

## Output Structure

```
rag_index/
├── embeddings/           # Vector embeddings per document
├── chunks/              # Chunked document content
├── metadata/            # Document metadata and hierarchy
├── index.json          # Master index with mappings
└── config.yaml         # Build configuration
```

## Integration

- **Query Interface**: Semantic search with similarity scoring
- **Context Assembly**: Intelligent chunk retrieval and ranking
- **Update Tracking**: Incremental updates for changed documents
- **Quality Metrics**: Embedding quality and chunk coherence scores

## LLM Optimization

- Preserves document hierarchy for context
- Maintains cross-references between chunks
- Optimizes chunk boundaries for question-answering
- Supports multi-document context assembly