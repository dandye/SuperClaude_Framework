---
title: "Coleman-Liau Index"
description: "Calculate Coleman-Liau Index and add to document frontmatter"
usage: "/coleman-liau [file_path]"
---

# Coleman-Liau Index Calculator

This command calculates the Coleman-Liau Index for a document and adds it to the document's YAML frontmatter.

## Formula
```
0.0588 × L - 0.296 × S - 15.8
```

Where:
- L = average number of letters per 100 words
- S = average number of sentences per 100 words

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

# Count letters (alphabetic characters only)
letters=$(echo "$content" | sed 's/[^a-zA-Z]//g' | wc -c)

# Calculate Coleman-Liau Index
if [ $words -gt 0 ]; then
    # Calculate L (letters per 100 words)
    L=$(echo "scale=4; 100 * $letters / $words" | bc -l)
    
    # Calculate S (sentences per 100 words)  
    S=$(echo "scale=4; 100 * $sentences / $words" | bc -l)
    
    # Calculate Coleman-Liau Index
    coleman_liau=$(echo "scale=1; 0.0588 * $L - 0.296 * $S - 15.8" | bc -l)
    
    # Determine reading level
    cli_int=$(echo "$coleman_liau" | cut -d. -f1)
    if [ $cli_int -le 5 ]; then
        level="Elementary School"
    elif [ $cli_int -le 8 ]; then
        level="Middle School"
    elif [ $cli_int -le 12 ]; then
        level="High School"
    elif [ $cli_int -le 16 ]; then
        level="College"
    else
        level="Graduate School"
    fi
    
    # Handle negative scores
    if (( $(echo "$coleman_liau < 0" | bc -l) )); then
        level="Very Easy (Below Elementary)"
    fi
    
    avg_letters_per_word=$(echo "scale=1; $letters / $words" | bc -l)
    avg_words_per_sentence=$(echo "scale=1; $words / $sentences" | bc -l)
    
    echo "Coleman-Liau Index: $coleman_liau ($level)"
    echo "Statistics: $words words, $sentences sentences, $letters letters"
    echo "Averages: $avg_letters_per_word letters/word, $avg_words_per_sentence words/sentence"
    
    # Add to frontmatter
    if head -1 "$file_path" | grep -q "^---$"; then
        # Has existing frontmatter - update or add coleman_liau_index
        if grep -q "^coleman_liau_index:" "$file_path"; then
            # Update existing value
            sed -i "s/^coleman_liau_index:.*/coleman_liau_index: $coleman_liau/" "$file_path"
        else
            # Add new field after other readability metrics or title
            if grep -q "^smog_index:" "$file_path"; then
                sed -i "/^smog_index:/a coleman_liau_index: $coleman_liau" "$file_path"
            elif grep -q "^gunning_fog_index:" "$file_path"; then
                sed -i "/^gunning_fog_index:/a coleman_liau_index: $coleman_liau" "$file_path"
            elif grep -q "^flesch_kincaid_grade:" "$file_path"; then
                sed -i "/^flesch_kincaid_grade:/a coleman_liau_index: $coleman_liau" "$file_path"
            elif grep -q "^flesch_reading_ease:" "$file_path"; then
                sed -i "/^flesch_reading_ease:/a coleman_liau_index: $coleman_liau" "$file_path"
            elif grep -q "^title:" "$file_path"; then
                sed -i "/^title:/a coleman_liau_index: $coleman_liau" "$file_path"
            else
                sed -i "2a coleman_liau_index: $coleman_liau" "$file_path"
            fi
        fi
    else
        # No frontmatter - add it
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "coleman_liau_index: $coleman_liau" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$file_path" >> "$temp_file"
        mv "$temp_file" "$file_path"
    fi
    
    echo "Updated $file_path with Coleman-Liau Index"
else
    echo "Error: No words found in document"
    exit 1
fi
```

## Usage Examples

```bash
# Calculate for specific file
/coleman-liau ~/documents/my-article.md

# Calculate for current document (will prompt for path)
/coleman-liau
```

## Output
- Displays the calculated Coleman-Liau Index and reading level
- Adds or updates `coleman_liau_index` field in document frontmatter
- Shows document statistics and averages

## Reading Level Interpretation  
- **Below 0**: Very Easy (Below Elementary)
- **1-5**: Elementary School
- **6-8**: Middle School
- **9-12**: High School
- **13-16**: College
- **17+**: Graduate School

## About Coleman-Liau
- **Character-based**: Uses letter counts instead of syllables, making it more reliable for automated analysis
- **Language independent**: Works better across different languages than syllable-based metrics
- **Precise counting**: No ambiguity in counting letters vs. the complexity of syllable counting
- **Academic origin**: Developed by Meri Coleman and T.L. Liau in 1975