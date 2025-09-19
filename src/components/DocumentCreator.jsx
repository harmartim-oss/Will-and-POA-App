import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, ArrowRight, Save, FileText, AlertCircle, CheckCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useToast } from '@/hooks/use-toast'

const DocumentCreator = () => {
  const { type } = useParams()
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const [currentStep, setCurrentStep] = useState(0)
  const [documentData, setDocumentData] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [validationErrors, setValidationErrors] = useState({})

  const documentTypes = {
    will: {
      title: 'Last Will and Testament',
      steps: [
        'Personal Information',
        'Executor Selection',
        'Asset Inventory',
        'Beneficiaries',
        'Specific Bequests',
        'Guardian Appointment',
        'Final Review'
      ]
    },
    poa_property: {
      title: 'Power of Attorney for Property',
      steps: [
        'Personal Information',
        'Attorney Selection',
        'Powers Granted',
        'Conditions & Limitations',
        'Final Review'
      ]
    },
    poa_care: {
      title: 'Power of Attorney for Personal Care',
      steps: [
        'Personal Information',
        'Attorney Selection',
        'Care Preferences',
        'Healthcare Directives',
        'Final Review'
      ]
    }
  }

  const currentDocType = documentTypes[type]
  const totalSteps = currentDocType?.steps.length || 0
  const progress = ((currentStep + 1) / totalSteps) * 100

  useEffect(() => {
    if (!currentDocType) {
      navigate('/')
    }
  }, [type, currentDocType, navigate])

  const updateDocumentData = (field, value) => {
    setDocumentData(prev => ({
      ...prev,
      [field]: value
    }))
    
    // Clear validation error for this field
    if (validationErrors[field]) {
      setValidationErrors(prev => ({
        ...prev,
        [field]: null
      }))
    }
  }

  const validateCurrentStep = () => {
    const errors = {}
    
    switch (currentStep) {
      case 0: // Personal Information
        if (!documentData.fullName) errors.fullName = 'Full name is required'
        if (!documentData.address) errors.address = 'Address is required'
        if (!documentData.dateOfBirth) errors.dateOfBirth = 'Date of birth is required'
        break
      case 1: // Executor/Attorney Selection
        if (!documentData.executorName) errors.executorName = 'Executor/Attorney name is required'
        if (!documentData.executorAddress) errors.executorAddress = 'Executor/Attorney address is required'
        break
      // Add more validation cases as needed
    }
    
    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (currentStep < totalSteps - 1) {
        setCurrentStep(currentStep + 1)
      } else {
        handleSaveDocument()
      }
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleSaveDocument = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/documents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_type: type,
          title: `${currentDocType.title} - ${documentData.fullName || 'Draft'}`,
          content: documentData
        })
      })

      if (response.ok) {
        const document = await response.json()
        toast({
          title: "Document Saved",
          description: "Your document has been saved successfully.",
        })
        navigate(`/preview/${document.id}`)
      } else {
        throw new Error('Failed to save document')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save document. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return <PersonalInformationStep 
          data={documentData} 
          updateData={updateDocumentData}
          errors={validationErrors}
        />
      case 1:
        return type === 'will' ? 
          <ExecutorSelectionStep 
            data={documentData} 
            updateData={updateDocumentData}
            errors={validationErrors}
          /> :
          <AttorneySelectionStep 
            data={documentData} 
            updateData={updateDocumentData}
            errors={validationErrors}
          />
      case 2:
        if (type === 'will') {
          return <AssetInventoryStep 
            data={documentData} 
            updateData={updateDocumentData}
            errors={validationErrors}
          />
        } else {
          return <PowersGrantedStep 
            data={documentData} 
            updateData={updateDocumentData}
            errors={validationErrors}
            documentType={type}
          />
        }
      // Add more cases for additional steps
      default:
        return <FinalReviewStep 
          data={documentData} 
          documentType={type}
        />
    }
  }

  if (!currentDocType) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => navigate('/')}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Home
              </Button>
            </div>
            <Badge variant="secondary">
              Step {currentStep + 1} of {totalSteps}
            </Badge>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-2xl font-bold text-gray-900">
              {currentDocType.title}
            </h1>
            <span className="text-sm text-gray-600">
              {Math.round(progress)}% Complete
            </span>
          </div>
          <Progress value={progress} className="h-2" />
          
          {/* Step indicators */}
          <div className="flex justify-between mt-4">
            {currentDocType.steps.map((step, index) => (
              <div 
                key={index}
                className={`text-xs text-center ${
                  index <= currentStep ? 'text-blue-600 font-medium' : 'text-gray-400'
                }`}
              >
                <div className={`w-8 h-8 rounded-full mx-auto mb-1 flex items-center justify-center ${
                  index < currentStep ? 'bg-blue-600 text-white' :
                  index === currentStep ? 'bg-blue-100 text-blue-600 border-2 border-blue-600' :
                  'bg-gray-200 text-gray-400'
                }`}>
                  {index < currentStep ? (
                    <CheckCircle className="h-4 w-4" />
                  ) : (
                    <span>{index + 1}</span>
                  )}
                </div>
                <span className="hidden sm:block">{step}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Step Content */}
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

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <Button 
            variant="outline"
            onClick={handlePrevious}
            disabled={currentStep === 0}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Previous
          </Button>
          
          <Button 
            onClick={handleNext}
            disabled={isLoading}
          >
            {currentStep === totalSteps - 1 ? (
              <>
                <Save className="h-4 w-4 mr-2" />
                Save Document
              </>
            ) : (
              <>
                Next
                <ArrowRight className="h-4 w-4 ml-2" />
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}

// Step Components
const PersonalInformationStep = ({ data, updateData, errors }) => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center space-x-2">
        <FileText className="h-5 w-5" />
        <span>Personal Information</span>
      </CardTitle>
      <CardDescription>
        Please provide your personal details as they should appear in the legal document.
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-6">
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="fullName">Full Legal Name *</Label>
          <Input
            id="fullName"
            value={data.fullName || ''}
            onChange={(e) => updateData('fullName', e.target.value)}
            placeholder="Enter your full legal name"
            className={errors.fullName ? 'border-red-500' : ''}
          />
          {errors.fullName && (
            <p className="text-red-500 text-sm mt-1 flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" />
              {errors.fullName}
            </p>
          )}
        </div>
        
        <div>
          <Label htmlFor="dateOfBirth">Date of Birth *</Label>
          <Input
            id="dateOfBirth"
            type="date"
            value={data.dateOfBirth || ''}
            onChange={(e) => updateData('dateOfBirth', e.target.value)}
            className={errors.dateOfBirth ? 'border-red-500' : ''}
          />
          {errors.dateOfBirth && (
            <p className="text-red-500 text-sm mt-1 flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" />
              {errors.dateOfBirth}
            </p>
          )}
        </div>
      </div>
      
      <div>
        <Label htmlFor="address">Full Address *</Label>
        <Textarea
          id="address"
          value={data.address || ''}
          onChange={(e) => updateData('address', e.target.value)}
          placeholder="Enter your complete address including postal code"
          className={errors.address ? 'border-red-500' : ''}
        />
        {errors.address && (
          <p className="text-red-500 text-sm mt-1 flex items-center">
            <AlertCircle className="h-4 w-4 mr-1" />
            {errors.address}
          </p>
        )}
      </div>
      
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="phone">Phone Number</Label>
          <Input
            id="phone"
            value={data.phone || ''}
            onChange={(e) => updateData('phone', e.target.value)}
            placeholder="(555) 123-4567"
          />
        </div>
        
        <div>
          <Label htmlFor="email">Email Address</Label>
          <Input
            id="email"
            type="email"
            value={data.email || ''}
            onChange={(e) => updateData('email', e.target.value)}
            placeholder="your.email@example.com"
          />
        </div>
      </div>
    </CardContent>
  </Card>
)

const ExecutorSelectionStep = ({ data, updateData, errors }) => (
  <Card>
    <CardHeader>
      <CardTitle>Executor Selection</CardTitle>
      <CardDescription>
        Choose someone you trust to carry out the instructions in your will.
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-6">
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="executorName">Executor Full Name *</Label>
          <Input
            id="executorName"
            value={data.executorName || ''}
            onChange={(e) => updateData('executorName', e.target.value)}
            placeholder="Enter executor's full name"
            className={errors.executorName ? 'border-red-500' : ''}
          />
          {errors.executorName && (
            <p className="text-red-500 text-sm mt-1 flex items-center">
              <AlertCircle className="h-4 w-4 mr-1" />
              {errors.executorName}
            </p>
          )}
        </div>
        
        <div>
          <Label htmlFor="executorRelationship">Relationship to You</Label>
          <Input
            id="executorRelationship"
            value={data.executorRelationship || ''}
            onChange={(e) => updateData('executorRelationship', e.target.value)}
            placeholder="e.g., Spouse, Child, Friend"
          />
        </div>
      </div>
      
      <div>
        <Label htmlFor="executorAddress">Executor Address *</Label>
        <Textarea
          id="executorAddress"
          value={data.executorAddress || ''}
          onChange={(e) => updateData('executorAddress', e.target.value)}
          placeholder="Enter executor's complete address"
          className={errors.executorAddress ? 'border-red-500' : ''}
        />
        {errors.executorAddress && (
          <p className="text-red-500 text-sm mt-1 flex items-center">
            <AlertCircle className="h-4 w-4 mr-1" />
            {errors.executorAddress}
          </p>
        )}
      </div>
      
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="executorPhone">Executor Phone</Label>
          <Input
            id="executorPhone"
            value={data.executorPhone || ''}
            onChange={(e) => updateData('executorPhone', e.target.value)}
            placeholder="(555) 123-4567"
          />
        </div>
        
        <div>
          <Label htmlFor="executorEmail">Executor Email</Label>
          <Input
            id="executorEmail"
            type="email"
            value={data.executorEmail || ''}
            onChange={(e) => updateData('executorEmail', e.target.value)}
            placeholder="executor@example.com"
          />
        </div>
      </div>
    </CardContent>
  </Card>
)

const AttorneySelectionStep = ({ data, updateData, errors }) => (
  <Card>
    <CardHeader>
      <CardTitle>Attorney Selection</CardTitle>
      <CardDescription>
        Choose someone you trust to make decisions on your behalf.
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-6">
      {/* Similar structure to ExecutorSelectionStep but for attorney */}
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="attorneyName">Attorney Full Name *</Label>
          <Input
            id="attorneyName"
            value={data.attorneyName || ''}
            onChange={(e) => updateData('attorneyName', e.target.value)}
            placeholder="Enter attorney's full name"
            className={errors.attorneyName ? 'border-red-500' : ''}
          />
        </div>
        
        <div>
          <Label htmlFor="attorneyRelationship">Relationship to You</Label>
          <Input
            id="attorneyRelationship"
            value={data.attorneyRelationship || ''}
            onChange={(e) => updateData('attorneyRelationship', e.target.value)}
            placeholder="e.g., Spouse, Child, Friend"
          />
        </div>
      </div>
      
      <div>
        <Label htmlFor="attorneyAddress">Attorney Address *</Label>
        <Textarea
          id="attorneyAddress"
          value={data.attorneyAddress || ''}
          onChange={(e) => updateData('attorneyAddress', e.target.value)}
          placeholder="Enter attorney's complete address"
          className={errors.attorneyAddress ? 'border-red-500' : ''}
        />
      </div>
    </CardContent>
  </Card>
)

const AssetInventoryStep = ({ data, updateData }) => (
  <Card>
    <CardHeader>
      <CardTitle>Asset Inventory</CardTitle>
      <CardDescription>
        List your major assets and how you want them distributed.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <p className="text-gray-600">Asset inventory form would go here...</p>
    </CardContent>
  </Card>
)

const PowersGrantedStep = ({ data, updateData, documentType }) => (
  <Card>
    <CardHeader>
      <CardTitle>Powers Granted</CardTitle>
      <CardDescription>
        Specify what powers you want to grant to your attorney.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <p className="text-gray-600">Powers selection form would go here...</p>
    </CardContent>
  </Card>
)

const FinalReviewStep = ({ data, documentType }) => (
  <Card>
    <CardHeader>
      <CardTitle>Final Review</CardTitle>
      <CardDescription>
        Review your information before creating the document.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div className="space-y-4">
        <div>
          <h4 className="font-medium">Personal Information</h4>
          <p className="text-sm text-gray-600">Name: {data.fullName}</p>
          <p className="text-sm text-gray-600">Address: {data.address}</p>
        </div>
        {/* Add more review sections */}
      </div>
    </CardContent>
  </Card>
)

export default DocumentCreator

