import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { FileText, Shield, Heart, ArrowRight, CheckCircle, Scale, Users, Sparkles, Brain, Lock, Zap, BookOpen, Star, Award, HelpCircle, Lightbulb, Target, TrendingUp } from 'lucide-react'
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
      title: 'AI-Powered Guidance', 
      description: 'Get intelligent suggestions and contextual help at every step',
      color: 'purple'
    },
    {
      icon: Lightbulb,
      title: 'Smart Dropdowns',
      description: 'Common responses based on Ontario precedents with custom options',
      color: 'yellow'
    },
    {
      icon: HelpCircle,
      title: 'Interactive Help',
      description: 'Explanatory guidance and tips throughout the document creation',
      color: 'green'
    },
    {
      icon: Target,
      title: 'Step-by-Step Process',
      description: 'Guided workflow that makes complex legal documents simple',
      color: 'red'
    },
    {
      icon: TrendingUp,
      title: 'Professional Results',
      description: 'Documents formatted to professional legal standards',
      color: 'indigo'
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Header */}
      <motion.header 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <div className="relative">
                <motion.div
                  animate={{ rotate: [0, 5, -5, 0] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                >
                  <Scale className="h-8 w-8 text-blue-600" />
                </motion.div>
                <motion.div
                  className="absolute -top-1 -right-1"
                  animate={{ scale: [1, 1.2, 1], opacity: [1, 0.7, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Sparkles className="h-4 w-4 text-yellow-500" />
                </motion.div>
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Ontario Legal Documents</h1>
                <p className="text-xs text-gray-500 hidden sm:block">Wills & Powers of Attorney</p>
              </div>
            </motion.div>
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="flex items-center space-x-3"
            >
              <Badge variant="secondary" className="text-sm bg-green-50 text-green-700 border-green-200 flex items-center space-x-1">
                <CheckCircle className="h-3 w-3" />
                <span>Ontario Compliant</span>
              </Badge>
            </motion.div>
          </div>
        </div>
      </motion.header>

      {/* Hero Section */}
      <section className="relative py-16 sm:py-24 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-pink-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
        </div>

        <div className="max-w-6xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={mounted ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={mounted ? { scale: 1, opacity: 1 } : {}}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="mb-6"
            >
              <Badge className="px-4 py-2 text-sm bg-blue-100 text-blue-700 border-blue-300 inline-flex items-center space-x-2">
                <Brain className="h-4 w-4" />
                <span>AI-Powered Legal Document Creator</span>
              </Badge>
            </motion.div>

            <motion.h2 
              className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight"
              initial={{ opacity: 0 }}
              animate={mounted ? { opacity: 1 } : {}}
              transition={{ delay: 0.2, duration: 0.8 }}
            >
              Create Legal Documents{" "}
              <br className="hidden sm:block" />
              <motion.span 
                className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 bg-clip-text text-transparent bg-[length:200%_auto]"
                animate={{ backgroundPosition: ["0% center", "200% center", "0% center"] }}
                transition={{ duration: 5, repeat: Infinity, ease: "linear" }}
              >
                with Confidence
              </motion.span>
            </motion.h2>
            
            <motion.p 
              className="text-lg sm:text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={mounted ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.4, duration: 0.8 }}
            >
              Create legally compliant wills and powers of attorney with our interactive platform. 
              Smart dropdowns, AI-powered tips, and step-by-step guidance based on Ontario legal precedents 
              make complex documents simple.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={mounted ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 mb-16"
            >
              <Button 
                size="lg" 
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all duration-300 group"
                onClick={() => document.getElementById('document-selection')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Get Started Now
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="px-8 py-6 text-lg hover:bg-gray-50"
                onClick={() => document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })}
              >
                Learn More
              </Button>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={mounted ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.8, duration: 0.8 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
            >
              {[
                { label: 'Documents Created', value: '10,000+', icon: FileText },
                { label: 'Success Rate', value: '99.9%', icon: CheckCircle },
                { label: 'Avg. Completion', value: '15 min', icon: Zap },
                { label: 'User Rating', value: '4.9/5', icon: Star }
              ].map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={mounted ? { opacity: 1, scale: 1 } : {}}
                  transition={{ delay: 1 + index * 0.1, duration: 0.5 }}
                  className="text-center"
                >
                  <stat.icon className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                  <div className="text-2xl sm:text-3xl font-bold text-gray-900">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-blue-50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <motion.h3 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"
            >
              How Our Interactive Platform Works
            </motion.h3>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-lg text-gray-600 max-w-3xl mx-auto"
            >
              Our intelligent system guides you through document creation with smart suggestions 
              based on Ontario legal precedents and best practices
            </motion.p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {[
              {
                step: '1',
                title: 'Smart Dropdowns',
                description: 'Select from common options based on Ontario precedents, or choose "Other" to enter your custom response',
                icon: Lightbulb,
                color: 'blue'
              },
              {
                step: '2',
                title: 'AI-Powered Tips',
                description: 'Get optional contextual guidance and explanations at each stage, powered by AI and legal expertise',
                icon: Brain,
                color: 'purple'
              },
              {
                step: '3',
                title: 'Interactive Help',
                description: 'Access detailed explanations, examples, and best practices with a simple click on any section',
                icon: HelpCircle,
                color: 'green'
              }
            ].map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                className="relative"
              >
                <Card className="h-full border-2 border-gray-200 hover:border-blue-400 transition-all duration-300 hover:shadow-xl">
                  <CardHeader>
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${
                        item.color === 'blue' ? 'from-blue-500 to-cyan-500' :
                        item.color === 'purple' ? 'from-purple-500 to-pink-500' :
                        'from-green-500 to-emerald-500'
                      } flex items-center justify-center text-white font-bold text-xl`}>
                        {item.step}
                      </div>
                      <item.icon className={`h-8 w-8 ${
                        item.color === 'blue' ? 'text-blue-600' :
                        item.color === 'purple' ? 'text-purple-600' :
                        'text-green-600'
                      }`} />
                    </div>
                    <CardTitle className="text-xl mb-2">{item.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base leading-relaxed">
                      {item.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <motion.h3 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4"
            >
              Comprehensive Features
            </motion.h3>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-lg text-gray-600"
            >
              Everything you need for professional legal documents
            </motion.p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const colorClasses = {
                blue: { gradient: 'from-blue-500 to-cyan-500', bg: 'from-blue-100 to-cyan-100', icon: 'text-blue-600' },
                purple: { gradient: 'from-purple-500 to-pink-500', bg: 'from-purple-100 to-pink-100', icon: 'text-purple-600' },
                yellow: { gradient: 'from-yellow-500 to-orange-500', bg: 'from-yellow-100 to-orange-100', icon: 'text-yellow-600' },
                green: { gradient: 'from-green-500 to-emerald-500', bg: 'from-green-100 to-emerald-100', icon: 'text-green-600' },
                red: { gradient: 'from-red-500 to-pink-500', bg: 'from-red-100 to-pink-100', icon: 'text-red-600' },
                indigo: { gradient: 'from-indigo-500 to-purple-500', bg: 'from-indigo-100 to-purple-100', icon: 'text-indigo-600' }
              };
              const colors = colorClasses[feature.color] || colorClasses.blue;
              
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.6 }}
                  whileHover={{ y: -8, transition: { duration: 0.2 } }}
                  className="relative p-8 rounded-2xl bg-gradient-to-br from-white to-gray-50 shadow-md hover:shadow-xl border border-gray-100 transition-all duration-300 group"
                >
                  <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${colors.gradient} rounded-t-2xl`}></div>
                  <motion.div 
                    className={`inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br ${colors.bg} mb-4 group-hover:scale-110 transition-transform duration-300`}
                  >
                    <feature.icon className={`h-7 w-7 ${colors.icon}`} />
                  </motion.div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Document Selection */}
      <section id="document-selection" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <Badge className="mb-4 px-4 py-2 bg-purple-100 text-purple-700 border-purple-300">
              <FileText className="h-4 w-4 mr-2 inline" />
              Select Your Document
            </Badge>
            <h3 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
              Choose Your Document Type
            </h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Select the legal document you need. Each document is professionally formatted and fully compliant with Ontario legal requirements.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {documentTypes.map((doc, index) => (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.15 }}
                whileHover={{ y: -8, transition: { duration: 0.3 } }}
              >
                <Card 
                  className={`h-full cursor-pointer transition-all duration-300 hover:shadow-2xl border-2 ${
                    selectedDocument === doc.id 
                      ? 'ring-4 ring-blue-400 border-blue-500 shadow-xl' 
                      : 'border-gray-200 hover:border-blue-300'
                  } bg-white relative overflow-hidden group`}
                  onClick={() => setSelectedDocument(doc.id)}
                >
                  {/* Gradient overlay */}
                  <div className={`absolute top-0 left-0 w-full h-2 bg-gradient-to-r ${
                    doc.id === 'will' ? 'from-blue-500 to-cyan-500' :
                    doc.id === 'poa_property' ? 'from-green-500 to-emerald-500' :
                    'from-red-500 to-pink-500'
                  }`}></div>
                  
                  <CardHeader className="pb-4 pt-6">
                    <div className="flex items-start justify-between mb-4">
                      <motion.div 
                        className={`p-4 rounded-xl ${doc.color} text-white shadow-lg`}
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        transition={{ duration: 0.2 }}
                      >
                        <doc.icon className="h-8 w-8" />
                      </motion.div>
                      <Badge variant="outline" className="text-xs border-2 px-3 py-1 font-semibold">
                        <Zap className="h-3 w-3 mr-1 inline" />
                        {doc.estimatedTime}
                      </Badge>
                    </div>
                    <CardTitle className="text-2xl mb-2 group-hover:text-blue-600 transition-colors">
                      {doc.title}
                    </CardTitle>
                    <CardDescription className="text-base leading-relaxed">
                      {doc.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="space-y-3 mb-6 border-t pt-4">
                      <p className="text-sm font-semibold text-gray-700 mb-2">Key Features:</p>
                      {doc.features.map((feature, idx) => (
                        <motion.div 
                          key={idx} 
                          initial={{ opacity: 0, x: -10 }}
                          whileInView={{ opacity: 1, x: 0 }}
                          viewport={{ once: true }}
                          transition={{ delay: idx * 0.05 }}
                          className="flex items-start space-x-3 text-sm text-gray-700"
                        >
                          <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="leading-tight">{feature}</span>
                        </motion.div>
                      ))}
                    </div>
                    <Button 
                      className={`w-full group relative overflow-hidden font-semibold py-6 text-base ${
                        doc.id === 'will' ? 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700' :
                        doc.id === 'poa_property' ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700' :
                        'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700'
                      } text-white shadow-lg hover:shadow-xl transition-all duration-300`}
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCreateDocument(doc.id)
                      }}
                      disabled={isLoading}
                    >
                      {isLoading && selectedDocument === doc.id ? (
                        <motion.div 
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="flex items-center justify-center"
                        >
                          <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            className="mr-2"
                          >
                            <Sparkles className="h-5 w-5" />
                          </motion.div>
                          Preparing Document...
                        </motion.div>
                      ) : (
                        <>
                          <span className="relative z-10">Start Creating</span>
                          <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-2 relative z-10" />
                          <motion.div
                            className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity duration-300"
                          />
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

