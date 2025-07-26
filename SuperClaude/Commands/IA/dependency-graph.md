---
title: Documentation Dependency Graph
description: Maps prerequisite relationships between documents to help LLMs load required context in the correct order
category: information-architecture
tags: [dependencies, prerequisites, knowledge-graph, learning-path, context-loading]
version: 1.0
---

# /dependency-graph

## Purpose
Create a directed graph of document dependencies showing which content requires prior understanding of other documents. Enables LLMs to load prerequisite context before attempting to understand dependent content, ensuring comprehensive understanding.

## Usage
```
/dependency-graph [directory] [--format=visual|yaml|json] [--analysis=deep|shallow] [--detect=explicit|implicit|both]
```

## Parameters
- `directory` (optional): Target directory to analyze (defaults to current directory)
- `--format`: Output format (interactive visualization, YAML, or JSON)
- `--analysis`: Depth of dependency detection (deep includes semantic analysis)
- `--detect`: Types of dependencies to detect (explicit links, implicit concepts, or both)

## Output Structure

### Dependency Graph
```yaml
dependency_graph:
  generated: 2024-01-15T10:30:00Z
  total_nodes: 42
  total_edges: 87
  acyclic: true  # No circular dependencies
  
  nodes:
    - id: "/docs/getting-started/installation.md"
      title: "Installation Guide"
      level: 0  # Foundation level - no dependencies
      type: "prerequisite"
      
      metadata:
        complexity: "beginner"
        estimated_reading_time: "5 minutes"
        key_concepts: ["installation", "setup", "requirements"]
        
    - id: "/docs/api/authentication.md"
      title: "API Authentication"
      level: 2
      type: "core_concept"
      
      dependencies:
        strong:
          - node: "/docs/getting-started/api-basics.md"
            reason: "Requires understanding of API fundamentals"
            confidence: 0.95
            
          - node: "/docs/concepts/security.md"
            reason: "Builds on security concepts"
            confidence: 0.87
            
        weak:
          - node: "/docs/tutorials/quickstart.md"
            reason: "References setup from quickstart"
            confidence: 0.62
            
      concepts_required:
        - "HTTP basics"
        - "API endpoints"
        - "Security tokens"
```

### Learning Paths
```yaml
learning_paths:
  beginner_to_expert:
    total_documents: 24
    estimated_time: "8 hours"
    
    stages:
      - stage: "Foundation"
        documents:
          - "/docs/getting-started/installation.md"
          - "/docs/getting-started/concepts.md"
          - "/docs/getting-started/first-project.md"
        concepts_learned: ["setup", "basic_concepts", "project_structure"]
        
      - stage: "Core Concepts"
        prerequisites: ["Foundation"]
        documents:
          - "/docs/concepts/architecture.md"
          - "/docs/api/basics.md"
          - "/docs/concepts/security.md"
        concepts_learned: ["system_design", "api_fundamentals", "security_basics"]
        
      - stage: "Implementation"
        prerequisites: ["Foundation", "Core Concepts"]
        documents:
          - "/docs/api/authentication.md"
          - "/docs/api/endpoints.md"
          - "/docs/tutorials/integration.md"
        concepts_learned: ["api_implementation", "integration_patterns"]
        
  task_specific:
    implement_oauth:
      goal: "Implement OAuth 2.0 authentication"
      required_reading:
        - order: 1
          document: "/docs/concepts/security.md"
          reason: "Understand security fundamentals"
          
        - order: 2
          document: "/docs/api/basics.md"
          reason: "Learn API structure"
          
        - order: 3
          document: "/docs/api/authentication.md"
          reason: "OAuth implementation details"
          
        - order: 4
          document: "/docs/examples/oauth-flow.md"
          reason: "See practical example"
```

### Dependency Analysis
```yaml
dependency_analysis:
  circular_dependencies: []  # None found
  
  orphaned_documents:
    - path: "/docs/misc/changelog.md"
      recommendation: "Consider linking to release process docs"
      
  dependency_chains:
    longest_chain:
      length: 6
      path:
        - "/docs/getting-started/installation.md"
        - "/docs/getting-started/concepts.md"
        - "/docs/api/basics.md"
        - "/docs/api/authentication.md"
        - "/docs/advanced/custom-auth.md"
        - "/docs/advanced/auth-plugins.md"
        
  bottleneck_documents:
    - document: "/docs/api/basics.md"
      dependent_count: 18
      criticality: "high"
      recommendation: "Ensure this document is comprehensive"
      
    - document: "/docs/concepts/security.md"
      dependent_count: 12
      criticality: "high"
      recommendation: "Keep updated with all security practices"
```

### Concept Propagation
```yaml
concept_flow:
  core_concepts:
    - concept: "authentication"
      introduced_in: "/docs/concepts/security.md"
      
      propagation_path:
        - document: "/docs/api/basics.md"
          usage: "mentioned"
          
        - document: "/docs/api/authentication.md"
          usage: "detailed_explanation"
          
        - document: "/docs/tutorials/oauth-setup.md"
          usage: "implementation"
          
        - document: "/docs/advanced/custom-auth.md"
          usage: "extension"
          
    - concept: "api_endpoint"
      introduced_in: "/docs/api/basics.md"
      assumed_knowledge_in: 
        - "/docs/api/endpoints.md"
        - "/docs/api/authentication.md"
        - "/docs/tutorials/integration.md"
```

### LLM Context Loading
```yaml
context_loading_strategies:
  comprehensive:
    description: "Load all prerequisites for complete understanding"
    
    example:
      target: "/docs/advanced/custom-auth.md"
      load_order:
        1: "/docs/concepts/security.md"  # 1200 tokens
        2: "/docs/api/basics.md"          # 1800 tokens
        3: "/docs/api/authentication.md"  # 2400 tokens
        4: "/docs/advanced/custom-auth.md" # 2000 tokens
      total_tokens: 7400
      
  minimal:
    description: "Load only essential prerequisites"
    
    example:
      target: "/docs/advanced/custom-auth.md"
      load_order:
        1: "/docs/api/authentication.md"  # 2400 tokens
        2: "/docs/advanced/custom-auth.md" # 2000 tokens
      total_tokens: 4400
      skipped_context: ["basic concepts", "security fundamentals"]
      
  progressive:
    description: "Load context as needed based on queries"
    
    strategy:
      - "Start with target document"
      - "Load prerequisites when referenced"
      - "Cache loaded context for session"
```

### Visualization Data
```yaml
graph_visualization:
  layout: "hierarchical"
  
  levels:
    0:  # Foundation
      documents: 3
      color: "#4CAF50"
      
    1:  # Basic concepts
      documents: 8
      color: "#2196F3"
      
    2:  # Implementation
      documents: 15
      color: "#FF9800"
      
    3:  # Advanced
      documents: 10
      color: "#9C27B0"
      
  edge_weights:
    strong_dependency: 1.0
    weak_dependency: 0.5
    implicit_reference: 0.3
```

## Implementation Strategy

### Dependency Detection
1. **Explicit Links**: Parse document links and references
2. **Import Analysis**: Detect code imports and includes
3. **Concept Tracking**: Follow concept introduction and usage
4. **Semantic Analysis**: Use NLP to find implicit dependencies

### Graph Construction
1. **Topological Sorting**: Order documents by dependency level
2. **Cycle Detection**: Identify and flag circular dependencies
3. **Path Finding**: Calculate learning paths
4. **Centrality Analysis**: Find critical documents

## Use Cases

### LLM Context Management
- Load prerequisites before dependent content
- Optimize token usage with minimal paths
- Ensure comprehensive understanding

### Learning Path Generation
- Create customized learning sequences
- Support different skill levels
- Enable task-specific documentation paths

### Documentation Quality
- Identify missing prerequisites
- Find over-connected documents
- Detect knowledge gaps

### Content Organization
- Restructure based on dependencies
- Create logical groupings
- Optimize navigation flow

## Integration with Other Commands

### Workflow Dependencies
- **Enhanced by**: `/content-inventory` for document metadata
- **Complements**: `/cross-reference` for relationship types
- **Feeds**: `/navigation-blueprint` for user journeys
- **Supports**: `/context-optimizer` for loading strategies

## Technical Notes

### Algorithms
- **Tarjan's Algorithm**: Detect strongly connected components
- **Topological Sort**: Order documents by dependencies
- **PageRank Variant**: Identify important documents
- **Dijkstra's Algorithm**: Find shortest learning paths

### Performance
- Incremental graph updates for new documents
- Caches computed paths and dependencies
- Parallel edge detection for large repos
- Optimized graph traversal algorithms