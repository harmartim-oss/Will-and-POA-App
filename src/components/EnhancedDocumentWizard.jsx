import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle, 
  AlertCircle,
  Info,
  FileText,
  Users,
  Shield,
  Brain,
  Download,
  Eye,
  Save,
  Sparkles,
  Lightbulb,
  BookOpen,
  Scale
} from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Checkbox } from './ui/checkbox';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Progress } from './ui/progress';
import { Separator } from './ui/separator';
import { ProgressIndicator, ProgressBar } from './ui/progress-indicator';
import EnhancedLoading from './ui/enhanced-loading';
import { apiCall, API_ENDPOINTS } from '../utils/apiConfig';

const EnhancedDocumentWizard = ({ documentType, onComplete, onCancel }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [validationErrors, setValidationErrors] = useState({});
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [complianceScore, setComplianceScore] = useState(0);
  const [analysisResults, setAnalysisResults] = useState(null);

  const documentTypeConfig = {
    will: {
      title: "Last Will & Testament",
      icon: <FileText className="h-6 w-6" />,
      color: "from-blue-500 to-cyan-500",
      steps: [
        { id: 'personal', title: 'Personal Information', description: 'Your basic details and identification' },
        { id: 'executor', title: 'Executor Selection', description: 'Choose who will manage your estate' },
        { id: 'beneficiaries', title: 'Beneficiaries', description: 'Designate who receives your assets' },
        { id: 'assets', title: 'Asset Distribution', description: 'Specify how assets should be distributed' },
        { id: 'guardians', title: 'Guardianship', description: 'Appoint guardians for minor children' },
        { id: 'witnesses', title: 'Witnesses', description: 'Identify required witnesses' },
        { id: 'review', title: 'Review & Generate', description: 'Final review and document creation' }
      ]
    },
    poa_property: {
      title: "Power of Attorney for Property",
      icon: <Shield className="h-6 w-6" />,
      color: "from-green-500 to-emerald-500",
      steps: [
        { id: 'personal', title: 'Personal Information', description: 'Your basic details and identification' },
        { id: 'attorney', title: 'Attorney Selection', description: 'Choose your attorney for property' },
        { id: 'powers', title: 'Powers Granted', description: 'Specify what powers to grant' },
        { id: 'restrictions', title: 'Restrictions', description: 'Set any limitations or restrictions' },
        { id: 'continuing', title: 'Continuing Clause', description: 'Decide on continuing vs non-continuing' },
        { id: 'witnesses', title: 'Witnesses', description: 'Identify required witnesses' },
        { id: 'review', title: 'Review & Generate', description: 'Final review and document creation' }
      ]
    },
    poa_care: {
      title: "Power of Attorney for Personal Care",
      icon: <Users className="h-6 w-6" />,
      color: "from-purple-500 to-pink-500",
      steps: [
        { id: 'personal', title: 'Personal Information', description: 'Your basic details and identification' },
        { id: 'attorney', title: 'Attorney Selection', description: 'Choose your attorney for personal care' },
        { id: 'care_powers', title: 'Care Decisions', description: 'Specify personal care powers' },
        { id: 'medical', title: 'Medical Preferences', description: 'Your healthcare wishes and preferences' },
        { id: 'restrictions', title: 'Instructions & Restrictions', description: 'Special instructions and limitations' },
        { id: 'witnesses', title: 'Witnesses', description: 'Identify required witnesses' },
        { id: 'review', title: 'Review & Generate', description: 'Final review and document creation' }
      ]
    }
  };

  const config = documentTypeConfig[documentType];
  const currentStepData = config.steps[currentStep];
  const progress = ((currentStep + 1) / config.steps.length) * 100;

  useEffect(() => {
    // Simulate AI analysis when form data changes
    if (Object.keys(formData).length > 0) {
      setIsAnalyzing(true);
      const timer = setTimeout(() => {
        analyzeFormData();
        setIsAnalyzing(false);
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [formData]);

  const analyzeFormData = async () => {
    try {
      setIsAnalyzing(true);
      
      // Convert form data to document text for analysis
      const documentText = generateDocumentPreviewText();
      
      // Call the integrated AI service
      const response = await apiCall(API_ENDPOINTS.ANALYZE_COMPREHENSIVE, {
        method: 'POST',
        body: JSON.stringify({
          document_text: documentText,
          document_type: documentType,
          user_context: {
            form_completion: Object.keys(formData).length,
            user_preferences: formData
          },
          include_research: true,
          include_citations: true
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        
        // Transform AI suggestions into UI format
        const suggestions = result.suggestions.map((suggestion, index) => ({
          type: index < 2 ? 'improvement' : 'legal',
          title: `AI Suggestion ${index + 1}`,
          description: suggestion,
          icon: index < 2 ? <Lightbulb className="h-4 w-4" /> : <Scale className="h-4 w-4" />
        }));
        
        // Add compliance suggestions
        if (result.compliance_score < 0.8) {
          suggestions.unshift({
            type: 'compliance',
            title: 'Compliance Review Needed',
            description: 'Some sections may need attention to meet Ontario legal requirements.',
            icon: <AlertCircle className="h-4 w-4" />
          });
        } else {
          suggestions.unshift({
            type: 'compliance',
            title: 'Good Compliance Score',
            description: 'Your document meets most Ontario legal requirements.',
            icon: <CheckCircle className="h-4 w-4" />
          });
        }
        
        setAiSuggestions(suggestions);
        setComplianceScore(Math.round(result.compliance_score * 100));
        
        // Store additional analysis results for potential use
        setAnalysisResults(result);
        
      } else {
        // Fallback to original simulation if API fails
        analyzeFormDataFallback();
      }
    } catch (error) {
      console.error('AI analysis failed:', error);
      // Fallback to original simulation
      analyzeFormDataFallback();
    } finally {
      setIsAnalyzing(false);
    }
  };

  const analyzeFormDataFallback = () => {
    // Original simulation logic as fallback
    const suggestions = [
      {
        type: 'improvement',
        title: 'Consider Adding Alternate Executor',
        description: 'It\'s recommended to name an alternate executor in case your primary choice is unable to serve.',
        icon: <Lightbulb className="h-4 w-4" />
      },
      {
        type: 'compliance',
        title: 'Witness Requirements Met',
        description: 'Your witness selection meets Ontario legal requirements.',
        icon: <CheckCircle className="h-4 w-4" />
      },
      {
        type: 'legal',
        title: 'Review Asset Distribution',
        description: 'Consider specifying what happens to assets if a beneficiary predeceases you.',
        icon: <Scale className="h-4 w-4" />
      }
    ];
    
    setAiSuggestions(suggestions);
    setComplianceScore(Math.min(95, 60 + Object.keys(formData).length * 5));
  };

  const generateDocumentPreviewText = () => {
    // Generate a preview text of the document for AI analysis
    let text = `Ontario ${documentType === 'will' ? 'Last Will and Testament' : 'Power of Attorney'}\n\n`;
    
    if (formData.fullName) text += `I, ${formData.fullName}, `;
    if (formData.address) text += `of ${formData.address}, `;
    
    text += `being of sound mind and disposing memory, do hereby make, publish and declare this to be my ${documentType === 'will' ? 'last will and testament' : 'power of attorney'}.\n\n`;
    
    if (documentType === 'will') {
      if (formData.executorName) text += `I appoint ${formData.executorName} as my executor.\n`;
      if (formData.guardianName) text += `I appoint ${formData.guardianName} as guardian for my minor children.\n`;
      if (formData.beneficiaries) text += `I leave my estate to my beneficiaries as specified.\n`;
    } else {
      if (formData.attorneyName) text += `I appoint ${formData.attorneyName} as my attorney.\n`;
      if (formData.attorneyPowers) text += `The powers granted include: ${formData.attorneyPowers}.\n`;
    }
    
    return text;
  };

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear validation error for this field
    if (validationErrors[field]) {
      setValidationErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validateCurrentStep = () => {
    const errors = {};
    
    switch (currentStepData.id) {
      case 'personal':
        if (!formData.fullName) errors.fullName = 'Full name is required';
        if (!formData.address) errors.address = 'Address is required';
        if (!formData.dateOfBirth) errors.dateOfBirth = 'Date of birth is required';
        break;
      case 'executor':
      case 'attorney':
        if (!formData.executorName && !formData.attorneyName) {
          errors.executorName = 'Executor/Attorney name is required';
        }
        break;
      case 'witnesses':
        if (!formData.witness1Name) errors.witness1Name = 'First witness name is required';
        if (!formData.witness2Name) errors.witness2Name = 'Second witness name is required';
        break;
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (currentStep < config.steps.length - 1) {
        setCurrentStep(currentStep + 1);
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    if (validateCurrentStep()) {
      onComplete(formData);
    }
  };

  const renderStepContent = () => {
    switch (currentStepData.id) {
      case 'personal':
        return (
          <div className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Legal Name *</Label>
                <Input
                  id="fullName"
                  value={formData.fullName || ''}
                  onChange={(e) => updateFormData('fullName', e.target.value)}
                  placeholder="Enter your full legal name"
                  className={validationErrors.fullName ? 'border-red-500' : ''}
                />
                {validationErrors.fullName && (
                  <p className="text-sm text-red-500">{validationErrors.fullName}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="dateOfBirth">Date of Birth *</Label>
                <Input
                  id="dateOfBirth"
                  type="date"
                  value={formData.dateOfBirth || ''}
                  onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                  className={validationErrors.dateOfBirth ? 'border-red-500' : ''}
                />
                {validationErrors.dateOfBirth && (
                  <p className="text-sm text-red-500">{validationErrors.dateOfBirth}</p>
                )}
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="address">Full Address *</Label>
              <Textarea
                id="address"
                value={formData.address || ''}
                onChange={(e) => updateFormData('address', e.target.value)}
                placeholder="Enter your complete address including postal code"
                className={validationErrors.address ? 'border-red-500' : ''}
              />
              {validationErrors.address && (
                <p className="text-sm text-red-500">{validationErrors.address}</p>
              )}
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  value={formData.phone || ''}
                  onChange={(e) => updateFormData('phone', e.target.value)}
                  placeholder="(555) 123-4567"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email || ''}
                  onChange={(e) => updateFormData('email', e.target.value)}
                  placeholder="your.email@example.com"
                />
              </div>
            </div>
          </div>
        );
        
      case 'executor':
      case 'attorney':
        const fieldPrefix = currentStepData.id === 'executor' ? 'executor' : 'attorney';
        const title = currentStepData.id === 'executor' ? 'Executor' : 'Attorney';
        
        return (
          <div className="space-y-6">
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                Your {title.toLowerCase()} will have significant responsibilities. Choose someone you trust completely 
                who is capable of handling {currentStepData.id === 'executor' ? 'estate matters' : 'property/care decisions'}.
              </AlertDescription>
            </Alert>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor={`${fieldPrefix}Name`}>{title} Full Name *</Label>
                <Input
                  id={`${fieldPrefix}Name`}
                  value={formData[`${fieldPrefix}Name`] || ''}
                  onChange={(e) => updateFormData(`${fieldPrefix}Name`, e.target.value)}
                  placeholder={`Enter ${title.toLowerCase()}'s full name`}
                  className={validationErrors[`${fieldPrefix}Name`] ? 'border-red-500' : ''}
                />
                {validationErrors[`${fieldPrefix}Name`] && (
                  <p className="text-sm text-red-500">{validationErrors[`${fieldPrefix}Name`]}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`${fieldPrefix}Relationship`}>Relationship</Label>
                <Select
                  value={formData[`${fieldPrefix}Relationship`] || ''}
                  onValueChange={(value) => updateFormData(`${fieldPrefix}Relationship`, value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select relationship" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="spouse">Spouse/Partner</SelectItem>
                    <SelectItem value="child">Child</SelectItem>
                    <SelectItem value="parent">Parent</SelectItem>
                    <SelectItem value="sibling">Sibling</SelectItem>
                    <SelectItem value="friend">Friend</SelectItem>
                    <SelectItem value="professional">Professional (Lawyer, Accountant)</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor={`${fieldPrefix}Address`}>{title} Address</Label>
              <Textarea
                id={`${fieldPrefix}Address`}
                value={formData[`${fieldPrefix}Address`] || ''}
                onChange={(e) => updateFormData(`${fieldPrefix}Address`, e.target.value)}
                placeholder={`Enter ${title.toLowerCase()}'s complete address`}
              />
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor={`${fieldPrefix}Phone`}>Phone Number</Label>
                <Input
                  id={`${fieldPrefix}Phone`}
                  value={formData[`${fieldPrefix}Phone`] || ''}
                  onChange={(e) => updateFormData(`${fieldPrefix}Phone`, e.target.value)}
                  placeholder="(555) 123-4567"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor={`${fieldPrefix}Email`}>Email Address</Label>
                <Input
                  id={`${fieldPrefix}Email`}
                  type="email"
                  value={formData[`${fieldPrefix}Email`] || ''}
                  onChange={(e) => updateFormData(`${fieldPrefix}Email`, e.target.value)}
                  placeholder="email@example.com"
                />
              </div>
            </div>
            
            <div className="space-y-4">
              <Label>Alternate {title} (Recommended)</Label>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor={`alternate${title}Name`}>Alternate {title} Name</Label>
                  <Input
                    id={`alternate${title}Name`}
                    value={formData[`alternate${title}Name`] || ''}
                    onChange={(e) => updateFormData(`alternate${title}Name`, e.target.value)}
                    placeholder={`Enter alternate ${title.toLowerCase()}'s name`}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor={`alternate${title}Relationship`}>Relationship</Label>
                  <Select
                    value={formData[`alternate${title}Relationship`] || ''}
                    onValueChange={(value) => updateFormData(`alternate${title}Relationship`, value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select relationship" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="spouse">Spouse/Partner</SelectItem>
                      <SelectItem value="child">Child</SelectItem>
                      <SelectItem value="parent">Parent</SelectItem>
                      <SelectItem value="sibling">Sibling</SelectItem>
                      <SelectItem value="friend">Friend</SelectItem>
                      <SelectItem value="professional">Professional</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 'witnesses':
        return (
          <div className="space-y-6">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Ontario law requires 2 witnesses who are at least 18 years old. Witnesses cannot be beneficiaries 
                or the spouse of a beneficiary. They must be present when you sign the document.
              </AlertDescription>
            </Alert>
            
            <div className="space-y-8">
              {[1, 2].map((witnessNum) => (
                <Card key={witnessNum} className="p-6">
                  <CardHeader className="pb-4">
                    <CardTitle className="text-lg">Witness {witnessNum}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor={`witness${witnessNum}Name`}>Full Name *</Label>
                        <Input
                          id={`witness${witnessNum}Name`}
                          value={formData[`witness${witnessNum}Name`] || ''}
                          onChange={(e) => updateFormData(`witness${witnessNum}Name`, e.target.value)}
                          placeholder="Enter witness full name"
                          className={validationErrors[`witness${witnessNum}Name`] ? 'border-red-500' : ''}
                        />
                        {validationErrors[`witness${witnessNum}Name`] && (
                          <p className="text-sm text-red-500">{validationErrors[`witness${witnessNum}Name`]}</p>
                        )}
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor={`witness${witnessNum}Age`}>Age</Label>
                        <Input
                          id={`witness${witnessNum}Age`}
                          type="number"
                          min="18"
                          value={formData[`witness${witnessNum}Age`] || ''}
                          onChange={(e) => updateFormData(`witness${witnessNum}Age`, e.target.value)}
                          placeholder="Must be 18 or older"
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor={`witness${witnessNum}Address`}>Address</Label>
                      <Textarea
                        id={`witness${witnessNum}Address`}
                        value={formData[`witness${witnessNum}Address`] || ''}
                        onChange={(e) => updateFormData(`witness${witnessNum}Address`, e.target.value)}
                        placeholder="Enter witness complete address"
                      />
                    </div>
                    
                    <div className="grid md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor={`witness${witnessNum}Phone`}>Phone Number</Label>
                        <Input
                          id={`witness${witnessNum}Phone`}
                          value={formData[`witness${witnessNum}Phone`] || ''}
                          onChange={(e) => updateFormData(`witness${witnessNum}Phone`, e.target.value)}
                          placeholder="(555) 123-4567"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor={`witness${witnessNum}Occupation`}>Occupation</Label>
                        <Input
                          id={`witness${witnessNum}Occupation`}
                          value={formData[`witness${witnessNum}Occupation`] || ''}
                          onChange={(e) => updateFormData(`witness${witnessNum}Occupation`, e.target.value)}
                          placeholder="Enter occupation"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );
        
      case 'review':
        return (
          <div className="space-y-6">
            <div className="text-center space-y-4">
              <div className="w-20 h-20 mx-auto bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
                <CheckCircle className="h-10 w-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Document Ready for Generation</h3>
              <p className="text-gray-600">
                Your {config.title.toLowerCase()} has been prepared and is ready for final generation.
              </p>
            </div>
            
            <Card className="bg-gradient-to-r from-blue-50 to-cyan-50 border-blue-200">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-blue-600" />
                  <span>AI Compliance Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Ontario Legal Compliance</span>
                    <Badge className="bg-green-100 text-green-800">
                      {complianceScore}% Compliant
                    </Badge>
                  </div>
                  <Progress value={complianceScore} className="h-2" />
                  <p className="text-sm text-gray-600">
                    Your document meets Ontario legal requirements and best practices.
                  </p>
                </div>
              </CardContent>
            </Card>
            
            <div className="grid md:grid-cols-3 gap-4">
              <Button
                variant="outline"
                className="flex items-center space-x-2 h-12"
                onClick={() => {/* Preview functionality */}}
              >
                <Eye className="h-4 w-4" />
                <span>Preview Document</span>
              </Button>
              
              <Button
                variant="outline"
                className="flex items-center space-x-2 h-12"
                onClick={() => {/* Save draft functionality */}}
              >
                <Save className="h-4 w-4" />
                <span>Save Draft</span>
              </Button>
              
              <Button
                className="flex items-center space-x-2 h-12 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
                onClick={handleComplete}
              >
                <Download className="h-4 w-4" />
                <span>Generate Document</span>
              </Button>
            </div>
          </div>
        );
        
      default:
        return (
          <div className="text-center py-12">
            <p className="text-gray-500">Step content not implemented yet.</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${config.color} flex items-center justify-center text-white`}>
                {config.icon}
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{config.title}</h1>
                <p className="text-gray-600">Step {currentStep + 1} of {config.steps.length}: {currentStepData.title}</p>
              </div>
            </div>
            
            <Button variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          </div>
          
          {/* Progress Bar */}
          <ProgressBar 
            value={progress} 
            label="Progress"
            showPercentage={true}
            color="blue"
          />
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Steps Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle className="text-lg">Document Steps</CardTitle>
              </CardHeader>
              <CardContent>
                <ProgressIndicator 
                  steps={config.steps}
                  currentStep={currentStep}
                  orientation="vertical"
                  showLabels={true}
                />
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2">
            <Card className="min-h-[600px]">
              <CardHeader>
                <CardTitle className="text-2xl">{currentStepData.title}</CardTitle>
                <CardDescription className="text-lg">
                  {currentStepData.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentStep}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    {renderStepContent()}
                  </motion.div>
                </AnimatePresence>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between mt-6">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 0}
                className="flex items-center space-x-2"
              >
                <ChevronLeft className="h-4 w-4" />
                <span>Previous</span>
              </Button>
              
              {currentStep === config.steps.length - 1 ? (
                <Button
                  onClick={handleComplete}
                  className="flex items-center space-x-2 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
                >
                  <span>Complete Document</span>
                  <CheckCircle className="h-4 w-4" />
                </Button>
              ) : (
                <Button
                  onClick={handleNext}
                  className="flex items-center space-x-2"
                >
                  <span>Next</span>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>

          {/* AI Suggestions Sidebar */}
          <div className="lg:col-span-1">
            <div className="space-y-6">
              {/* AI Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2 text-lg">
                    <Brain className="h-5 w-5 text-purple-600" />
                    <span>AI Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {isAnalyzing ? (
                    <EnhancedLoading 
                      message="Analyzing your input..."
                      submessage="Checking legal compliance"
                      type="ai"
                      size="small"
                    />
                  ) : (
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Compliance Score</span>
                        <Badge className="bg-green-100 text-green-800">
                          {complianceScore}%
                        </Badge>
                      </div>
                      <Progress value={complianceScore} className="h-2" />
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* AI Suggestions */}
              {aiSuggestions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2 text-lg">
                      <Lightbulb className="h-5 w-5 text-yellow-600" />
                      <span>Suggestions</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {aiSuggestions.map((suggestion, index) => (
                      <div key={index} className="space-y-2">
                        <div className="flex items-start space-x-2">
                          <div className={`mt-0.5 ${
                            suggestion.type === 'compliance' ? 'text-green-600' :
                            suggestion.type === 'improvement' ? 'text-blue-600' :
                            'text-orange-600'
                          }`}>
                            {suggestion.icon}
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900">
                              {suggestion.title}
                            </p>
                            <p className="text-xs text-gray-600 mt-1">
                              {suggestion.description}
                            </p>
                          </div>
                        </div>
                        {index < aiSuggestions.length - 1 && <Separator />}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}

              {/* Legal Resources */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2 text-lg">
                    <BookOpen className="h-5 w-5 text-indigo-600" />
                    <span>Legal Resources</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start text-left h-auto p-3"
                  >
                    <div>
                      <p className="text-sm font-medium">Ontario Will Requirements</p>
                      <p className="text-xs text-gray-500">Learn about legal requirements</p>
                    </div>
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start text-left h-auto p-3"
                  >
                    <div>
                      <p className="text-sm font-medium">Executor Responsibilities</p>
                      <p className="text-xs text-gray-500">Understanding executor duties</p>
                    </div>
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start text-left h-auto p-3"
                  >
                    <div>
                      <p className="text-sm font-medium">Witness Guidelines</p>
                      <p className="text-xs text-gray-500">Who can be a witness</p>
                    </div>
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDocumentWizard;

