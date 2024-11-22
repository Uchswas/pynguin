#!/bin/bash

# Delete the 'reports' directory if it exists
if [ -d "reports" ]; then
    echo "Deleting 'reports' directory..."
    rm -rf reports
else
    echo "'reports' directory does not exist."
fi

# Delete the 'generated_tests' directory if it exists
if [ -d "generated_tests" ]; then
    echo "Deleting 'generated_tests' directory..."
    rm -rf generated_tests
else
    echo "'generated_tests' directory does not exist."
fi

# Delete all '__pycache__' directories recursively
echo "Deleting '__pycache__' directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleanup complete!"

