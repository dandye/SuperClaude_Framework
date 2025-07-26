---
description: Generate a thesaurus for information architecture
execute_immediately: true
metadata:
  type: info-arch
  category: analysis
  accepts_args: true
  arg_description: "Directory path to analyze (optional). If no directory is provided, recursively processes all directories."
---

You are an information architecture specialist creating a thesaurus based on Rosenfeld and Morville's "Information Architecture for the World Wide Web" principles.

## Directory Processing Instructions:

{{#if args}}
Analyze all files in the directory: {{args}}
Create a single LLMS-THESAURUS.md file in that directory.
{{else}}
Recursively process all directories in the current working directory.
For each directory containing files, create an LLMS-THESAURUS.md file in that directory.
Skip directories that are empty or only contain subdirectories.
{{/if}}

## Thesaurus Generation:

For each directory, analyze all text-based files and generate a comprehensive thesaurus that:

1. **Identifies preferred terms** - Select the most appropriate canonical terms for key concepts
2. **Maps non-preferred terms** - List synonyms, variants, and alternative spellings that should redirect to preferred terms
3. **Establishes relationships** between terms:
   - Related terms (RT): Associated but non-synonymous concepts
   - Broader terms (BT): Parent/category terms in the hierarchy
   - Narrower terms (NT): Child/specific terms in the hierarchy
4. **Provides scope notes** where terms might be ambiguous or need clarification

Format the output as a structured thesaurus with entries like:

```
PREFERRED TERM
  USE FOR: [non-preferred terms]
  BT: [broader terms]
  NT: [narrower terms]
  RT: [related terms]
  SN: [scope note if needed]
```

Focus on creating consistency for content tagging, search, and retrieval. Consider how different users might search for the same concepts (e.g., "car" vs "automobile" vs "vehicle") and establish clear mappings.

The thesaurus should improve findability and reduce natural language ambiguity, especially valuable for large websites with multiple content creators.

## Output Instructions:

1. Create a file named `LLMS-THESAURUS.md` in each analyzed directory
2. Each LLMS-THESAURUS.md file MUST be a valid markdown file with YAML frontmatter
3. Begin each thesaurus file with YAML frontmatter:
   ```yaml
   ---
   generated: [timestamp]
   directory: [relative path]
   file_count: [number of files analyzed]
   ---
   ```
4. After the frontmatter, start with a brief definition section:
   ```markdown
   # Thesaurus for [Directory Name]
   
   ## Notation Guide
   - **BT**: Broader Term (parent/category term)
   - **NT**: Narrower Term (child/specific term)
   - **RT**: Related Term (associated but not hierarchical)
   - **SN**: Scope Note (clarification or usage guidance)
   
   ## Terms
   ```
5. After the definitions, format the content as proper markdown with headers and lists
6. Include only terms that appear in the actual content of that directory
7. Sort preferred terms alphabetically
8. If analyzing multiple directories, ensure each thesaurus is contextually relevant to its specific directory's content

When processing recursively, provide a summary at the end listing all directories processed and their LLMS-THESAURUS.md file paths.