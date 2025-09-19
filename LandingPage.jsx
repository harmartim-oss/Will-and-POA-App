import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { FileText, Shield, Heart, ArrowRight, CheckCircle, Scale, Users } from 'lucide-react'
import { motion } from 'framer-motion'

const LandingPage = () => {
  const navigate = useNavigate()
  const [selectedDocument, setSelectedDocument] = useState(null)

  const documentTypes = [
    {
      id: 'will',
      title: 'Last Will and Testament',
      description: 'Create a legally compliant will to distribute your assets and appoint guardians',
      icon: FileText,
      features: [
        'Asset distribution planning',
        'Executor appointment',
        'Guardian designation',
        'Specific bequests',
        'Residuary estate planning'
      ],
      color: 'bg-blue-500',
      estimatedTime: '15-30 minutes'
    },
    {
      id: 'poa_property',
      title: 'Power of Attorney for Property',
      description: 'Authorize someone to make financial and property decisions on your behalf',
      icon: Shield,
      features: [
        'Financial decision authority',
        'Property management',
        'Banking permissions',
        'Investment decisions',
        'Continuing or limited powers'
      ],
      color: 'bg-green-500',
      estimatedTime: '10-20 minutes'
    },
    {
      id: 'poa_care',
      title: 'Power of Attorney for Personal Care',
      description: 'Authorize someone to make personal care and health decisions for you',
      icon: Heart,
      features: [
        'Healthcare decisions',
        'Living arrangements',
        'Personal care choices',
        'Medical treatment consent',
        'End-of-life preferences'
      ],
      color: 'bg-red-500',
      estimatedTime: '10-20 minutes'
    }
  ]

  const features = [
    {
      icon: Scale,
      title: 'Ontario Law Compliant',
      description: 'All documents meet Ontario legal requirements and regulations'
    },
    {
      icon: CheckCircle,
      title: 'AI-Powered Suggestions',
      description: 'Get intelligent wording suggestions and legal guidance'
    },
    {
      icon: Users,
      title: 'Professional Formatting',
      description: 'Documents formatted to professional legal standards'
    }
  ]

  const handleCreateDocument = (type) => {
    navigate(`/create/${type}`)
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Scale className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Ontario Legal Documents</h1>
            </div>
            <Badge variant="secondary" className="text-sm">
              Ontario Law Compliant
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Create Legal Documents with Confidence
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Generate professionally formatted wills and power of attorney documents that comply with Ontario law. 
              Our AI-powered platform guides you through every step with intelligent suggestions and legal expertise.
            </p>
          </motion.div>

          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="grid md:grid-cols-3 gap-6 mb-12"
          >
            {features.map((feature, index) => (
              <Card key={index} className="border-0 shadow-lg">
                <CardContent className="p-6 text-center">
                  <feature.icon className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Document Selection */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="text-center mb-12"
          >
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Choose Your Document Type
            </h3>
            <p className="text-lg text-gray-600">
              Select the legal document you need to create. Each document is tailored to Ontario legal requirements.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {documentTypes.map((doc, index) => (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              >
                <Card 
                  className={`cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${
                    selectedDocument === doc.id ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => setSelectedDocument(doc.id)}
                >
                  <CardHeader className="pb-4">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={`p-3 rounded-lg ${doc.color} text-white`}>
                        <doc.icon className="h-6 w-6" />
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {doc.estimatedTime}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl">{doc.title}</CardTitle>
                    <CardDescription className="text-sm">
                      {doc.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2 mb-6">
                      {doc.features.map((feature, idx) => (
                        <div key={idx} className="flex items-center space-x-2 text-sm text-gray-600">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                    <Button 
                      className="w-full"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCreateDocument(doc.id)
                      }}
                    >
                      Create {doc.title}
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <Scale className="h-6 w-6" />
              <span className="text-lg font-semibold">Ontario Legal Documents</span>
            </div>
            <p className="text-gray-400 text-sm mb-4">
              Professional legal document creation platform compliant with Ontario law
            </p>
            <div className="flex justify-center space-x-6 text-sm text-gray-400">
              <span>© 2024 Ontario Legal Documents</span>
              <span>•</span>
              <span>Ontario Law Compliant</span>
              <span>•</span>
              <span>AI-Powered</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

