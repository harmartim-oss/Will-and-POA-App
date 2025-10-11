import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  FileText, 
  Sparkles, 
  Eye, 
  Download,
  Shield,
  Zap,
  Users,
  Scale
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import PremiumDocumentCreator from './PremiumDocumentCreator';
import DocumentPreviewEnhanced from './DocumentPreviewEnhanced';
import EnhancedAIAssistant from './EnhancedAIAssistant';

const DemoShowcase = () => {
  const [activeDemo, setActiveDemo] = useState(null);
  const [showPreview, setShowPreview] = useState(false);

  const features = [
    {
      id: 'ai-assistant',
      title: 'Enhanced AI Assistant',
      description: 'Advanced AI-powered legal guidance with 3D visualization and real-time analysis',
      icon: Brain,
      color: 'from-blue-500 to-purple-600',
      highlights: [
        '3D brain visualization',
        'Real-time compliance checking',
        'Case law integration',
        'Voice interaction support'
      ]
    },
    {
      id: 'document-creator',
      title: 'Premium Document Creator',
      description: '3D-enhanced document creation with professional animations and AI optimization',
      icon: FileText,
      color: 'from-green-500 to-blue-600',
      highlights: [
        '3D document visualization',
        'Step-by-step guidance',
        'AI-powered optimization',
        'Professional styling'
      ]
    },
    {
      id: 'preview-system',
      title: 'Advanced Preview System',
      description: 'Professional document preview with AI analysis and PDF generation',
      icon: Eye,
      color: 'from-purple-500 to-pink-600',
      highlights: [
        'Real-time PDF generation',
        'AI compliance analysis',
        'Interactive zoom/rotate',
        'Professional layouts'
      ]
    }
  ];

  const handleFeatureDemo = (featureId) => {
    setActiveDemo(featureId);
    
    if (featureId === 'document-creator') {
      // Already shows the premium creator
    } else if (featureId === 'preview-system') {
      setShowPreview(true);
    }
  };

  const handleSave = () => {
    console.log('Document saved');
  };

  const handlePreview = () => {
    setShowPreview(true);
  };

  if (activeDemo === 'document-creator') {
    return (
      <PremiumDocumentCreator
        documentType="will"
        onSave={handleSave}
        onPreview={handlePreview}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-950 dark:to-purple-950">
      {/* Header */}
      <div className="container mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Ontario Will & POA App
            <span className="block text-3xl text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mt-2">
              Enhanced with Advanced AI
            </span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Experience the future of legal document creation with AI-powered analysis, 
            3D visualizations, and professional-grade document generation.
          </p>
          
          <div className="flex justify-center space-x-4 mt-8">
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Brain className="w-4 h-4 mr-2" />
              AI-Powered
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Shield className="w-4 h-4 mr-2" />
              Ontario Compliant
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Sparkles className="w-4 h-4 mr-2" />
              3D Enhanced
            </Badge>
          </div>
        </motion.div>

        {/* Feature Showcase */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <Card className="h-full hover:shadow-2xl transition-all duration-300 cursor-pointer group"
                    onClick={() => handleFeatureDemo(feature.id)}>
                <CardHeader>
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <feature.icon className="w-8 h-8 text-white" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {feature.highlights.map((highlight, idx) => (
                      <li key={idx} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                        <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-3" />
                        {highlight}
                      </li>
                    ))}
                  </ul>
                  
                  <Button className="w-full mt-6 group-hover:bg-gradient-to-r group-hover:from-blue-600 group-hover:to-purple-600">
                    <Zap className="w-4 h-4 mr-2" />
                    Try Demo
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Key Improvements Section */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 dark:border-gray-700/20 p-8 mb-16"
        >
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-8">
            Enhanced Features Implementation
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Brain className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="font-semibold mb-2">Advanced AI Engine</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Enhanced with transformers, spaCy, and sentence embeddings for superior legal analysis
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Sparkles className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="font-semibold mb-2">3D Visualizations</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Three.js integration with React Three Fiber for immersive document creation
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="font-semibold mb-2">Professional Documents</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Enhanced document generation with DOCX, PDF, and WeasyPrint support
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Scale className="w-6 h-6 text-red-600" />
              </div>
              <h3 className="font-semibold mb-2">Case Law Integration</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Advanced case law analyzer with Ontario-specific precedents and risk assessment
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Shield className="w-6 h-6 text-yellow-600" />
              </div>
              <h3 className="font-semibold mb-2">Enhanced Security</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Legal-grade encryption and comprehensive audit trails for compliance
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <Users className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="font-semibold mb-2">Premium UX</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Framer Motion animations and glass-morphism design for professional experience
              </p>
            </div>
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="text-center"
        >
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Enhanced Technology Stack
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg p-4">
              <h4 className="font-semibold text-sm mb-2">Frontend</h4>
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <div>React 19 + TypeScript</div>
                <div>Three.js + React Three Fiber</div>
                <div>Framer Motion</div>
                <div>Tailwind CSS</div>
              </div>
            </div>
            
            <div className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg p-4">
              <h4 className="font-semibold text-sm mb-2">AI/NLP</h4>
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <div>spaCy + Transformers</div>
                <div>Sentence Transformers</div>
                <div>OpenAI Integration</div>
                <div>scikit-learn</div>
              </div>
            </div>
            
            <div className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg p-4">
              <h4 className="font-semibold text-sm mb-2">Backend</h4>
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <div>FastAPI + Python</div>
                <div>AsyncIO Support</div>
                <div>PostgreSQL + Redis</div>
                <div>Celery Processing</div>
              </div>
            </div>
            
            <div className="bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-lg p-4">
              <h4 className="font-semibold text-sm mb-2">Documents</h4>
              <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                <div>python-docx</div>
                <div>ReportLab + WeasyPrint</div>
                <div>React PDF</div>
                <div>html2canvas</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* AI Assistant (always available) */}
      <EnhancedAIAssistant 
        documentType="will"
        onAIResponse={(response) => console.log('AI Response:', response)}
      />

      {/* Preview Modal */}
      {showPreview && (
        <DocumentPreviewEnhanced
          documentData={{}}
          documentType="will"
          onClose={() => setShowPreview(false)}
          onDownload={() => console.log('Download')}
          onShare={() => console.log('Share')}
        />
      )}
    </div>
  );
};

export default DemoShowcase;
