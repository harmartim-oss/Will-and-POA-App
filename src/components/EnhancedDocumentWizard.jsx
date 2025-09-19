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
  Scale,
  HelpCircle
} from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Checkbox } from '../ui/checkbox';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { Progress } from '../ui/progress';
import { Separator } from '../ui/separator';
import { Stepper } from '../ui/stepper';
import { ActionBar } from '../ui/action-bar';
import { SectionHeading } from '../ui/section-heading';
import { FormField, FormGroup, FormError, FormHelp, FormLabel } from '../ui/form-field';
import PageHeader from '../layout/PageHeader';

const EnhancedDocumentWizard = ({ documentType, onComplete, onCancel }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [validationErrors, setValidationErrors] = useState({});
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [complianceScore, setComplianceScore] = useState(0);
  const [helpPanelOpen, setHelpPanelOpen] = useState(false);

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

  const analyzeFormData = () => {
    // Simulate AI analysis and suggestions
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
          <div className="space-y-8">
            <SectionHeading
              title="Personal Details"
              description="Please provide your personal information as it will appear in the legal document."
              level={3}
            />
            
            <FormGroup layout="horizontal">
              <FormField>
                <FormLabel htmlFor="fullName" required>
                  Full Legal Name
                </FormLabel>
                <Input
                  id="fullName"
                  value={formData.fullName || ''}
                  onChange={(e) => updateFormData('fullName', e.target.value)}
                  placeholder="Enter your full legal name"
                />
                <FormError>{validationErrors.fullName}</FormError>
                <FormHelp>
                  Use your name exactly as it appears on government identification
                </FormHelp>
              </FormField>
              
              <FormField>
                <FormLabel htmlFor="dateOfBirth" required>
                  Date of Birth
                </FormLabel>
                <Input
                  id="dateOfBirth"
                  type="date"
                  value={formData.dateOfBirth || ''}
                  onChange={(e) => updateFormData('dateOfBirth', e.target.value)}
                />
                <FormError>{validationErrors.dateOfBirth}</FormError>
                <FormHelp>
                  You must be at least 18 years old to create a will
                </FormHelp>
              </FormField>
            </FormGroup>
            
            <FormField>
              <FormLabel htmlFor="address" required>
                Complete Address
              </FormLabel>
              <Textarea
                id="address"
                value={formData.address || ''}
                onChange={(e) => updateFormData('address', e.target.value)}
                placeholder="Enter your complete address including postal code"
                rows={3}
              />
              <FormError>{validationErrors.address}</FormError>
              <FormHelp>
                Include street address, city, province, and postal code
              </FormHelp>
            </FormField>
            
            <FormGroup layout="horizontal">
              <FormField>
                <FormLabel htmlFor="phone">
                  Phone Number
                </FormLabel>
                <Input
                  id="phone"
                  value={formData.phone || ''}
                  onChange={(e) => updateFormData('phone', e.target.value)}
                  placeholder="(555) 123-4567"
                />
                <FormHelp>
                  Optional but recommended for contact purposes
                </FormHelp>
              </FormField>
              
              <FormField>
                <FormLabel htmlFor="email">
                  Email Address
                </FormLabel>
                <Input
                  id="email"
                  type="email"
                  value={formData.email || ''}
                  onChange={(e) => updateFormData('email', e.target.value)}
                  placeholder="your.email@example.com"
                />
                <FormHelp>
                  Optional but useful for document delivery
                </FormHelp>
              </FormField>
            </FormGroup>
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

  // Helper functions for contextual help
  const getStepHelp = (stepId) => {
    const helpContent = {
      personal: "Provide your complete legal name as it appears on official documents. This information will be used throughout your legal document.",
      executor: "Choose someone you trust completely to manage your estate. They should be organized, responsible, and willing to take on this important role.",
      beneficiaries: "List everyone who should receive something from your estate. Be specific about what each person should receive.",
      assets: "Detail how you want your assets distributed. Consider both monetary and sentimental items.",
      guardians: "If you have minor children, designate who should care for them. This is one of the most important decisions in your will.",
      attorney: "Select someone you trust to make decisions on your behalf. They should understand your values and preferences.",
      powers: "Carefully consider what authority you want to grant. You can be as specific or general as needed.",
      restrictions: "Set any limitations on the powers you're granting. This helps protect your interests.",
      witnesses: "Witnesses must be present when you sign your document and must also sign it themselves.",
      review: "Carefully review all information before generating your final document."
    };
    return helpContent[stepId] || "Complete this step to continue with your document creation.";
  };

  const getStepTips = (stepId) => {
    const tips = {
      personal: [
        "Use your full legal name exactly as it appears on government ID",
        "Include middle names or initials if they're part of your legal name",
        "Ensure your address is current and complete"
      ],
      executor: [
        "Choose someone younger than you who lives nearby",
        "Consider naming an alternate executor",
        "Discuss the role with them before naming them"
      ],
      beneficiaries: [
        "Be specific about percentages or amounts",
        "Consider what happens if a beneficiary predeceases you",
        "Think about both family and charitable beneficiaries"
      ],
      witnesses: [
        "Witnesses must be at least 18 years old",
        "They cannot be beneficiaries in your will",
        "They must be present when you sign"
      ]
    };
    return tips[stepId] || ["Follow the prompts to complete this step"];
  };

  const getLegalRequirements = (stepId) => {
    const requirements = {
      personal: [
        "Must be at least 18 years old",
        "Must be of sound mind",
        "Must provide complete legal name"
      ],
      executor: [
        "Must be at least 18 years old",
        "Should be mentally capable",
        "Cannot be bankrupt"
      ],
      witnesses: [
        "Requires exactly two witnesses",
        "Witnesses must be at least 18",
        "Cannot be beneficiaries",
        "Must sign in presence of testator"
      ],
      attorney: [
        "Must be at least 18 years old",
        "Should be mentally capable",
        "Must consent to the appointment"
      ]
    };
    return requirements[stepId] || ["Ensure all information is complete and accurate"];
  };

  return (
    <div className="space-y-6">
      {/* Page Header with Progress */}
      <PageHeader
        title={config.title}
        description={`Step ${currentStep + 1} of ${config.steps.length}: ${currentStepData.title}`}
        breadcrumbs={[
          { label: 'Home', href: '/' },
          { label: 'Documents', href: '/create/will' },
          { label: config.title }
        ]}
        actions={
          <ActionBar>
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setHelpPanelOpen(!helpPanelOpen)}
            >
              <HelpCircle className="h-4 w-4 mr-2" />
              Help
            </Button>
            <Button variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          </ActionBar>
        }
      >
        {/* Progress indicator */}
        <div className="mt-4 space-y-3">
          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
            <span>Progress</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>
      </PageHeader>

      {/* Step Navigation */}
      <Card>
        <CardContent className="pt-6">
          <Stepper.Wizard 
            steps={config.steps}
            currentStep={currentStep}
            onStepClick={(stepIndex) => {
              if (stepIndex <= currentStep) {
                setCurrentStep(stepIndex);
              }
            }}
          />
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-4 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-3">
          <Card className="min-h-[600px]">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${config.color} flex items-center justify-center text-white`}>
                  {config.icon}
                </div>
                <div>
                  <CardTitle level={2}>{currentStepData.title}</CardTitle>
                  <CardDescription className="text-base">
                    {currentStepData.description}
                  </CardDescription>
                </div>
              </div>
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

          {/* Navigation Actions */}
          <ActionBar className="mt-6" align="between">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 0}
            >
              <ChevronLeft className="h-4 w-4 mr-2" />
              Previous
            </Button>
            
            {currentStep === config.steps.length - 1 ? (
              <Button
                onClick={handleComplete}
                variant="primary"
                className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
              >
                Complete Document
                <CheckCircle className="h-4 w-4 ml-2" />
              </Button>
            ) : (
              <Button onClick={handleNext} variant="primary">
                Next
                <ChevronRight className="h-4 w-4 ml-2" />
              </Button>
            )}
          </ActionBar>
        </div>

        {/* Help Panel Sidebar */}
        <div className="lg:col-span-1">
          <div className="space-y-6">
            {/* Contextual Help Panel */}
            {helpPanelOpen && (
              <Card>
                <CardHeader>
                  <CardTitle level={3} className="flex items-center space-x-2">
                    <Lightbulb className="h-5 w-5 text-yellow-600" />
                    <span>Step Guide</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {getStepHelp(currentStepData.id)}
                    </p>
                    <div className="space-y-2">
                      <h4 className="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                        Tips
                      </h4>
                      <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                        {getStepTips(currentStepData.id).map((tip, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <span className="text-blue-600 dark:text-blue-400 mt-0.5">•</span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* AI Analysis */}
            <Card className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 border-blue-200 dark:border-blue-800">
              <CardHeader>
                <CardTitle level={3} className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-blue-600" />
                  <span>AI Analysis</span>
                  {isAnalyzing && (
                    <div className="animate-spin h-4 w-4 border-2 border-blue-600 border-t-transparent rounded-full" />
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Compliance Score</span>
                    <Badge 
                      variant={complianceScore >= 90 ? "success" : complianceScore >= 70 ? "warning" : "danger"}
                    >
                      {complianceScore}%
                    </Badge>
                  </div>
                  <Progress value={complianceScore} className="h-2" />
                  
                  {aiSuggestions.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                        Suggestions
                      </h4>
                      <div className="space-y-2">
                        {aiSuggestions.slice(0, 3).map((suggestion, index) => (
                          <Alert key={index} variant="default">
                            <Lightbulb className="h-4 w-4" />
                            <AlertDescription className="text-sm">
                              {suggestion}
                            </AlertDescription>
                          </Alert>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Legal Requirements */}
            <Card>
              <CardHeader>
                <CardTitle level={3} className="flex items-center space-x-2">
                  <Scale className="h-5 w-5 text-purple-600" />
                  <span>Legal Requirements</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Key requirements for this step:
                  </p>
                  <ul className="text-sm space-y-2">
                    {getLegalRequirements(currentStepData.id).map((requirement, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700 dark:text-gray-300">{requirement}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
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
                    <div className="flex items-center space-x-2 text-gray-600">
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      >
                        <Sparkles className="h-4 w-4" />
                      </motion.div>
                      <span className="text-sm">Analyzing your input...</span>
                    </div>
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

