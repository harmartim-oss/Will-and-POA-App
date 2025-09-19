import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ArrowLeft, Save, Eye, Lightbulb, CheckCircle, X } from 'lucide-react'
import { motion } from 'framer-motion'
import { useToast } from '@/hooks/use-toast'

const DocumentEditor = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const [document, setDocument] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState([])
  const [selectedSection, setSelectedSection] = useState('personal_info')

  useEffect(() => {
    fetchDocument()
  }, [id])

  const fetchDocument = async () => {
    try {
      const response = await fetch(`/api/documents/${id}`)
      if (response.ok) {
        const doc = await response.json()
        setDocument(doc)
      } else {
        throw new Error('Failed to fetch document')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load document.",
        variant: "destructive"
      })
      navigate('/')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      const response = await fetch(`/api/documents/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: document.content
        })
      })

      if (response.ok) {
        toast({
          title: "Document Saved",
          description: "Your changes have been saved successfully.",
        })
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
      setIsSaving(false)
    }
  }

  const getAISuggestions = async (section, text) => {
    try {
      const response = await fetch(`/api/documents/${id}/ai-suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section,
          text
        })
      })

      if (response.ok) {
        const suggestions = await response.json()
        setAiSuggestions(suggestions)
      }
    } catch (error) {
      console.error('Failed to get AI suggestions:', error)
    }
  }

  const applySuggestion = (suggestion) => {
    // Apply the suggestion to the document content
    const updatedContent = { ...document.content }
    // Implementation would depend on the specific section and suggestion
    setDocument(prev => ({
      ...prev,
      content: updatedContent
    }))
    
    // Remove the applied suggestion
    setAiSuggestions(prev => prev.filter(s => s.id !== suggestion.id))
  }

  const updateContent = (field, value) => {
    setDocument(prev => ({
      ...prev,
      content: {
        ...prev.content,
        [field]: value
      }
    }))
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading document...</p>
        </div>
      </div>
    )
  }

  if (!document) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
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
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{document.title}</h1>
                <p className="text-sm text-gray-500">
                  Last updated: {new Date(document.updated_at).toLocaleDateString()}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant={document.is_completed ? "default" : "secondary"}>
                {document.is_completed ? "Completed" : "Draft"}
              </Badge>
              <Button 
                variant="outline"
                onClick={() => navigate(`/preview/${id}`)}
              >
                <Eye className="h-4 w-4 mr-2" />
                Preview
              </Button>
              <Button 
                onClick={handleSave}
                disabled={isSaving}
              >
                <Save className="h-4 w-4 mr-2" />
                {isSaving ? 'Saving...' : 'Save'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Editor */}
          <div className="lg:col-span-2">
            <Tabs value={selectedSection} onValueChange={setSelectedSection}>
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="personal_info">Personal</TabsTrigger>
                <TabsTrigger value="executor">Executor</TabsTrigger>
                <TabsTrigger value="bequests">Bequests</TabsTrigger>
                <TabsTrigger value="review">Review</TabsTrigger>
              </TabsList>
              
              <TabsContent value="personal_info" className="mt-6">
                <PersonalInfoEditor 
                  content={document.content}
                  updateContent={updateContent}
                  onRequestSuggestions={(text) => getAISuggestions('personal_info', text)}
                />
              </TabsContent>
              
              <TabsContent value="executor" className="mt-6">
                <ExecutorEditor 
                  content={document.content}
                  updateContent={updateContent}
                  onRequestSuggestions={(text) => getAISuggestions('executor', text)}
                />
              </TabsContent>
              
              <TabsContent value="bequests" className="mt-6">
                <BequestsEditor 
                  content={document.content}
                  updateContent={updateContent}
                  onRequestSuggestions={(text) => getAISuggestions('bequests', text)}
                />
              </TabsContent>
              
              <TabsContent value="review" className="mt-6">
                <ReviewEditor 
                  content={document.content}
                  documentType={document.document_type}
                />
              </TabsContent>
            </Tabs>
          </div>

          {/* AI Suggestions Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  <span>AI Suggestions</span>
                </CardTitle>
                <CardDescription>
                  Intelligent recommendations to improve your document
                </CardDescription>
              </CardHeader>
              <CardContent>
                {aiSuggestions.length > 0 ? (
                  <div className="space-y-4">
                    {aiSuggestions.map((suggestion, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-3 border rounded-lg bg-blue-50"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <Badge variant="outline" className="text-xs">
                            {suggestion.type}
                          </Badge>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setAiSuggestions(prev => 
                              prev.filter((_, i) => i !== index)
                            )}
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                        <p className="text-sm text-gray-700 mb-3">
                          {suggestion.text}
                        </p>
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            onClick={() => applySuggestion(suggestion)}
                          >
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Apply
                          </Button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Lightbulb className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">
                      Select text and click "Get Suggestions" to receive AI-powered recommendations
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

// Editor Components
const PersonalInfoEditor = ({ content, updateContent, onRequestSuggestions }) => (
  <Card>
    <CardHeader>
      <CardTitle>Personal Information</CardTitle>
      <CardDescription>
        Edit your personal details as they appear in the document
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Full Name</label>
        <Textarea
          value={content.fullName || ''}
          onChange={(e) => updateContent('fullName', e.target.value)}
          placeholder="Enter your full legal name"
          rows={1}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Address</label>
        <Textarea
          value={content.address || ''}
          onChange={(e) => updateContent('address', e.target.value)}
          placeholder="Enter your complete address"
          rows={3}
        />
      </div>
      <Button 
        variant="outline" 
        size="sm"
        onClick={() => onRequestSuggestions(content.fullName + ' ' + content.address)}
      >
        <Lightbulb className="h-4 w-4 mr-2" />
        Get Suggestions
      </Button>
    </CardContent>
  </Card>
)

const ExecutorEditor = ({ content, updateContent, onRequestSuggestions }) => (
  <Card>
    <CardHeader>
      <CardTitle>Executor Information</CardTitle>
      <CardDescription>
        Edit executor details and responsibilities
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Executor Name</label>
        <Textarea
          value={content.executorName || ''}
          onChange={(e) => updateContent('executorName', e.target.value)}
          placeholder="Enter executor's full name"
          rows={1}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Executor Address</label>
        <Textarea
          value={content.executorAddress || ''}
          onChange={(e) => updateContent('executorAddress', e.target.value)}
          placeholder="Enter executor's address"
          rows={3}
        />
      </div>
      <Button 
        variant="outline" 
        size="sm"
        onClick={() => onRequestSuggestions(content.executorName + ' ' + content.executorAddress)}
      >
        <Lightbulb className="h-4 w-4 mr-2" />
        Get Suggestions
      </Button>
    </CardContent>
  </Card>
)

const BequestsEditor = ({ content, updateContent, onRequestSuggestions }) => (
  <Card>
    <CardHeader>
      <CardTitle>Bequests and Distributions</CardTitle>
      <CardDescription>
        Edit how your assets should be distributed
      </CardDescription>
    </CardHeader>
    <CardContent className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Specific Bequests</label>
        <Textarea
          value={content.bequests || ''}
          onChange={(e) => updateContent('bequests', e.target.value)}
          placeholder="List specific items and who should receive them"
          rows={5}
        />
      </div>
      <div>
        <label className="block text-sm font-medium mb-2">Residuary Estate</label>
        <Textarea
          value={content.residuary || ''}
          onChange={(e) => updateContent('residuary', e.target.value)}
          placeholder="Who should receive the remainder of your estate"
          rows={3}
        />
      </div>
      <Button 
        variant="outline" 
        size="sm"
        onClick={() => onRequestSuggestions(content.bequests + ' ' + content.residuary)}
      >
        <Lightbulb className="h-4 w-4 mr-2" />
        Get Suggestions
      </Button>
    </CardContent>
  </Card>
)

const ReviewEditor = ({ content, documentType }) => (
  <Card>
    <CardHeader>
      <CardTitle>Document Review</CardTitle>
      <CardDescription>
        Review all sections of your document
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div className="space-y-6">
        <div>
          <h4 className="font-medium text-sm text-gray-900 mb-2">Personal Information</h4>
          <div className="bg-gray-50 p-3 rounded text-sm">
            <p><strong>Name:</strong> {content.fullName || 'Not specified'}</p>
            <p><strong>Address:</strong> {content.address || 'Not specified'}</p>
          </div>
        </div>
        
        <div>
          <h4 className="font-medium text-sm text-gray-900 mb-2">
            {documentType === 'will' ? 'Executor' : 'Attorney'}
          </h4>
          <div className="bg-gray-50 p-3 rounded text-sm">
            <p><strong>Name:</strong> {content.executorName || content.attorneyName || 'Not specified'}</p>
            <p><strong>Address:</strong> {content.executorAddress || content.attorneyAddress || 'Not specified'}</p>
          </div>
        </div>
        
        {documentType === 'will' && (
          <div>
            <h4 className="font-medium text-sm text-gray-900 mb-2">Bequests</h4>
            <div className="bg-gray-50 p-3 rounded text-sm">
              <p>{content.bequests || 'No specific bequests specified'}</p>
            </div>
          </div>
        )}
      </div>
    </CardContent>
  </Card>
)

export default DocumentEditor

