#!/bin/bash

OUTPUT_DIR="models"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Read names from names.txt and generate a model for each
while IFS= read -r name; do
    # Skip empty lines and comments
    if [ -z "$name" ] || [[ "$name" =~ ^\ *#.* ]]; then
        continue
    fi
    
    echo "Generating whistle for: $name"
    
    python whistle.py "$name"
    
    filename=$(echo "$name" | tr ' ' '_')
    mv whistle.step "$OUTPUT_DIR/whistle-${filename}.step"
    
done < names.txt

echo "Done! Generated $(ls -1 $OUTPUT_DIR/*.step 2>/dev/null | wc -l) whistles in the '$OUTPUT_DIR' directory."
