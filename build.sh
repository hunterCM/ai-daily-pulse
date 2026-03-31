#!/usr/bin/env bash
set -o errexit

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Build React frontend
cd ../frontend
npm install
npm run build

# Copy built frontend into backend/static for serving
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

echo "Build complete!"
