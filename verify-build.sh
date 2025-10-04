#!/bin/bash
# Verification script for GitHub Pages deployment

echo "🔍 Verifying build output..."
echo ""

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo "❌ dist folder not found. Run 'npm run build' first."
    exit 1
fi

echo "✅ dist folder found"

# Check for .nojekyll file
if [ -f "dist/.nojekyll" ]; then
    echo "✅ .nojekyll file present"
else
    echo "❌ .nojekyll file missing"
    exit 1
fi

# Check for index.html
if [ -f "dist/index.html" ]; then
    echo "✅ index.html present"
else
    echo "❌ index.html missing"
    exit 1
fi

# Check for 404.html
if [ -f "dist/404.html" ]; then
    echo "✅ 404.html present"
else
    echo "⚠️  404.html missing (optional but recommended)"
fi

# Check if assets folder exists
if [ -d "dist/assets" ]; then
    echo "✅ assets folder present"
    asset_count=$(ls -1 dist/assets/*.js 2>/dev/null | wc -l)
    echo "   Found $asset_count JavaScript files"
else
    echo "❌ assets folder missing"
    exit 1
fi

# Check base path in index.html
if grep -q "/Will-and-POA-App/" dist/index.html; then
    echo "✅ Base path configured correctly in index.html"
else
    echo "⚠️  Base path may not be configured correctly"
fi

# Check if favicon exists
if [ -f "dist/favicon.svg" ]; then
    echo "✅ favicon.svg present"
else
    echo "⚠️  favicon.svg missing"
fi

echo ""
echo "✅ Build verification complete!"
echo ""
echo "📦 Build size:"
du -sh dist
echo ""
echo "📄 Files in dist:"
ls -lah dist/ | grep -v "^total" | tail -n +2
echo ""
echo "🚀 Ready for deployment to GitHub Pages!"
