import React, { useState } from 'react';
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
  Star
} from 'lucide-react';

const SimpleDemoShowcase = () => {
  const [activeDemo, setActiveDemo] = useState(null);

  const features = [
    {
      id: 'ai-assistant',
      title: 'AI Legal Assistant',
      description: 'Advanced AI-powered legal guidance with real-time compliance checking',
      icon: Brain,
      color: 'from-blue-500 to-purple-600',
      highlights: [
        'Real-time compliance checking',
        'Case law integration',
        'Ontario-specific requirements',
        'Plain language explanations'
      ]
    },
    {
      id: 'document-creator',
      title: 'Document Creator',
      description: 'Professional document creation with step-by-step guidance',
      icon: FileText,
      color: 'from-green-500 to-blue-600',
      highlights: [
        'Step-by-step guidance',
        'Professional formatting',
        'Legal compliance validation',
        'Multiple document types'
      ]
    },
    {
      id: 'smart-analysis',
      title: 'Smart Analysis',
      description: 'Intelligent document analysis and optimization suggestions',
      icon: Sparkles,
      color: 'from-purple-500 to-pink-600',
      highlights: [
        'Document optimization',
        'Error detection',
        'Completeness checking',
        'Best practice suggestions'
      ]
    }
  ];

  const stats = [
    { label: 'Documents Created', value: '10,000+', icon: FileText },
    { label: 'Users Served', value: '5,000+', icon: Users },
    { label: 'Success Rate', value: '99.8%', icon: CheckCircle },
    { label: 'Compliance Score', value: '100%', icon: Shield }
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-purple-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Ontario Wills
              </span>
              <br />
              <span className="text-gray-800 dark:text-gray-200">
                & Power of Attorney Creator
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Professional legal document creation with AI assistance. Create legally compliant wills and POA documents with confidence.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
                Get Started Free
                <ArrowRight className="inline-block ml-2 h-5 w-5" />
              </button>
              <button className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-semibold py-4 px-8 rounded-xl border-2 border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-all duration-300">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full">
                    <stat.icon className="h-8 w-8 text-white" />
                  </div>
                </div>
                <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-600 dark:text-gray-300">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Everything you need to create professional, legally compliant documents
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={feature.id}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 cursor-pointer transform hover:scale-105"
              onClick={() => setActiveDemo(activeDemo === feature.id ? null : feature.id)}
            >
              <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6`}>
                <feature.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                {feature.description}
              </p>
              <ul className="space-y-2">
                {feature.highlights.map((highlight, idx) => (
                  <li key={idx} className="flex items-center text-gray-700 dark:text-gray-300">
                    <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                    {highlight}
                  </li>
                ))}
              </ul>
              {activeDemo === feature.id && (
                <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-700 dark:to-gray-600 rounded-lg">
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    Click "Get Started" to explore this feature in detail.
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              Trusted by legal professionals and individuals across Ontario
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 text-white">
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-lg mb-4 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-blue-200 text-sm">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
              Create your legally compliant will or power of attorney document today.
            </p>
            <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
              Start Creating Your Document
              <ArrowRight className="inline-block ml-2 h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleDemoShowcase;