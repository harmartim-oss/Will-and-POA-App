// Mock API responses for development
export const mockApiResponses = {
  '/api/ai/analyze': {
    success: true,
    analysis: {
      compliance_score: 0.85,
      legal_issues: ['Consider appointing alternate executor', 'Add witness requirements section'],
      recommendations: ['Include specific bequest instructions', 'Add guardian appointment clause'],
      confidence_score: 0.92,
      document_type: 'will',
      missing_requirements: ['Guardian appointment for minor children'],
      risk_factors: ['Unequal distributions may lead to family disputes'],
      case_law_references: ['Banks v. Goodfellow: Established the test for testamentary capacity'],
      improvement_suggestions: ['Add document creation date', 'Specify jurisdiction (Province of Ontario)']
    },
    insights: {
      summary: {
        compliance_score: 0.85,
        confidence_score: 0.92,
        total_issues: 2,
        total_recommendations: 4
      },
      compliance: {
        score: 0.85,
        issues: ['Missing alternate executor', 'Incomplete witness section'],
        missing_requirements: ['Guardian appointment for minor children']
      },
      recommendations: {
        priority_recommendations: [
          'Appoint an alternate executor for redundancy',
          'Complete witness signature requirements',
          'Add guardian appointment for minor children'
        ],
        all_recommendations: [
          'Include specific bequest instructions',
          'Add guardian appointment clause',
          'Consider tax planning strategies',
          'Ensure proper execution with witnesses'
        ],
        risk_factors: ['Previous marriages may create family law claims']
      },
      legal_research: {
        relevant_case_law: [
          'Banks v. Goodfellow: Established the test for testamentary capacity',
          'Vout v. Hay: Modern approach to suspicious circumstances in will challenges'
        ],
        legal_citations: [
          'Succession Law Reform Act, R.S.O. 1990, c. S.26',
          'Estates Act, R.S.O. 1990, c. E.21'
        ]
      },
      improvements: {
        suggestions: ['Add document creation date', 'Specify jurisdiction'],
        next_steps: [
          'Address legal compliance issues before proceeding',
          'Complete all required document sections',
          'Review document with legal professional'
        ]
      }
    }
  },
  
  '/api/documents/will/create': {
    success: true,
    document_id: 'will_' + Date.now(),
    document_path: '/tmp/generated_will.docx',
    format: 'docx',
    compliance_score: 0.92,
    ai_analysis: {
      compliance_score: 0.92,
      recommendations: ['Document looks comprehensive', 'Consider adding alternate executor']
    },
    generation_time: new Date().toISOString()
  },
  
  '/api/documents/poa/create': {
    success: true,
    document_id: 'poa_' + Date.now(),
    document_path: '/tmp/generated_poa.docx',
    format: 'docx',
    compliance_score: 0.88,
    ai_analysis: {
      compliance_score: 0.88,
      recommendations: ['POA document meets Ontario requirements', 'Consider adding specific powers']
    },
    generation_time: new Date().toISOString()
  }
};

// Mock fetch implementation for development
export const mockFetch = (url, options = {}) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const response = mockApiResponses[url];
      if (response) {
        resolve({
          ok: true,
          json: () => Promise.resolve(response)
        });
      } else {
        resolve({
          ok: false,
          status: 404,
          json: () => Promise.resolve({ error: 'Not found' })
        });
      }
    }, 1000 + Math.random() * 1000); // Simulate network delay
  });
};

// Replace global fetch in development
if (import.meta.env.DEV) {
  window.fetch = mockFetch;
}

export default mockApiResponses;