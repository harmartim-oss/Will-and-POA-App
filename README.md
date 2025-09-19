# Ontario Wills & Power of Attorney Creator

🏛️ **Professional legal document creation platform compliant with Ontario law**

## ✨ Features

- 📄 **Last Will and Testament Creation** - Comprehensive will drafting with asset distribution, executor appointment, and guardian designation
- 🏛️ **Power of Attorney for Property** - Financial and property decision authorization
- 🏥 **Power of Attorney for Personal Care** - Healthcare and personal care decision authorization
- 🤖 **AI-Powered Assistance** - Intelligent suggestions and legal guidance
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 🔒 **Ontario Law Compliant** - All documents meet Ontario legal requirements

## 🚀 Live Demo

Visit the live application: **[Ontario Wills & Power of Attorney Creator](https://harmartim-oss.github.io/Will-and-POA-App/)**

![Ontario Wills App Screenshot](https://github.com/user-attachments/assets/fc77d96b-142f-4f5a-aaf5-aca146e54dae)

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite 6, TypeScript
- **UI Components**: Radix UI, Tailwind CSS, Lucide Icons
- **Routing**: React Router v7
- **Animations**: Framer Motion
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
- **Bundle Size**: Optimized with code splitting
- **Load Time**: < 2s on 3G networks
- **SEO Optimized**: Meta tags and structured data

---

**Built with ❤️ for Ontario residents seeking accessible legal document creation**