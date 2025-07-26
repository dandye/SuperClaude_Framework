---
title: Context Window Optimizer
category: information-architecture
type: llm-tool
model: gemini-pro-2.5
platform: vertex-ai
created: 2025-07-13
---

# Context Window Optimizer

Intelligently packages related documents within LLM token limits for optimal context assembly and query performance.

## Purpose

Maximizes context utilization by strategically selecting and organizing document chunks to fit within model context windows while preserving semantic coherence and relevance.

## Features

- **Token Budget Management**: Precise token counting with model-specific limits
- **Relevance Ranking**: Semantic similarity scoring for chunk selection
- **Context Coherence**: Maintains logical document flow and relationships
- **Priority Weighting**: Emphasizes recent, authoritative, or user-specified content
- **Adaptive Chunking**: Dynamically adjusts chunk sizes based on available context

## Configuration

```yaml
context_optimizer:
  max_tokens: 200000      # Gemini Pro 2.5 context limit
  reserve_tokens: 10000   # Reserve for response generation
  min_relevance: 0.7      # Minimum similarity threshold
  prioritize_recent: true # Weight newer documents higher
  preserve_hierarchy: true # Maintain document structure
  overlap_penalty: 0.1    # Reduce score for overlapping content
```

## Context Assembly Strategies

### 1. Relevance-First Assembly
```python
# Prioritize highest similarity scores
chunks = rank_by_relevance(query_embedding, all_chunks)
context = assemble_within_budget(chunks, token_budget)
```

### 2. Hierarchical Assembly
```python
# Preserve document structure and relationships
context = build_hierarchical_context(
    primary_docs=high_relevance_docs,
    supporting_docs=related_docs,
    token_budget=budget
)
```

### 3. Temporal Assembly
```python
# Weight by recency and relevance
context = temporal_weighted_assembly(
    chunks=ranked_chunks,
    time_decay=0.1,
    token_budget=budget
)
```

## Usage

```bash
# Optimize context for specific query
./scripts/context-optimizer.py --query "security operations setup" --budget 180000

# Build context from document collection
./scripts/context-optimizer.py --docs docs/ --topic "authentication" --format structured

# Interactive context optimization
./scripts/context-optimizer.py --interactive --rag-index rag_index/
```

## Output Formats

### Structured Context
```markdown
# Primary Context: Authentication Setup (85% relevance)
[Document chunk with highest relevance]

## Supporting Context: Related Procedures (72% relevance)
[Related document chunks]

## Reference Context: Background Information (65% relevance)
[Additional context within token budget]
```

### JSON Context Package
```json
{
  "context_id": "ctx_auth_setup_20250713",
  "query": "authentication setup procedures",
  "total_tokens": 178450,
  "chunks": [
    {
      "chunk_id": "abc123",
      "relevance": 0.89,
      "doc_path": "auth/setup.md",
      "tokens": 1250,
      "priority": "primary"
    }
  ],
  "metadata": {
    "assembly_strategy": "relevance-first",
    "optimization_score": 0.94
  }
}
```

## Optimization Features

- **Deduplication**: Removes redundant information across chunks
- **Gap Filling**: Identifies and includes bridging context
- **Quality Scoring**: Evaluates context completeness and coherence
- **Budget Visualization**: Shows token utilization and optimization opportunities

## Integration Points

- **RAG Index**: Reads from RAG-indexed document collections
- **Query Analysis**: Semantic query understanding and expansion
- **Response Planning**: Pre-assembles context for common query patterns
- **Feedback Loop**: Learns from successful context assemblies