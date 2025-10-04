import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Brain, 
  FileText, 
  Sparkles, 
  Shield,
  Zap,
  Users,
  Scale,
  CheckCircle,
  ArrowRight,
  Star,
  Award,
  Clock,
  Download,
  Eye,
  Layers,
  PlusCircle,
  Heart,
  TrendingUp,
  Activity,
  BarChart3,
  Filter,
  Search,
  Calendar,
  MessageSquare,
  Bell,
  Plus,
  ChevronRight,
  Bookmark,
  Globe,
  Target
} from 'lucide-react';

const SimpleDemoShowcase = () => {
  const navigate = useNavigate();
  const [activeDemo, setActiveDemo] = useState(null);
  const [isVisible, setIsVisible] = useState(false);
  const [showDocumentTypes, setShowDocumentTypes] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  console.log('🎨 SimpleDemoShowcase component initializing...');

  useEffect(() => {
    console.log('✅ SimpleDemoShowcase mounted successfully');
    // Set visible with a small delay to ensure smooth rendering
    setTimeout(() => {
      setIsVisible(true);
      // Signal that the app is fully loaded and ready
      window.dispatchEvent(new Event('app-ready'));
      console.log('🎉 App is fully ready and visible');
    }, 50);
  }, []);

  const documentTypes = [
    {
      id: 'will',
      title: 'Last Will & Testament',
      description: 'Plan your estate and distribute your assets',
      icon: FileText,
      color: 'from-blue-500 to-cyan-500',
      estimatedTime: '15-30 minutes'
    },
    {
      id: 'poa_property',
      title: 'Power of Attorney for Property',
      description: 'Authorize financial and property decisions',
      icon: Shield,
      color: 'from-green-500 to-emerald-500',
      estimatedTime: '10-20 minutes'
    },
    {
      id: 'poa_care',
      title: 'Power of Attorney for Personal Care',
      description: 'Authorize healthcare and personal decisions',
      icon: Heart,
      color: 'from-red-500 to-pink-500',
      estimatedTime: '10-20 minutes'
    }
  ];

  const features = [
    {
      id: 'ai-assistant',
      title: 'AI Legal Assistant',
      description: 'Advanced AI-powered legal guidance with real-time compliance checking and Ontario case law integration',
      icon: Brain,
      color: 'from-blue-500 to-purple-600',
      highlights: [
        'Real-time compliance checking',
        'Ontario case law integration',
        'Plain language explanations',
        'Smart document suggestions'
      ],
      demo: 'Interactive AI chat with legal document analysis'
    },
    {
      id: 'document-creator',
      title: 'Professional Document Creator',
      description: 'Create legally compliant documents with step-by-step guidance and professional formatting',
      icon: FileText,
      color: 'from-green-500 to-blue-600',
      highlights: [
        'Step-by-step guided process',
        'Professional legal formatting',
        'Compliance validation',
        'Multiple document templates'
      ],
      demo: 'Visual document builder with live preview'
    },
    {
      id: 'smart-analysis',
      title: 'Smart Document Analysis',
      description: 'Intelligent document analysis with optimization suggestions and error detection',
      icon: Sparkles,
      color: 'from-purple-500 to-pink-600',
      highlights: [
        'Advanced document optimization',
        'Real-time error detection',
        'Completeness verification',
        'Best practice recommendations'
      ],
      demo: 'Document analysis dashboard with insights'
    }
  ];

  const stats = [
    { label: 'Documents Created', value: '15,000+', icon: FileText, trend: '+12%' },
    { label: 'Active Users', value: '8,500+', icon: Users, trend: '+23%' },
    { label: 'Success Rate', value: '99.9%', icon: CheckCircle, trend: '+0.1%' },
    { label: 'Legal Compliance', value: '100%', icon: Shield, trend: 'Perfect' }
  ];

  const testimonials = [
    {
      name: 'Sarah Mitchell',
      role: 'Family Lawyer',
      content: 'This tool has revolutionized how I help clients with estate planning. The AI assistance is incredibly accurate.',
      rating: 5
    },
    {
      name: 'David Chen',
      role: 'Individual User',
      content: 'Creating my will was so much easier than I expected. The guidance was clear and thorough.',
      rating: 5
    },
    {
      name: 'Maria Rodriguez',
      role: 'Legal Aid Clinic',
      content: 'Perfect for helping clients understand complex legal requirements in simple terms.',
      rating: 5
    }
  ];

  return (
    <div className={`min-h-screen bg-gray-50 dark:bg-gray-900 transition-all duration-500 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      {/* Header Section with Breadcrumbs and Actions */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-16 lg:top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                <Target className="h-6 w-6 mr-2 text-blue-500" />
                Dashboard
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Welcome back! Create and manage your legal documents
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors">
                <Bell className="h-5 w-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <button
                onClick={() => setShowDocumentTypes(true)}
                className="flex items-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg"
              >
                <Plus className="h-4 w-4 mr-2" />
                New Document
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Stats Dashboard */}
        <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 transform transition-all duration-700 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <FileText className="h-6 w-6" />
              </div>
              <div className="flex items-center text-sm">
                <TrendingUp className="h-4 w-4 mr-1" />
                <span>+12%</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-1">15,247</div>
            <div className="text-blue-100 text-sm">Documents Created</div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <Users className="h-6 w-6" />
              </div>
              <div className="flex items-center text-sm">
                <TrendingUp className="h-4 w-4 mr-1" />
                <span>+23%</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-1">8,592</div>
            <div className="text-purple-100 text-sm">Active Users</div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <CheckCircle className="h-6 w-6" />
              </div>
              <div className="flex items-center text-sm">
                <Activity className="h-4 w-4 mr-1" />
                <span>100%</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-1">99.9%</div>
            <div className="text-green-100 text-sm">Success Rate</div>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer">
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <Shield className="h-6 w-6" />
              </div>
              <div className="flex items-center text-sm">
                <CheckCircle className="h-4 w-4 mr-1" />
                <span>Perfect</span>
              </div>
            </div>
            <div className="text-3xl font-bold mb-1">100%</div>
            <div className="text-orange-100 text-sm">Legal Compliance</div>
          </div>
        </div>

        {/* Search and Filter Bar */}
        <div className={`bg-white dark:bg-gray-800 rounded-xl shadow-md p-4 mb-8 transform transition-all duration-700 delay-100 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search documents, templates, or features..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedFilter('all')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  selectedFilter === 'all'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setSelectedFilter('wills')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  selectedFilter === 'wills'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                Wills
              </button>
              <button
                onClick={() => setSelectedFilter('poa')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  selectedFilter === 'poa'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                POA
              </button>
            </div>
          </div>
        </div>

        {/* Main Content Grid - Two Column Layout */}
        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          {/* Left Column - Document Creation Cards */}
          <div className={`lg:col-span-2 space-y-6 transform transition-all duration-700 delay-200 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                  <Sparkles className="h-5 w-5 mr-2 text-yellow-500" />
                  Quick Start - Create Your Document
                </h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Choose a document type to begin the creation process
                </p>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-2 gap-4">
                  {documentTypes.map((docType) => (
                    <button
                      key={docType.id}
                      onClick={() => {
                        console.log(`Creating document: ${docType.id}`);
                        alert(`Document creation for "${docType.title}" will open the creation wizard. This is a demo version showcasing the new dashboard layout.`);
                      }}
                      className="group relative bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 rounded-xl p-6 border-2 border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 text-left"
                    >
                      <div className={`w-14 h-14 bg-gradient-to-r ${docType.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-lg`}>
                        <docType.icon className="h-7 w-7 text-white" />
                      </div>
                      <h3 className="font-bold text-gray-900 dark:text-white mb-2">
                        {docType.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                        {docType.description}
                      </p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                          <Clock className="h-3 w-3 mr-1" />
                          {docType.estimatedTime}
                        </div>
                        <ChevronRight className="h-5 w-5 text-blue-500 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Feature Showcase Grid */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                  <Zap className="h-5 w-5 mr-2 text-purple-500" />
                  Platform Features
                </h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Powerful tools to help you create professional documents
                </p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {features.map((feature, index) => (
                    <div
                      key={feature.id}
                      onClick={() => setActiveDemo(activeDemo === feature.id ? null : feature.id)}
                      className={`group cursor-pointer bg-gray-50 dark:bg-gray-700/50 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/10 dark:hover:to-purple-900/10 rounded-xl p-5 border border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 ${
                        activeDemo === feature.id ? 'ring-2 ring-blue-500 bg-blue-50/50 dark:bg-blue-900/20' : ''
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform shadow-md`}>
                          <feature.icon className="h-6 w-6 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-bold text-gray-900 dark:text-white mb-1 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                            {feature.title}
                          </h3>
                          <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                            {feature.description}
                          </p>
                          {activeDemo === feature.id && (
                            <div className="mt-3 space-y-2">
                              {feature.highlights.map((highlight, idx) => (
                                <div key={idx} className="flex items-center text-sm text-gray-700 dark:text-gray-300">
                                  <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                                  <span>{highlight}</span>
                                </div>
                              ))}
                              <button className="mt-3 w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-600 hover:to-purple-600 transition-all duration-200 flex items-center justify-center">
                                <PlusCircle className="h-4 w-4 mr-2" />
                                Try {feature.title}
                              </button>
                            </div>
                          )}
                        </div>
                        <ChevronRight className={`h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-all ${activeDemo === feature.id ? 'rotate-90' : ''}`} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Activity and Info */}
          <div className={`space-y-6 transform transition-all duration-700 delay-300 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
            {/* Recent Activity */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-green-500" />
                  Recent Activity
                </h3>
              </div>
              <div className="p-6 space-y-4">
                <div className="flex items-start space-x-3 pb-4 border-b border-gray-100 dark:border-gray-700">
                  <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center flex-shrink-0">
                    <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">New Will Created</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">2 hours ago</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 pb-4 border-b border-gray-100 dark:border-gray-700">
                  <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center flex-shrink-0">
                    <Shield className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">POA Approved</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">5 hours ago</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center flex-shrink-0">
                    <Users className="h-5 w-5 text-green-600 dark:text-green-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">New User Registered</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">1 day ago</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Links */}
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl shadow-md overflow-hidden text-white p-6">
              <h3 className="text-lg font-bold mb-4 flex items-center">
                <Bookmark className="h-5 w-5 mr-2" />
                Quick Links
              </h3>
              <div className="space-y-3">
                <button className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-lg p-3 text-left transition-all duration-200 flex items-center justify-between">
                  <span className="text-sm font-medium">Legal Resources</span>
                  <ChevronRight className="h-4 w-4" />
                </button>
                <button className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-lg p-3 text-left transition-all duration-200 flex items-center justify-between">
                  <span className="text-sm font-medium">Help Center</span>
                  <ChevronRight className="h-4 w-4" />
                </button>
                <button className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-lg p-3 text-left transition-all duration-200 flex items-center justify-between">
                  <span className="text-sm font-medium">Contact Support</span>
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Testimonial Card */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden p-6">
              <div className="flex items-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-sm text-gray-700 dark:text-gray-300 italic mb-4">
                "This platform has made creating legal documents so much easier. Highly recommended!"
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mr-3">
                  <span className="text-white font-bold text-sm">SM</span>
                </div>
                <div>
                  <div className="font-semibold text-sm text-gray-900 dark:text-white">Sarah Mitchell</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Family Lawyer</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA Section */}
        <div className={`bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-2xl shadow-xl overflow-hidden transform transition-all duration-700 delay-400 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="p-8 md:p-12 text-center text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Create Your Document?
            </h2>
            <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of satisfied users who trust our platform for their legal document needs
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => setShowDocumentTypes(true)}
                className="bg-white text-blue-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg flex items-center justify-center"
              >
                Start Creating Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </button>
              <button
                onClick={() => alert('Sample documents feature coming soon!')}
                className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-8 rounded-xl border-2 border-white/50 hover:border-white transition-all duration-300 flex items-center justify-center"
              >
                <Download className="mr-2 h-5 w-5" />
                View Samples
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Document Type Selection Modal */}
      {showDocumentTypes && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowDocumentTypes(false)}>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Choose Your Document Type
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Select a document type to begin the creation process
              </p>
            </div>
            <div className="p-6">
              <div className="grid md:grid-cols-3 gap-6">
                {documentTypes.map((docType) => (
                  <button
                    key={docType.id}
                    onClick={() => {
                      console.log(`Creating document: ${docType.id}`);
                      alert(`Document creation for "${docType.title}" will open the creation wizard. This is a demo showcasing the new dashboard layout.`);
                      setShowDocumentTypes(false);
                    }}
                    className="group bg-gradient-to-br from-gray-50 to-white dark:from-gray-700 dark:to-gray-800 hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 rounded-xl p-6 border-2 border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 text-left"
                  >
                    <div className={`w-16 h-16 bg-gradient-to-r ${docType.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-lg`}>
                      <docType.icon className="h-8 w-8 text-white" />
                    </div>
                    <h3 className="font-bold text-gray-900 dark:text-white mb-2">
                      {docType.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                      {docType.description}
                    </p>
                    <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                      <Clock className="h-3 w-3 mr-1" />
                      {docType.estimatedTime}
                    </div>
                  </button>
                ))}
              </div>
            </div>
            <div className="p-6 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => setShowDocumentTypes(false)}
                className="w-full py-3 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white font-medium transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SimpleDemoShowcase;
