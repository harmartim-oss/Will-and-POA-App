import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  User, 
  Users, 
  Shield, 
  CheckCircle, 
  AlertTriangle, 
  ArrowRight, 
  ArrowLeft, 
  Save, 
  Eye,
  Lightbulb,
  Scale,
  Heart,
  Building,
  Calendar,
  MapPin,
  Phone,
  Mail
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Separator } from '../ui/separator';
import { Switch } from '../ui/switch';

const EnhancedDocumentCreator = ({ documentType, onSave, onPreview }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    // Personal Information
    fullName: '',
    dateOfBirth: '',
    address: '',
    city: '',
    province: 'Ontario',
    postalCode: '',
    phone: '',
    email: '',
    
    // Document-specific data
    executors: [],
    beneficiaries: [],
    attorneys: [],
    witnesses: [],
    assets: [],
    bequests: [],
    specialInstructions: [],
    
    // Options
    isContining: true,
    includeDigitalAssets: false,
    includePetCare: false,
    includeCharitableBequests: false
  });
  
  const [validationErrors, setValidationErrors] = useState({});
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [showAiHelp, setShowAiHelp] = useState(false);

  // Define steps based on document type
  const getSteps = () => {
    const baseSteps = [
      {
        id: 'personal',
        title: 'Personal Information',
        description: 'Your basic information and contact details',
        icon: User,
        required: true
      }
    ];

    if (documentType === 'will') {
      return [
        ...baseSteps,
        {
          id: 'executors',
          title: 'Executors',
          description: 'People who will manage your estate',
          icon: Shield,
          required: true
        },
        {
          id: 'beneficiaries',
          title: 'Beneficiaries',
          description: 'Who will inherit your assets',
          icon: Users,
          required: true
        },
        {
          id: 'assets',
          title: 'Assets & Bequests',
          description: 'Your property and specific gifts',
          icon: Building,
          required: false
        },
        {
          id: 'special',
          title: 'Special Instructions',
          description: 'Additional wishes and instructions',
          icon: FileText,
          required: false
        },
        {
          id: 'witnesses',
          title: 'Witnesses',
          description: 'Required witnesses for execution',
          icon: Eye,
          required: true
        }
      ];
    } else if (documentType === 'power_of_attorney_property') {
      return [
        ...baseSteps,
        {
          id: 'attorneys',
          title: 'Attorneys',
          description: 'People authorized to manage your property',
          icon: Shield,
          required: true
        },
        {
          id: 'powers',
          title: 'Powers & Restrictions',
          description: 'What your attorneys can and cannot do',
          icon: Scale,
          required: true
        },
        {
          id: 'witnesses',
          title: 'Witnesses',
          description: 'Required witnesses for execution',
          icon: Eye,
          required: true
        }
      ];
    } else if (documentType === 'power_of_attorney_care') {
      return [
        ...baseSteps,
        {
          id: 'attorneys',
          title: 'Attorneys',
          description: 'People authorized to make personal care decisions',
          icon: Heart,
          required: true
        },
        {
          id: 'care_instructions',
          title: 'Care Instructions',
          description: 'Your preferences for personal care',
          icon: Heart,
          required: false
        },
        {
          id: 'witnesses',
          title: 'Witnesses',
          description: 'Required witnesses for execution',
          icon: Eye,
          required: true
        }
      ];
    }

    return baseSteps;
  };

  const steps = getSteps();
  const progress = ((currentStep + 1) / steps.length) * 100;

  // Mock AI suggestions
  useEffect(() => {
    const suggestions = [
      "Consider appointing alternate executors in case your primary executor cannot serve",
      "You may want to include specific instructions for digital assets like social media accounts",
      "Consider adding a clause about organ donation preferences",
      "Think about including instructions for pet care if applicable"
    ];
    setAiSuggestions(suggestions);
  }, [currentStep, documentType]);

  const validateStep = (stepId) => {
    const errors = {};
    
    switch (stepId) {
      case 'personal':
        if (!formData.fullName.trim()) errors.fullName = 'Full name is required';
        if (!formData.dateOfBirth) errors.dateOfBirth = 'Date of birth is required';
        if (!formData.address.trim()) errors.address = 'Address is required';
        if (!formData.city.trim()) errors.city = 'City is required';
        if (!formData.postalCode.trim()) errors.postalCode = 'Postal code is required';
        break;
      
      case 'executors':
        if (formData.executors.length === 0) {
          errors.executors = 'At least one executor is required';
        }
        break;
      
      case 'beneficiaries':
        if (formData.beneficiaries.length === 0) {
          errors.beneficiaries = 'At least one beneficiary is required';
        }
        break;
      
      case 'attorneys':
        if (formData.attorneys.length === 0) {
          errors.attorneys = 'At least one attorney is required';
        }
        break;
      
      case 'witnesses':
        if (formData.witnesses.length < 2) {
          errors.witnesses = 'At least two witnesses are required';
        }
        break;
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleNext = () => {
    const currentStepId = steps[currentStep].id;
    if (validateStep(currentStepId)) {
      setCurrentStep(Math.min(currentStep + 1, steps.length - 1));
    }
  };

  const handlePrevious = () => {
    setCurrentStep(Math.max(currentStep - 1, 0));
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear validation error for this field
    if (validationErrors[field]) {
      setValidationErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  const addListItem = (listName, item) => {
    setFormData(prev => ({
      ...prev,
      [listName]: [...prev[listName], item]
    }));
  };

  const removeListItem = (listName, index) => {
    setFormData(prev => ({
      ...prev,
      [listName]: prev[listName].filter((_, i) => i !== index)
    }));
  };

  const PersonForm = ({ person, onChange, fields = ['name', 'relationship', 'address', 'phone'] }) => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {fields.includes('name') && (
        <div>
          <Label htmlFor="name">Full Name *</Label>
          <Input
            id="name"
            value={person.name || ''}
            onChange={(e) => onChange({ ...person, name: e.target.value })}
            placeholder="Enter full name"
          />
        </div>
      )}
      
      {fields.includes('relationship') && (
        <div>
          <Label htmlFor="relationship">Relationship</Label>
          <Input
            id="relationship"
            value={person.relationship || ''}
            onChange={(e) => onChange({ ...person, relationship: e.target.value })}
            placeholder="e.g., Spouse, Child, Friend"
          />
        </div>
      )}
      
      {fields.includes('address') && (
        <div className="md:col-span-2">
          <Label htmlFor="address">Address</Label>
          <Input
            id="address"
            value={person.address || ''}
            onChange={(e) => onChange({ ...person, address: e.target.value })}
            placeholder="Street address"
          />
        </div>
      )}
      
      <div>
        <Label htmlFor="city">City</Label>
        <Input
          id="city"
          value={person.city || ''}
          onChange={(e) => onChange({ ...person, city: e.target.value })}
          placeholder="City"
        />
      </div>
      
      <div>
        <Label htmlFor="province">Province</Label>
        <Input
          id="province"
          value={person.province || 'Ontario'}
          onChange={(e) => onChange({ ...person, province: e.target.value })}
          placeholder="Province"
        />
      </div>
      
      {fields.includes('phone') && (
        <div>
          <Label htmlFor="phone">Phone</Label>
          <Input
            id="phone"
            value={person.phone || ''}
            onChange={(e) => onChange({ ...person, phone: e.target.value })}
            placeholder="Phone number"
          />
        </div>
      )}
      
      {fields.includes('email') && (
        <div>
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={person.email || ''}
            onChange={(e) => onChange({ ...person, email: e.target.value })}
            placeholder="Email address"
          />
        </div>
      )}
    </div>
  );

  const renderStepContent = () => {
    const step = steps[currentStep];
    
    switch (step.id) {
      case 'personal':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="fullName">Full Legal Name *</Label>
                <Input
                  id="fullName"
                  value={formData.fullName}
                  onChange={(e) => handleInputChange('fullName', e.target.value)}
                  placeholder="Enter your full legal name"
                  className={validationErrors.fullName ? 'border-red-500' : ''}
                />
                {validationErrors.fullName && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.fullName}</p>
                )}
              </div>
              
              <div>
                <Label htmlFor="dateOfBirth">Date of Birth *</Label>
                <Input
                  id="dateOfBirth"
                  type="date"
                  value={formData.dateOfBirth}
                  onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                  className={validationErrors.dateOfBirth ? 'border-red-500' : ''}
                />
                {validationErrors.dateOfBirth && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.dateOfBirth}</p>
                )}
              </div>
            </div>
            
            <div>
              <Label htmlFor="address">Address *</Label>
              <Input
                id="address"
                value={formData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                placeholder="Street address"
                className={validationErrors.address ? 'border-red-500' : ''}
              />
              {validationErrors.address && (
                <p className="text-red-500 text-sm mt-1">{validationErrors.address}</p>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="city">City *</Label>
                <Input
                  id="city"
                  value={formData.city}
                  onChange={(e) => handleInputChange('city', e.target.value)}
                  placeholder="City"
                  className={validationErrors.city ? 'border-red-500' : ''}
                />
                {validationErrors.city && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.city}</p>
                )}
              </div>
              
              <div>
                <Label htmlFor="province">Province</Label>
                <Input
                  id="province"
                  value={formData.province}
                  onChange={(e) => handleInputChange('province', e.target.value)}
                  placeholder="Province"
                />
              </div>
              
              <div>
                <Label htmlFor="postalCode">Postal Code *</Label>
                <Input
                  id="postalCode"
                  value={formData.postalCode}
                  onChange={(e) => handleInputChange('postalCode', e.target.value)}
                  placeholder="A1A 1A1"
                  className={validationErrors.postalCode ? 'border-red-500' : ''}
                />
                {validationErrors.postalCode && (
                  <p className="text-red-500 text-sm mt-1">{validationErrors.postalCode}</p>
                )}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  placeholder="(555) 123-4567"
                />
              </div>
              
              <div>
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  placeholder="your.email@example.com"
                />
              </div>
            </div>
          </div>
        );
      
      case 'executors':
        return (
          <div className="space-y-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">About Executors</h4>
              <p className="text-blue-800 text-sm">
                Executors are responsible for managing your estate after you pass away. They will handle tasks like 
                paying debts, distributing assets, and filing tax returns. Choose people you trust who are organized 
                and capable of handling financial matters.
              </p>
            </div>
            
            {formData.executors.map((executor, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-lg">Executor {index + 1}</CardTitle>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => removeListItem('executors', index)}
                    >
                      Remove
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <PersonForm
                    person={executor}
                    onChange={(updatedExecutor) => {
                      const newExecutors = [...formData.executors];
                      newExecutors[index] = updatedExecutor;
                      handleInputChange('executors', newExecutors);
                    }}
                  />
                </CardContent>
              </Card>
            ))}
            
            <Button
              onClick={() => addListItem('executors', { name: '', relationship: '', address: '', city: '', province: 'Ontario', phone: '' })}
              variant="outline"
              className="w-full"
            >
              Add Executor
            </Button>
            
            {validationErrors.executors && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{validationErrors.executors}</AlertDescription>
              </Alert>
            )}
          </div>
        );
      
      case 'beneficiaries':
        return (
          <div className="space-y-6">
            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-semibold text-green-900 mb-2">About Beneficiaries</h4>
              <p className="text-green-800 text-sm">
                Beneficiaries are the people or organizations who will inherit your assets. You can specify 
                what each beneficiary will receive, or leave it to your executor to distribute according 
                to your general wishes.
              </p>
            </div>
            
            {formData.beneficiaries.map((beneficiary, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-lg">Beneficiary {index + 1}</CardTitle>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => removeListItem('beneficiaries', index)}
                    >
                      Remove
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <PersonForm
                    person={beneficiary}
                    onChange={(updatedBeneficiary) => {
                      const newBeneficiaries = [...formData.beneficiaries];
                      newBeneficiaries[index] = updatedBeneficiary;
                      handleInputChange('beneficiaries', newBeneficiaries);
                    }}
                  />
                  
                  <div>
                    <Label htmlFor={`inheritance-${index}`}>Inheritance Details</Label>
                    <Textarea
                      id={`inheritance-${index}`}
                      value={beneficiary.inheritance || ''}
                      onChange={(e) => {
                        const newBeneficiaries = [...formData.beneficiaries];
                        newBeneficiaries[index] = { ...beneficiary, inheritance: e.target.value };
                        handleInputChange('beneficiaries', newBeneficiaries);
                      }}
                      placeholder="Describe what this beneficiary will inherit (e.g., '50% of residual estate', 'Family home', 'All jewelry')"
                      rows={3}
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
            
            <Button
              onClick={() => addListItem('beneficiaries', { 
                name: '', 
                relationship: '', 
                address: '', 
                city: '', 
                province: 'Ontario', 
                phone: '',
                inheritance: ''
              })}
              variant="outline"
              className="w-full"
            >
              Add Beneficiary
            </Button>
            
            {validationErrors.beneficiaries && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{validationErrors.beneficiaries}</AlertDescription>
              </Alert>
            )}
          </div>
        );
      
      case 'witnesses':
        return (
          <div className="space-y-6">
            <div className="bg-amber-50 p-4 rounded-lg">
              <h4 className="font-semibold text-amber-900 mb-2">Witness Requirements</h4>
              <p className="text-amber-800 text-sm mb-2">
                In Ontario, you need at least 2 witnesses to sign your will. Witnesses must:
              </p>
              <ul className="text-amber-800 text-sm space-y-1 ml-4">
                <li>• Be at least 18 years old</li>
                <li>• Be mentally capable</li>
                <li>• Not be beneficiaries in your will</li>
                <li>• Not be married to beneficiaries</li>
                <li>• Sign in your presence and in each other's presence</li>
              </ul>
            </div>
            
            {formData.witnesses.map((witness, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-lg">Witness {index + 1}</CardTitle>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => removeListItem('witnesses', index)}
                    >
                      Remove
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <PersonForm
                    person={witness}
                    onChange={(updatedWitness) => {
                      const newWitnesses = [...formData.witnesses];
                      newWitnesses[index] = updatedWitness;
                      handleInputChange('witnesses', newWitnesses);
                    }}
                    fields={['name', 'address', 'phone']}
                  />
                </CardContent>
              </Card>
            ))}
            
            <Button
              onClick={() => addListItem('witnesses', { name: '', address: '', city: '', province: 'Ontario', phone: '' })}
              variant="outline"
              className="w-full"
            >
              Add Witness
            </Button>
            
            {validationErrors.witnesses && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{validationErrors.witnesses}</AlertDescription>
              </Alert>
            )}
          </div>
        );
      
      default:
        return (
          <div className="text-center py-8">
            <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">Step content coming soon...</p>
          </div>
        );
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Create Your {documentType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </h1>
        <p className="text-gray-600">
          Follow the step-by-step guide to create a legally compliant document
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Step {currentStep + 1} of {steps.length}
          </span>
          <span className="text-sm text-gray-500">
            {Math.round(progress)}% Complete
          </span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Step Navigation */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-2">
          {steps.map((step, index) => {
            const StepIcon = step.icon;
            const isCompleted = index < currentStep;
            const isCurrent = index === currentStep;
            const isAccessible = index <= currentStep;
            
            return (
              <Button
                key={step.id}
                variant={isCurrent ? "default" : isCompleted ? "secondary" : "outline"}
                size="sm"
                onClick={() => isAccessible && setCurrentStep(index)}
                disabled={!isAccessible}
                className={`flex items-center space-x-2 ${
                  isCompleted ? 'bg-green-100 text-green-800 border-green-300' : ''
                }`}
              >
                <StepIcon className="w-4 h-4" />
                <span className="hidden sm:inline">{step.title}</span>
                {isCompleted && <CheckCircle className="w-4 h-4" />}
              </Button>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-3">
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-3">
                {React.createElement(steps[currentStep].icon, { className: "w-6 h-6 text-blue-600" })}
                <div>
                  <CardTitle className="text-xl">{steps[currentStep].title}</CardTitle>
                  <CardDescription>{steps[currentStep].description}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {renderStepContent()}
            </CardContent>
          </Card>

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-6">
            <Button
              variant="outline"
              onClick={handlePrevious}
              disabled={currentStep === 0}
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Previous
            </Button>
            
            <div className="space-x-2">
              <Button variant="outline" onClick={() => onSave?.(formData)}>
                <Save className="w-4 h-4 mr-2" />
                Save Draft
              </Button>
              
              {currentStep === steps.length - 1 ? (
                <Button onClick={() => onPreview?.(formData)}>
                  <Eye className="w-4 h-4 mr-2" />
                  Preview Document
                </Button>
              ) : (
                <Button onClick={handleNext}>
                  Next
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              )}
            </div>
          </div>
        </div>

        {/* AI Assistance Sidebar */}
        <div className="lg:col-span-1">
          <Card className="sticky top-6">
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <Lightbulb className="w-5 h-5 mr-2 text-yellow-600" />
                AI Assistant
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Show suggestions</span>
                <Switch
                  checked={showAiHelp}
                  onCheckedChange={setShowAiHelp}
                />
              </div>
              
              {showAiHelp && (
                <div className="space-y-3">
                  {aiSuggestions.map((suggestion, index) => (
                    <div key={index} className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                      <p className="text-sm text-yellow-800">{suggestion}</p>
                    </div>
                  ))}
                </div>
              )}
              
              <Separator />
              
              <div className="space-y-2">
                <h4 className="font-semibold text-sm">Quick Actions</h4>
                <Button variant="outline" size="sm" className="w-full text-xs">
                  <Scale className="w-3 h-3 mr-1" />
                  Legal Research
                </Button>
                <Button variant="outline" size="sm" className="w-full text-xs">
                  <FileText className="w-3 h-3 mr-1" />
                  Sample Clauses
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDocumentCreator;

