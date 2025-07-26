---
title: Document Clustering
category: information-architecture
type: llm-tool
model: gemini-pro-2.5
platform: vertex-ai
created: 2025-07-13
---

# Document Clustering

Groups similar documents using semantic similarity for improved organization and discovery in large documentation collections.

## Purpose

Automatically discovers thematic clusters in documentation using vector embeddings and clustering algorithms, enabling better navigation and context assembly for LLMs.

## Features

- **Semantic Clustering**: Uses embedding-based similarity for content grouping
- **Hierarchical Organization**: Multi-level clustering for complex document sets
- **Topic Extraction**: Automatic cluster labeling and theme identification
- **Cluster Validation**: Quality metrics and coherence scoring
- **Dynamic Reclustering**: Adapts to new documents and changing content

## Configuration

```yaml
clustering_config:
  algorithm: "hierarchical"    # hierarchical, kmeans, dbscan
  similarity_threshold: 0.75   # Minimum similarity for grouping
  min_cluster_size: 3         # Minimum documents per cluster
  max_clusters: 20            # Maximum number of clusters
  embedding_model: "textembedding-gecko@003"
  topic_extraction: true      # Extract cluster topics
  hierarchy_levels: 3         # Maximum nesting depth
```

## Clustering Algorithms

### 1. Hierarchical Clustering
```python
# Bottom-up clustering with similarity threshold
clusters = hierarchical_cluster(
    embeddings=doc_embeddings,
    threshold=similarity_threshold,
    linkage="ward"
)
```

### 2. K-Means Clustering
```python
# Fixed number of clusters
clusters = kmeans_cluster(
    embeddings=doc_embeddings,
    n_clusters=optimal_k,
    random_state=42
)
```

### 3. DBSCAN Clustering
```python
# Density-based clustering for irregular shapes
clusters = dbscan_cluster(
    embeddings=doc_embeddings,
    eps=0.3,
    min_samples=min_cluster_size
)
```

## Usage

```bash
# Cluster all documentation
./scripts/document-clustering.py --input docs/ --algorithm hierarchical

# Cluster with specific parameters
./scripts/document-clustering.py --input docs/ --clusters 15 --threshold 0.8

# Update existing clusters with new documents
./scripts/document-clustering.py --update --cluster-index clusters/

# Interactive cluster exploration
./scripts/document-clustering.py --interactive --rag-index rag_index/
```

## Output Structure

```
clusters/
├── cluster_index.json       # Master cluster index
├── cluster_metadata.yaml    # Clustering configuration
├── clusters/
│   ├── cluster_001/         # Authentication & Security
│   │   ├── documents.json   # Document list and metadata
│   │   ├── summary.md       # Cluster summary and topics
│   │   └── embedding.json   # Cluster centroid embedding
│   └── cluster_002/         # API Documentation
├── hierarchy.json          # Hierarchical cluster structure
└── quality_metrics.json    # Clustering quality scores
```

## Cluster Analysis

### Topic Extraction
```python
# Extract key topics from cluster content
topics = extract_cluster_topics(
    cluster_documents=cluster_docs,
    max_topics=5,
    method="tfidf"  # tfidf, lda, bertopic
)
```

### Quality Metrics
- **Silhouette Score**: Cluster separation and cohesion
- **Inertia**: Within-cluster sum of squared distances
- **Calinski-Harabasz Index**: Cluster validity measure
- **Topic Coherence**: Semantic consistency of cluster themes

### Cluster Visualization
```python
# 2D visualization using t-SNE or UMAP
plot_clusters(
    embeddings=doc_embeddings,
    cluster_labels=labels,
    method="umap",
    output="cluster_visualization.html"
)
```

## Integration Features

- **Search Enhancement**: Cluster-aware semantic search
- **Context Assembly**: Group related documents for LLM context
- **Navigation Aid**: Hierarchical document browsing
- **Recommendation Engine**: Suggest related documents within clusters
- **Quality Monitoring**: Track cluster stability over time

## LLM Optimization

- **Cluster-Based Context**: Assemble context from related clusters
- **Topic-Aware Retrieval**: Use cluster topics for better matching
- **Hierarchical Navigation**: Multi-level document exploration
- **Cluster Summaries**: Condensed overviews for quick understanding