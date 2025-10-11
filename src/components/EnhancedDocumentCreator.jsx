import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Mail,
  Download,
  Home
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Separator } from './ui/separator';
import { Switch } from './ui/switch';
import { useToast } from '../hooks/use-toast';

const EnhancedDocumentCreator = () => {
  const { type } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const documentType = type;
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

  const handleSaveDraft = () => {
    try {
      localStorage.setItem(`draft_${documentType}`, JSON.stringify(formData));
      toast({
        title: "Draft Saved",
        description: "Your document draft has been saved successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save draft. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handlePreviewDocument = () => {
    // Generate preview content
    const previewContent = generateDocumentPreview(formData, documentType);
    // Store in sessionStorage for preview page
    sessionStorage.setItem('documentPreview', JSON.stringify({
      type: documentType,
      content: previewContent,
      data: formData
    }));
    toast({
      title: "Preview Ready",
      description: "Opening document preview...",
    });
    // Could navigate to preview page or show modal
  };

  const handleGenerateDocument = async () => {
    try {
      toast({
        title: "Generating Document",
        description: "Please wait while we create your document...",
      });

      // Generate document content
      const documentContent = generateDocumentContent(formData, documentType);
      
      // Create downloadable file
      await downloadDocument(documentContent, documentType, formData.fullName || 'Document');
      
      toast({
        title: "Success!",
        description: "Your document has been generated and downloaded.",
      });
    } catch (error) {
      console.error('Error generating document:', error);
      toast({
        title: "Error",
        description: "Failed to generate document. Please try again.",
        variant: "destructive",
      });
    }
  };

  const generateDocumentPreview = (data, type) => {
    // Generate formatted preview text
    return `
      ${type === 'will' ? 'LAST WILL AND TESTAMENT' : 
        type === 'poa_property' ? 'POWER OF ATTORNEY FOR PROPERTY' :
        'POWER OF ATTORNEY FOR PERSONAL CARE'}
      
      This ${type === 'will' ? 'Will' : 'Power of Attorney'} is made on ${new Date().toLocaleDateString()}
      
      By: ${data.fullName || '[Your Name]'}
      Address: ${data.address || '[Your Address]'}, ${data.city || '[City]'}, ${data.province || 'Ontario'}
      Date of Birth: ${data.dateOfBirth || '[Date of Birth]'}
      
      ${generateSectionContent(data, type)}
    `.trim();
  };

  const generateSectionContent = (data, type) => {
    if (type === 'will') {
      return `
        EXECUTORS:
        ${data.executors?.map((e, i) => `${i + 1}. ${e.name || '[Name]'} - ${e.relationship || '[Relationship]'}`).join('\n') || 'No executors specified'}
        
        BENEFICIARIES:
        ${data.beneficiaries?.map((b, i) => `${i + 1}. ${b.name || '[Name]'} - ${b.share || '[Share]'}`).join('\n') || 'No beneficiaries specified'}
        
        WITNESSES:
        ${data.witnesses?.map((w, i) => `${i + 1}. ${w.name || '[Name]'}`).join('\n') || 'Witnesses to be added at signing'}
      `;
    } else if (type === 'poa_property') {
      return `
        ATTORNEYS FOR PROPERTY:
        ${data.attorneys?.map((a, i) => `${i + 1}. ${a.name || '[Name]'} - ${a.relationship || '[Relationship]'}`).join('\n') || 'No attorneys specified'}
        
        This Power of Attorney is ${data.isContinuing ? 'CONTINUING' : 'NON-CONTINUING'}.
        
        POWERS GRANTED:
        - Financial management
        - Property decisions
        - Banking authority
        ${data.specialInstructions?.length ? '\n\nSPECIAL INSTRUCTIONS:\n' + data.specialInstructions.join('\n') : ''}
      `;
    } else {
      return `
        ATTORNEYS FOR PERSONAL CARE:
        ${data.attorneys?.map((a, i) => `${i + 1}. ${a.name || '[Name]'} - ${a.relationship || '[Relationship]'}`).join('\n') || 'No attorneys specified'}
        
        POWERS GRANTED:
        - Healthcare decisions
        - Personal care choices
        - Medical treatment consent
        ${data.specialInstructions?.length ? '\n\nSPECIAL INSTRUCTIONS:\n' + data.specialInstructions.join('\n') : ''}
      `;
    }
  };

  const generateDocumentContent = (data, type) => {
    const docTitle = type === 'will' ? 'LAST WILL AND TESTAMENT' : 
                     type === 'poa_property' ? 'CONTINUING POWER OF ATTORNEY FOR PROPERTY' :
                     'POWER OF ATTORNEY FOR PERSONAL CARE';
    
    const content = `
${docTitle}

This document is made on ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}

GRANTOR INFORMATION:
Name: ${data.fullName || '[Your Name]'}
Address: ${data.address || '[Your Address]'}
City: ${data.city || '[City]'}, ${data.province || 'Ontario'}
Postal Code: ${data.postalCode || '[Postal Code]'}
Date of Birth: ${data.dateOfBirth || '[Date of Birth]'}
Phone: ${data.phone || '[Phone]'}
Email: ${data.email || '[Email]'}

${generateDetailedContent(data, type)}

SIGNATURES:

___________________________    ___________________________
Grantor Signature              Date

WITNESSES:

___________________________    ___________________________
Witness 1 Name                 Witness 1 Signature

___________________________    ___________________________
Witness 2 Name                 Witness 2 Signature

This document complies with the laws of Ontario, Canada.
Generated on ${new Date().toISOString()}
    `.trim();
    
    return content;
  };

  const generateDetailedContent = (data, type) => {
    if (type === 'will') {
      return `
ARTICLE 1 - REVOCATION
I revoke all former wills and codicils.

ARTICLE 2 - EXECUTORS
I appoint the following person(s) as my Executor(s):
${data.executors?.map((e, i) => `${i + 1}. ${e.name || '[Name]'}\n   Address: ${e.address || '[Address]'}\n   Relationship: ${e.relationship || '[Relationship]'}`).join('\n\n') || 'No executors specified'}

ARTICLE 3 - BENEFICIARIES AND DISTRIBUTION
I give, devise and bequeath my estate to the following beneficiaries:
${data.beneficiaries?.map((b, i) => `${i + 1}. ${b.name || '[Name]'} - ${b.share || '[Share]'}%\n   Address: ${b.address || '[Address]'}\n   Relationship: ${b.relationship || '[Relationship]'}`).join('\n\n') || 'No beneficiaries specified'}

ARTICLE 4 - RESIDUARY ESTATE
Any remaining portion of my estate shall be distributed equally among the named beneficiaries.

${data.specialInstructions?.length ? `ARTICLE 5 - SPECIAL INSTRUCTIONS\n${data.specialInstructions.join('\n')}` : ''}
      `.trim();
    } else if (type === 'poa_property') {
      return `
ARTICLE 1 - APPOINTMENT OF ATTORNEY(S)
I appoint the following person(s) as my Attorney(s) for Property:
${data.attorneys?.map((a, i) => `${i + 1}. ${a.name || '[Name]'}\n   Address: ${a.address || '[Address]'}\n   Relationship: ${a.relationship || '[Relationship]'}`).join('\n\n') || 'No attorneys specified'}

ARTICLE 2 - AUTHORITY
This Power of Attorney is ${data.isContinuing ? 'CONTINUING' : 'NON-CONTINUING'} and ${data.isContinuing ? 'shall continue' : 'shall not continue'} to be effective in the event of my mental incapacity.

ARTICLE 3 - POWERS GRANTED
My Attorney(s) shall have the authority to:
- Manage my financial affairs
- Make decisions regarding my property
- Access my bank accounts and financial institutions
- Make investment decisions on my behalf
- Pay bills and manage expenses
- File tax returns
- Manage real estate
${data.specialInstructions?.length ? '\n\nARTICLE 4 - RESTRICTIONS AND SPECIAL INSTRUCTIONS\n' + data.specialInstructions.join('\n') : ''}
      `.trim();
    } else {
      return `
ARTICLE 1 - APPOINTMENT OF ATTORNEY(S)
I appoint the following person(s) as my Attorney(s) for Personal Care:
${data.attorneys?.map((a, i) => `${i + 1}. ${a.name || '[Name]'}\n   Address: ${a.address || '[Address]'}\n   Relationship: ${a.relationship || '[Relationship]'}`).join('\n\n') || 'No attorneys specified'}

ARTICLE 2 - AUTHORITY
My Attorney(s) shall have the authority to make decisions on my behalf regarding:
- Healthcare and medical treatment
- Nutrition and hydration
- Shelter and accommodation
- Clothing and personal care
- Safety and supervision

ARTICLE 3 - HEALTHCARE WISHES
${data.healthcareWishes || 'I wish my Attorney(s) to make decisions in my best interests based on my values and beliefs.'}

${data.specialInstructions?.length ? '\nARTICLE 4 - SPECIAL INSTRUCTIONS\n' + data.specialInstructions.join('\n') : ''}
      `.trim();
    }
  };

  const downloadDocument = async (content, type, name) => {
    const docType = type === 'will' ? 'Will' : type === 'poa_property' ? 'POA-Property' : 'POA-PersonalCare';
    const filename = `${docType}_${name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.txt`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    // Also offer PDF download (in a real app, you'd use a PDF library)
    toast({
      title: "Document Downloaded",
      description: `Your ${docType} has been downloaded as ${filename}. For PDF/Word format, please use a document conversion tool.`,
    });
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
    <div className="max-w-4xl mx-auto p-6 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-gray-900 dark:to-blue-900 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Create Your {type ? type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'Document'}
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Follow the step-by-step guide to create a legally compliant document
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Step {currentStep + 1} of {steps.length}
          </span>
          <span className="text-sm text-gray-500 dark:text-gray-400">
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
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={() => navigate('/')}
              >
                <Home className="w-4 h-4 mr-2" />
                Home
              </Button>
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 0}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Previous
              </Button>
            </div>
            
            <div className="space-x-2">
              <Button variant="outline" onClick={handleSaveDraft}>
                <Save className="w-4 h-4 mr-2" />
                Save Draft
              </Button>
              
              {currentStep === steps.length - 1 ? (
                <>
                  <Button variant="outline" onClick={handlePreviewDocument}>
                    <Eye className="w-4 h-4 mr-2" />
                    Preview
                  </Button>
                  <Button onClick={handleGenerateDocument} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                    <Download className="w-4 h-4 mr-2" />
                    Generate & Download
                  </Button>
                </>
              ) : (
                <Button onClick={handleNext} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
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

