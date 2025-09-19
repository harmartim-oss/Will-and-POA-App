import { useParams, useNavigate } from 'react-router-dom'
import { useToast } from '@/hooks/use-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { ArrowLeft, ArrowRight, FileText } from 'lucide-react'
import { useState } from 'react'
import PageHeader from './layout/PageHeader'
import { Stepper } from './ui/stepper'
import { ActionBar } from './ui/action-bar'
import { FormField, FormGroup, FormError, FormHelp, FormLabel } from './ui/form-field'

const DocumentCreator = () => {
  const { type } = useParams()
  const navigate = useNavigate()
  const { toast } = useToast()
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState({})
  const [validationErrors, setValidationErrors] = useState({})

  const documentConfig = {
    will: {
      title: "Last Will & Testament",
      icon: <FileText className="h-6 w-6" />,
      steps: [
        { id: 'personal', title: 'Personal Information', description: 'Your basic details and identification' },
        { id: 'executor', title: 'Executor Selection', description: 'Choose who will manage your estate' },
        { id: 'beneficiaries', title: 'Beneficiaries', description: 'Designate who receives your assets' },
        { id: 'review', title: 'Review & Generate', description: 'Final review and document creation' }
      ]
    }
  }

  const config = documentConfig[type] || documentConfig.will
  const progress = ((currentStep + 1) / config.steps.length) * 100

  const updateFormData = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    
    // Clear validation error
    if (validationErrors[field]) {
      setValidationErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  const validateCurrentStep = () => {
    const errors = {}
    const stepId = config.steps[currentStep].id

    switch (stepId) {
      case 'personal':
        if (!formData.fullName) errors.fullName = 'Full name is required'
        if (!formData.address) errors.address = 'Address is required'
        break
    }
    
    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (currentStep < config.steps.length - 1) {
        setCurrentStep(currentStep + 1)
      } else {
        handleComplete()
      }
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleComplete = () => {
    toast({
      title: "Document Created Successfully",
      description: "Your document has been generated and is ready for download.",
    })
    navigate('/')
  }

  const renderStepContent = () => {
    const stepId = config.steps[currentStep].id

    switch (stepId) {
      case 'personal':
        return (
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
          </FormGroup>
        )
      
      default:
        return (
          <div className="text-center py-12">
            <p className="text-gray-500">Step content for {config.steps[currentStep].title} coming soon.</p>
          </div>
        )
    }
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={config.title}
        description={`Step ${currentStep + 1} of ${config.steps.length}: ${config.steps[currentStep].title}`}
        breadcrumbs={[
          { label: 'Home', href: '/' },
          { label: 'Documents', href: '/' },
          { label: config.title }
        ]}
        actions={
          <ActionBar>
            <Button variant="outline" onClick={() => navigate('/')}>
              Cancel
            </Button>
          </ActionBar>
        }
      >
        <div className="mt-4 space-y-3">
          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
            <span>Progress</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>
      </PageHeader>

      <Card>
        <CardContent className="pt-6">
          <Stepper.Wizard 
            steps={config.steps}
            currentStep={currentStep}
            onStepClick={(stepIndex) => {
              if (stepIndex <= currentStep) {
                setCurrentStep(stepIndex)
              }
            }}
          />
        </CardContent>
      </Card>

      <Card className="min-h-[400px]">
        <CardHeader>
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-lg bg-blue-600 dark:bg-blue-500 flex items-center justify-center text-white">
              {config.icon}
            </div>
            <div>
              <CardTitle level={2}>{config.steps[currentStep].title}</CardTitle>
              <CardDescription className="text-base">
                {config.steps[currentStep].description}
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {renderStepContent()}
        </CardContent>
      </Card>

      <ActionBar align="between">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentStep === 0}
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Previous
        </Button>
        
        <Button onClick={handleNext} variant="primary">
          {currentStep === config.steps.length - 1 ? 'Complete Document' : 'Next'}
          {currentStep < config.steps.length - 1 && <ArrowRight className="h-4 w-4 ml-2" />}
        </Button>
      </ActionBar>
    </div>
  )
}

export default DocumentCreator