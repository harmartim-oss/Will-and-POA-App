# Ontario Wills & Power of Attorney Creator ✨

🏛️ **Professional legal document creation platform compliant with Ontario law**

## 🎯 Recent Enhancements (v2.2)

✅ **🔌 Progressive Web App (PWA)** - Install on any device, works offline!  
✅ **💾 Offline Storage** - Auto-save drafts with IndexedDB (Dexie.js)  
✅ **🔄 Smart Caching** - Service worker with Workbox for instant loading  
✅ **📱 Installable** - Add to home screen on mobile and desktop  
✅ **🔔 Update Notifications** - Automatic update prompts for new versions  
✅ **🚀 Performance** - Lighthouse score 95+ across all metrics  
✅ **🐛 Fixed Deployment** - Removed conflicting workflow files  
✅ **📦 Optimized Bundle** - Reduced from 7+ chunks to 3 optimized chunks  
✅ **⚡ Non-blocking Fonts** - Asynchronous font loading prevents render blocking  
✅ **🎨 Enhanced UI/UX** - Modern design with smooth animations  

> 📖 **[See PWA Features Documentation](./PWA_FEATURES.md)** for detailed information about offline capabilities, installation, and usage.  

## ✨ Features

- 📄 **Last Will and Testament Creation** - Comprehensive will drafting with asset distribution, executor appointment, and guardian designation
- 🏛️ **Power of Attorney for Property** - Financial and property decision authorization  
- 🏥 **Power of Attorney for Personal Care** - Healthcare and personal care decision authorization
- 🤖 **AI-Powered Assistance** - Intelligent suggestions and legal guidance
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 🔒 **Ontario Law Compliant** - All documents meet Ontario legal requirements
- ✨ **Beautiful Animations** - Smooth transitions and interactive elements
- 🎨 **Modern UI** - Professional design with enhanced user experience
- 🔌 **Works Offline** - Progressive Web App with offline support
- 💾 **Auto-Save** - Drafts automatically saved to local storage
- 📲 **Installable** - Add to home screen for app-like experience

## 🚀 Live Demo

Visit the live application: **[Ontario Wills & Power of Attorney Creator](https://harmartim-oss.github.io/Will-and-POA-App/)**

### 📸 App Screenshots

**Enhanced Version (v2.0):**
![Enhanced App](https://github.com/user-attachments/assets/850eea95-826e-42b2-84fc-016bce51c84b)

*Features: Sticky header with animations, gradient backgrounds, enhanced feature cards, and improved typography*

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite 6, TypeScript
- **UI Components**: Radix UI, Tailwind CSS, Lucide Icons
- **Routing**: React Router v7
- **Animations**: Framer Motion
- **PWA**: vite-plugin-pwa, Workbox
- **Offline Storage**: Dexie.js (IndexedDB)
- **Build**: Vite with code splitting and optimization
- **Deployment**: GitHub Pages with GitHub Actions CI/CD

## 📦 Installation & Development

```bash
# Clone the repository
git clone https://github.com/harmartim-oss/Will-and-POA-App.git
cd Will-and-POA-App

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 Deployment

The application is automatically deployed to GitHub Pages using GitHub Actions:

- **Production URL**: https://harmartim-oss.github.io/Will-and-POA-App/
- **Auto-deployment**: On every push to `main` branch
- **SPA Support**: Full client-side routing support
- **Optimized**: Code splitting and asset optimization

### Deployment Features:
- ✅ Automated CI/CD with GitHub Actions
- ✅ SPA routing support for direct URL access
- ✅ Optimized production builds
- ✅ Environment-specific configuration
- ✅ Asset optimization and compression

### 🔍 Deployment Verification

Run the build verification script to ensure everything is properly configured:

```bash
# Build the application
npm run build

# Verify build output
./verify-build.sh
```

This script verifies:
- ✅ `.nojekyll` file present (critical for GitHub Pages)
- ✅ All required files (index.html, 404.html, favicon.svg)
- ✅ Assets folder with JavaScript bundles
- ✅ Base path configuration in HTML
- ✅ Build size and file listing

### 🆘 Troubleshooting Deployment Issues

If you encounter deployment issues, see [DEPLOYMENT_TROUBLESHOOTING.md](./DEPLOYMENT_TROUBLESHOOTING.md) for:
- Common issues and solutions
- Debug logging information
- Verification steps
- Quick fix checklist

## 📱 Application Features

### Document Creation Workflow
1. **Select Document Type** - Choose from will or power of attorney options
2. **Step-by-Step Guidance** - Intuitive multi-step forms with progress tracking
3. **Legal Compliance** - Built-in Ontario law requirements and validation
4. **Professional Output** - Generate properly formatted legal documents

### User Experience
- **Responsive Design** - Optimized for all device sizes
- **Modern UI** - Clean, professional interface using Radix UI components
- **Progress Tracking** - Visual progress indicators throughout document creation
- **Form Validation** - Real-time validation with helpful error messages
- **Accessibility** - WCAG compliant with keyboard navigation support

## 🏗️ Project Structure

```
src/
├── components/           # React components
│   ├── ui/              # Reusable UI components
│   ├── LandingPage.jsx  # Homepage component
│   ├── DocumentCreator.jsx
│   └── ...
├── config/              # Configuration files
│   └── environment.js   # Environment-specific settings
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions
├── main.jsx            # Application entry point
├── App.jsx             # Main app component
└── index.css           # Global styles
```

## 🔧 Configuration

The application automatically detects the deployment environment:

- **Development**: Full feature set with local API
- **GitHub Pages**: Demo mode with offline data
- **Production**: Optimized build with CDN assets

## 📄 Legal Disclaimer

This tool provides templates and guidance for creating legal documents. While designed to comply with Ontario law, it's recommended to consult with a qualified legal professional for complex situations or validation of important legal documents.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the documentation in the `/documentation` folder
- Review the deployment guides for setup assistance

## 📊 Performance

- **Lighthouse Score**: 95+ Performance, 100 Accessibility
- **Bundle Size**: Optimized - Only 3 chunks (288 KB total, 82 KB gzipped)
- **Load Time**: 1-2s initial load, < 500ms cached loads
- **Offline Support**: Service worker enables offline functionality
- **SEO Optimized**: Meta tags and structured data
- **Non-blocking Assets**: Asynchronous font and resource loading

See [PERFORMANCE_IMPROVEMENTS.md](./PERFORMANCE_IMPROVEMENTS.md) for detailed optimization information.

---

**Built with ❤️ for Ontario residents seeking accessible legal document creation**