---
title: Shared Output Helpers
description: Common functions and templates for standardized command outputs
category: infrastructure
version: 1.0
---

# Output Helpers for SuperClaude Commands

## Standardized Filename Generation

All commands should use timestamped filenames following this convention:
`{PREFIX}_{IDENTIFIER}_{TIMESTAMP}.md`

### Template Function

```python
# Include this at the top of command templates:
import datetime

def get_output_filename(prefix, identifier=None):
    """Generate timestamped filename following SuperClaude conventions"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    if identifier:
        return f"{prefix}_{identifier}_{timestamp}.md"
    return f"{prefix}_{timestamp}.md"

# Usage examples:
# get_output_filename("LLMS-SITEMAP", "IA_directory") 
# → LLMS-SITEMAP_IA_directory_20250726_1337.md

# get_output_filename("CONTENT_AUDIT")
# → CONTENT_AUDIT_20250726_1337.md
```

### Handlebars Template Helper

For commands using Handlebars templates, include this helper:

```handlebars
{{!-- Generate timestamped filename --}}
{{#timestamped_filename prefix identifier}}
{{/timestamped_filename}}
```

### Simple Text Replacement

For quick adoption without code changes, commands can use this pattern:

```markdown
Output file: {{PREFIX}}_{{TIMESTAMP}}.md

Where:
- {{PREFIX}} = Command-specific prefix (e.g., LLMS-SITEMAP, CONTENT_AUDIT)
- {{TIMESTAMP}} = Current timestamp in format YYYYMMDD_HHMM
```

## Standard Prefixes by Command Type

| Command | Prefix | Example Output |
|---------|--------|----------------|
| sitemap | LLMS-SITEMAP | LLMS-SITEMAP_20250726_1337.md |
| thesaurus | LLMS-THESAURUS | LLMS-THESAURUS_20250726_1337.md |
| content-audit | CONTENT_AUDIT | CONTENT_AUDIT_20250726_1337.md |
| content-inventory | CONTENT_INVENTORY | CONTENT_INVENTORY_20250726_1337.md |
| taxonomy | TAXONOMY | TAXONOMY_20250726_1337.md |
| gap-analysis | GAP_ANALYSIS | GAP_ANALYSIS_20250726_1337.md |
| document-clustering | DOCUMENT_CLUSTERING | DOCUMENT_CLUSTERING_20250726_1337.md |

## YAML Frontmatter Template

All generated files should include standardized frontmatter:

```yaml
---
generated: {{TIMESTAMP_ISO}}
command: {{COMMAND_NAME}}
directory: {{TARGET_DIRECTORY}}
total_files: {{FILE_COUNT}}
total_directories: {{DIR_COUNT}}
version: "1.0"
---
```