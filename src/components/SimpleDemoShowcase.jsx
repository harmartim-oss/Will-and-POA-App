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
  const [showWelcome, setShowWelcome] = useState(false);
  const [showKeyboardHint, setShowKeyboardHint] = useState(false);

  console.log('🎨 SimpleDemoShowcase component initializing...');

  useEffect(() => {
    console.log('✅ SimpleDemoShowcase mounted successfully');
    // Set visible with a small delay to ensure smooth rendering
    setTimeout(() => {
      setIsVisible(true);
      // Signal that the app is fully loaded and ready
      window.dispatchEvent(new Event('app-ready'));
      console.log('🎉 App is fully ready and visible');
      
      // Show welcome message after a brief delay
      setTimeout(() => {
        setShowWelcome(true);
        // Auto-hide welcome after 5 seconds
        setTimeout(() => setShowWelcome(false), 5000);
      }, 500);
    }, 50);
    
    // Keyboard shortcuts
    const handleKeyPress = (e) => {
      // Show keyboard hint on '?' key
      if (e.key === '?' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        setShowKeyboardHint(true);
      }
      // Close modals on Escape
      if (e.key === 'Escape') {
        setShowDocumentTypes(false);
        setShowKeyboardHint(false);
      }
      // Quick search focus on '/'
      if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        document.querySelector('input[type="text"]')?.focus();
      }
      // Quick new document on Ctrl/Cmd + N
      if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        setShowDocumentTypes(true);
      }
    };
    
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
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
      {/* Welcome Notification Toast */}
      {showWelcome && (
        <div className="fixed top-20 right-4 z-50 animate-in slide-in-from-right duration-500">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-4 rounded-xl shadow-2xl max-w-md">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0">
                <Sparkles className="h-6 w-6 text-yellow-300" />
              </div>
              <div className="flex-1">
                <h4 className="font-bold text-lg mb-1">Welcome to Ontario Legal Documents! 🎉</h4>
                <p className="text-sm text-blue-100">
                  Create professional legal documents with AI-powered assistance. All documents are Ontario law compliant.
                </p>
              </div>
              <button
                onClick={() => setShowWelcome(false)}
                className="flex-shrink-0 text-white/80 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Header Section with Breadcrumbs and Actions - Enhanced */}
      <div className="bg-white/95 dark:bg-gray-800/95 backdrop-blur-md border-b border-gray-200 dark:border-gray-700 sticky top-16 lg:top-0 z-30 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center">
                <Target className="h-7 w-7 mr-3 text-blue-500" />
                Dashboard
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2 font-medium">
                Welcome back! Create and manage your legal documents
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-all hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl">
                <Bell className="h-5 w-5" />
                <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse"></span>
              </button>
              <button
                onClick={() => setShowDocumentTypes(true)}
                className="flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02]"
              >
                <Plus className="h-5 w-5 mr-2" />
                New Document
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Stats Dashboard - Enhanced with animated gradients and depth */}
        <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 transform transition-all duration-700 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="group relative bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-[1.03] cursor-pointer overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-400/0 via-white/10 to-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white/25 rounded-xl backdrop-blur-sm shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <FileText className="h-6 w-6" />
                </div>
                <div className="flex items-center text-sm bg-white/20 px-2.5 py-1 rounded-full backdrop-blur-sm">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  <span className="font-semibold">+12%</span>
                </div>
              </div>
              <div className="text-3xl font-bold mb-1 tracking-tight">15,247</div>
              <div className="text-blue-100 text-sm font-medium">Documents Created</div>
            </div>
          </div>

          <div className="group relative bg-gradient-to-br from-purple-500 via-purple-600 to-pink-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-[1.03] cursor-pointer overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-400/0 via-white/10 to-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white/25 rounded-xl backdrop-blur-sm shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <Users className="h-6 w-6" />
                </div>
                <div className="flex items-center text-sm bg-white/20 px-2.5 py-1 rounded-full backdrop-blur-sm">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  <span className="font-semibold">+23%</span>
                </div>
              </div>
              <div className="text-3xl font-bold mb-1 tracking-tight">8,592</div>
              <div className="text-purple-100 text-sm font-medium">Active Users</div>
            </div>
          </div>

          <div className="group relative bg-gradient-to-br from-green-500 via-emerald-600 to-teal-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-[1.03] cursor-pointer overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-tr from-green-400/0 via-white/10 to-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white/25 rounded-xl backdrop-blur-sm shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <CheckCircle className="h-6 w-6" />
                </div>
                <div className="flex items-center text-sm bg-white/20 px-2.5 py-1 rounded-full backdrop-blur-sm">
                  <Activity className="h-4 w-4 mr-1" />
                  <span className="font-semibold">100%</span>
                </div>
              </div>
              <div className="text-3xl font-bold mb-1 tracking-tight">99.9%</div>
              <div className="text-green-100 text-sm font-medium">Success Rate</div>
            </div>
          </div>

          <div className="group relative bg-gradient-to-br from-orange-500 via-red-500 to-rose-600 rounded-2xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-[1.03] cursor-pointer overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-tr from-orange-400/0 via-white/10 to-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-white/25 rounded-xl backdrop-blur-sm shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <Shield className="h-6 w-6" />
                </div>
                <div className="flex items-center text-sm bg-white/20 px-2.5 py-1 rounded-full backdrop-blur-sm">
                  <CheckCircle className="h-4 w-4 mr-1" />
                  <span className="font-semibold">Perfect</span>
                </div>
              </div>
              <div className="text-3xl font-bold mb-1 tracking-tight">100%</div>
              <div className="text-orange-100 text-sm font-medium">Legal Compliance</div>
            </div>
          </div>
        </div>

        {/* Search and Filter Bar - Enhanced with better depth and styling */}
        <div className={`bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-5 mb-8 transform transition-all duration-700 delay-100 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
              <input
                type="text"
                placeholder="Search documents, templates, or features..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-gray-50 dark:bg-gray-700/50 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:text-white transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
            <div className="flex gap-2 flex-wrap sm:flex-nowrap">
              <button
                onClick={() => setSelectedFilter('all')}
                className={`px-5 py-3 rounded-xl font-semibold transition-all duration-200 ${
                  selectedFilter === 'all'
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md hover:shadow-lg scale-105'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setSelectedFilter('wills')}
                className={`px-5 py-3 rounded-xl font-semibold transition-all duration-200 ${
                  selectedFilter === 'wills'
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md hover:shadow-lg scale-105'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105'
                }`}
              >
                Wills
              </button>
              <button
                onClick={() => setSelectedFilter('poa')}
                className={`px-5 py-3 rounded-xl font-semibold transition-all duration-200 ${
                  selectedFilter === 'poa'
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md hover:shadow-lg scale-105'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 hover:scale-105'
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
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden">
              <div className="p-6 bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-gray-800 dark:via-gray-750 dark:to-gray-800 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                  <Sparkles className="h-6 w-6 mr-2 text-yellow-500 animate-pulse" />
                  Quick Start - Create Your Document
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Choose a document type to begin the creation process
                </p>
              </div>
              <div className="p-6">
                <div className="grid md:grid-cols-2 gap-5">
                  {documentTypes.map((docType) => (
                    <button
                      key={docType.id}
                      onClick={() => {
                        console.log(`Creating document: ${docType.id}`);
                        alert(`Document creation for "${docType.title}" will open the creation wizard. This is a demo version showcasing the new dashboard layout.`);
                      }}
                      className="group relative bg-gradient-to-br from-white to-gray-50 dark:from-gray-700 dark:to-gray-600 hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/30 dark:hover:to-purple-900/30 rounded-xl p-6 border-2 border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 text-left shadow-md hover:shadow-xl hover:-translate-y-1"
                    >
                      <div className={`w-16 h-16 bg-gradient-to-br ${docType.color} rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg`}>
                        <docType.icon className="h-8 w-8 text-white" />
                      </div>
                      <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                        {docType.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
                        {docType.description}
                      </p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-full">
                          <Clock className="h-3.5 w-3.5 mr-1.5" />
                          {docType.estimatedTime}
                        </div>
                        <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center group-hover:bg-blue-500 transition-colors">
                          <ChevronRight className="h-5 w-5 text-blue-600 dark:text-blue-400 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Feature Showcase Grid - Enhanced with better visual hierarchy */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden">
              <div className="p-6 bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50 dark:from-gray-800 dark:via-gray-750 dark:to-gray-800 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                  <Zap className="h-6 w-6 mr-2 text-purple-500" />
                  Platform Features
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Powerful tools to help you create professional documents
                </p>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {features.map((feature, index) => (
                    <div
                      key={feature.id}
                      onClick={() => setActiveDemo(activeDemo === feature.id ? null : feature.id)}
                      className={`group cursor-pointer bg-gradient-to-br from-white to-gray-50 dark:from-gray-700/50 dark:to-gray-700 hover:from-blue-50 hover:via-purple-50 hover:to-pink-50 dark:hover:from-blue-900/20 dark:hover:via-purple-900/20 dark:hover:to-pink-900/20 rounded-xl p-5 border-2 border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 shadow-md hover:shadow-lg ${
                        activeDemo === feature.id ? 'ring-2 ring-blue-500 border-blue-500 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/30 dark:to-purple-900/30 shadow-lg' : ''
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300 shadow-lg`}>
                          <feature.icon className="h-7 w-7 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-1.5 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                            {feature.title}
                          </h3>
                          <p className="text-sm text-gray-600 dark:text-gray-300 mb-3 leading-relaxed">
                            {feature.description}
                          </p>
                          {activeDemo === feature.id && (
                            <div className="mt-4 space-y-2.5 animate-in fade-in duration-300">
                              {feature.highlights.map((highlight, idx) => (
                                <div key={idx} className="flex items-start text-sm text-gray-700 dark:text-gray-300">
                                  <CheckCircle className="h-5 w-5 text-green-500 mr-2.5 flex-shrink-0 mt-0.5" />
                                  <span>{highlight}</span>
                                </div>
                              ))}
                              <button className="mt-4 w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white px-5 py-3 rounded-xl text-sm font-semibold hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 transition-all duration-200 flex items-center justify-center shadow-md hover:shadow-lg hover:scale-[1.02]">
                                <PlusCircle className="h-5 w-5 mr-2" />
                                Try {feature.title}
                              </button>
                            </div>
                          )}
                        </div>
                        <div className={`w-8 h-8 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center group-hover:bg-blue-100 dark:group-hover:bg-blue-900/30 transition-all ${activeDemo === feature.id ? 'bg-blue-500 dark:bg-blue-600' : ''}`}>
                          <ChevronRight className={`h-5 w-5 text-gray-400 group-hover:text-blue-600 transition-all duration-300 ${activeDemo === feature.id ? 'rotate-90 text-white' : ''}`} />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Activity and Info - Enhanced with modern styling */}
          <div className={`space-y-6 transform transition-all duration-700 delay-300 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
            {/* Recent Activity */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden">
              <div className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-gray-800 dark:to-gray-750 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
                  <Activity className="h-5 w-5 mr-2 text-green-500" />
                  Recent Activity
                </h3>
              </div>
              <div className="p-6 space-y-4">
                <div className="group flex items-start space-x-3 pb-4 border-b border-gray-100 dark:border-gray-700 hover:bg-blue-50 dark:hover:bg-blue-900/10 -mx-3 px-3 py-2 rounded-lg transition-all">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md group-hover:scale-110 transition-transform">
                    <FileText className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">New Will Created</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center mt-1">
                      <Clock className="h-3 w-3 mr-1" />
                      2 hours ago
                    </p>
                  </div>
                </div>
                <div className="group flex items-start space-x-3 pb-4 border-b border-gray-100 dark:border-gray-700 hover:bg-purple-50 dark:hover:bg-purple-900/10 -mx-3 px-3 py-2 rounded-lg transition-all">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md group-hover:scale-110 transition-transform">
                    <Shield className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">POA Approved</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center mt-1">
                      <Clock className="h-3 w-3 mr-1" />
                      5 hours ago
                    </p>
                  </div>
                </div>
                <div className="group flex items-start space-x-3 hover:bg-green-50 dark:hover:bg-green-900/10 -mx-3 px-3 py-2 rounded-lg transition-all">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md group-hover:scale-110 transition-transform">
                    <Users className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-900 dark:text-white">New User Registered</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center mt-1">
                      <Clock className="h-3 w-3 mr-1" />
                      1 day ago
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Links - Enhanced with better gradients */}
            <div className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl shadow-xl overflow-hidden text-white p-6">
              <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-white/20"></div>
              <div className="relative z-10">
                <h3 className="text-lg font-bold mb-5 flex items-center">
                  <Bookmark className="h-5 w-5 mr-2" />
                  Quick Links
                </h3>
                <div className="space-y-3">
                  <button className="group w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all duration-200 flex items-center justify-between shadow-md hover:shadow-lg hover:scale-[1.02]">
                    <span className="text-sm font-semibold">Legal Resources</span>
                    <ChevronRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                  <button className="group w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all duration-200 flex items-center justify-between shadow-md hover:shadow-lg hover:scale-[1.02]">
                    <span className="text-sm font-semibold">Help Center</span>
                    <ChevronRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                  <button className="group w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl p-4 text-left transition-all duration-200 flex items-center justify-between shadow-md hover:shadow-lg hover:scale-[1.02]">
                    <span className="text-sm font-semibold">Contact Support</span>
                    <ChevronRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>
            </div>

            {/* Testimonial Card - Enhanced styling */}
            <div className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl shadow-xl border-2 border-gray-100 dark:border-gray-700 overflow-hidden p-6">
              <div className="flex items-center mb-4 space-x-1">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current drop-shadow-sm" />
                ))}
              </div>
              <p className="text-sm text-gray-700 dark:text-gray-300 italic mb-5 leading-relaxed">
                "This platform has made creating legal documents so much easier. Highly recommended!"
              </p>
              <div className="flex items-center">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center mr-3 shadow-lg">
                  <span className="text-white font-bold text-base">SM</span>
                </div>
                <div>
                  <div className="font-bold text-sm text-gray-900 dark:text-white">Sarah Mitchell</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">Family Lawyer</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA Section - Enhanced with animated gradient overlay */}
        <div className={`relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-700 delay-400 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}>
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-white/20"></div>
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjA1IiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-30"></div>
          <div className="relative z-10 p-10 md:p-16 text-center text-white">
            <h2 className="text-3xl md:text-5xl font-extrabold mb-5 tracking-tight">
              Ready to Create Your Document?
            </h2>
            <p className="text-lg md:text-xl text-white/90 mb-10 max-w-2xl mx-auto leading-relaxed">
              Join thousands of satisfied users who trust our platform for their legal document needs
            </p>
            <div className="flex flex-col sm:flex-row gap-5 justify-center">
              <button
                onClick={() => setShowDocumentTypes(true)}
                className="group bg-white text-blue-600 hover:bg-gray-50 font-bold py-4 px-10 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-3xl flex items-center justify-center"
              >
                Start Creating Now
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => alert('Sample documents feature coming soon!')}
                className="group bg-white/20 hover:bg-white/30 backdrop-blur-md text-white font-semibold py-4 px-10 rounded-2xl border-2 border-white/50 hover:border-white transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 flex items-center justify-center"
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

      {/* Keyboard Shortcuts Modal */}
      {showKeyboardHint && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowKeyboardHint(false)}>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                <Zap className="h-6 w-6 mr-2 text-yellow-500" />
                Keyboard Shortcuts
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Speed up your workflow with these handy shortcuts
              </p>
            </div>
            <div className="p-6 space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <span className="text-sm text-gray-700 dark:text-gray-300">Show this help</span>
                <kbd className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono">?</kbd>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <span className="text-sm text-gray-700 dark:text-gray-300">Focus search</span>
                <kbd className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono">/</kbd>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <span className="text-sm text-gray-700 dark:text-gray-300">New document</span>
                <div className="flex items-center space-x-1">
                  <kbd className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono">Ctrl</kbd>
                  <span className="text-gray-400">+</span>
                  <kbd className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono">N</kbd>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <span className="text-sm text-gray-700 dark:text-gray-300">Close modal</span>
                <kbd className="px-3 py-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm font-mono">Esc</kbd>
              </div>
            </div>
            <div className="p-6 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => setShowKeyboardHint(false)}
                className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium rounded-lg transition-all"
              >
                Got it!
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating Keyboard Hint Button */}
      <button
        onClick={() => setShowKeyboardHint(true)}
        className="fixed bottom-6 right-6 w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center z-40 group"
        title="Keyboard Shortcuts (Press ?)"
      >
        <span className="text-xl font-bold group-hover:scale-110 transition-transform">?</span>
      </button>
    </div>
  );
};

export default SimpleDemoShowcase;
