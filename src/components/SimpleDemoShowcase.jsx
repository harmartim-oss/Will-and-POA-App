import React, { useState, useEffect } from 'react';
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
  PlusCircle
} from 'lucide-react';

const SimpleDemoShowcase = () => {
  const [activeDemo, setActiveDemo] = useState(null);
  const [isVisible, setIsVisible] = useState(false);

  console.log('🎨 SimpleDemoShowcase component initializing...');

  useEffect(() => {
    console.log('✅ SimpleDemoShowcase mounted successfully');
    setIsVisible(true);
  }, []);

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
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-purple-900 transition-all duration-1000 ${isVisible ? 'opacity-100' : 'opacity-0'}`}>
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-purple-600/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-green-400/20 to-blue-600/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-60 h-60 bg-gradient-to-r from-purple-400/10 to-pink-400/10 rounded-full blur-2xl animate-pulse" style={{animationDelay: '4s'}}></div>
      </div>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className={`transform transition-all duration-1000 delay-300 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6">
                <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent animate-pulse">
                  Ontario Wills
                </span>
                <br />
                <span className="text-gray-800 dark:text-gray-200">
                  & Power of Attorney Creator
                </span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
                Professional legal document creation with <span className="font-semibold text-blue-600 dark:text-blue-400">AI assistance</span>. 
                Create legally compliant wills and POA documents with confidence and ease.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                  <span className="flex items-center justify-center">
                    Get Started Free
                    <ArrowRight className="inline-block ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </span>
                </button>
                <button className="group bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm text-gray-900 dark:text-white font-semibold py-4 px-8 rounded-xl border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-all duration-300 hover:shadow-lg">
                  <span className="flex items-center justify-center">
                    <Eye className="mr-2 h-5 w-5" />
                    Watch Demo
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Stats Section */}
      <div className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-md border-t border-gray-200/50 dark:border-gray-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className={`transform transition-all duration-1000 delay-500 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center group cursor-default">
                  <div className="flex justify-center mb-4">
                    <div className="p-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-110">
                      <stat.icon className="h-8 w-8 text-white" />
                    </div>
                  </div>
                  <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {stat.value}
                  </div>
                  <div className="text-gray-600 dark:text-gray-300 mb-1">
                    {stat.label}
                  </div>
                  <div className="text-sm text-green-600 dark:text-green-400 font-medium">
                    {stat.trend}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className={`transform transition-all duration-1000 delay-700 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Features</span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Everything you need to create professional, legally compliant documents with confidence and ease
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.id}
                className={`group bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 cursor-pointer transform hover:scale-105 border border-gray-200/50 dark:border-gray-700/50 ${
                  activeDemo === feature.id ? 'ring-2 ring-blue-500 bg-blue-50/50 dark:bg-blue-900/20' : ''
                }`}
                onClick={() => setActiveDemo(activeDemo === feature.id ? null : feature.id)}
                style={{animationDelay: `${index * 200}ms`}}
              >
                <div className={`w-20 h-20 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                  <feature.icon className="h-10 w-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
                  {feature.description}
                </p>
                <ul className="space-y-3 mb-6">
                  {feature.highlights.map((highlight, idx) => (
                    <li key={idx} className="flex items-center text-gray-700 dark:text-gray-300">
                      <CheckCircle className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-sm">{highlight}</span>
                    </li>
                  ))}
                </ul>
                
                {activeDemo === feature.id && (
                  <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-700 dark:to-gray-600 rounded-2xl border border-blue-200/50 dark:border-blue-400/30 animate-fade-in">
                    <div className="flex items-center mb-3">
                      <Layers className="h-5 w-5 text-blue-500 mr-2" />
                      <span className="font-semibold text-blue-700 dark:text-blue-300">Demo Preview</span>
                    </div>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
                      {feature.demo}
                    </p>
                    <button className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-600 hover:to-purple-600 transition-all duration-200 flex items-center justify-center">
                      <PlusCircle className="h-4 w-4 mr-2" />
                      Try Feature
                    </button>
                  </div>
                )}
                
                <div className="text-center mt-4">
                  <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">
                    {activeDemo === feature.id ? 'Hide Details' : 'View Details'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Enhanced Testimonials Section */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className={`transform transition-all duration-1000 delay-900 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                What Our <span className="text-yellow-300">Users Say</span>
              </h2>
              <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                Trusted by legal professionals and individuals across Ontario
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <div key={index} className="group bg-white/15 backdrop-blur-md rounded-3xl p-6 text-white hover:bg-white/20 transition-all duration-300 border border-white/20 hover:border-white/30">
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-lg mb-6 italic leading-relaxed">
                    "{testimonial.content}"
                  </p>
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mr-4">
                      <span className="text-white font-bold text-lg">
                        {testimonial.name.charAt(0)}
                      </span>
                    </div>
                    <div>
                      <div className="font-semibold text-white">{testimonial.name}</div>
                      <div className="text-blue-200 text-sm">{testimonial.role}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Call to Action */}
      <div className="bg-white dark:bg-gray-900 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 dark:from-blue-900/20 dark:to-purple-900/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className={`transform transition-all duration-1000 delay-1100 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
            <div className="text-center">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
                Ready to Get <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Started?</span>
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
                Create your legally compliant will or power of attorney document today. 
                Join thousands of satisfied users who trust our platform.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
                <button className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
                  <span className="flex items-center justify-center">
                    Start Creating Your Document
                    <ArrowRight className="inline-block ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </span>
                </button>
                <button className="group bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white font-semibold py-4 px-8 rounded-xl border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-all duration-300">
                  <span className="flex items-center justify-center">
                    <Download className="mr-2 h-5 w-5" />
                    Download Sample
                  </span>
                </button>
              </div>
              
              {/* Trust Indicators */}
              <div className="flex flex-wrap justify-center items-center gap-6 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-green-500" />
                  Bank-level Security
                </div>
                <div className="flex items-center">
                  <Award className="h-4 w-4 mr-2 text-blue-500" />
                  Legally Compliant
                </div>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-2 text-purple-500" />
                  24/7 Support
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleDemoShowcase;