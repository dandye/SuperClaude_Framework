---
title: Context Window Optimizer
description: Analyzes and optimizes document chunking for LLM token limits, ensuring maximum context utilization while maintaining semantic coherence
category: information-architecture
tags: [context-window, chunking, tokens, llm-optimization, segmentation]
version: 1.0
---

# /context-optimizer

## Purpose
Optimize document segmentation for LLM context windows by analyzing token usage, creating intelligent chunks that respect semantic boundaries, and providing model-specific recommendations for context loading.

## Usage
```
/context-optimizer [directory] [--model=gpt-4|claude|llama] [--strategy=semantic|sliding|hierarchical] [--max-tokens=8000]
```

## Parameters
- `directory` (optional): Target directory to analyze (defaults to current directory)
- `--model`: Target LLM model for optimization (affects token counting and limits)
- `--strategy`: Chunking strategy (semantic boundaries, sliding window, or hierarchical)
- `--max-tokens`: Maximum tokens per chunk (default based on model)

## Output Structure

### Token Analysis
```yaml
token_analysis:
  generated: 2024-01-15T10:30:00Z
  tokenizer: "cl100k_base"  # GPT-4 tokenizer. # FixMe: I use Claude Code or Gemini 2.5 pro
  total_documents: 42
  total_tokens: 156789

  document_metrics:
    - path: "/docs/api/authentication.md"
      total_tokens: 3456
      sentences: 124
      paragraphs: 18
      code_blocks: 6

      token_distribution:
        text_tokens: 2890
        code_tokens: 456
        whitespace_tokens: 110

      complexity_factors:
        technical_terms: 89
        cross_references: 12
        prerequisites: 3
```

### Optimal Chunking
```yaml
chunking_strategy:
  method: "semantic_boundaries"
  target_model: "gpt-4"
  context_limit: 8192
  reserved_tokens: 1000  # For prompts/responses

  documents:
    "/docs/api/authentication.md":
      recommended_chunks: 3

      chunks:
        - chunk_id: "auth_chunk_1"
          title: "Authentication Overview"
          tokens: 2145
          start_line: 1
          end_line: 67

          boundaries:
            start: "section_header"
            end: "paragraph_end"

          context_preservation:
            overlap_tokens: 128
            shared_concepts: ["authentication", "api"]

          semantic_coherence: 0.92
          self_contained: true

        - chunk_id: "auth_chunk_2"
          title: "OAuth 2.0 Implementation"
          tokens: 2234
          start_line: 68
          end_line: 156

          dependencies:
            requires: ["auth_chunk_1"]
            references: ["/docs/security/oauth.md"]

          code_blocks:
            - language: "python"
              tokens: 234
              purpose: "oauth_flow_example"
```

### Model-Specific Recommendations
```yaml
model_recommendations:
  gpt-4:
    context_window: 8192
    recommended_chunks: 3-4
    optimal_chunk_size: 2000-2500

    loading_strategy:
      - "Load prerequisite context first"
      - "Include 128 token overlap between chunks"
      - "Reserve 1500 tokens for system prompt"

    example_prompt: |
      <context>
      {chunk_1}
      </context>

      <context>
      {chunk_2}
      </context>

      Question: {user_query}

  claude-3:
    context_window: 100000
    recommended_chunks: 15-20
    optimal_chunk_size: 4000-5000

    loading_strategy:
      - "Can load entire document sections"
      - "Group related documents together"
      - "Use XML tags for context separation"

  llama-2:
    context_window: 4096
    recommended_chunks: 1-2
    optimal_chunk_size: 1200-1500

    loading_strategy:
      - "Aggressive summarization needed"
      - "Focus on most relevant sections"
      - "Consider pre-computed summaries"
```

### Chunk Relationships
```yaml
chunk_graph:
  nodes:
    - id: "auth_chunk_1"
      type: "overview"
      standalone: true

    - id: "auth_chunk_2"
      type: "implementation"
      requires: ["auth_chunk_1"]

    - id: "auth_chunk_3"
      type: "examples"
      requires: ["auth_chunk_1", "auth_chunk_2"]

  edges:
    - from: "auth_chunk_1"
      to: "auth_chunk_2"
      relationship: "prerequisite"
      strength: 0.9

    - from: "auth_chunk_2"
      to: "oauth_chunk_1"
      relationship: "references"
      strength: 0.7
```

### Context Loading Patterns
```yaml
loading_patterns:
  question_answering:
    pattern: "focused"
    strategy:
      - "Identify most relevant chunk via embedding search"
      - "Load prerequisite chunks if needed"
      - "Include overlap for context continuity"

    example:
      query: "How do I implement OAuth?"
      chunks_loaded: ["auth_chunk_2", "auth_chunk_1", "oauth_chunk_1"]
      total_tokens: 6234

  comprehensive_understanding:
    pattern: "progressive"
    strategy:
      - "Start with overview chunks"
      - "Progressively load detailed sections"
      - "Maintain conceptual coherence"

  code_generation:
    pattern: "example_focused"
    strategy:
      - "Prioritize chunks with code examples"
      - "Include minimal explanatory text"
      - "Load related API documentation"
```

### Optimization Metrics
```yaml
optimization_results:
  before_optimization:
    average_chunk_size: 4567
    context_overflow_rate: 0.34
    semantic_breaks: 45
    orphaned_references: 23

  after_optimization:
    average_chunk_size: 2234
    context_overflow_rate: 0.02
    semantic_breaks: 3
    orphaned_references: 0

  improvements:
    context_utilization: "+38%"
    retrieval_accuracy: "+24%"
    response_relevance: "+31%"
```

## Implementation Strategy

### Chunking Algorithms
1. **Semantic Boundary Detection**: Use NLP to find natural breaks
2. **Token Counting**: Accurate model-specific tokenization
3. **Overlap Calculation**: Maintain context between chunks
4. **Hierarchy Preservation**: Respect document structure

### Optimization Techniques
1. **Dynamic Programming**: Find optimal chunk boundaries
2. **Graph Algorithms**: Model chunk dependencies
3. **Compression**: Identify removable content
4. **Caching**: Store pre-computed chunks

## Use Cases

### RAG Systems
- Optimize document chunks for retrieval
- Ensure retrieved content fits context windows
- Maintain semantic coherence in responses

### Documentation Q&A
- Structure content for efficient querying
- Reduce token waste from irrelevant content
- Improve response accuracy

### Code Understanding
- Separate code from explanations
- Group related code examples
- Maintain execution context

### Multi-Document Synthesis
- Optimize loading multiple related documents
- Manage token budget across sources
- Preserve cross-document relationships

## Integration with Other Commands

### Workflow Dependencies
- **Uses**: `/content-inventory` for document structure
- **Enhanced by**: `/document-embeddings` for semantic chunking
- **Feeds**: `/chunk-retriever` with optimized segments
- **Supports**: `/qa-generator` with coherent contexts

## Technical Notes

### Token Counting
- Uses model-specific tokenizers (tiktoken, sentencepiece)
- Accounts for special tokens and formatting
- Handles code vs. text differently

### Performance
- Pre-computes chunks for common models
- Supports incremental updates
- Provides fast chunk retrieval
- Implements lazy loading for large repos

### Extensibility
- Plugin system for custom chunking strategies
- Support for new model configurations
- Custom boundary detection rules
- Integration with fine-tuned models