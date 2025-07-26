---
title: Content Gap Analysis
description: Identifies missing documentation, coverage gaps, and content opportunities through systematic analysis of expected vs actual content
category: information-architecture
tags: [gap-analysis, coverage, missing-content, planning]
version: 1.0
---

# /gap-analysis

## Purpose
Systematically identify missing content and coverage gaps by comparing existing documentation against expected topics, user needs, feature coverage, and industry standards. Provides prioritized recommendations for new content creation and coverage improvement.

## Usage
```
/gap-analysis [directory] [--template=api|product|tutorial] [--against=features|competitors|standards] [--depth=shallow|deep]
```

## Parameters
- `directory` (optional): Target directory to analyze (defaults to current directory)
- `--template`: Apply analysis template for specific content types
- `--against`: Compare against external references (feature lists, competitor docs, standards)
- `--depth`: Analysis thoroughness level

## Output Structure

### Gap Analysis Summary
```yaml
gap_analysis:
  generated: 2024-01-15T10:30:00Z
  scope: "/docs/"
  analysis_type: "comprehensive"
  
  coverage_score: 6.8/10
  
  gap_summary:
    critical_gaps: 5
    major_gaps: 12
    minor_gaps: 18
    over_documented: 3
    
  recommendations:
    new_documents: 15
    expand_existing: 8
    consolidate: 3
    remove_obsolete: 2
```

### Critical Content Gaps
```yaml
critical_gaps:
  - category: "getting_started"
    gap_type: "missing_fundamental"
    priority: "critical"
    title: "Quick Start Guide"
    description: "No entry-level documentation for new users"
    evidence:
      - "Support tickets frequently ask basic setup questions"
      - "User onboarding time exceeds 2 hours"
      - "Competitor docs include prominent quick start"
    recommended_content:
      - title: "5-Minute Quick Start"
        format: "tutorial"
        estimated_effort: "2-3 days"
        audience: "new_users"
        
  - category: "api_reference"
    gap_type: "incomplete_coverage"
    priority: "critical"
    title: "Webhook API Documentation"
    description: "Webhooks mentioned but not documented"
    evidence:
      - "API has 15 webhook endpoints with no documentation"
      - "Developer forum shows confusion about webhook implementation"
      - "Feature exists in code but missing from docs"
    recommended_content:
      - title: "Webhook API Reference"
        format: "api_docs"
        estimated_effort: "1 week"
        dependencies: ["API schema review"]
```

### Coverage Gaps by Category
```yaml
category_analysis:
  getting_started:
    coverage: 40%
    expected_docs: 5
    existing_docs: 2
    gaps:
      - "Installation guide for Windows"
      - "Quick start tutorial"
      - "Common troubleshooting"
    priority: "high"
    
  api_reference:
    coverage: 75%
    expected_docs: 20
    existing_docs: 15
    gaps:
      - "Webhook endpoints"
      - "Rate limiting details"
      - "Error code reference"
      - "SDK examples"
      - "Postman collection"
    priority: "medium"
    
  tutorials:
    coverage: 60%
    expected_docs: 10
    existing_docs: 6
    gaps:
      - "Advanced configuration"
      - "Integration patterns"
      - "Performance optimization"
      - "Security best practices"
    priority: "medium"
```

### Feature Coverage Analysis
```yaml
feature_coverage:
  total_features: 45
  documented_features: 32
  undocumented_features: 13
  
  undocumented:
    - feature: "Advanced Search Filters"
      version_introduced: "v2.1.0"
      usage_analytics: "high"
      priority: "critical"
      estimated_effort: "3 days"
      
    - feature: "Bulk Operations API"
      version_introduced: "v2.3.0" 
      usage_analytics: "medium"
      priority: "high"
      estimated_effort: "1 week"
      
    - feature: "Custom Themes"
      version_introduced: "v1.8.0"
      usage_analytics: "low"
      priority: "low"
      estimated_effort: "2 days"
```

### User Journey Gaps
```yaml
user_journey_analysis:
  personas:
    - name: "New Developer"
      journey_gaps:
        - stage: "discovery"
          gap: "No clear value proposition document"
          impact: "high"
          
        - stage: "first_integration"
          gap: "Missing step-by-step tutorial"
          impact: "critical"
          
        - stage: "troubleshooting"
          gap: "No centralized error reference"
          impact: "medium"
          
    - name: "System Administrator"
      journey_gaps:
        - stage: "deployment"
          gap: "Production deployment guide missing"
          impact: "critical"
          
        - stage: "monitoring"
          gap: "Observability setup not documented"
          impact: "high"
```

### Competitive Analysis
```yaml
competitive_gaps:
  benchmark_against: ["competitor_a", "competitor_b", "industry_standard"]
  
  content_gaps:
    - topic: "Interactive API Explorer"
      competitors_have: ["competitor_a", "competitor_b"]
      our_status: "missing"
      user_value: "high"
      implementation_effort: "medium"
      
    - topic: "Video Tutorials"
      competitors_have: ["competitor_b"]
      our_status: "limited"
      current_count: 2
      recommended_count: 8
      
  content_advantages:
    - topic: "Detailed Architecture Guides"
      our_strength: "comprehensive"
      competitor_weakness: "surface_level"
      maintain_advantage: true
```

## Implementation Strategy

### Gap Detection Methods
1. **Content Inventory Analysis**: Compare existing vs expected content taxonomies
2. **Feature Mapping**: Match product features to documentation coverage
3. **User Flow Analysis**: Identify missing steps in user journeys
4. **Support Ticket Mining**: Extract frequently asked but undocumented questions
5. **Competitive Benchmarking**: Compare against industry leaders and competitors

### Gap Prioritization Framework
1. **Impact Assessment**: User pain points, support ticket volume, feature importance
2. **Effort Estimation**: Content creation complexity and resource requirements
3. **Strategic Value**: Business goals alignment, competitive advantage
4. **Dependencies**: Technical requirements, prerequisite content
5. **ROI Calculation**: Value delivered vs effort invested

### Evidence Collection
1. **Quantitative Data**: Analytics, support metrics, feature usage stats
2. **Qualitative Insights**: User feedback, support conversations, surveys
3. **Technical Analysis**: Code coverage, API completeness, feature audits
4. **Market Research**: Competitive analysis, industry standards, best practices

### Recommendation Generation
1. **Content Specifications**: Detailed briefs for new content creation
2. **Enhancement Plans**: Improvements for existing inadequate content
3. **Consolidation Opportunities**: Merge or restructure overlapping content
4. **Sunset Recommendations**: Remove outdated or redundant documentation

## Use Cases

### Product Documentation Planning
- Ensure complete coverage of product features and capabilities
- Align documentation with product roadmap and releases
- Identify user experience gaps in documentation flow

### Content Strategy Development
- Inform content creation priorities and resource allocation
- Guide information architecture improvements
- Support editorial calendar and content planning

### Onboarding Optimization
- Identify barriers in user adoption and onboarding flows
- Ensure smooth progression from discovery to proficiency
- Reduce time-to-value for new users

### Competitive Positioning
- Ensure documentation quality matches or exceeds competitors
- Identify documentation as competitive advantage opportunities
- Address gaps that may disadvantage market position

## Integration with Other Commands

### Data Dependencies
- **Requires**: `/content-inventory` for baseline content catalog
- **Enhanced by**: `/cross-reference` for relationship understanding
- **Informed by**: `/content-audit` for quality assessment
- **Validates**: `/sitemap` for structural completeness

### Workflow Integration
- **Feeds**: `/taxonomy` with identified content categories
- **Informs**: `/navigation-blueprint` with user journey insights
- **Provides metrics**: `/ia-scorecard` with coverage scores

## Technical Notes

### Analysis Methods
1. **Template-Based Analysis**: Predefined content frameworks for different domains
2. **Machine Learning**: Pattern recognition for gap identification
3. **Semantic Analysis**: Content similarity and topic modeling
4. **Graph Analysis**: Relationship-based gap detection

### Data Sources
- Product feature databases and release notes
- User analytics and behavior data
- Support ticket systems and FAQ databases
- Competitive intelligence and market research
- Industry standards and best practice guides

### Output Formats
- **Executive Summary**: High-level gaps and recommendations
- **Detailed Report**: Comprehensive analysis with evidence
- **Action Plan**: Prioritized tasks with effort estimates
- **Content Briefs**: Specifications for new content creation

### Automation Capabilities
- Scheduled gap analysis for continuous monitoring
- Integration with product management tools
- Automated competitive monitoring and comparison
- Content performance tracking and gap emergence detection