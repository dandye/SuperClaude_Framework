---
title: Content Inventory Generator
description: Creates comprehensive catalogs of documentation with detailed metadata, metrics, and attributes for systematic content management
category: information-architecture
tags: [content-management, inventory, metadata, metrics]
version: 1.0
---

# /content-inventory

## Purpose
Generate a comprehensive catalog of all documents with detailed metadata, content metrics, and file attributes. Unlike structural tools like sitemap, this focuses on the intrinsic characteristics of each document.

## Usage
```
/content-inventory [directory] [--format=table|json|yaml] [--metrics] [--deep-scan]
```

## Parameters
- `directory` (optional): Target directory to inventory (defaults to current directory)
- `--format`: Output format - table (default), json, or yaml
- `--metrics`: Include detailed content metrics (word count, reading time, complexity)
- `--deep-scan`: Include content analysis (headings, links, images)

## Output Structure

### Basic Inventory
```yaml
content_inventory:
  generated: 2024-01-15T10:30:00Z
  total_files: 42
  total_size: "2.3MB"
  
  documents:
    - path: "/docs/api/authentication.md"
      title: "API Authentication Guide"
      size: "4.2KB"
      modified: "2024-01-10T15:20:00Z"
      author: "dev-team"
      type: "markdown"
      language: "en"
      
      frontmatter:
        category: "api"
        tags: ["auth", "security", "guide"]
        status: "published"
        
      metrics:
        word_count: 1247
        reading_time: "5 minutes"
        complexity_score: 3.2
        heading_count: 8
        link_count: 12
        image_count: 2
```

### Extended Metrics (with --metrics)
```yaml
      extended_metrics:
        sentences: 87
        paragraphs: 23
        code_blocks: 6
        tables: 2
        lists: 4
        flesch_reading_ease: 65.2
        grade_level: 8.5
        last_update_age: "5 days"
        maintenance_score: 85
```

### Deep Scan Analysis (with --deep-scan)
```yaml
      content_analysis:
        headings:
          - level: 1
            text: "API Authentication Guide"
          - level: 2
            text: "OAuth 2.0 Setup"
            
        internal_links:
          - target: "/docs/api/endpoints.md"
            text: "API Endpoints"
          - target: "/docs/security/best-practices.md"
            text: "Security Best Practices"
            
        external_links:
          - url: "https://oauth.net/2/"
            text: "OAuth 2.0 Specification"
            status: "active"
            
        images:
          - src: "/assets/auth-flow.png"
            alt: "Authentication Flow Diagram"
            size: "245KB"
```

## Implementation Strategy

### File Discovery and Classification
1. **Recursive File Traversal**: Walk directory tree identifying documentation files
2. **File Type Detection**: Classify by extension and content inspection
3. **Encoding Detection**: Handle various text encodings properly
4. **Binary File Filtering**: Exclude non-text files from content analysis

### Metadata Extraction
1. **YAML Frontmatter Parsing**: Extract structured metadata from document headers
2. **Git Integration**: Pull author, creation date, and modification history
3. **File System Attributes**: Size, permissions, timestamps
4. **Language Detection**: Identify document language for appropriate processing

### Content Metrics Calculation
1. **Text Statistics**: Word count, sentence count, paragraph count
2. **Readability Scores**: Flesch Reading Ease, grade level assessment
3. **Structural Elements**: Count headings, lists, tables, code blocks
4. **Link Analysis**: Internal vs external links, broken link detection
5. **Media Inventory**: Images, videos, attachments with size analysis

### Quality Assessment
1. **Maintenance Score**: Based on recency, completeness, link health
2. **Completeness Check**: Required metadata presence, content depth
3. **Freshness Analysis**: Time since last update, content aging indicators
4. **Consistency Metrics**: Naming conventions, structure adherence

## Use Cases

### Documentation Audit
- Identify outdated or unmaintained content
- Track content ownership and responsibility
- Measure documentation coverage and quality

### Content Migration Planning
- Assess content volume and complexity for migration efforts
- Identify dependencies and relationships between documents
- Plan content consolidation and restructuring

### Performance Optimization
- Identify large files that may need compression
- Find duplicate or similar content for consolidation
- Assess image and media optimization opportunities

### Compliance and Governance
- Verify metadata completeness for governance requirements
- Track content approval status and review cycles
- Monitor content freshness for compliance standards

## Integration with Other Commands

### Workflow Synergies
- **Pre-requisite for**: `/content-audit`, `/gap-analysis`, `/cross-reference`
- **Complements**: `/sitemap` (structure vs attributes), `/metadata-schema` (validation)
- **Feeds into**: `/ia-scorecard` (provides base metrics)

### Data Exchange
- Outputs can be consumed by other IA tools for analysis
- JSON/YAML formats enable programmatic processing
- Integrates with existing CI/CD pipelines for automated reporting

## Technical Notes

### Performance Considerations
- Implements streaming processing for large repositories
- Caches expensive operations (readability calculations)
- Provides progress indicators for long-running scans
- Supports incremental updates for changed files only

### Extensibility
- Plugin architecture for custom metric calculations
- Configurable output templates
- Support for custom file type handlers
- Integration hooks for external metadata sources