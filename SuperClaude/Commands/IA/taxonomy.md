---
title: Taxonomy Builder
description: Creates hierarchical classification systems for organizing content into structured parent-child category trees
category: information-architecture
tags: [taxonomy, classification, hierarchy, categories]
version: 1.0
---

# /taxonomy

## Purpose
Build hierarchical classification systems for organizing content into structured parent-child category trees. Unlike thesaurus which maps term relationships, taxonomy focuses on categorical structures for navigation and organization.

## Usage
```
/taxonomy [directory] [--method=auto|guided|hybrid] [--depth=3] [--format=tree|json|yaml]
```

## Parameters
- `directory` (optional): Target directory to analyze (defaults to current directory)
- `--method`: Classification approach (auto-generated, guided creation, or hybrid)
- `--depth`: Maximum hierarchy depth (default: 3 levels)
- `--format`: Output format for the taxonomy structure

## Output Structure

### Hierarchical Taxonomy
```yaml
taxonomy:
  name: "Documentation Taxonomy"
  version: "1.0"
  generated: 2024-01-15T10:30:00Z
  max_depth: 3
  total_categories: 24
  
  root_categories:
    getting_started:
      label: "Getting Started"
      description: "Initial setup and basic concepts"
      document_count: 8
      
      subcategories:
        installation:
          label: "Installation & Setup"
          description: "System installation and initial configuration"
          document_count: 3
          documents:
            - "/docs/installation/quick-start.md"
            - "/docs/installation/advanced-setup.md"
            - "/docs/installation/troubleshooting.md"
            
          subcategories:
            platform_specific:
              label: "Platform-Specific Guides"
              description: "Installation guides for different operating systems"
              document_count: 3
              documents:
                - "/docs/installation/windows.md"
                - "/docs/installation/macos.md"
                - "/docs/installation/linux.md"
                
        first_steps:
          label: "First Steps"
          description: "Basic tutorials for new users"
          document_count: 5
          documents:
            - "/docs/tutorials/hello-world.md"
            - "/docs/tutorials/basic-configuration.md"
            
    api_reference:
      label: "API Reference"
      description: "Complete API documentation and examples"
      document_count: 15
      
      subcategories:
        authentication:
          label: "Authentication"
          description: "Authentication methods and security"
          document_count: 4
          
        endpoints:
          label: "API Endpoints"
          description: "Individual endpoint documentation"
          document_count: 11
          
          subcategories:
            user_management:
              label: "User Management"
              document_count: 4
              
            data_operations:
              label: "Data Operations"
              document_count: 7
```

### Category Metadata
```yaml
category_definitions:
  getting_started:
    scope: "Entry-level content for new users"
    target_audience: "beginners"
    typical_formats: ["tutorial", "guide", "quickstart"]
    content_guidelines:
      - "Step-by-step instructions"
      - "Minimal prerequisites assumed"
      - "Clear success criteria"
      - "Troubleshooting sections"
    
  api_reference:
    scope: "Technical reference documentation"
    target_audience: "developers"
    typical_formats: ["reference", "specification", "example"]
    content_guidelines:
      - "Complete parameter documentation"
      - "Request/response examples"
      - "Error code explanations"
      - "SDK code samples"
      
  advanced_topics:
    scope: "Complex implementations and edge cases"
    target_audience: "experienced_users"
    typical_formats: ["guide", "deep-dive", "case-study"]
    content_guidelines:
      - "Assumes domain knowledge"
      - "Performance considerations"
      - "Architecture discussions"
      - "Best practice recommendations"
```

### Auto-Classification Results
```yaml
classification_analysis:
  method: "hybrid"
  confidence_threshold: 0.75
  
  auto_classified:
    high_confidence:
      - document: "/docs/api/users/create.md"
        category: "api_reference.endpoints.user_management"
        confidence: 0.95
        signals:
          - "API endpoint structure detected"
          - "HTTP method specified"
          - "Request/response examples present"
          
    medium_confidence:
      - document: "/docs/guides/performance.md"
        category: "advanced_topics.optimization"
        confidence: 0.68
        signals:
          - "Performance keywords detected"
          - "Advanced terminology used"
        review_needed: true
        
  manual_review_required:
    - document: "/docs/misc/changelog.md"
      reason: "Mixed content patterns"
      suggested_categories:
        - "maintenance.release_notes"
        - "project_info.history"
      confidence_scores: [0.45, 0.42]
      
  unclassified:
    - document: "/docs/legal/terms.md"
      reason: "No matching category patterns"
      suggestions:
        - "Create new category: legal_documents"
        - "Consider exclusion from main taxonomy"
```

### Navigation Structure
```yaml
navigation_mapping:
  primary_navigation:
    - label: "Get Started"
      category: "getting_started"
      order: 1
      featured_pages:
        - "/docs/installation/quick-start.md"
        - "/docs/tutorials/hello-world.md"
        
    - label: "API Docs"
      category: "api_reference"
      order: 2
      featured_pages:
        - "/docs/api/overview.md"
        - "/docs/api/authentication.md"
        
  sidebar_structure:
    getting_started:
      expanded_by_default: true
      show_subcategories: true
      max_visible_items: 10
      
    api_reference:
      expanded_by_default: false
      show_subcategories: true
      grouping: "by_subcategory"
```

## Implementation Strategy

### Content Analysis Methods
1. **Metadata Extraction**: Analyze existing categories, tags, and classifications
2. **Content Clustering**: Group similar documents using NLP techniques
3. **Pattern Recognition**: Identify common content structures and formats
4. **Topic Modeling**: Discover latent themes and subject areas
5. **User Path Analysis**: Understand how content is actually consumed

### Hierarchy Construction
1. **Bottom-Up Approach**: Group similar content then create parent categories
2. **Top-Down Design**: Start with major domains then subdivide
3. **Hybrid Method**: Combine automated clustering with domain expertise
4. **Iterative Refinement**: Test and adjust based on usage patterns

### Classification Rules
1. **Content-Based**: Classify by subject matter and topic
2. **Format-Based**: Group by document type and structure
3. **Audience-Based**: Organize by user role and experience level
4. **Task-Based**: Arrange by user goals and workflows
5. **Lifecycle-Based**: Structure by document maturity and maintenance

### Validation and Quality Assurance
1. **Completeness Check**: Ensure all content fits into taxonomy
2. **Balance Analysis**: Avoid overly deep or broad categories
3. **Overlap Detection**: Identify content that fits multiple categories
4. **Usability Testing**: Validate findability and logical organization

## Use Cases

### Website Navigation Design
- Create intuitive menu structures and page hierarchies
- Design breadcrumb navigation and site maps
- Organize content for optimal user discovery

### Content Management Systems
- Structure CMS categories and content types
- Enable faceted search and filtering
- Support automated content recommendations

### Knowledge Management
- Organize enterprise documentation and resources
- Create subject matter expert directories
- Enable knowledge discovery and sharing

### Information Architecture
- Design logical content structures for complex domains
- Support content migration and reorganization projects
- Establish governance frameworks for content classification

## Integration with Other Commands

### Workflow Dependencies
- **Built from**: `/content-inventory` content analysis
- **Enhanced by**: `/thesaurus` term relationships
- **Validates**: `/sitemap` structural organization
- **Supports**: `/faceted-classification` category frameworks

### Data Exchange
- Provides category structures for navigation design
- Feeds classification schemes into content management
- Supports automated content organization workflows

## Advanced Features

### Multi-Dimensional Taxonomies
```yaml
dimensional_taxonomies:
  by_audience:
    - developers
    - administrators
    - end_users
    
  by_complexity:
    - basic
    - intermediate
    - advanced
    
  by_format:
    - tutorial
    - reference
    - conceptual
    
  cross_classification:
    - document: "/docs/api/advanced-auth.md"
      primary: "api_reference.authentication"
      secondary: ["advanced_topics", "security"]
      audience: "developers"
      complexity: "advanced"
```

### Dynamic Taxonomy Features
- **Adaptive Structure**: Automatically adjust based on content growth
- **Usage Analytics**: Optimize categories based on user behavior
- **A/B Testing**: Compare different taxonomic approaches
- **Temporal Evolution**: Track how content categories change over time

## Technical Notes

### Algorithm Selection
- **K-means Clustering**: For content similarity grouping
- **Hierarchical Clustering**: For natural tree structure discovery
- **Topic Modeling (LDA)**: For theme-based categorization
- **Graph Algorithms**: For relationship-based classification

### Performance Considerations
- Implements incremental classification for new content
- Caches expensive clustering computations
- Provides real-time classification confidence scoring
- Supports distributed processing for large content sets

### Extensibility
- Plugin architecture for custom classification algorithms
- Configurable taxonomy templates for different domains
- Integration with external classification systems
- Support for multilingual taxonomies and localization