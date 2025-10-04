# Deployment Troubleshooting Guide

This guide helps troubleshoot common deployment issues with the Ontario Wills & Power of Attorney Creator on GitHub Pages.

## ✅ Prerequisites Checklist

Before deploying, ensure:

- [ ] `.nojekyll` file exists in `public/` directory
- [ ] `vite.config.js` has correct `base` path: `/Will-and-POA-App/`
- [ ] `package.json` has correct `homepage`: `https://harmartim-oss.github.io/Will-and-POA-App`
- [ ] GitHub Pages is enabled in repository settings
- [ ] GitHub Actions workflow has proper permissions

## 🔍 Common Issues and Solutions

### Issue 1: "Application Failed to Load" on Deployed Page

**Symptoms:**
- Page shows "Application Failed to Load" error
- Console shows 404 errors for JavaScript files
- Assets not loading

**Root Cause:**
Missing `.nojekyll` file causes GitHub Pages to ignore files/folders starting with underscores (created by modern build tools).

**Solution:**
```bash
# Create .nojekyll file
touch public/.nojekyll

# Rebuild
npm run build

# Verify it's in dist
ls -la dist/.nojekyll
```

✅ **Fixed in this PR!**

### Issue 2: Blank Page After Deployment

**Symptoms:**
- Page loads but shows nothing
- Console shows routing errors
- Assets load but app doesn't render

**Root Cause:**
Incorrect base path configuration in `vite.config.js` or router.

**Solution:**
```javascript
// vite.config.js
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/Will-and-POA-App/' : '/',
  // ... rest of config
})

// App.jsx - Router basename
<Router basename={config.githubPages.basePath}>
```

✅ **Already configured correctly!**

### Issue 3: Assets Loading from Wrong Path

**Symptoms:**
- Console shows 404 errors for CSS/JS files
- Network tab shows requests to wrong URLs
- Favicon not loading

**Root Cause:**
Assets not using correct base path in production.

**Solution:**
Vite handles this automatically when `base` is set correctly. For manual paths:
```javascript
// Use Vite's import.meta.env.BASE_URL
const assetPath = `${import.meta.env.BASE_URL}assets/image.png`;
```

✅ **Handled by Vite configuration!**

### Issue 4: 404 Errors on Page Refresh

**Symptoms:**
- App works on initial load
- Refreshing any non-root page shows 404
- Direct navigation to routes fails

**Root Cause:**
GitHub Pages doesn't support SPA routing natively.

**Solution:**
The `404.html` file redirects all routes to `index.html`:
```bash
# Ensure 404.html is in public/
ls public/404.html
```

✅ **Already configured!**

### Issue 5: Fonts Not Loading

**Symptoms:**
- Text appears in fallback fonts
- Console shows CORS errors for fonts
- Google Fonts not working

**Root Cause:**
Missing preconnect or CORS issues.

**Solution:**
```html
<!-- In index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
```

✅ **Already configured!**

## 🛠️ Verification Steps

### Local Verification

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Run verification script:**
   ```bash
   ./verify-build.sh
   ```

3. **Test with preview server:**
   ```bash
   npm run preview
   ```
   Open: http://localhost:4173/Will-and-POA-App/

4. **Check browser console:**
   - No 404 errors
   - All assets load correctly
   - App renders successfully

### Production Verification

1. **Check GitHub Actions workflow:**
   - Go to repository Actions tab
   - Verify latest workflow run succeeded
   - Check for any errors in logs

2. **Check GitHub Pages settings:**
   - Go to Settings → Pages
   - Source should be "GitHub Actions"
   - Custom domain (if any) configured correctly

3. **Test deployed site:**
   - Visit: https://harmartim-oss.github.io/Will-and-POA-App/
   - Open browser console (F12)
   - Check for errors
   - Test navigation between pages
   - Verify all features work

## 📊 Debug Information

### Enable Debug Logging

The app includes extensive debug logging. Check console for:
- `🚀 Application starting up...` - Initial load
- `🔧 App component initializing...` - React mounting
- `✅ React app rendered successfully` - Successful render
- `🔄 Removing initial loader` - Loader cleanup

### Common Console Messages

**Normal:**
```
🚀 Application starting up...
🔧 App component initializing...
✅ React app rendered successfully
🔄 Removing initial loader
✅ Initial loader removed - app fully loaded
```

**Warning (but OK):**
```
⚠️ Incorrect base path detected
```
This is normal in development mode.

**Error (needs attention):**
```
❌ Failed to initialize React app
❌ Global error
```
Check the full error message and stack trace.

## 🔧 Build Configuration

### Critical Files

1. **public/.nojekyll** - Prevents Jekyll processing
2. **public/404.html** - Handles SPA routing
3. **vite.config.js** - Build configuration with base path
4. **src/config/environment.js** - Runtime configuration

### Environment Variables

Set in GitHub Actions workflow:
```yaml
env:
  NODE_ENV: production
  VITE_GITHUB_PAGES: true
```

## 📝 Quick Fix Checklist

If deployment fails, check:

- [ ] Run `./verify-build.sh` - all checks pass?
- [ ] `.nojekyll` file in dist folder?
- [ ] `index.html` references assets with `/Will-and-POA-App/` base path?
- [ ] GitHub Actions workflow succeeded?
- [ ] Browser console shows specific errors?
- [ ] Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)?
- [ ] Test in different browser?
- [ ] Check GitHub Pages status page?

## 🆘 Getting Help

If issues persist:

1. **Check browser console** - Copy full error messages
2. **Check GitHub Actions logs** - Look for build failures
3. **Run locally** - Does `npm run preview` work?
4. **Compare with working commit** - What changed?

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [React Router GitHub Pages](https://reactrouter.com/en/main/router-components/browser-router)
- [SPA GitHub Pages](https://github.com/rafgraph/spa-github-pages)

---

**Note:** The fixes applied in this PR address the primary issue (missing `.nojekyll` file) and add extensive debugging capabilities. If you still experience issues after merging, follow the troubleshooting steps above.
