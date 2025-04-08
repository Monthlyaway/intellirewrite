#!/bin/bash

echo "Cleaning rewriter data..., make sure the OUTPUT_DIR is `output`, or you need to manually modify this clearning script."

# Check if tasks.json exists and delete it
if [ -f "tasks.json" ]; then
    echo "Deleting tasks.json..."
    rm -f tasks.json
fi

# Check if output folder exists and delete it
if [ -d "output" ]; then
    echo "Deleting output folder..."
    rm -rf output
fi

echo "Cleanup complete!"
echo ""
echo "All task files and chapter data have been removed."
echo "You can now start fresh with new tasks."
echo "" 