#!/bin/bash

# Build script for GitHub Pages deployment
echo "🚀 Building for GitHub Pages deployment..."

# Set environment variables
export NODE_ENV=production
export VITE_GITHUB_PAGES=true

# Build the application
npm run build

# Fix favicon path for GitHub Pages
echo "🔧 Fixing favicon path for GitHub Pages..."
sed -i 's|href="./favicon.svg"|href="/Will-and-POA-App/favicon.svg"|g' dist/index.html

echo "✅ Build complete! Ready for deployment to GitHub Pages."
echo "📁 Files ready in dist/ directory"