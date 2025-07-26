---
title: Cross-Reference Matrix Generator
description: Maps inter-document relationships, dependencies, and reference patterns to visualize content interconnections
category: information-architecture
tags: [relationships, dependencies, cross-reference, links]
version: 1.0
---

# /cross-reference

## Purpose
Build a comprehensive matrix showing inter-document relationships, citations, and dependencies. Analyzes internal links, references, and content relationships to identify connection patterns, dependency chains, and orphaned documents.

## Usage
```
/cross-reference [directory] [--format=matrix|graph|json] [--include-external] [--depth=2]
```

## Parameters
- `directory` (optional): Target directory to analyze (defaults to current directory)
- `--format`: Output format - matrix (default), graph, or json
- `--include-external`: Include external URL references in analysis
- `--depth`: Relationship depth to analyze (1=direct, 2=2nd degree, etc.)

## Output Structure

### Reference Matrix
```yaml
cross_reference_matrix:
  generated: 2024-01-15T10:30:00Z
  total_documents: 42
  total_relationships: 156
  orphaned_documents: 3
  
  matrix:
    "/docs/api/auth.md":
      outbound_references:
        - target: "/docs/api/endpoints.md"
          type: "direct_link"
          context: "See endpoint documentation"
          line: 45
          
        - target: "/docs/security/oauth.md"
          type: "content_reference"
          context: "OAuth implementation details"
          line: 78
          
      inbound_references:
        - source: "/docs/getting-started.md"
          type: "direct_link"
          context: "Authentication setup"
          
        - source: "/docs/tutorials/quick-start.md"
          type: "content_reference"
          context: "Login configuration"
          
      relationship_strength: 8.5
      centrality_score: 0.65
      
  dependency_chains:
    - chain: ["/docs/setup.md", "/docs/config.md", "/docs/deployment.md"]
      type: "sequential"
      strength: "strong"
      
    - chain: ["/docs/api/auth.md", "/docs/api/endpoints.md", "/docs/api/errors.md"]
      type: "hierarchical"
      strength: "medium"
```

### Relationship Graph (with --format=graph)
```yaml
relationship_graph:
  nodes:
    - id: "/docs/api/auth.md"
      title: "API Authentication"
      type: "documentation"
      centrality: 0.65
      cluster: "api"
      
    - id: "/docs/security/oauth.md"
      title: "OAuth Configuration"
      type: "guide"
      centrality: 0.42
      cluster: "security"
      
  edges:
    - source: "/docs/api/auth.md"
      target: "/docs/security/oauth.md"
      weight: 3
      type: "reference"
      bidirectional: false
      
  clusters:
    - name: "api"
      documents: 8
      internal_connections: 15
      external_connections: 7
      
    - name: "security" 
      documents: 5
      internal_connections: 8
      external_connections: 12
```

### Relationship Analysis
```yaml
analysis:
  hub_documents:
    - path: "/docs/api/overview.md"
      inbound_count: 12
      outbound_count: 8
      centrality: 0.85
      role: "central_hub"
      
  authority_documents:
    - path: "/docs/architecture/principles.md"
      inbound_count: 15
      outbound_count: 2
      authority_score: 0.92
      role: "reference_authority"
      
  orphaned_documents:
    - path: "/docs/legacy/old-api.md"
      reason: "no_inbound_references"
      last_modified: "2023-06-15"
      recommendation: "review_for_removal"
      
  broken_references:
    - source: "/docs/tutorials/setup.md"
      target: "/docs/config/database.md"
      line: 34
      error: "file_not_found"
      
  circular_dependencies:
    - cycle: ["/docs/a.md", "/docs/b.md", "/docs/c.md", "/docs/a.md"]
      severity: "medium"
      recommendation: "restructure_relationships"
```

## Implementation Strategy

### Link Discovery and Classification
1. **Markdown Link Parsing**: Extract `[text](url)` and `<url>` references
2. **Wiki-style Links**: Handle `[[page]]` and `[[page|display]]` formats
3. **Reference Patterns**: Detect implicit references via content analysis
4. **Include/Import Detection**: Find file inclusion and import statements

### Relationship Strength Calculation
1. **Direct Links**: Explicit hyperlinks between documents
2. **Content References**: Mentions without direct links
3. **Shared Terminology**: Common keywords and concepts
4. **Sequential Flow**: Documents in logical progression
5. **Hierarchical Structure**: Parent-child relationships

### Network Analysis Metrics
1. **Centrality Measures**: Betweenness, closeness, eigenvector centrality
2. **Hub Detection**: Documents with many outbound connections
3. **Authority Identification**: Documents with many inbound connections
4. **Cluster Analysis**: Related document groupings
5. **Path Analysis**: Shortest paths between document pairs

### Dependency Chain Detection
1. **Sequential Dependencies**: A→B→C progression patterns
2. **Hierarchical Dependencies**: Parent-child document structures
3. **Circular Dependencies**: Problematic reference loops
4. **Missing Links**: Expected but absent connections

## Use Cases

### Content Architecture Review
- Identify poorly connected or orphaned content
- Find over-connected documents that may need splitting
- Discover natural content clusters and topics

### Navigation Design
- Identify key hub documents for navigation menus
- Find logical pathways through content
- Optimize content discoverability

### Content Maintenance
- Detect broken internal links and references
- Identify outdated cross-references
- Plan content restructuring efforts

### Knowledge Mapping
- Visualize expertise domains and subject areas
- Track information flow through documentation
- Identify knowledge gaps and overlaps

## Integration with Other Commands

### Workflow Dependencies
- **Requires**: Well-structured internal linking
- **Enhances**: `/sitemap` with relationship data
- **Feeds**: `/navigation-blueprint` with connection patterns
- **Validates**: `/content-inventory` link health metrics

### Data Synergies
- Provides relationship data for `/content-relationships` visualization
- Informs `/gap-analysis` with connection patterns
- Supplies metrics for `/ia-scorecard` connectivity scores

## Technical Notes

### Performance Optimization
- Implements caching for expensive relationship calculations
- Uses graph databases for complex relationship queries
- Provides incremental analysis for changed documents
- Supports parallel processing for large document sets

### Output Formats
- **Matrix**: Tabular view showing all document interconnections
- **Graph**: Node-edge format suitable for visualization tools
- **JSON**: Machine-readable format for programmatic analysis
- **Interactive**: HTML output with clickable relationship explorer

### Extensibility
- Plugin system for custom relationship detection
- Configurable relationship weighting algorithms
- Support for external link validation services
- Integration with version control for relationship history tracking