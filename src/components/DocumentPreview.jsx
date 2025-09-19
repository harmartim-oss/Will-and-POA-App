import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { ArrowLeft, Download, FileText, Edit, Printer, Share } from 'lucide-react'
import { motion } from 'framer-motion'
import { useToast } from '@/hooks/use-toast'

const DocumentPreview = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { toast } = useToast()
  
  const [document, setDocument] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isExporting, setIsExporting] = useState(false)

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

  const handleExport = async (format) => {
    setIsExporting(true)
    try {
      const endpoint = format === 'pdf' ? 'generate-pdf' : 'generate-word'
      const response = await fetch(`/api/documents/${id}/${endpoint}`, {
        method: 'POST'
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = `${document.title}.${format === 'pdf' ? 'pdf' : 'docx'}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        
        toast({
          title: "Export Successful",
          description: `Document exported as ${format.toUpperCase()} successfully.`,
        })
      } else {
        throw new Error('Failed to export document')
      }
    } catch (error) {
      toast({
        title: "Export Failed",
        description: "Failed to export document. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsExporting(false)
    }
  }

  const getDocumentTypeTitle = (type) => {
    const titles = {
      will: 'Last Will and Testament',
      poa_property: 'Power of Attorney for Property',
      poa_care: 'Power of Attorney for Personal Care'
    }
    return titles[type] || 'Legal Document'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading document preview...</p>
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
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
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
                  {getDocumentTypeTitle(document.document_type)}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant={document.is_completed ? "default" : "secondary"}>
                {document.is_completed ? "Completed" : "Draft"}
              </Badge>
              <Button 
                variant="outline"
                onClick={() => navigate(`/edit/${id}`)}
              >
                <Edit className="h-4 w-4 mr-2" />
                Edit
              </Button>
              <Button 
                variant="outline"
                onClick={() => handleExport('pdf')}
                disabled={isExporting}
              >
                <Download className="h-4 w-4 mr-2" />
                PDF
              </Button>
              <Button 
                onClick={() => handleExport('word')}
                disabled={isExporting}
              >
                <FileText className="h-4 w-4 mr-2" />
                Word
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Document Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Card className="shadow-lg">
            <CardHeader className="bg-gray-50 border-b">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">
                    {getDocumentTypeTitle(document.document_type)}
                  </CardTitle>
                  <CardDescription className="mt-2">
                    Created: {new Date(document.created_at).toLocaleDateString()} • 
                    Last updated: {new Date(document.updated_at).toLocaleDateString()}
                  </CardDescription>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">
                    <Printer className="h-4 w-4 mr-2" />
                    Print
                  </Button>
                  <Button variant="outline" size="sm">
                    <Share className="h-4 w-4 mr-2" />
                    Share
                  </Button>
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="p-8">
              {/* Document Content */}
              <div className="prose max-w-none">
                {document.document_type === 'will' && (
                  <WillPreview content={document.content} />
                )}
                {document.document_type === 'poa_property' && (
                  <POAPropertyPreview content={document.content} />
                )}
                {document.document_type === 'poa_care' && (
                  <POACarePreview content={document.content} />
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Export Options */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-8"
        >
          <Card>
            <CardHeader>
              <CardTitle>Export Options</CardTitle>
              <CardDescription>
                Download your document in different formats for printing or sharing
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="p-2 bg-red-100 rounded">
                      <FileText className="h-5 w-5 text-red-600" />
                    </div>
                    <div>
                      <h4 className="font-medium">PDF Format</h4>
                      <p className="text-sm text-gray-600">Professional, print-ready format</p>
                    </div>
                  </div>
                  <Button 
                    className="w-full"
                    onClick={() => handleExport('pdf')}
                    disabled={isExporting}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download PDF
                  </Button>
                </div>
                
                <div className="p-4 border rounded-lg">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="p-2 bg-blue-100 rounded">
                      <FileText className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-medium">Word Document</h4>
                      <p className="text-sm text-gray-600">Editable format for further modifications</p>
                    </div>
                  </div>
                  <Button 
                    variant="outline"
                    className="w-full"
                    onClick={() => handleExport('word')}
                    disabled={isExporting}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Word
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Legal Notice */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-8"
        >
          <Card className="border-yellow-200 bg-yellow-50">
            <CardContent className="p-6">
              <div className="flex items-start space-x-3">
                <div className="p-2 bg-yellow-100 rounded">
                  <FileText className="h-5 w-5 text-yellow-600" />
                </div>
                <div>
                  <h4 className="font-medium text-yellow-800 mb-2">Important Legal Notice</h4>
                  <div className="text-sm text-yellow-700 space-y-2">
                    <p>
                      This document has been generated based on Ontario legal requirements. 
                      However, it is strongly recommended that you:
                    </p>
                    <ul className="list-disc list-inside space-y-1 ml-4">
                      <li>Have the document reviewed by a qualified lawyer</li>
                      <li>Ensure proper witnessing and signing procedures are followed</li>
                      <li>Store the original document in a safe location</li>
                      <li>Inform relevant parties of the document's existence and location</li>
                    </ul>
                    <p className="mt-3">
                      This tool provides guidance but does not constitute legal advice.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

// Preview Components
const WillPreview = ({ content }) => (
  <div className="space-y-8">
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-4">LAST WILL AND TESTAMENT</h1>
      <h2 className="text-xl font-semibold">OF {(content.fullName || '[NAME]').toUpperCase()}</h2>
    </div>
    
    <Separator />
    
    <div>
      <h3 className="text-lg font-semibold mb-3">DECLARATION</h3>
      <p className="text-justify leading-relaxed">
        I, {content.fullName || '[NAME]'}, of {content.address || '[ADDRESS]'}, 
        in the Province of Ontario, being of sound mind and disposing memory and not acting under duress, 
        menace, fraud, or undue influence of any person whomsoever, do make, publish and declare this to be 
        my Last Will and Testament, hereby revoking all former Wills and Codicils by me at any time heretofore made.
      </p>
    </div>
    
    <div>
      <h3 className="text-lg font-semibold mb-3">APPOINTMENT OF EXECUTOR</h3>
      <p className="text-justify leading-relaxed">
        I appoint {content.executorName || '[EXECUTOR NAME]'} of {content.executorAddress || '[EXECUTOR ADDRESS]'} 
        to be the Executor of this my Will.
      </p>
    </div>
    
    {content.bequests && (
      <div>
        <h3 className="text-lg font-semibold mb-3">SPECIFIC BEQUESTS</h3>
        <p className="text-justify leading-relaxed whitespace-pre-line">
          {content.bequests}
        </p>
      </div>
    )}
    
    <div>
      <h3 className="text-lg font-semibold mb-3">RESIDUARY ESTATE</h3>
      <p className="text-justify leading-relaxed">
        I give, devise and bequeath all the rest, residue and remainder of my estate, 
        both real and personal, of whatsoever nature and wheresoever situate, to {content.residuary || '[RESIDUARY BENEFICIARY]'}.
      </p>
    </div>
    
    <div className="mt-12 space-y-8">
      <p>
        IN WITNESS WHEREOF I have hereunto set my hand this _____ day of _____________, 20____.
      </p>
      
      <div className="space-y-4">
        <div>
          <div className="border-b border-gray-400 w-64 mb-2"></div>
          <p>{content.fullName || '[NAME]'}, Testator</p>
        </div>
        
        <div className="mt-8">
          <p className="text-sm text-justify leading-relaxed mb-6">
            SIGNED, PUBLISHED AND DECLARED by the above-named Testator as and for his/her Last Will and Testament, 
            in the presence of us, both present at the same time, who at his/her request, in his/her presence, 
            and in the presence of each other, have hereunto subscribed our names as witnesses.
          </p>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #1 Signature</p>
              </div>
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #1 Name (Print)</p>
              </div>
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #1 Address</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #2 Signature</p>
              </div>
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #2 Name (Print)</p>
              </div>
              <div>
                <div className="border-b border-gray-400 w-full mb-2"></div>
                <p className="text-sm">Witness #2 Address</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
)

const POAPropertyPreview = ({ content }) => (
  <div className="space-y-8">
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-4">CONTINUING POWER OF ATTORNEY FOR PROPERTY</h1>
    </div>
    
    <Separator />
    
    <div>
      <h3 className="text-lg font-semibold mb-3">GRANTOR INFORMATION</h3>
      <p className="text-justify leading-relaxed">
        I, {content.fullName || '[NAME]'}, of {content.address || '[ADDRESS]'}, 
        in the Province of Ontario, being of sound mind, do hereby appoint the person(s) named below as my attorney(s) 
        for property with authority to act on my behalf in accordance with the Substitute Decisions Act, 1992.
      </p>
    </div>
    
    <div>
      <h3 className="text-lg font-semibold mb-3">APPOINTMENT OF ATTORNEY</h3>
      <p className="text-justify leading-relaxed">
        I appoint {content.attorneyName || '[ATTORNEY NAME]'} of {content.attorneyAddress || '[ATTORNEY ADDRESS]'} 
        to be my attorney for property.
      </p>
    </div>
    
    {content.powers && (
      <div>
        <h3 className="text-lg font-semibold mb-3">POWERS GRANTED</h3>
        <p className="text-justify leading-relaxed whitespace-pre-line">
          {content.powers}
        </p>
      </div>
    )}
    
    {content.conditions && (
      <div>
        <h3 className="text-lg font-semibold mb-3">CONDITIONS AND RESTRICTIONS</h3>
        <p className="text-justify leading-relaxed whitespace-pre-line">
          {content.conditions}
        </p>
      </div>
    )}
    
    <div className="mt-12 space-y-8">
      <p>
        IN WITNESS WHEREOF I have executed this Power of Attorney this _____ day of _____________, 20____.
      </p>
      
      <div>
        <div className="border-b border-gray-400 w-64 mb-2"></div>
        <p>{content.fullName || '[NAME]'}, Grantor</p>
      </div>
    </div>
  </div>
)

const POACarePreview = ({ content }) => (
  <div className="space-y-8">
    <div className="text-center">
      <h1 className="text-3xl font-bold mb-4">POWER OF ATTORNEY FOR PERSONAL CARE</h1>
    </div>
    
    <Separator />
    
    <div>
      <h3 className="text-lg font-semibold mb-3">GRANTOR INFORMATION</h3>
      <p className="text-justify leading-relaxed">
        I, {content.fullName || '[NAME]'}, of {content.address || '[ADDRESS]'}, 
        in the Province of Ontario, being of sound mind, do hereby appoint the person(s) named below as my attorney(s) 
        for personal care with authority to make decisions about my personal care.
      </p>
    </div>
    
    <div>
      <h3 className="text-lg font-semibold mb-3">APPOINTMENT OF ATTORNEY</h3>
      <p className="text-justify leading-relaxed">
        I appoint {content.attorneyName || '[ATTORNEY NAME]'} of {content.attorneyAddress || '[ATTORNEY ADDRESS]'} 
        to be my attorney for personal care.
      </p>
    </div>
    
    {content.carePreferences && (
      <div>
        <h3 className="text-lg font-semibold mb-3">CARE PREFERENCES</h3>
        <p className="text-justify leading-relaxed whitespace-pre-line">
          {content.carePreferences}
        </p>
      </div>
    )}
    
    <div className="mt-12 space-y-8">
      <p>
        IN WITNESS WHEREOF I have executed this Power of Attorney this _____ day of _____________, 20____.
      </p>
      
      <div>
        <div className="border-b border-gray-400 w-64 mb-2"></div>
        <p>{content.fullName || '[NAME]'}, Grantor</p>
      </div>
    </div>
  </div>
)

export default DocumentPreview

