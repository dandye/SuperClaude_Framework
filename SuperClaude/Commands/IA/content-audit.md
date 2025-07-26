---
title: Content Quality Audit
description: Evaluates documentation quality, relevance, maintenance needs, and provides actionable improvement recommendations
category: information-architecture
tags: [audit, quality, maintenance, recommendations]
version: 1.0
---

# /content-audit

## Purpose
Perform comprehensive quality assessment of documentation to identify outdated information, broken links, missing metadata, duplicate content, and quality issues. Provides actionable recommendations for content improvement and maintenance prioritization.

## Usage
```
/content-audit [directory] [--severity=all|high|medium|low] [--category=all|quality|freshness|structure|metadata]
```

## Parameters
- `directory` (optional): Target directory to audit (defaults to current directory)
- `--severity`: Filter issues by severity level
- `--category`: Focus on specific audit categories
- `--fix-mode`: Suggest automated fixes where possible

## Output Structure

### Audit Summary
```yaml
content_audit:
  generated: 2024-01-15T10:30:00Z
  scope: "/docs/"
  files_audited: 42
  
  overall_score: 7.2/10
  
  issue_summary:
    critical: 3
    high: 8
    medium: 15
    low: 24
    
  categories:
    quality_issues: 18
    freshness_issues: 12
    structure_issues: 10
    metadata_issues: 10
```

### Quality Issues
```yaml
quality_issues:
  - file: "/docs/api/authentication.md"
    severity: "high"
    category: "broken_links"
    issue: "External link returns 404"
    line: 67
    details:
      url: "https://example.com/oauth-guide"
      status_code: 404
      last_checked: "2024-01-15T09:15:00Z"
    recommendation: "Update link to current OAuth documentation"
    auto_fix: false
    
  - file: "/docs/tutorials/setup.md"
    severity: "medium"
    category: "readability"
    issue: "Poor readability score"
    details:
      flesch_score: 32.1
      grade_level: 14.2
      recommended_max: 8.0
    recommendation: "Simplify language and break up complex sentences"
    auto_fix: false
    
  - file: "/docs/config/database.md"
    severity: "critical"
    category: "security"
    issue: "Contains exposed credentials"
    line: 23
    details:
      pattern: "password=supersecret123"
      type: "hardcoded_credential"
    recommendation: "Replace with environment variable reference"
    auto_fix: true
    suggested_fix: "password=${DB_PASSWORD}"
```

### Freshness Assessment
```yaml
freshness_issues:
  - file: "/docs/deployment/docker.md"
    severity: "high"
    category: "outdated_content"
    issue: "References deprecated Docker syntax"
    last_modified: "2022-03-15T10:20:00Z"
    age_days: 305
    details:
      deprecated_syntax: "MAINTAINER instruction"
      current_syntax: "LABEL maintainer"
    recommendation: "Update to current Docker best practices"
    
  - file: "/docs/api/v1/endpoints.md"
    severity: "medium"  
    category: "stale_content"
    issue: "No updates in 6+ months for active API"
    last_modified: "2023-06-10T14:30:00Z"
    age_days: 218
    recommendation: "Review for accuracy and update if needed"
```

### Structure Issues
```yaml
structure_issues:
  - file: "/docs/guides/advanced-features.md"
    severity: "medium"
    category: "heading_structure"
    issue: "Skipped heading levels (H1 to H3)"
    line: 45
    details:
      found: "### Advanced Configuration"
      expected: "## Advanced Configuration"
    recommendation: "Use sequential heading levels for better navigation"
    auto_fix: true
    
  - file: "/docs/troubleshooting/errors.md"
    severity: "low"
    category: "document_length"
    issue: "Extremely long document"
    details:
      word_count: 4567
      recommended_max: 2000
      sections: 15
    recommendation: "Consider splitting into multiple focused documents"
```

### Metadata Issues
```yaml
metadata_issues:
  - file: "/docs/api/webhooks.md"
    severity: "high"
    category: "missing_frontmatter"
    issue: "No YAML frontmatter present"
    recommendation: "Add standard frontmatter with title, description, tags"
    auto_fix: true
    suggested_frontmatter: |
      ---
      title: "Webhook Configuration"
      description: "Guide to setting up and managing webhooks"
      category: "api"
      tags: ["webhooks", "integration", "events"]
      ---
      
  - file: "/docs/tutorials/getting-started.md"
    severity: "medium"
    category: "incomplete_metadata"
    issue: "Missing required metadata fields"
    details:
      missing_fields: ["category", "audience", "difficulty"]
      present_fields: ["title", "description"]
    recommendation: "Complete metadata schema requirements"
```

### Duplicate Content Detection
```yaml
duplicate_content:
  - similarity_score: 0.87
    files:
      - "/docs/setup/manual-install.md"
      - "/docs/installation/manual-setup.md"
    issue: "Nearly identical content in different locations"
    recommendation: "Consolidate or cross-reference to avoid maintenance burden"
    
  - similarity_score: 0.72
    files:
      - "/docs/api/auth.md"
      - "/docs/security/authentication.md"
    sections:
      - "OAuth Setup" (lines 15-45 vs 23-48)
      - "Token Management" (lines 67-89 vs 78-102)
    recommendation: "Extract common content to shared include file"
```

## Implementation Strategy

### Quality Assessment Criteria
1. **Link Health**: Check internal and external link validity
2. **Readability Analysis**: Flesch-Kincaid scores, sentence complexity
3. **Security Scanning**: Detect exposed credentials, sensitive data
4. **Accessibility**: Alt text, heading structure, semantic markup
5. **Consistency**: Naming conventions, formatting standards

### Freshness Evaluation
1. **Temporal Analysis**: Last modification vs content volatility
2. **Version Alignment**: Documentation vs software version sync
3. **Reference Currency**: External links and technology references
4. **Maintenance Patterns**: Update frequency and regularity

### Structure Assessment
1. **Document Architecture**: Heading hierarchy, section organization
2. **Navigation Elements**: TOC, breadcrumbs, cross-references
3. **Content Length**: Optimal document size for topic complexity
4. **Format Consistency**: Markdown standards, style adherence

### Metadata Validation
1. **Schema Compliance**: Required vs optional field completion
2. **Taxonomy Adherence**: Controlled vocabulary usage
3. **Classification Accuracy**: Category and tag appropriateness
4. **Completeness Scoring**: Metadata richness assessment

## Automated Fix Capabilities

### Safe Automated Fixes
- Heading level correction (H1→H2→H3 progression)
- Basic metadata template insertion
- Link format standardization
- Simple markup corrections

### Suggested Fixes (Manual Review Required)
- Content restructuring recommendations
- Language simplification suggestions
- Duplicate content consolidation
- Security issue remediation

## Use Cases

### Content Maintenance Planning
- Prioritize documentation updates by severity and impact
- Identify high-maintenance content requiring attention
- Plan systematic quality improvement initiatives

### Migration Preparation
- Assess content quality before platform migrations
- Identify cleanup tasks for successful transitions
- Ensure content meets target platform standards

### Compliance and Standards
- Verify adherence to documentation standards
- Ensure security and accessibility compliance
- Maintain consistent quality across large document sets

### Team Accountability
- Track content ownership and maintenance responsibility
- Identify training needs for content creators
- Measure documentation quality improvements over time

## Integration with Other Commands

### Workflow Integration
- **Builds on**: `/content-inventory` for baseline metrics
- **Informs**: `/gap-analysis` with quality insights
- **Feeds**: `/ia-scorecard` with quality scoring
- **Validates**: `/metadata-schema` compliance

### Continuous Improvement
- Scheduled audits for ongoing quality monitoring
- Integration with CI/CD for quality gates
- Automated issue tracking and resolution workflows

## Technical Notes

### Performance Considerations
- Implements caching for expensive quality checks
- Supports incremental auditing for changed files only
- Provides progress tracking for large document sets
- Offers parallel processing for independent checks

### Extensibility
- Plugin architecture for custom quality rules
- Configurable severity thresholds and scoring
- Custom fix suggestions and automation rules
- Integration with external quality tools and services