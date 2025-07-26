---
title: "SMOG Index"
description: "Calculate SMOG (Simple Measure of Gobbledygook) Index and add to document frontmatter"
usage: "/smog [file_path]"
---

# SMOG Index Calculator

This command calculates the SMOG (Simple Measure of Gobbledygook) Index for a document and adds it to the document's YAML frontmatter.

## Formula
```
1.0430 × √(polysyllable count × (30 / sentence count)) + 3.1291
```

Where polysyllables are words with 3+ syllables.

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

# Count polysyllabic words (3+ syllables)
polysyllable_count=0
if [ $words -gt 0 ]; then
    # Extract individual words and count syllables for each
    word_list=$(echo "$content" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z ]/ /g' | tr -s ' ' | tr ' ' '\n' | grep -v '^$')
    
    while IFS= read -r word; do
        if [ -n "$word" ]; then
            # Count vowel groups in word (rough syllable approximation)
            syllable_count=$(echo "$word" | grep -o '[aeiou]\+' | wc -l)
            
            # Count as polysyllabic if 3+ syllables
            if [ $syllable_count -ge 3 ]; then
                polysyllable_count=$((polysyllable_count + 1))
            fi
        fi
    done <<< "$word_list"
fi

# Calculate SMOG Index
if [ $words -gt 0 ] && [ $sentences -gt 0 ]; then
    # Calculate polysyllable density adjusted for 30 sentences
    poly_density=$(echo "scale=6; $polysyllable_count * (30.0 / $sentences)" | bc -l)
    
    # Calculate square root of polysyllable density
    if (( $(echo "$poly_density >= 0" | bc -l) )); then
        sqrt_poly=$(echo "scale=6; sqrt($poly_density)" | bc -l)
        smog_index=$(echo "scale=1; 1.0430 * $sqrt_poly + 3.1291" | bc -l)
        
        # Determine reading level
        smog_int=$(echo "$smog_index" | cut -d. -f1)
        if [ $smog_int -le 6 ]; then
            level="Elementary School"
        elif [ $smog_int -le 8 ]; then
            level="Middle School"
        elif [ $smog_int -le 12 ]; then
            level="High School"
        elif [ $smog_int -le 16 ]; then
            level="College"
        else
            level="Graduate School"
        fi
        
        poly_percentage=$(echo "scale=1; 100 * $polysyllable_count / $words" | bc -l)
        
        echo "SMOG Index: $smog_index ($level)"
        echo "Statistics: $words words, $sentences sentences, $polysyllable_count polysyllabic words (${poly_percentage}%)"
        
        # Add to frontmatter
        if head -1 "$file_path" | grep -q "^---$"; then
            # Has existing frontmatter - update or add smog_index
            if grep -q "^smog_index:" "$file_path"; then
                # Update existing value
                sed -i "s/^smog_index:.*/smog_index: $smog_index/" "$file_path"
            else
                # Add new field after other readability metrics or title
                if grep -q "^gunning_fog_index:" "$file_path"; then
                    sed -i "/^gunning_fog_index:/a smog_index: $smog_index" "$file_path"
                elif grep -q "^flesch_kincaid_grade:" "$file_path"; then
                    sed -i "/^flesch_kincaid_grade:/a smog_index: $smog_index" "$file_path"
                elif grep -q "^flesch_reading_ease:" "$file_path"; then
                    sed -i "/^flesch_reading_ease:/a smog_index: $smog_index" "$file_path"
                elif grep -q "^title:" "$file_path"; then
                    sed -i "/^title:/a smog_index: $smog_index" "$file_path"
                else
                    sed -i "2a smog_index: $smog_index" "$file_path"
                fi
            fi
        else
            # No frontmatter - add it
            temp_file=$(mktemp)
            echo "---" > "$temp_file"
            echo "smog_index: $smog_index" >> "$temp_file"
            echo "---" >> "$temp_file"
            echo "" >> "$temp_file"
            cat "$file_path" >> "$temp_file"
            mv "$temp_file" "$file_path"
        fi
        
        echo "Updated $file_path with SMOG Index"
    else
        echo "Error: Invalid polysyllable density calculation"
        exit 1
    fi
else
    echo "Error: No words or sentences found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/smog ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/smog
```

## Output
- Displays the calculated SMOG Index and reading level
- Adds or updates `smog_index` field in document frontmatter  
- Shows document statistics including polysyllabic word percentage

## Reading Level Interpretation
- **6 or below**: Elementary School
- **7-8**: Middle School
- **9-12**: High School
- **13-16**: College
- **17+**: Graduate School

## About SMOG
- **Focused on complexity**: Only counts polysyllabic words (3+ syllables)
- **Widely used**: Popular in healthcare and government for plain language
- **Conservative**: Tends to give higher (more difficult) scores than Flesch-Kincaid
- **Sample size**: Originally designed for 30+ sentences, but adapted for shorter texts