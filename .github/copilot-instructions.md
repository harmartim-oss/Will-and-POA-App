# Copilot Instructions for Ontario Wills & Power of Attorney Creator

## Project Overview

This is a professional legal document creation platform compliant with Ontario law. The application helps users create Last Will and Testaments, Power of Attorney for Property, and Power of Attorney for Personal Care documents.

## Tech Stack

### Frontend
- **Framework**: React 19 with Vite 6
- **UI Components**: Radix UI, shadcn/ui, Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router v7
- **Animations**: Framer Motion
- **Forms**: React Hook Form with Zod validation
- **Build**: Vite with code splitting and optimization

### Backend (Optional/Future)
- **Framework**: FastAPI with Python 3.9+
- **AI/ML**: spaCy, OpenAI API, Langchain
- **Document Generation**: python-docx, ReportLab
- **Database**: SQLAlchemy with PostgreSQL

### Deployment
- **Primary**: GitHub Pages with GitHub Actions CI/CD
- **Base Path**: `/Will-and-POA-App/` for production builds
- **Production URL**: https://harmartim-oss.github.io/Will-and-POA-App/

## Coding Standards

### JavaScript/React
- Use ES6+ modern JavaScript features
- Prefer functional components with React Hooks
- Use arrow functions for components and callbacks
- Follow React best practices (useCallback, useMemo for optimization)
- Use TypeScript-style JSDoc comments for complex functions
- Avoid console.log in production code (configure via esbuild)
- Use `@` alias for src imports (configured in vite.config.js)

### Code Style
- Run `npm run lint` before committing
- Follow ESLint rules defined in `eslint.config.js`
- Unused variables should be prefixed with `_` if intentional
- React hooks dependencies should be complete (no exhaustive-deps warnings)

### Component Structure
```javascript
// Preferred pattern
import { useState, useCallback } from 'react'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

const MyComponent = ({ prop1, prop2 }) => {
  const [state, setState] = useState(initialValue)
  
  const handleAction = useCallback(() => {
    // Action logic
  }, [dependencies])
  
  return (
    <Card>
      <CardHeader>...</CardHeader>
      <CardContent>...</CardContent>
    </Card>
  )
}

export default MyComponent
```

### State Management
- Use React Context for global state (see `src/hooks/` for examples)
- Prefer local component state when possible
- Use useReducer for complex state logic

## File Organization

```
src/
├── components/       # Reusable UI components
│   ├── ui/          # Base shadcn/ui components
│   └── ...          # Feature components
├── config/          # Configuration files
├── design/          # Design system tokens
├── hooks/           # Custom React hooks
├── lib/             # Utility libraries
├── utils/           # Utility functions
└── App.jsx          # Main application component
```

## Legal Compliance Requirements

### Ontario Law Compliance
All documents must comply with Ontario legal requirements:

#### Last Will and Testament
- Testator must be 18+ years old and mentally capable
- Must be in writing and signed by testator
- Requires TWO witnesses present at signing
- Witnesses CANNOT be beneficiaries
- Holographic wills (entirely handwritten) don't need witnesses

#### Power of Attorney for Property
- Grantor must be 18+ years old and mentally capable
- Must be in writing and signed
- Requires TWO witnesses
- Witnesses cannot be the attorney or their spouse

#### Power of Attorney for Personal Care
- Grantor must be 16+ years old and mentally capable
- Must be in writing and signed
- Requires TWO witnesses
- Witnesses cannot be the attorney or their spouse

### Important Notes
- NO notarization required in Ontario
- Physical "wet signature" required for legal validity
- Documents must include clear revocation clauses
- Consider contingency provisions for beneficiaries

## Development Workflow

### Local Development
```bash
npm install          # Install dependencies
npm run dev          # Start development server (port 5173)
npm run build        # Build for production
npm run preview      # Preview production build (port 4173)
```

### Testing
```bash
npm run lint         # Run ESLint
npm run test         # Run Vitest tests
```

### Deployment
- Automatic deployment via GitHub Actions on push to `main`
- Manual: `npm run deploy` (requires GITHUB_TOKEN)
- Always verify build with `./verify-build.sh` after building

## Build Configuration

### Critical Files
- `vite.config.js` - Build configuration with base path `/Will-and-POA-App/`
- `public/.nojekyll` - REQUIRED for GitHub Pages (prevents Jekyll processing)
- `public/404.html` - Handles SPA routing on GitHub Pages
- `package.json` - Homepage set to GitHub Pages URL

### Environment-Specific Settings
- Production base path: `/Will-and-POA-App/`
- Development base path: `/`
- Assets optimized and code-split in production
- Console logs dropped in production builds

## Performance Optimization

### Code Splitting
- React vendor bundle separate from application code
- UI components split by usage patterns
- Heavy libraries (PDF, 3D) lazy-loaded
- Manual chunks defined in `vite.config.js`

### Loading Strategy
- Fonts loaded asynchronously (non-blocking)
- Service Worker for offline support
- Progress indicators for long-running operations

## UI/UX Guidelines

### Design System
- Use Tailwind CSS utility classes
- Follow spacing scale from design tokens
- Use Radix UI primitives for accessibility
- Implement smooth animations with Framer Motion
- Ensure responsive design (mobile, tablet, desktop)

### Accessibility
- All interactive elements must be keyboard accessible
- Provide proper ARIA labels
- Maintain proper heading hierarchy
- Ensure sufficient color contrast

### User Experience
- Show loading states for async operations
- Display clear error messages with recovery options
- Use confirmation dialogs for destructive actions
- Provide helpful tooltips and hints

## Common Tasks

### Adding a New Component
1. Create component in appropriate directory under `src/components/`
2. Follow existing component patterns
3. Import from `@/components/` using alias
4. Add proper prop types and validation

### Adding a New Page
1. Create page component
2. Add route in `App.jsx` or router configuration
3. Consider lazy loading for better code splitting
4. Update navigation if needed

### Working with AI Features
- Mock AI responses for development/testing
- Use placeholder data that looks realistic
- Consider loading states and error handling
- Follow Ontario legal standards in AI suggestions

### Document Generation
- Use existing document templates as reference
- Ensure all required legal clauses are included
- Validate user input before generating documents
- Include proper disclaimers about legal review

## Troubleshooting

### Build Issues
- Check `DEPLOYMENT_TROUBLESHOOTING.md` for common issues
- Verify `.nojekyll` file exists in `public/` directory
- Ensure base path is correct in `vite.config.js`
- Clear `dist/` and `node_modules/` if needed

### Deployment Issues
- Verify GitHub Actions workflow succeeded
- Check GitHub Pages settings in repository
- Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
- Run `./verify-deployment.sh` after build

### Development Issues
- Clear Vite cache: `rm -rf node_modules/.vite`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check console for ESLint warnings
- Verify all imports use correct paths

## Security Considerations

- Never commit API keys or secrets
- Sanitize user input before processing
- Use proper CORS settings for API calls
- Validate all form data on both client and server
- Follow OWASP best practices for web security

## Documentation

- Document complex logic with comments
- Update README.md for major feature additions
- Keep deployment guides current
- Maintain changelog for version tracking

## AI Assistant Usage

When using AI features in the application:
- Provide clear disclaimers that AI is advisory only
- Always recommend professional legal review
- Base suggestions on Ontario legal requirements
- Include references to relevant legislation (e.g., Succession Law Reform Act)
- Implement appropriate error handling for AI service failures

## References

- Ontario Succession Law Reform Act
- Ontario Substitute Decisions Act
- Legal requirements documented in `legal_requirements.md`
- Deployment guides in various markdown files
- Component examples in `src/components/`
