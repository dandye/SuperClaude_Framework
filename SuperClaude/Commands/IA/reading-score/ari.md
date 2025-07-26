---
title: "Automated Readability Index (ARI)"
description: "Calculate ARI (Automated Readability Index) and add to document frontmatter"
usage: "/ari [file_path]"
---

# Automated Readability Index (ARI) Calculator

This command calculates the Automated Readability Index for a document and adds it to the document's YAML frontmatter.

## Formula
```
4.71 × (characters / words) + 0.5 × (words / sentences) - 21.43
```

Where characters include letters, numbers, and punctuation.

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

# Count characters (excluding whitespace)
characters=$(echo "$content" | sed 's/[[:space:]]//g' | wc -c)

# Calculate ARI
if [ $words -gt 0 ] && [ $sentences -gt 0 ]; then
    # Calculate character to word ratio
    char_per_word=$(echo "scale=4; $characters / $words" | bc -l)
    
    # Calculate word to sentence ratio
    word_per_sentence=$(echo "scale=4; $words / $sentences" | bc -l)
    
    # Calculate ARI
    ari=$(echo "scale=1; 4.71 * $char_per_word + 0.5 * $word_per_sentence - 21.43" | bc -l)
    
    # Determine reading level
    ari_int=$(echo "$ari" | cut -d. -f1)
    if [ $ari_int -le 1 ]; then
        level="Kindergarten"
    elif [ $ari_int -le 2 ]; then
        level="1st-2nd Grade"
    elif [ $ari_int -le 3 ]; then
        level="3rd Grade"
    elif [ $ari_int -le 4 ]; then
        level="4th Grade"
    elif [ $ari_int -le 5 ]; then
        level="5th Grade"
    elif [ $ari_int -le 6 ]; then
        level="6th Grade"
    elif [ $ari_int -le 7 ]; then
        level="7th Grade"
    elif [ $ari_int -le 8 ]; then
        level="8th Grade"
    elif [ $ari_int -le 9 ]; then
        level="9th Grade"
    elif [ $ari_int -le 10 ]; then
        level="10th Grade"
    elif [ $ari_int -le 11 ]; then
        level="11th Grade"
    elif [ $ari_int -le 12 ]; then
        level="12th Grade"
    elif [ $ari_int -le 13 ]; then
        level="College"
    else
        level="Graduate School"
    fi
    
    # Handle negative scores
    if (( $(echo "$ari < 0" | bc -l) )); then
        level="Very Easy (Pre-Kindergarten)"
    fi
    
    avg_chars_per_word=$(echo "scale=1; $characters / $words" | bc -l)
    avg_words_per_sentence=$(echo "scale=1; $words / $sentences" | bc -l)
    
    echo "Automated Readability Index (ARI): $ari ($level)"
    echo "Statistics: $words words, $sentences sentences, $characters characters"
    echo "Averages: $avg_chars_per_word chars/word, $avg_words_per_sentence words/sentence"
    
    # Add to frontmatter
    if head -1 "$file_path" | grep -q "^---$"; then
        # Has existing frontmatter - update or add ari_index
        if grep -q "^ari_index:" "$file_path"; then
            # Update existing value
            sed -i "s/^ari_index:.*/ari_index: $ari/" "$file_path"
        else
            # Add new field after other readability metrics or title
            if grep -q "^coleman_liau_index:" "$file_path"; then
                sed -i "/^coleman_liau_index:/a ari_index: $ari" "$file_path"
            elif grep -q "^smog_index:" "$file_path"; then
                sed -i "/^smog_index:/a ari_index: $ari" "$file_path"
            elif grep -q "^gunning_fog_index:" "$file_path"; then
                sed -i "/^gunning_fog_index:/a ari_index: $ari" "$file_path"
            elif grep -q "^flesch_kincaid_grade:" "$file_path"; then
                sed -i "/^flesch_kincaid_grade:/a ari_index: $ari" "$file_path"
            elif grep -q "^flesch_reading_ease:" "$file_path"; then
                sed -i "/^flesch_reading_ease:/a ari_index: $ari" "$file_path"
            elif grep -q "^title:" "$file_path"; then
                sed -i "/^title:/a ari_index: $ari" "$file_path"
            else
                sed -i "2a ari_index: $ari" "$file_path"
            fi
        fi
    else
        # No frontmatter - add it
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "ari_index: $ari" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
        mv "$temp_file" "$file_path"
    fi
    
    echo "Updated $file_path with ARI Index"
else
    echo "Error: No words or sentences found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/ari ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/ari
```

## Output
- Displays the calculated ARI and reading level
- Adds or updates `ari_index` field in document frontmatter
- Shows document statistics and averages

## Reading Level Interpretation
- **<0**: Very Easy (Pre-Kindergarten)
- **1**: Kindergarten
- **2**: 1st-2nd Grade
- **3**: 3rd Grade
- **4**: 4th Grade
- **5**: 5th Grade
- **6**: 6th Grade
- **7**: 7th Grade
- **8**: 8th Grade
- **9**: 9th Grade
- **10**: 10th Grade
- **11**: 11th Grade
- **12**: 12th Grade
- **13**: College
- **14+**: Graduate School

## About ARI
- **Character-based**: Uses character counts instead of syllables for more precise automated analysis
- **Early development**: One of the first readability formulas designed for computer calculation (1967)
- **Military origins**: Developed for the U.S. Air Force to assess technical manual readability
- **Precise measurement**: No ambiguity in character counting vs. subjective syllable counting