import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import LoadingSpinner from '@/components/ui/loading-spinner'
import { FileText, Shield, Heart, ArrowRight, CheckCircle, Scale, Users, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

const LandingPage = () => {
  const navigate = useNavigate()
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

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
      description: 'All documents meet Ontario legal requirements and regulations',
      color: 'blue'
    },
    {
      icon: Sparkles,
      title: 'AI-Powered Suggestions', 
      description: 'Get intelligent wording suggestions and legal guidance',
      color: 'purple'
    },
    {
      icon: Users,
      title: 'Professional Formatting',
      description: 'Documents formatted to professional legal standards',
      color: 'green'
    }
  ]

  const handleCreateDocument = async (type) => {
    setIsLoading(true)
    setSelectedDocument(type)
    
    // Simulate loading delay for better UX
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    navigate(`/create/${type}`)
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <motion.header 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="bg-white/95 backdrop-blur-md shadow-sm border-b sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <div className="relative">
                <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-lg">
                  <Scale className="h-6 w-6 text-white" />
                </div>
                <motion.div
                  className="absolute -top-1 -right-1"
                  animate={{ rotate: [0, 10, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                >
                  <Sparkles className="h-3 w-3 text-yellow-500" />
                </motion.div>
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Ontario Legal Documents</h1>
                <p className="text-xs text-gray-500 hidden sm:block">Professional • Secure • Ontario Law Compliant</p>
              </div>
            </motion.div>
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="flex items-center space-x-3"
            >
              <Badge variant="secondary" className="text-sm bg-blue-50 text-blue-700 border-blue-200">
                Ontario Law Compliant
              </Badge>
              <Badge variant="secondary" className="text-sm bg-green-50 text-green-700 border-green-200">
                AI-Powered
              </Badge>
            </motion.div>
          </div>
        </div>
      </motion.header>

      {/* Hero Section */}
      <section className="py-12 sm:py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-32 w-80 h-80 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-32 w-80 h-80 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse" style={{animationDelay: '2s'}}></div>
        </div>
        <div className="max-w-4xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={mounted ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <motion.h2 
              className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight"
              initial={{ opacity: 0 }}
              animate={mounted ? { opacity: 1 } : {}}
              transition={{ delay: 0.2, duration: 0.8 }}
            >
              Create Legal Documents with{" "}
              <motion.span 
                className="text-blue-600"
                animate={{ color: ["#2563eb", "#7c3aed", "#2563eb"] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              >
                Confidence
              </motion.span>
            </motion.h2>
            <motion.p 
              className="text-lg sm:text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={mounted ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.4, duration: 0.8 }}
            >
              Generate professionally formatted wills and power of attorney documents that comply with Ontario law. 
              Our AI-powered platform guides you through every step with intelligent suggestions and legal expertise.
            </motion.p>
          </motion.div>

          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={mounted ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="grid md:grid-cols-3 gap-6 sm:gap-8 mb-12"
          >
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={mounted ? { opacity: 1, y: 0 } : {}}
                transition={{ delay: 0.8 + index * 0.1, duration: 0.6 }}
                whileHover={{ 
                  y: -5,
                  transition: { duration: 0.2 }
                }}
                className="text-center p-6 rounded-xl bg-white shadow-sm border hover:shadow-md transition-all duration-300"
              >
                <motion.div 
                  className={`inline-flex items-center justify-center w-12 h-12 rounded-full mb-4 ${
                    feature.color === 'blue' ? 'bg-blue-100' :
                    feature.color === 'purple' ? 'bg-purple-100' : 
                    'bg-green-100'
                  }`}
                  whileHover={{ scale: 1.1, rotate: 10 }}
                  transition={{ duration: 0.2 }}
                >
                  <feature.icon className={`h-6 w-6 ${
                    feature.color === 'blue' ? 'text-blue-600' :
                    feature.color === 'purple' ? 'text-purple-600' : 
                    'text-green-600'
                  }`} />
                </motion.div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{feature.description}</p>
              </motion.div>
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
            <p className="text-lg text-gray-600 mb-8">
              Select the legal document you need to create. Each document is tailored to Ontario legal requirements.
            </p>
            
            {/* Trust indicators */}
            <div className="flex flex-wrap justify-center items-center gap-8 mb-8 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <span>Ontario Law Verified</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="h-5 w-5 text-blue-500" />
                <span>Secure & Private</span>
              </div>
              <div className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-purple-500" />
                <span>AI-Powered Guidance</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-green-500" />
                <span>1000+ Documents Created</span>
              </div>
            </div>
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
                      className="w-full group relative overflow-hidden"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCreateDocument(doc.id)
                      }}
                      disabled={isLoading}
                    >
                      {isLoading && selectedDocument === doc.id ? (
                        <div className="flex items-center">
                          <LoadingSpinner size="sm" className="mr-2" />
                          Creating Document...
                        </div>
                      ) : (
                        <>
                          Create {doc.title}
                          <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                        </>
                      )}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="text-3xl font-bold text-white mb-4">
              Ready to Create Your Legal Documents?
            </h3>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of Ontarians who have created their legal documents with confidence using our platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                variant="secondary"
                onClick={() => handleCreateDocument('will')}
                className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4"
              >
                Start with a Will
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button 
                size="lg" 
                variant="outline"
                onClick={() => handleCreateDocument('poa_property')}
                className="border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4"
              >
                Create Power of Attorney
                <Shield className="ml-2 h-5 w-5" />
              </Button>
            </div>
          </motion.div>
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

