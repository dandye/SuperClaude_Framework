---
title: Metadata Schema Manager
description: Defines, validates, and maintains consistent metadata structures and YAML frontmatter standards across documentation
category: information-architecture
tags: [metadata, schema, frontmatter, validation, standards]
version: 1.0
---

# /metadata-schema

## Purpose
Create and enforce standardized metadata field definitions, validation rules, and templates for different document types. Ensures consistency across all YAML frontmatter usage and provides validation for metadata compliance.

## Usage
```
/metadata-schema [action] [--template=type] [--validate] [--generate-docs]
```

## Actions
- `create`: Generate new metadata schema
- `validate`: Check existing documents against schema
- `template`: Generate frontmatter templates
- `report`: Analyze current metadata usage patterns

## Parameters
- `--template`: Document type (api, tutorial, guide, reference, etc.)
- `--validate`: Run validation against existing documents
- `--generate-docs`: Create documentation for the schema

## Output Structure

### Schema Definition
```yaml
metadata_schema:
  version: "1.0"
  generated: 2024-01-15T10:30:00Z
  
  global_fields:
    title:
      type: "string"
      required: true
      description: "Human-readable document title"
      pattern: "^[A-Z].*"
      max_length: 80
      
    description:
      type: "string"
      required: true
      description: "Brief summary of document content"
      max_length: 200
      min_length: 20
      
    category:
      type: "string"
      required: true
      description: "Primary content category"
      enum: ["api", "tutorial", "guide", "reference", "concept"]
      
    tags:
      type: "array"
      required: false
      description: "Topic keywords for classification"
      items:
        type: "string"
        pattern: "^[a-z0-9-]+$"
      max_items: 10
      
    version:
      type: "string"
      required: false
      description: "Document version"
      pattern: "^\d+\.\d+(\.\d+)?$"
      
    last_reviewed:
      type: "date"
      required: false
      description: "Last content review date"
      format: "YYYY-MM-DD"
      
  document_types:
    api:
      extends: "global_fields"
      additional_fields:
        endpoint:
          type: "string"
          required: true
          description: "API endpoint path"
          pattern: "^/.*"
          
        method:
          type: "string"
          required: true
          description: "HTTP method"
          enum: ["GET", "POST", "PUT", "DELETE", "PATCH"]
          
        authentication:
          type: "string"
          required: true
          description: "Required authentication type"
          enum: ["none", "api_key", "oauth", "basic_auth"]
          
    tutorial:
      extends: "global_fields"
      additional_fields:
        difficulty:
          type: "string"
          required: true
          description: "Tutorial difficulty level"
          enum: ["beginner", "intermediate", "advanced"]
          
        duration:
          type: "string"
          required: true
          description: "Estimated completion time"
          pattern: "^\d+\s+(minutes?|hours?)$"
          
        prerequisites:
          type: "array"
          required: false
          description: "Required prior knowledge or setup"
          items:
            type: "string"
```

### Document Templates
```yaml
templates:
  api_reference:
    frontmatter: |
      ---
      title: "{{endpoint_name}} API"
      description: "{{brief_description}}"
      category: "api"
      tags: ["api", "{{service_name}}", "{{method_lower}}"]
      endpoint: "{{endpoint_path}}"
      method: "{{http_method}}"
      authentication: "{{auth_type}}"
      version: "{{api_version}}"
      last_reviewed: "{{current_date}}"
      ---
      
  tutorial:
    frontmatter: |
      ---
      title: "{{tutorial_title}}"
      description: "{{tutorial_description}}"
      category: "tutorial"
      tags: ["tutorial", "{{primary_topic}}", "{{secondary_topic}}"]
      difficulty: "{{difficulty_level}}"
      duration: "{{estimated_time}}"
      prerequisites: {{prerequisite_list}}
      version: "1.0"
      last_reviewed: "{{current_date}}"
      ---
      
  guide:
    frontmatter: |
      ---
      title: "{{guide_title}}"
      description: "{{guide_description}}"
      category: "guide"
      tags: ["guide", "{{topic}}", "{{subtopic}}"]
      audience: "{{target_audience}}"
      complexity: "{{complexity_level}}"
      version: "{{guide_version}}"
      last_reviewed: "{{current_date}}"
      ---
```

### Validation Report
```yaml
validation_report:
  generated: 2024-01-15T10:30:00Z
  files_checked: 42
  
  compliance_summary:
    fully_compliant: 28
    partially_compliant: 10
    non_compliant: 4
    compliance_rate: 67%
    
  common_violations:
    - violation: "missing_required_field"
      field: "description"
      count: 8
      severity: "error"
      
    - violation: "invalid_enum_value"
      field: "category"
      invalid_values: ["docs", "help"]
      expected_values: ["api", "tutorial", "guide", "reference", "concept"]
      count: 3
      severity: "error"
      
    - violation: "pattern_mismatch"
      field: "tags"
      pattern: "^[a-z0-9-]+$"
      invalid_examples: ["API-Guide", "Setup_Tutorial"]
      count: 5
      severity: "warning"
      
  file_specific_issues:
    "/docs/api/webhooks.md":
      issues:
        - type: "missing_field"
          field: "endpoint"
          message: "API documents must specify endpoint"
          
        - type: "invalid_value"
          field: "method"
          value: "post"
          expected: "POST"
          
    "/docs/tutorials/setup.md":
      issues:
        - type: "missing_field"
          field: "difficulty"
          message: "Tutorials must specify difficulty level"
          suggested_value: "beginner"
```

### Auto-Fix Suggestions
```yaml
auto_fix_suggestions:
  - file: "/docs/api/authentication.md"
    fixes:
      - action: "add_missing_field"
        field: "last_reviewed"
        suggested_value: "2024-01-15"
        confidence: "high"
        
      - action: "normalize_case"
        field: "method"
        current: "get"
        suggested: "GET"
        confidence: "high"
        
  - file: "/docs/guides/deployment.md"
    fixes:
      - action: "standardize_tags"
        field: "tags"
        current: ["Deployment-Guide", "Setup_Help"]
        suggested: ["deployment-guide", "setup-help"]
        confidence: "high"
```

## Implementation Strategy

### Schema Design Principles
1. **Inheritance**: Base fields extended by document-type-specific fields
2. **Flexibility**: Required vs optional field definitions
3. **Validation**: Pattern matching, enums, and constraints
4. **Evolution**: Versioned schemas for backward compatibility
5. **Documentation**: Self-documenting with descriptions and examples

### Validation Engine
1. **Syntax Validation**: YAML parsing and structure verification
2. **Schema Compliance**: Field presence, type checking, constraint validation
3. **Business Rules**: Cross-field dependencies and logical constraints
4. **Content Quality**: Value appropriateness and consistency checks

### Template Generation
1. **Dynamic Templates**: Variable substitution based on context
2. **Interactive Prompts**: Guided frontmatter creation
3. **Batch Application**: Apply templates to multiple documents
4. **Custom Templates**: User-defined templates for specific needs

### Auto-Fix Capabilities
1. **Safe Corrections**: Unambiguous fixes like case normalization
2. **Suggested Fixes**: Recommendations requiring human review
3. **Batch Operations**: Apply consistent fixes across multiple files
4. **Rollback Support**: Undo automatic changes if needed

## Use Cases

### Documentation Standardization
- Enforce consistent metadata across large documentation sets
- Migrate legacy documents to standardized metadata schemas
- Onboard new team members with clear metadata guidelines

### Quality Assurance
- Validate metadata completeness and accuracy
- Prevent publication of documents with incomplete metadata
- Maintain metadata quality over time with regular validation

### Content Management
- Enable powerful filtering and search based on metadata
- Support automated content workflows and publishing pipelines
- Facilitate content audit and maintenance processes

### Integration Support
- Provide structured metadata for static site generators
- Enable API-driven content management systems
- Support automated documentation generation tools

## Integration with Other Commands

### Workflow Dependencies
- **Validates**: `/content-inventory` metadata completeness
- **Supports**: `/yaml-frontmatter` with standardized schemas
- **Enables**: `/faceted-classification` with consistent field structures
- **Informs**: `/content-audit` with metadata quality rules

### Data Flow
- Provides validation rules for other IA tools
- Supplies templates for new document creation
- Feeds metadata standards into content management workflows

## Technical Notes

### Schema Format
- Uses JSON Schema standard for validation rules
- Supports YAML and JSON output formats
- Provides human-readable documentation generation
- Enables programmatic schema validation

### Performance Optimization
- Caches parsed schemas for repeated validation
- Supports incremental validation for changed files only
- Provides batch processing for large document sets
- Implements efficient pattern matching algorithms

### Extensibility
- Plugin architecture for custom validation rules
- Support for organization-specific metadata requirements
- Integration with external schema registries
- Custom template creation and management

### Integration Capabilities
- CI/CD integration for automated validation
- IDE plugin support for real-time validation
- API for programmatic schema management
- Export to documentation generation tools