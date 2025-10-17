#!/bin/bash
# PWA Deployment Verification Script
# This script verifies that the PWA build is ready for deployment

set -e

echo "🔍 Starting PWA Deployment Verification..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if dist directory exists
echo "📁 Checking dist directory..."
if [ -d "dist" ]; then
    echo -e "${GREEN}✓${NC} dist directory exists"
else
    echo -e "${RED}✗${NC} dist directory not found. Run 'npm run build' first."
    exit 1
fi

# Check for essential files
echo ""
echo "📄 Checking essential files..."

files=(
    "dist/index.html"
    "dist/.nojekyll"
    "dist/404.html"
    "dist/sw.js"
    "dist/manifest.webmanifest"
    "dist/robots.txt"
    "dist/favicon.svg"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file missing"
        exit 1
    fi
done

# Check for PWA icons
echo ""
echo "🎨 Checking PWA icons..."

icons=(
    "dist/pwa-64x64.png"
    "dist/pwa-192x192.png"
    "dist/pwa-512x512.png"
    "dist/maskable-icon-512x512.png"
)

for icon in "${icons[@]}"; do
    if [ -f "$icon" ]; then
        size=$(stat -f%z "$icon" 2>/dev/null || stat -c%s "$icon" 2>/dev/null)
        echo -e "${GREEN}✓${NC} $icon exists (${size} bytes)"
    else
        echo -e "${RED}✗${NC} $icon missing"
        exit 1
    fi
done

# Check manifest.webmanifest content
echo ""
echo "📋 Checking manifest content..."
if grep -q "Ontario Wills" "dist/manifest.webmanifest"; then
    echo -e "${GREEN}✓${NC} Manifest contains app name"
else
    echo -e "${RED}✗${NC} Manifest missing app name"
    exit 1
fi

if grep -q "/Will-and-POA-App/" "dist/manifest.webmanifest"; then
    echo -e "${GREEN}✓${NC} Manifest has correct base path"
else
    echo -e "${YELLOW}⚠${NC} Manifest may have incorrect base path"
fi

# Check service worker
echo ""
echo "⚙️  Checking service worker..."
if grep -q "workbox" "dist/sw.js"; then
    echo -e "${GREEN}✓${NC} Service worker contains Workbox"
else
    echo -e "${YELLOW}⚠${NC} Service worker may not be properly configured"
fi

# Check index.html
echo ""
echo "🏠 Checking index.html..."
if grep -q "manifest.webmanifest" "dist/index.html"; then
    echo -e "${GREEN}✓${NC} index.html links to manifest"
else
    echo -e "${RED}✗${NC} index.html missing manifest link"
    exit 1
fi

if grep -q "/Will-and-POA-App/" "dist/index.html"; then
    echo -e "${GREEN}✓${NC} index.html has correct base path"
else
    echo -e "${YELLOW}⚠${NC} index.html may have incorrect base path"
fi

# Check for JavaScript chunks
echo ""
echo "📦 Checking JavaScript bundles..."
js_files=$(find dist/js -name "*.js" 2>/dev/null | wc -l)
if [ "$js_files" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Found $js_files JavaScript chunk(s)"
    find dist/js -name "*.js" -exec basename {} \; | head -5
else
    echo -e "${RED}✗${NC} No JavaScript chunks found"
    exit 1
fi

# Check for CSS files
echo ""
echo "🎨 Checking CSS files..."
css_files=$(find dist/assets -name "*.css" 2>/dev/null | wc -l)
if [ "$css_files" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} Found $css_files CSS file(s)"
else
    echo -e "${YELLOW}⚠${NC} No CSS files found"
fi

# Calculate total build size
echo ""
echo "📊 Build statistics..."
total_size=$(du -sh dist 2>/dev/null | cut -f1)
echo -e "${BLUE}ℹ${NC} Total build size: $total_size"

js_size=$(du -sh dist/js 2>/dev/null | cut -f1)
echo -e "${BLUE}ℹ${NC} JavaScript size: $js_size"

assets_size=$(du -sh dist/assets 2>/dev/null | cut -f1)
echo -e "${BLUE}ℹ${NC} Assets size: $assets_size"

# File count
file_count=$(find dist -type f | wc -l)
echo -e "${BLUE}ℹ${NC} Total files: $file_count"

# Check .nojekyll content
echo ""
echo "🔧 Checking .nojekyll..."
if [ -f "dist/.nojekyll" ]; then
    if [ -s "dist/.nojekyll" ]; then
        echo -e "${YELLOW}⚠${NC} .nojekyll has content (should be empty)"
    else
        echo -e "${GREEN}✓${NC} .nojekyll is empty (correct)"
    fi
else
    echo -e "${RED}✗${NC} .nojekyll missing"
    exit 1
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════"
echo -e "${GREEN}✅ PWA Build Verification Complete!${NC}"
echo "════════════════════════════════════════════════════"
echo ""
echo "The build is ready for deployment to GitHub Pages."
echo ""
echo "Next steps:"
echo "1. Commit and push to trigger GitHub Actions deployment"
echo "2. Wait for deployment to complete (check Actions tab)"
echo "3. Visit https://harmartim-oss.github.io/Will-and-POA-App/"
echo "4. Test PWA features:"
echo "   - Open DevTools → Application → Service Workers"
echo "   - Check 'Offline' in Network tab and reload"
echo "   - Click install icon in address bar"
echo ""
echo "For detailed PWA features, see PWA_FEATURES.md"
echo ""
