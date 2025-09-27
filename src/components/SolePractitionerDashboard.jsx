import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Users, 
  FileText, 
  DollarSign, 
  Clock, 
  AlertTriangle,
  TrendingUp,
  Calendar,
  Search,
  Plus,
  CheckCircle
} from 'lucide-react';

const SolePractitionerDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [caseLawQuery, setCaseLawQuery] = useState('');
  const [caseLawResults, setCaseLawResults] = useState([]);
  const [complianceCheck, setComplianceCheck] = useState({
    document_type: 'will',
    content: {}
  });
  const [complianceResults, setComplianceResults] = useState(null);

  // Mock API base URL (use environment variable in production)
  const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/sole-practitioner/dashboard`);
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data.data);
      } else {
        // Use mock data if API not available
        setDashboardData({
          active_matters: 12,
          total_clients: 35,
          unbilled_amount: 8750.50,
          overdue_tasks: 3,
          monthly_revenue: 15425.00,
          lawyer_name: "John Doe, Barrister & Solicitor",
          law_society_number: "12345P",
          last_updated: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('Dashboard fetch error:', error);
      // Use mock data on error
      setDashboardData({
        active_matters: 12,
        total_clients: 35,
        unbilled_amount: 8750.50,
        overdue_tasks: 3,
        monthly_revenue: 15425.00,
        lawyer_name: "John Doe, Barrister & Solicitor",
        law_society_number: "12345P",
        last_updated: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  const searchCaseLaw = async () => {
    if (!caseLawQuery.trim()) return;
    
    try {
      const response = await fetch(`${API_BASE}/api/sole-practitioner/legal/case-law/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: caseLawQuery,
          category: 'wills_interpretation'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setCaseLawResults(data.case_results || []);
      } else {
        // Mock results for demo
        setCaseLawResults([
          {
            case_name: "Banks v. Goodfellow",
            year: 1870,
            court: "Court of Appeal",
            citation: "(1870) LR 5 QB 549",
            key_principles: ["Testamentary capacity", "Sound disposing mind"],
            legal_test: "Test for testamentary capacity",
            outcome: "Established capacity requirements"
          },
          {
            case_name: "Vout v. Hay",
            year: 1995,
            court: "Supreme Court of Canada",
            citation: "[1995] 2 S.C.R. 876",
            key_principles: ["Suspicious circumstances", "Will challenges"],
            legal_test: "Modern approach to suspicious circumstances",
            outcome: "Updated burden of proof standards"
          }
        ]);
      }
    } catch (error) {
      console.error('Case law search error:', error);
      // Mock results on error
      setCaseLawResults([
        {
          case_name: "Banks v. Goodfellow",
          year: 1870,
          court: "Court of Appeal",
          citation: "(1870) LR 5 QB 549",
          key_principles: ["Testamentary capacity", "Sound disposing mind"],
          legal_test: "Test for testamentary capacity",
          outcome: "Established capacity requirements"
        }
      ]);
    }
  };

  const checkCompliance = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/sole-practitioner/legal/compliance/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(complianceCheck)
      });
      
      if (response.ok) {
        const data = await response.json();
        setComplianceResults(data);
      } else {
        // Mock compliance results
        setComplianceResults({
          compliance_score: 0.85,
          compliance_issues: [
            {
              type: "execution",
              severity: "critical",
              description: "Missing testator signature",
              requirement: "Will must be signed by testator",
              fix: "Add testator signature"
            }
          ],
          summary: {
            total_issues: 1,
            critical_issues: 1,
            major_issues: 0,
            is_compliant: false
          }
        });
      }
    } catch (error) {
      console.error('Compliance check error:', error);
      // Mock results on error
      setComplianceResults({
        compliance_score: 0.85,
        compliance_issues: [
          {
            type: "execution",
            severity: "critical",
            description: "Missing testator signature",
            requirement: "Will must be signed by testator",
            fix: "Add testator signature"
          }
        ],
        summary: {
          total_issues: 1,
          critical_issues: 1,
          major_issues: 0,
          is_compliant: false
        }
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <FileText className="h-8 w-8 text-blue-600" />
            Ontario Solo Practice Management
          </h1>
          <p className="text-gray-600 mt-2">
            {dashboardData?.lawyer_name} - Law Society #{dashboardData?.law_society_number}
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="case-law">Case Law Search</TabsTrigger>
            <TabsTrigger value="compliance">Compliance Check</TabsTrigger>
            <TabsTrigger value="documents">Document Generator</TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Matters</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData?.active_matters}</div>
                  <p className="text-xs text-muted-foreground">
                    Ongoing legal matters
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Clients</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData?.total_clients}</div>
                  <p className="text-xs text-muted-foreground">
                    Active client relationships
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Unbilled Amount</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    ${dashboardData?.unbilled_amount?.toLocaleString('en-CA', { minimumFractionDigits: 2 })}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Ready to invoice
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Overdue Tasks</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">{dashboardData?.overdue_tasks}</div>
                  <p className="text-xs text-muted-foreground">
                    Require immediate attention
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Monthly Revenue</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    ${dashboardData?.monthly_revenue?.toLocaleString('en-CA', { minimumFractionDigits: 2 })}
                  </div>
                  <div className="flex items-center text-sm text-muted-foreground">
                    <TrendingUp className="h-4 w-4 mr-1" />
                    Current month earnings
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button className="w-full justify-start">
                    <Plus className="h-4 w-4 mr-2" />
                    Create New Matter
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Users className="h-4 w-4 mr-2" />
                    Add New Client
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Clock className="h-4 w-4 mr-2" />
                    Log Time Entry
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <DollarSign className="h-4 w-4 mr-2" />
                    Generate Invoice
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Case Law Search Tab */}
          <TabsContent value="case-law" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Ontario Case Law Search</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="Search case law (e.g., testamentary capacity, undue influence)"
                    value={caseLawQuery}
                    onChange={(e) => setCaseLawQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && searchCaseLaw()}
                  />
                  <Button onClick={searchCaseLaw}>
                    <Search className="h-4 w-4 mr-2" />
                    Search
                  </Button>
                </div>

                {caseLawResults.length > 0 && (
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Search Results ({caseLawResults.length})</h3>
                    {caseLawResults.map((case_law, index) => (
                      <Card key={index} className="border-l-4 border-l-blue-600">
                        <CardContent className="pt-4">
                          <div className="space-y-2">
                            <div className="flex justify-between items-start">
                              <h4 className="font-semibold text-lg">{case_law.case_name}</h4>
                              <Badge variant="secondary">{case_law.year}</Badge>
                            </div>
                            <p className="text-sm text-muted-foreground">
                              {case_law.court} - {case_law.citation}
                            </p>
                            <div className="space-y-1">
                              <p className="text-sm"><strong>Legal Test:</strong> {case_law.legal_test}</p>
                              <p className="text-sm"><strong>Key Principles:</strong></p>
                              <ul className="list-disc list-inside text-sm text-muted-foreground">
                                {case_law.key_principles.map((principle, i) => (
                                  <li key={i}>{principle}</li>
                                ))}
                              </ul>
                              <p className="text-sm"><strong>Outcome:</strong> {case_law.outcome}</p>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Compliance Check Tab */}
          <TabsContent value="compliance" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Document Compliance Checker</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="document-type">Document Type</Label>
                  <select
                    id="document-type"
                    className="w-full mt-1 p-2 border rounded-md"
                    value={complianceCheck.document_type}
                    onChange={(e) => setComplianceCheck({
                      ...complianceCheck,
                      document_type: e.target.value
                    })}
                  >
                    <option value="will">Will</option>
                    <option value="poa_property">Power of Attorney for Property</option>
                    <option value="poa_personal_care">Power of Attorney for Personal Care</option>
                  </select>
                </div>

                <Button onClick={checkCompliance}>
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Check Compliance
                </Button>

                {complianceResults && (
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <div className="text-2xl font-bold">
                        Compliance Score: {Math.round(complianceResults.compliance_score * 100)}%
                      </div>
                      <Badge variant={complianceResults.summary.is_compliant ? "success" : "destructive"}>
                        {complianceResults.summary.is_compliant ? "Compliant" : "Issues Found"}
                      </Badge>
                    </div>

                    {complianceResults.compliance_issues.length > 0 && (
                      <div>
                        <h4 className="font-semibold mb-2">Compliance Issues:</h4>
                        <div className="space-y-2">
                          {complianceResults.compliance_issues.map((issue, index) => (
                            <Card key={index} className="border-l-4 border-l-red-500">
                              <CardContent className="pt-4">
                                <div className="space-y-1">
                                  <div className="flex justify-between items-start">
                                    <p className="font-medium">{issue.description}</p>
                                    <Badge variant={issue.severity === 'critical' ? 'destructive' : 'secondary'}>
                                      {issue.severity}
                                    </Badge>
                                  </div>
                                  <p className="text-sm text-muted-foreground">
                                    <strong>Requirement:</strong> {issue.requirement}
                                  </p>
                                  <p className="text-sm text-green-700">
                                    <strong>Fix:</strong> {issue.fix}
                                  </p>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Document Generator Tab */}
          <TabsContent value="documents" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Professional Document Generator</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card className="border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer transition-colors">
                    <CardContent className="p-6 text-center">
                      <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                      <h3 className="font-semibold mb-2">Generate Will</h3>
                      <p className="text-sm text-muted-foreground">
                        Create professional Ontario will documents with AI assistance
                      </p>
                    </CardContent>
                  </Card>

                  <Card className="border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer transition-colors">
                    <CardContent className="p-6 text-center">
                      <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                      <h3 className="font-semibold mb-2">POA for Property</h3>
                      <p className="text-sm text-muted-foreground">
                        Generate Power of Attorney for Property documents
                      </p>
                    </CardContent>
                  </Card>

                  <Card className="border-2 border-dashed border-gray-300 hover:border-blue-500 cursor-pointer transition-colors">
                    <CardContent className="p-6 text-center">
                      <FileText className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                      <h3 className="font-semibold mb-2">POA for Personal Care</h3>
                      <p className="text-sm text-muted-foreground">
                        Create Power of Attorney for Personal Care documents
                      </p>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default SolePractitionerDashboard;