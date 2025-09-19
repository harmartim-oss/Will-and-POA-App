import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Scale, FileText, ExternalLink, Filter, Clock, Star, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { ScrollArea } from '../ui/scroll-area';
import { Separator } from '../ui/separator';
import { Alert, AlertDescription } from '../ui/alert';

const LegalResearchPanel = ({ documentText, documentType, onCaseSelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [recentCases, setRecentCases] = useState([]);
  const [documentAnalysis, setDocumentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('search');
  const [selectedFilters, setSelectedFilters] = useState({
    jurisdiction: 'on',
    courtLevel: 'all',
    dateRange: 'all'
  });

  // Mock data for demonstration
  const mockCases = [
    {
      id: '2023onca456',
      title: 'Smith v. Estate of Johnson',
      citation: '2023 ONCA 456',
      court: 'Ontario Court of Appeal',
      date: '2023-08-15',
      relevanceScore: 0.92,
      summary: 'Court clarified requirements for valid will execution under Ontario law, particularly regarding witness requirements and mental capacity.',
      keywords: ['will execution', 'witness requirements', 'mental capacity'],
      url: 'https://canlii.ca/t/jxyz123'
    },
    {
      id: '2023onsc789',
      title: 'Brown v. Power of Attorney Services',
      citation: '2023 ONSC 789',
      court: 'Ontario Superior Court',
      date: '2023-06-22',
      relevanceScore: 0.88,
      summary: 'Decision regarding scope of powers under continuing power of attorney for property and fiduciary duties of attorneys.',
      keywords: ['power of attorney', 'fiduciary duty', 'property management'],
      url: 'https://canlii.ca/t/jxyz456'
    },
    {
      id: '2023oncj234',
      title: 'Re: Estate Planning Guidelines',
      citation: '2023 ONCJ 234',
      court: 'Ontario Court of Justice',
      date: '2023-04-10',
      relevanceScore: 0.85,
      summary: 'Comprehensive review of estate planning best practices and common pitfalls in document preparation.',
      keywords: ['estate planning', 'document preparation', 'best practices'],
      url: 'https://canlii.ca/t/jxyz789'
    }
  ];

  const mockLegislation = [
    {
      title: 'Succession Law Reform Act',
      citation: 'RSO 1990, c S.26',
      relevance: 'Primary legislation governing wills in Ontario',
      sections: ['s. 5 (Formal validity)', 's. 6 (Age requirements)', 's. 9 (Witnesses)']
    },
    {
      title: 'Substitute Decisions Act',
      citation: '1992, SO 1992, c 30',
      relevance: 'Governs powers of attorney in Ontario',
      sections: ['s. 8 (Continuing POA)', 's. 10 (Witness requirements)', 's. 32 (Personal care POA)']
    }
  ];

  useEffect(() => {
    // Load recent cases on component mount
    setRecentCases(mockCases);
  }, []);

  useEffect(() => {
    // Analyze document when text changes
    if (documentText && documentText.length > 100) {
      analyzeDocument();
    }
  }, [documentText, documentType]);

  const analyzeDocument = async () => {
    setLoading(true);
    try {
      // Simulate API call for document analysis
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setDocumentAnalysis({
        relevantCases: mockCases.slice(0, 2),
        relatedLegislation: mockLegislation,
        riskFactors: [
          'Consider adding specific instructions for digital assets',
          'Ensure witness requirements are clearly understood',
          'Review powers granted to attorneys for completeness'
        ],
        suggestions: [
          'Add clause for alternate executors',
          'Consider including funeral wishes',
          'Specify accounting requirements for attorneys'
        ]
      });
    } catch (error) {
      console.error('Error analyzing document:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Filter mock cases based on search query
      const filtered = mockCases.filter(case_ => 
        case_.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
        case_.keywords.some(keyword => keyword.toLowerCase().includes(searchQuery.toLowerCase()))
      );
      
      setSearchResults(filtered);
      setActiveTab('results');
    } catch (error) {
      console.error('Error searching cases:', error);
    } finally {
      setLoading(false);
    }
  };

  const CaseCard = ({ case_, showRelevance = false }) => (
    <Card className="mb-4 hover:shadow-md transition-shadow cursor-pointer" onClick={() => onCaseSelect?.(case_)}>
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold text-blue-900 hover:text-blue-700 transition-colors">
              {case_.title}
            </CardTitle>
            <CardDescription className="text-sm text-gray-600 mt-1">
              {case_.citation} • {case_.court} • {case_.date}
            </CardDescription>
          </div>
          {showRelevance && (
            <Badge variant="secondary" className="ml-2">
              {Math.round(case_.relevanceScore * 100)}% match
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-700 mb-3 leading-relaxed">
          {case_.summary}
        </p>
        <div className="flex flex-wrap gap-2 mb-3">
          {case_.keywords.map((keyword, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {keyword}
            </Badge>
          ))}
        </div>
        <div className="flex justify-between items-center">
          <Button variant="outline" size="sm" className="text-xs">
            <ExternalLink className="w-3 h-3 mr-1" />
            View on CanLII
          </Button>
          <Button variant="ghost" size="sm" className="text-xs">
            <Star className="w-3 h-3 mr-1" />
            Save Case
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  const LegislationCard = ({ legislation }) => (
    <Card className="mb-3">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-green-900">
          {legislation.title}
        </CardTitle>
        <CardDescription className="text-sm">
          {legislation.citation} • {legislation.relevance}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-1">
          {legislation.sections.map((section, index) => (
            <div key={index} className="text-sm text-gray-600 flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              {section}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
          <Scale className="w-8 h-8 mr-3 text-blue-600" />
          Legal Research Center
        </h2>
        <p className="text-gray-600">
          Find relevant cases, legislation, and legal authorities for your documents
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4 mb-6">
          <TabsTrigger value="search" className="flex items-center">
            <Search className="w-4 h-4 mr-2" />
            Search
          </TabsTrigger>
          <TabsTrigger value="analysis" className="flex items-center">
            <FileText className="w-4 h-4 mr-2" />
            Document Analysis
          </TabsTrigger>
          <TabsTrigger value="recent" className="flex items-center">
            <Clock className="w-4 h-4 mr-2" />
            Recent Cases
          </TabsTrigger>
          <TabsTrigger value="results" className="flex items-center">
            <BookOpen className="w-4 h-4 mr-2" />
            Results
          </TabsTrigger>
        </TabsList>

        <TabsContent value="search" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Search className="w-5 h-5 mr-2" />
                Case Search
              </CardTitle>
              <CardDescription>
                Search Ontario case law and legislation relevant to your document
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-2">
                <Input
                  placeholder="Search for cases, legal concepts, or keywords..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="flex-1"
                />
                <Button onClick={handleSearch} disabled={loading}>
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </div>
              
              <div className="flex space-x-4 text-sm">
                <div className="flex items-center space-x-2">
                  <Filter className="w-4 h-4" />
                  <span>Filters:</span>
                </div>
                <select 
                  value={selectedFilters.jurisdiction}
                  onChange={(e) => setSelectedFilters({...selectedFilters, jurisdiction: e.target.value})}
                  className="border rounded px-2 py-1"
                >
                  <option value="on">Ontario</option>
                  <option value="ca">Federal</option>
                </select>
                <select 
                  value={selectedFilters.courtLevel}
                  onChange={(e) => setSelectedFilters({...selectedFilters, courtLevel: e.target.value})}
                  className="border rounded px-2 py-1"
                >
                  <option value="all">All Courts</option>
                  <option value="appeal">Appeal Courts</option>
                  <option value="superior">Superior Courts</option>
                </select>
                <select 
                  value={selectedFilters.dateRange}
                  onChange={(e) => setSelectedFilters({...selectedFilters, dateRange: e.target.value})}
                  className="border rounded px-2 py-1"
                >
                  <option value="all">All Dates</option>
                  <option value="recent">Last 2 Years</option>
                  <option value="5years">Last 5 Years</option>
                </select>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Search Suggestions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {['will execution', 'power of attorney', 'mental capacity', 'witness requirements', 'estate planning', 'fiduciary duty'].map((suggestion) => (
                  <Button
                    key={suggestion}
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setSearchQuery(suggestion);
                      handleSearch();
                    }}
                    className="text-xs"
                  >
                    {suggestion}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-6">
          {documentText ? (
            <>
              {loading ? (
                <Card>
                  <CardContent className="flex items-center justify-center py-8">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                      <p>Analyzing your document...</p>
                    </div>
                  </CardContent>
                </Card>
              ) : documentAnalysis ? (
                <>
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2 text-amber-600" />
                        Risk Factors & Suggestions
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {documentAnalysis.riskFactors.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-amber-800 mb-2">Risk Factors:</h4>
                          {documentAnalysis.riskFactors.map((risk, index) => (
                            <Alert key={index} className="mb-2">
                              <AlertCircle className="h-4 w-4" />
                              <AlertDescription>{risk}</AlertDescription>
                            </Alert>
                          ))}
                        </div>
                      )}
                      
                      {documentAnalysis.suggestions.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-blue-800 mb-2">Suggestions:</h4>
                          <div className="space-y-2">
                            {documentAnalysis.suggestions.map((suggestion, index) => (
                              <div key={index} className="flex items-start space-x-2 p-2 bg-blue-50 rounded">
                                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                                <span className="text-sm">{suggestion}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Relevant Cases</CardTitle>
                      <CardDescription>
                        Cases identified as relevant to your document
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <ScrollArea className="h-96">
                        {documentAnalysis.relevantCases.map((case_, index) => (
                          <CaseCard key={index} case_={case_} showRelevance={true} />
                        ))}
                      </ScrollArea>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Related Legislation</CardTitle>
                    </CardHeader>
                    <CardContent>
                      {documentAnalysis.relatedLegislation.map((legislation, index) => (
                        <LegislationCard key={index} legislation={legislation} />
                      ))}
                    </CardContent>
                  </Card>
                </>
              ) : (
                <Card>
                  <CardContent className="text-center py-8">
                    <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">Click "Analyze Document" to get started</p>
                    <Button onClick={analyzeDocument} className="mt-4">
                      Analyze Document
                    </Button>
                  </CardContent>
                </Card>
              )}
            </>
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No document text available for analysis</p>
                <p className="text-sm text-gray-500 mt-2">
                  Create or edit a document to see relevant legal research
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="recent" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Ontario Cases</CardTitle>
              <CardDescription>
                Latest estate planning and power of attorney decisions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-96">
                {recentCases.map((case_, index) => (
                  <CaseCard key={index} case_={case_} />
                ))}
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="results" className="space-y-6">
          {searchResults.length > 0 ? (
            <Card>
              <CardHeader>
                <CardTitle>Search Results</CardTitle>
                <CardDescription>
                  Found {searchResults.length} cases matching "{searchQuery}"
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  {searchResults.map((case_, index) => (
                    <CaseCard key={index} case_={case_} showRelevance={true} />
                  ))}
                </ScrollArea>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No search results yet</p>
                <p className="text-sm text-gray-500 mt-2">
                  Use the search tab to find relevant cases and legislation
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LegalResearchPanel;

