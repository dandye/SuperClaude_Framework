---
description: Analyze and organize documentation structure using information architecture principles
execute_immediately: true
metadata:
  type: info-arch
  category: analysis
  accepts_args: true
  arg_description: "Directory path to analyze and organize. If no argument provided, analyzes current directory."
---

{{#if args}}
Analyze the documentation structure in: {{args}}
{{else}}
Analyze the documentation structure in the current directory.
{{/if}}

Create a comprehensive organization report that includes:

## 1. Current Structure Analysis
- Identify existing organization patterns
- Detect inconsistencies in naming conventions
- Find orphaned or misplaced documents
- Analyze depth and breadth of directory hierarchy

## 2. Content Classification
- Group documents by type (guides, references, tutorials, examples)
- Identify document purposes and audiences
- Detect content overlaps and gaps
- Classify by update frequency and maintenance needs

## 3. Suggested Reorganization
Based on information architecture best practices, propose:

### Directory Structure
- Logical grouping by function, audience, or topic
- Consistent naming conventions
- Appropriate hierarchy depth (typically 3-4 levels max)
- Clear parent-child relationships

### File Naming Standards
- Descriptive, lowercase names with hyphens
- Consistent suffixes for document types
- Version indicators where appropriate
- Date prefixes for time-sensitive content

### Navigation Improvements
- Index files for each major section
- Cross-reference suggestions
- Breadcrumb path recommendations
- Related document linkages

## 4. Implementation Plan
Provide step-by-step reorganization instructions:
1. Create new directory structure
2. Move files with git mv commands
3. Update internal references
4. Create redirect mappings for moved content
5. Generate new index/navigation files

## 5. Metadata Recommendations
Suggest YAML frontmatter fields for:
- Document categorization
- Relationship mapping
- Maintenance tracking
- Audience targeting

Output the analysis as a markdown report with:
- Executive summary of findings
- Detailed current state assessment
- Proposed future state with rationale
- Migration checklist with specific commands
- Quality metrics for measuring improvement

Focus on creating an organization that:
- Reduces cognitive load for users
- Improves findability and navigation
- Supports both browse and search patterns
- Scales gracefully as content grows
- Facilitates maintenance and updates