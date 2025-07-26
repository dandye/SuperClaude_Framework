---
title: "Gunning Fog Index"
description: "Calculate Gunning Fog Index and add to document frontmatter"
usage: "/gunning-fog [file_path]"
---

# Gunning Fog Index Calculator

This command calculates the Gunning Fog Index for a document and adds it to the document's YAML frontmatter.

## Formula
```
0.4 × ((total words / total sentences) + 100 × (complex words / total words))
```

Complex words are defined as words with 3+ syllables, excluding:
- Proper nouns
- Words ending in -es, -ed, -ing that become 2 syllables when suffix removed

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

# Count complex words (simplified approximation)
# Words with 3+ syllables (using vowel groups as proxy)
complex_words=0
if [ $words -gt 0 ]; then
    # Extract individual words and count syllables for each
    word_list=$(echo "$content" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z ]/ /g' | tr -s ' ' | tr ' ' '\n' | grep -v '^$')
    
    while IFS= read -r word; do
        if [ -n "$word" ]; then
            # Count vowel groups in word
            syllable_count=$(echo "$word" | grep -o '[aeiou]\+' | wc -l)
            
            # Simple exclusion for common suffixes
            if echo "$word" | grep -E '(ed|es|ing)$' > /dev/null; then
                # Reduce count by 1 for these suffixes if it makes the word 2 syllables
                if [ $syllable_count -eq 3 ]; then
                    syllable_count=2
                fi
            fi
            
            # Count as complex if 3+ syllables
            if [ $syllable_count -ge 3 ]; then
                complex_words=$((complex_words + 1))
            fi
        fi
    done <<< "$word_list"
fi

# Calculate Gunning Fog Index
if [ $words -gt 0 ]; then
    avg_sentence_length=$(echo "scale=2; $words / $sentences" | bc -l)
    complex_word_percentage=$(echo "scale=4; 100 * $complex_words / $words" | bc -l)
    
    fog_index=$(echo "scale=1; 0.4 * ($avg_sentence_length + $complex_word_percentage)" | bc -l)
    
    # Determine reading level
    fog_int=$(echo "$fog_index" | cut -d. -f1)
    if [ $fog_int -le 6 ]; then
        level="Elementary School"
    elif [ $fog_int -le 8 ]; then
        level="Middle School"
    elif [ $fog_int -le 12 ]; then
        level="High School"
    elif [ $fog_int -le 16 ]; then
        level="College"
    else
        level="Graduate School"
    fi
    
    echo "Gunning Fog Index: $fog_index ($level)"
    echo "Statistics: $words words, $sentences sentences, $complex_words complex words (${complex_word_percentage}%)"
    
    # Add to frontmatter
    if head -1 "$file_path" | grep -q "^---$"; then
        # Has existing frontmatter - update or add gunning_fog_index
        if grep -q "^gunning_fog_index:" "$file_path"; then
            # Update existing value
            sed -i "s/^gunning_fog_index:.*/gunning_fog_index: $fog_index/" "$file_path"
        else
            # Add new field after other readability metrics or title
            if grep -q "^flesch_kincaid_grade:" "$file_path"; then
                sed -i "/^flesch_kincaid_grade:/a gunning_fog_index: $fog_index" "$file_path"
            elif grep -q "^flesch_reading_ease:" "$file_path"; then
                sed -i "/^flesch_reading_ease:/a gunning_fog_index: $fog_index" "$file_path"
            elif grep -q "^title:" "$file_path"; then
                sed -i "/^title:/a gunning_fog_index: $fog_index" "$file_path"
            else
                sed -i "2a gunning_fog_index: $fog_index" "$file_path"
            fi
        fi
    else
        # No frontmatter - add it
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "gunning_fog_index: $fog_index" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
        mv "$temp_file" "$file_path"
    fi
    
    echo "Updated $file_path with Gunning Fog Index"
else
    echo "Error: No words found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/gunning-fog ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/gunning-fog
```

## Output
- Displays the calculated Fog Index and reading level
- Adds or updates `gunning_fog_index` field in document frontmatter
- Shows document statistics including complex word percentage

## Reading Level Interpretation
- **6 or below**: Elementary School
- **7-8**: Middle School
- **9-12**: High School
- **13-16**: College
- **17+**: Graduate School

## What Makes Words "Complex"
- 3+ syllables (e.g., "computer", "understand", "beautiful")
- Excludes common suffixes that don't add meaning complexity
- Simpler than syllable-only counts since it focuses on true complexity