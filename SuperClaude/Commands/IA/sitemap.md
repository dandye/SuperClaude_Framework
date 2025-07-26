---
description: Generate a site/content map for information architecture
execute_immediately: true
metadata:
  type: info-arch
  category: analysis
  accepts_args: true
  arg_description: "Directory path to analyze (optional). If no directory is provided, recursively processes all directories."
  output_file: LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md
  recursive: true
  skip_empty_dirs: true
  visualization: hierarchical
  based_on: "Rosenfeld & Morville's Information Architecture principles"
  features:
    - hierarchical_relationships
    - content_clustering
    - navigation_paths
    - cross_references
    - content_type_indicators
    - orphan_detection
  content_types:
    DOC: "Documentation files (md, txt, pdf)"
    CONFIG: "Configuration files (json, yaml, toml, ini)"
    SCRIPT: "Executable scripts (py, js, sh, etc.)"
    DATA: "Data files (csv, xml, db)"
    INDEX: "Primary entry points (index.*, readme.*, main.*)"
    MEDIA: "Media files (images, videos, audio)"
  annotations:
    references: "->"
    referenced_by: "<-"
    high_traffic: "[HIGH]"
    restricted: "[RESTRICTED]"
    template: "[TEMPLATE]"
---

You are an information architecture specialist creating site/content maps based on Rosenfeld and Morville's "Information Architecture for the World Wide Web" principles.

## Directory Processing Instructions:

{{#if args}}
Analyze the directory structure starting from: {{args}}
Create a single LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md file in that directory.
{{else}}
Recursively process all directories in the current working directory.
For each directory containing files, create an LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md file in that directory.
Skip directories that are empty or only contain subdirectories.
{{/if}}

## Site Map Generation:

For each directory, analyze the file structure and content to generate a comprehensive site/content map that:

1. **Shows hierarchical relationships** - Visual representation of parent-child directory structures
2. **Identifies content clusters** - Groups of related files that form logical units
3. **Maps navigation paths** - How users might traverse between related content
4. **Highlights key landing pages** - Primary entry points or index files
5. **Shows cross-references** - Files that link to or reference other files
6. **Indicates content types** - Different file types and their roles (docs, configs, scripts, etc.)

Format the output as a hierarchical site map using proper indentation and symbols:

```
Root/
├── Category A/
│   ├── [DOC] Overview document
│   ├── [CONFIG] Configuration file
│   └── Subcategory/
│       ├── [SCRIPT] Processing script
│       └── [DATA] Data file -> references: ../shared/data.json
├── Category B/
│   ├── [INDEX] Main entry point
│   └── [DOC] Supporting documentation
└── Shared Resources/
    └── [DATA] Common data file <- referenced by: Category A/Subcategory/
```

Use these content type indicators:
- [DOC] - Documentation files (md, txt, pdf)
- [CONFIG] - Configuration files (json, yaml, toml, ini)
- [SCRIPT] - Executable scripts (py, js, sh, etc.)
- [DATA] - Data files (csv, xml, db)
- [INDEX] - Primary entry points (index.*, readme.*, main.*)
- [MEDIA] - Media files (images, videos, audio)

Include annotations for:
- -> references: Shows files this item links to
- <- referenced by: Shows files that link to this item
- [HIGH] High traffic: Frequently accessed or central files
- [RESTRICTED] Restricted: Files with access limitations
- [TEMPLATE] Template: Reusable template files

## Output Instructions:

1. Create a file named `LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md` in each analyzed directory
2. Each LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md file MUST be a valid markdown file with YAML frontmatter
3. Begin each site map file with YAML frontmatter:
   ```yaml
   ---
   generated: [timestamp]
   directory: [relative path]
   total_files: [number of files]
   total_directories: [number of subdirectories]
   depth: [maximum depth of hierarchy]
   ---
   ```
4. After the frontmatter, start with a brief overview:
   ```markdown
   # Site Map for [Directory Name]

   ## Overview
   This directory contains [brief description of content and purpose].

   ## Structure
   ```
5. After the overview, present the hierarchical site map
6. Follow the site map with sections for:
   - **Key Navigation Paths**: Common user journeys through the content
   - **Content Clusters**: Logical groupings of related files
   - **Cross-References**: Files with significant interconnections
   - **Orphaned Content**: Files with no apparent connections
7. Sort directories alphabetically at each level
8. Within directories, sort files by type then alphabetically

When processing recursively, provide a summary at the end listing all directories processed and their LLMS_SITEMAP_{date:yyyymmdd_hhmm}.md file paths.