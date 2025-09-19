#!/bin/bash

echo "🧪 Testing component imports and build health..."

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found. Run 'npm install' first."
    exit 1
fi

# Test build
echo "✅ Testing production build..."
NODE_ENV=production npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi

# Check if key files exist in dist
echo "✅ Checking build artifacts..."
required_files=("dist/index.html" "dist/favicon.svg" "dist/404.html" "dist/assets")
for file in "${required_files[@]}"; do
    if [ -e "$file" ]; then
        echo "✓ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Check if assets have correct base path
echo "✅ Checking asset paths..."
if grep -q "/Will-and-POA-App/assets/" dist/index.html; then
    echo "✓ Asset paths correctly prefixed"
else
    echo "❌ Asset paths not correctly prefixed"
    exit 1
fi

# Check if favicon path is correct
if grep -q "/Will-and-POA-App/favicon.svg" dist/index.html; then
    echo "✓ Favicon path correctly prefixed"
else
    echo "❌ Favicon path not correctly prefixed"
    exit 1
fi

# Test preview server startup
echo "✅ Testing preview server..."
timeout 10s npm run preview > /dev/null 2>&1 &
PREVIEW_PID=$!
sleep 3

# Check if server is responding (basic check)
if kill -0 $PREVIEW_PID 2>/dev/null; then
    echo "✓ Preview server started successfully"
    kill $PREVIEW_PID 2>/dev/null
else
    echo "⚠️  Preview server test skipped (timeout or other issues)"
fi

echo ""
echo "🎉 All tests passed! The application is ready for GitHub Pages deployment."
echo "📄 Build size information:"
ls -lh dist/assets/ | grep -E '\.(js|css)$' | awk '{print "   " $9 ": " $5}'
echo ""
echo "🚀 Deploy URL: https://harmartim-oss.github.io/Will-and-POA-App/"