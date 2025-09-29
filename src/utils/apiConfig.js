/**
 * API Configuration for different environments
 * Handles API endpoints for development, production, and GitHub Pages deployment
 */

const isDevelopment = import.meta.env.DEV;
const isGitHubPages = window.location.hostname.includes('github.io');

// API Base URLs for different environments
const API_CONFIGS = {
  development: {
    baseUrl: 'http://localhost:8000',
    mockMode: false
  },
  production: {
    baseUrl: process.env.VITE_API_BASE_URL || 'https://your-api-domain.com',
    mockMode: false
  },
  githubPages: {
    baseUrl: '', // No real backend on GitHub Pages
    mockMode: true // Use mock responses
  }
};

// Determine current configuration
const getCurrentConfig = () => {
  if (isDevelopment) {
    return API_CONFIGS.development;
  } else if (isGitHubPages) {
    return API_CONFIGS.githubPages;
  } else {
    return API_CONFIGS.production;
  }
};

const config = getCurrentConfig();

// Mock responses for GitHub Pages deployment
const MOCK_RESPONSES = {
  '/api/integrated-ai/analyze-comprehensive': {
    success: true,
    analysis: {
      nlp_analysis: {
        entities: [],
        sentiment: { positive: 0.7, negative: 0.1, neutral: 0.2 },
        readability_score: 75,
        legal_concepts: ['executor', 'beneficiary', 'assets'],
        complexity_score: 0.6,
        word_count: 150
      },
      legal_research: {
        search_query: 'will testament ontario',
        cases: [
          {
            title: 'Estate v. Beneficiary',
            citation: '2023 ONCA 123',
            relevance_score: 0.85
          }
        ],
        total_results: 1
      }
    },
    confidence_score: 0.85,
    compliance_score: 0.78,
    suggestions: [
      'Consider adding an alternate executor',
      'Specify what happens if a beneficiary predeceases you',
      'Include specific funeral instructions'
    ],
    improvements: [
      'Add witness signature requirements',
      'Include date and location of signing',
      'Consider tax implications of bequests'
    ],
    risk_assessment: {
      risk_factors: [
        {
          severity: 'medium',
          description: 'Missing alternate executor appointment'
        }
      ]
    },
    legal_citations: [
      {
        title: 'Succession Law Reform Act',
        citation: 'RSO 1990, c S.26',
        relevance: 'Primary legislation for wills in Ontario'
      }
    ],
    processing_time_ms: 150
  },
  '/api/integrated-ai/status': {
    status: 'operational',
    services: {
      initialized: true,
      nlp_service: true,
      research_service: true,
      ai_service: true
    },
    initialized: true,
    timestamp: new Date().toISOString()
  }
};

/**
 * Enhanced fetch function that handles API calls with mock responses
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<Response>} - Fetch response or mock response
 */
export const apiCall = async (endpoint, options = {}) => {
  const fullUrl = config.baseUrl + endpoint;
  
  if (config.mockMode) {
    // Return mock response for GitHub Pages
    const mockResponse = MOCK_RESPONSES[endpoint];
    if (mockResponse) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponse),
        status: 200,
        statusText: 'OK'
      });
    } else {
      // Return a generic success response for unmocked endpoints
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true, message: 'Mock response' }),
        status: 200,
        statusText: 'OK'
      });
    }
  }
  
  try {
    // Make actual API call
    const response = await fetch(fullUrl, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    return response;
  } catch (error) {
    console.error('API call failed:', error);
    
    // Fallback to mock response if available
    const mockResponse = MOCK_RESPONSES[endpoint];
    if (mockResponse) {
      console.log('Falling back to mock response');
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponse),
        status: 200,
        statusText: 'OK (Mock Fallback)'
      });
    }
    
    throw error;
  }
};

/**
 * Get API configuration information
 */
export const getApiConfig = () => ({
  ...config,
  environment: isDevelopment ? 'development' : (isGitHubPages ? 'githubPages' : 'production'),
  mockMode: config.mockMode
});

/**
 * Check if API is in mock mode
 */
export const isMockMode = () => config.mockMode;

/**
 * API endpoints object for easy reference
 */
export const API_ENDPOINTS = {
  ANALYZE_COMPREHENSIVE: '/api/integrated-ai/analyze-comprehensive',
  AI_STATUS: '/api/integrated-ai/status',
  AI_INITIALIZE: '/api/integrated-ai/initialize',
  ANALYZE_NLP_ONLY: '/api/integrated-ai/analyze-nlp-only',
  HEALTH_CHECK: '/api/integrated-ai/health'
};

export default {
  apiCall,
  getApiConfig,
  isMockMode,
  API_ENDPOINTS
};