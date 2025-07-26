---
title: "Flesch Reading Ease Score"
description: "Calculate Flesch Reading Ease score and add to document frontmatter"
usage: "/flesch-reading-ease [file_path]"
---

# Flesch Reading Ease Score Calculator

This command calculates the Flesch Reading Ease score for a document and adds it to the document's YAML frontmatter.

## Formula
```
206.835 - 1.015 × (total words/total sentences) - 84.6 × (total syllables/total words)
```

## Implementation

```bash
#!/bin/bash

# Get the file path from argument or prompt
if [ $# -eq 0 ]; then
    read -p "Enter file path: " file_path
else
    file_path="$1"
fi

# Check if file exists
if [ ! -f "$file_path" ]; then
    echo "Error: File '$file_path' not found"
    exit 1
fi

# Extract content (skip YAML frontmatter if present)
content=$(sed '1{/^---$/!q;};1,/^---$/d' "$file_path")

# Count sentences (approximate - count periods, exclamation marks, question marks)
sentences=$(echo "$content" | grep -o '[.!?]' | wc -l)
if [ $sentences -eq 0 ]; then sentences=1; fi

# Count words
words=$(echo "$content" | wc -w)

# Count syllables (rough approximation using vowel groups)
syllables=$(echo "$content" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z]/ /g' | \
    grep -o '[aeiou]\+' | wc -l)

# Calculate Flesch Reading Ease
if [ $words -gt 0 ]; then
    avg_sentence_length=$(echo "scale=2; $words / $sentences" | bc -l)
    avg_syllables_per_word=$(echo "scale=2; $syllables / $words" | bc -l)
    
    flesch_score=$(echo "scale=1; 206.835 - 1.015 * $avg_sentence_length - 84.6 * $avg_syllables_per_word" | bc -l)
    
    # Determine reading level
    if (( $(echo "$flesch_score >= 90" | bc -l) )); then
        level="Very Easy (5th grade)"
    elif (( $(echo "$flesch_score >= 80" | bc -l) )); then
        level="Easy (6th grade)"
    elif (( $(echo "$flesch_score >= 70" | bc -l) )); then
        level="Fairly Easy (7th grade)"
    elif (( $(echo "$flesch_score >= 60" | bc -l) )); then
        level="Standard (8th-9th grade)"
    elif (( $(echo "$flesch_score >= 50" | bc -l) )); then
        level="Fairly Difficult (10th-12th grade)"
    elif (( $(echo "$flesch_score >= 30" | bc -l) )); then
        level="Difficult (College)"
    elif (( $(echo "$flesch_score >= 0" | bc -l) )); then
        level="Very Difficult (Graduate)"
    else
        level="Extremely Difficult (Professional)"
    fi
    
    echo "Flesch Reading Ease Score: $flesch_score ($level)"
    echo "Statistics: $words words, $sentences sentences, $syllables syllables"
    
    # Add to frontmatter
    if head -1 "$file_path" | grep -q "^---$"; then
        # Has existing frontmatter - update or add flesch_reading_ease
        if grep -q "^flesch_reading_ease:" "$file_path"; then
            # Update existing value
            sed -i "s/^flesch_reading_ease:.*/flesch_reading_ease: $flesch_score/" "$file_path"
        else
            # Add new field after title if it exists, otherwise after first line
            if grep -q "^title:" "$file_path"; then
                sed -i "/^title:/a flesch_reading_ease: $flesch_score" "$file_path"
            else
                sed -i "2a flesch_reading_ease: $flesch_score" "$file_path"
            fi
        fi
    else
        # No frontmatter - add it
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "flesch_reading_ease: $flesch_score" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
        mv "$temp_file" "$file_path"
    fi
    
    echo "Updated $file_path with Flesch Reading Ease score"
else
    echo "Error: No words found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/flesch-reading-ease ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/flesch-reading-ease
```

## Output
- Displays the calculated score and reading level
- Adds or updates `flesch_reading_ease` field in document frontmatter
- Shows document statistics (words, sentences, syllables)