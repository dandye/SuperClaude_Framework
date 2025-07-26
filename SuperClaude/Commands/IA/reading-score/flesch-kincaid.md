---
title: "Flesch-Kincaid Grade Level"
description: "Calculate Flesch-Kincaid Grade Level and add to document frontmatter"
usage: "/flesch-kincaid [file_path]"
---

# Flesch-Kincaid Grade Level Calculator

This command calculates the Flesch-Kincaid Grade Level for a document and adds it to the document's YAML frontmatter.

## Formula
```
0.39 × (total words / total sentences) + 11.8 × (total syllables / total words) - 15.59
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

# Calculate Flesch-Kincaid Grade Level
if [ $words -gt 0 ]; then
    avg_sentence_length=$(echo "scale=2; $words / $sentences" | bc -l)
    avg_syllables_per_word=$(echo "scale=2; $syllables / $words" | bc -l)
    
    grade_level=$(echo "scale=1; 0.39 * $avg_sentence_length + 11.8 * $avg_syllables_per_word - 15.59" | bc -l)
    
    # Determine education level
    grade_int=$(echo "$grade_level" | cut -d. -f1)
    if [ $grade_int -le 5 ]; then
        education_level="Elementary School"
    elif [ $grade_int -le 8 ]; then
        education_level="Middle School"
    elif [ $grade_int -le 12 ]; then
        education_level="High School"
    elif [ $grade_int -le 16 ]; then
        education_level="College"
    else
        education_level="Graduate School"
    fi
    
    echo "Flesch-Kincaid Grade Level: $grade_level ($education_level)"
    echo "Statistics: $words words, $sentences sentences, $syllables syllables"
    
    # Add to frontmatter
    if head -1 "$file_path" | grep -q "^---$"; then
        # Has existing frontmatter - update or add flesch_kincaid_grade
        if grep -q "^flesch_kincaid_grade:" "$file_path"; then
            # Update existing value
            sed -i "s/^flesch_kincaid_grade:.*/flesch_kincaid_grade: $grade_level/" "$file_path"
        else
            # Add new field after flesch_reading_ease if it exists, otherwise after title
            if grep -q "^flesch_reading_ease:" "$file_path"; then
                sed -i "/^flesch_reading_ease:/a flesch_kincaid_grade: $grade_level" "$file_path"
            elif grep -q "^title:" "$file_path"; then
                sed -i "/^title:/a flesch_kincaid_grade: $grade_level" "$file_path"
            else
                sed -i "2a flesch_kincaid_grade: $grade_level" "$file_path"
            fi
        fi
    else
        # No frontmatter - add it
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "flesch_kincaid_grade: $grade_level" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
        mv "$temp_file" "$file_path"
    fi
    
    echo "Updated $file_path with Flesch-Kincaid Grade Level"
else
    echo "Error: No words found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/flesch-kincaid ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/flesch-kincaid
```

## Output
- Displays the calculated grade level and education level
- Adds or updates `flesch_kincaid_grade` field in document frontmatter
- Shows document statistics (words, sentences, syllables)

## Grade Level Interpretation
- **1-5**: Elementary School level
- **6-8**: Middle School level  
- **9-12**: High School level
- **13-16**: College level
- **17+**: Graduate School level