#!/bin/bash
set -e

echo "Building frontend..."
npm ci --legacy-peer-deps
npm run build

echo "Build complete!"