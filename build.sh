#!/usr/bin/env bash
set -o errexit

echo "==> Installing Python dependencies..."
cd backend
pip install -r requirements.txt

echo "==> Building React frontend..."
cd ../frontend
npm install
npm run build

echo "==> Copying frontend build to backend/static..."
rm -rf ../backend/static
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

echo "==> Build complete!"
ls -la ../backend/static/
