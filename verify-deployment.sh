#!/bin/bash

echo "🚀 Verifying GitHub Pages deployment setup..."

# Check if package.json has correct homepage
echo "✅ Checking package.json homepage..."
grep -q "harmartim-oss.github.io/Will-and-POA-App" package.json && echo "✓ Homepage correctly set" || echo "❌ Homepage not set correctly"

# Check if vite.config.js has correct base
echo "✅ Checking vite.config.js base path..."
grep -q "/Will-and-POA-App/" vite.config.js && echo "✓ Base path correctly set" || echo "❌ Base path not set correctly"

# Check if dist directory exists and has correct files
echo "✅ Checking dist directory..."
if [ -d "dist" ]; then
    echo "✓ dist directory exists"
    
    if [ -f "dist/index.html" ]; then
        echo "✓ index.html exists"
        grep -q "/Will-and-POA-App/assets/" dist/index.html && echo "✓ Asset paths are correct" || echo "❌ Asset paths incorrect"
    else
        echo "❌ index.html missing"
    fi
    
    if [ -f "dist/404.html" ]; then
        echo "✓ 404.html exists"
    else
        echo "❌ 404.html missing"
    fi
    
    if [ -f "dist/favicon.svg" ]; then
        echo "✓ favicon.svg exists"
    else
        echo "❌ favicon.svg missing"
    fi
    
    if [ -d "dist/assets" ]; then
        echo "✓ assets directory exists"
        ls -la dist/assets/ | head -5
    else
        echo "❌ assets directory missing"
    fi
else
    echo "❌ dist directory does not exist - run npm run build first"
fi

echo "🎯 Deployment verification complete!"