import React, { Suspense, lazy } from 'react';
import EnhancedLoading from './ui/enhanced-loading';
import ErrorBoundary from './ui/error-boundary';

// Lazy load heavy components
const DocumentCreator = lazy(() => import('./DocumentCreator'));
const EnhancedDocumentCreator = lazy(() => import('./EnhancedDocumentCreator'));
const PremiumDocumentCreator = lazy(() => import('./PremiumDocumentCreator'));

// Lazy load 3D components
const ThreeDDocumentViewer = lazy(() => 
  import('./ThreeDDocumentViewer').catch(() => ({
    default: () => <div>3D Viewer not available</div>
  }))
);

// Lazy load PDF components
const DocumentPreviewEnhanced = lazy(() => 
  import('./DocumentPreviewEnhanced').catch(() => ({
    default: () => <div>PDF Preview not available</div>
  }))
);

const LazyDocumentCreator = ({ 
  type = 'enhanced', 
  documentType = 'will',
  onSave,
  onPreview,
  ...props 
}) => {
  const getComponent = () => {
    switch (type) {
      case 'premium':
        return PremiumDocumentCreator;
      case 'enhanced':
        return EnhancedDocumentCreator;
      case 'basic':
      default:
        return DocumentCreator;
    }
  };

  const Component = getComponent();

  const getLoadingMessage = () => {
    switch (type) {
      case 'premium':
        return {
          message: "Loading Premium Document Creator",
          submessage: "Initializing 3D visualization and AI features...",
          type: 'ai'
        };
      case 'enhanced':
        return {
          message: "Loading Enhanced Document Creator",
          submessage: "Setting up advanced legal tools...",
          type: 'legal'
        };
      default:
        return {
          message: "Loading Document Creator",
          submessage: "Preparing your legal document wizard...",
          type: 'document'
        };
    }
  };

  const loadingProps = getLoadingMessage();

  return (
    <ErrorBoundary>
      <Suspense 
        fallback={
          <div className="min-h-screen flex items-center justify-center">
            <EnhancedLoading 
              {...loadingProps}
              size="large"
            />
          </div>
        }
      >
        <Component
          documentType={documentType}
          onSave={onSave}
          onPreview={onPreview}
          {...props}
        />
      </Suspense>
    </ErrorBoundary>
  );
};

// Export individual lazy components for more granular loading
export const LazyThreeDViewer = ({ ...props }) => (
  <ErrorBoundary>
    <Suspense 
      fallback={
        <div className="w-full h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-900 rounded-lg">
          <EnhancedLoading 
            message="Loading 3D Viewer"
            submessage="Initializing Three.js components..."
            type="ai"
          />
        </div>
      }
    >
      <ThreeDDocumentViewer {...props} />
    </Suspense>
  </ErrorBoundary>
);

export const LazyPDFPreview = ({ ...props }) => (
  <ErrorBoundary>
    <Suspense 
      fallback={
        <div className="w-full h-96 flex items-center justify-center bg-gray-50 dark:bg-gray-900 rounded-lg">
          <EnhancedLoading 
            message="Loading PDF Preview"
            submessage="Preparing document preview..."
            type="document"
          />
        </div>
      }
    >
      <DocumentPreviewEnhanced {...props} />
    </Suspense>
  </ErrorBoundary>
);

// Higher-order component for lazy loading any component
export const withLazyLoading = (
  importFunc, 
  fallbackComponent = null,
  errorFallback = null
) => {
  const LazyComponent = lazy(importFunc);
  
  return (props) => (
    <ErrorBoundary fallback={errorFallback}>
      <Suspense fallback={fallbackComponent || <EnhancedLoading />}>
        <LazyComponent {...props} />
      </Suspense>
    </ErrorBoundary>
  );
};

// Preload functions for better UX
export const preloadDocumentCreator = (type = 'enhanced') => {
  switch (type) {
    case 'premium':
      return import('./PremiumDocumentCreator');
    case 'enhanced':
      return import('./EnhancedDocumentCreator');
    default:
      return import('./DocumentCreator');
  }
};

export const preloadThreeDViewer = () => {
  return import('./ThreeDDocumentViewer').catch(() => null);
};

export const preloadPDFPreview = () => {
  return import('./DocumentPreviewEnhanced').catch(() => null);
};

// Hook for preloading components on user interaction
export const usePreload = () => {
  const preload = React.useCallback((componentType) => {
    switch (componentType) {
      case 'document-creator':
        return preloadDocumentCreator();
      case 'premium-creator':
        return preloadDocumentCreator('premium');
      case '3d-viewer':
        return preloadThreeDViewer();
      case 'pdf-preview':
        return preloadPDFPreview();
      default:
        return Promise.resolve();
    }
  }, []);

  return { preload };
};

export default LazyDocumentCreator;
