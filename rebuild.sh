#!/bin/bash

# 1. Clean up old build artifacts
echo "Cleaning up old build files..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info

# 2. Ensure the 'build' package is installed
python3 -m pip install --quiet build

# 3. Build the Source Distribution (sdist) and Wheel (bdist_wheel)
echo "Starting fresh build..."
python3 -m build

# 4. Verify the contents (optional but recommended)
echo "Contents of the new Wheel:"
unzip -l dist/*.whl | grep -E '(\.py|\.json|\.sql|\.xml)$'

echo "Done! Your package is ready in the dist/ folder."
