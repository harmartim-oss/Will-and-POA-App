// Environment configuration for different deployment scenarios

const isDevelopment = import.meta.env.MODE === 'development';
const isProduction = import.meta.env.MODE === 'production';
const isGitHubPages = window.location.hostname.includes('github.io');

// API Base URLs for different environments
const API_ENDPOINTS = {
  development: 'http://localhost:5000/api',
  production: isGitHubPages 
    ? 'https://your-backend-domain.com/api'  // Replace with your actual backend URL
    : 'http://localhost:5000/api',
  staging: 'https://staging-api.your-domain.com/api'
};

// Get current API base URL
export const getApiBaseUrl = () => {
  if (isDevelopment) {
    return API_ENDPOINTS.development;
  }
  
  if (isGitHubPages) {
    return API_ENDPOINTS.production;
  }
  
  return API_ENDPOINTS.production;
};

// Application configuration
export const config = {
  apiBaseUrl: getApiBaseUrl(),
  isDevelopment,
  isProduction,
  isGitHubPages,
  
  // Feature flags
  features: {
    enableAIAnalysis: true,
    enableESignature: !isGitHubPages, // Disable for GitHub Pages demo
    enableLawyerReview: !isGitHubPages, // Disable for GitHub Pages demo
    enableSecureStorage: !isGitHubPages, // Disable for GitHub Pages demo
    enableOfflineMode: true,
    enableDarkMode: true,
    enableNotifications: true
  },
  
  // App metadata
  app: {
    name: 'Ontario Wills & Power of Attorney Creator',
    version: '2.0.0',
    description: 'Professional legal document creation with AI assistance',
    author: 'Ontario Legal Tech Solutions',
    supportEmail: 'support@ontariowills.com',
    privacyPolicyUrl: '/privacy',
    termsOfServiceUrl: '/terms'
  },
  
  // GitHub Pages specific configuration
  githubPages: {
    basePath: isGitHubPages ? '/Will-and-POA-App' : '',
    demoMode: isGitHubPages,
    offlineData: isGitHubPages // Use local storage for demo data
  },
  
  // Storage configuration
  storage: {
    prefix: 'ontario_wills_',
    version: '2.0',
    encryptionEnabled: true
  },
  
  // UI configuration
  ui: {
    theme: {
      defaultTheme: 'light',
      allowThemeToggle: true
    },
    animations: {
      enabled: true,
      duration: 300
    },
    notifications: {
      position: 'top-right',
      duration: 5000
    }
  },
  
  // Document configuration
  documents: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    allowedFormats: ['pdf', 'docx', 'txt'],
    autoSave: true,
    autoSaveInterval: 30000, // 30 seconds
    versionHistory: true,
    maxVersions: 10
  },
  
  // Security configuration
  security: {
    sessionTimeout: 24 * 60 * 60 * 1000, // 24 hours
    maxLoginAttempts: 5,
    passwordMinLength: 8,
    requireStrongPassword: true,
    enableTwoFactor: false // Disabled for demo
  }
};

// Environment-specific overrides
if (isGitHubPages) {
  // GitHub Pages demo mode overrides
  config.features.enableESignature = false;
  config.features.enableLawyerReview = false;
  config.features.enableSecureStorage = false;
  config.githubPages.demoMode = true;
  config.githubPages.offlineData = true;
}

// Export individual configurations for convenience
export const {
  apiBaseUrl,
  features,
  app,
  githubPages,
  storage,
  ui,
  documents,
  security
} = config;

// Utility functions
export const isFeatureEnabled = (featureName) => {
  return config.features[featureName] || false;
};

export const getStorageKey = (key) => {
  return `${storage.prefix}${key}`;
};

export const getFullUrl = (path) => {
  const basePath = githubPages.basePath;
  return basePath + path;
};

// Debug information (development only)
if (isDevelopment) {
  console.log('Environment Configuration:', {
    mode: import.meta.env.MODE,
    apiBaseUrl: config.apiBaseUrl,
    isGitHubPages,
    features: config.features,
    githubPages: config.githubPages
  });
}

export default config;

