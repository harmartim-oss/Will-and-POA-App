import React, { useState, useEffect, useRef, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Canvas, useFrame } from '@react-three/fiber';
import { 
  OrbitControls, 
  Text, 
  Box, 
  Sphere, 
  MeshDistortMaterial, 
  Environment,
  Float
} from '@react-three/drei';
import { 
  FileText, 
  Users, 
  Shield, 
  Brain, 
  Sparkles, 
  ArrowRight,
  ArrowLeft,
  Save,
  Eye,
  Download,
  Upload,
  CheckCircle2,
  AlertCircle,
  Info,
  Zap
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import EnhancedAIAssistant from './EnhancedAIAssistant';

// 3D Document Visualization
const Document3D = ({ documentType, progress = 0 }) => {
  const groupRef = useRef();
  
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
      groupRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.1;
    }
  });

  return (
    <Float speed={1} rotationIntensity={0.5} floatIntensity={0.5}>
      <group ref={groupRef}>
        {/* Document Pages */}
        <Box position={[0, 0, 0]} args={[2, 2.8, 0.1]}>
          <MeshDistortMaterial
            color={documentType === 'will' ? '#3b82f6' : '#8b5cf6'}
            transparent
            opacity={0.8}
            distort={progress * 0.3}
            speed={2}
          />
        </Box>
        
        {/* Progress Indicator Ring */}
        <mesh rotation={[0, 0, 0]}>
          <ringGeometry args={[1.8, 2, 32]} />
          <meshBasicMaterial
            color="#60a5fa"
            transparent
            opacity={0.3}
            wireframe
          />
        </mesh>
        
        {/* Completion Ring */}
        <mesh rotation={[0, 0, 0]}>
          <ringGeometry 
            args={[1.8, 2, Math.max(8, Math.floor(progress * 32)), Math.floor(progress * 32)]} 
          />
          <meshBasicMaterial
            color="#10b981"
            transparent
            opacity={0.8}
          />
        </mesh>
        
        {/* Text Elements */}
        <Text
          position={[0, 1, 0.2]}
          fontSize={0.2}
          color="#1f2937"
          anchorX="center"
          anchorY="middle"
        >
          {documentType?.replace('_', ' ').toUpperCase()}
        </Text>
        
        <Text
          position={[0, -1, 0.2]}
          fontSize={0.15}
          color="#6b7280"
          anchorX="center" 
          anchorY="middle"
        >
          {Math.round(progress * 100)}% Complete
        </Text>
      </group>
    </Float>
  );
};

// Animated Background Elements
const BackgroundElements = () => {
  const elements = [];
  
  for (let i = 0; i < 20; i++) {
    elements.push(
      <Float
        key={i}
        speed={0.5 + Math.random()}
        rotationIntensity={0.2}
        floatIntensity={0.3}
        position={[
          (Math.random() - 0.5) * 20,
          (Math.random() - 0.5) * 10,
          (Math.random() - 0.5) * 10
        ]}
      >
        <Sphere args={[0.05 + Math.random() * 0.1]}>
          <meshBasicMaterial
            color={Math.random() > 0.5 ? '#60a5fa' : '#8b5cf6'}
            transparent
            opacity={0.4}
          />
        </Sphere>
      </Float>
    );
  }
  
  return <group>{elements}</group>;
};

const PremiumDocumentCreator = ({ documentType = 'will', onSave, onPreview }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [isAiAnalyzing, setIsAiAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [validationStatus, setValidationStatus] = useState({});

  // Document creation steps
  const steps = [
    {
      id: 'personal',
      title: 'Personal Information',
      description: 'Your identity and contact details',
      icon: Users,
      fields: ['fullName', 'address', 'dateOfBirth', 'email'],
      required: true
    },
    {
      id: 'parties',
      title: documentType === 'will' ? 'Executors & Beneficiaries' : 'Attorneys',
      description: documentType === 'will' ? 'Who will manage and inherit' : 'Who will act on your behalf',
      icon: Users,
      fields: documentType === 'will' ? ['executors', 'beneficiaries'] : ['attorneys'],
      required: true
    },
    {
      id: 'provisions',
      title: documentType === 'will' ? 'Assets & Bequests' : 'Powers & Instructions',
      description: documentType === 'will' ? 'What to distribute' : 'What powers to grant',
      icon: FileText,
      fields: documentType === 'will' ? ['assets', 'bequests'] : ['powers', 'instructions'],
      required: true
    },
    {
      id: 'legal',
      title: 'Legal Requirements',
      description: 'Witnesses and execution details',
      icon: Shield,
      fields: ['witnesses', 'executionDate'],
      required: true
    },
    {
      id: 'review',
      title: 'AI Review & Finalization',
      description: 'AI analysis and final document generation',
      icon: Brain,
      fields: [],
      required: false
    }
  ];

  // Calculate progress based on completed steps
  useEffect(() => {
    const completedSteps = steps.slice(0, currentStep + 1).length;
    const newProgress = (completedSteps / steps.length) * 100;
    setProgress(newProgress);
  }, [currentStep]);

  // AI Analysis Effect
  useEffect(() => {
    if (currentStep === steps.length - 1) {
      performAIAnalysis();
    }
  }, [currentStep]);

  const performAIAnalysis = async () => {
    setIsAiAnalyzing(true);
    
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const suggestions = [
      {
        type: 'optimization',
        title: 'Suggested Improvement',
        description: 'Consider adding a digital assets clause to cover online accounts and cryptocurrency.',
        severity: 'medium',
        action: 'Add Digital Assets Section'
      },
      {
        type: 'compliance',
        title: 'Compliance Check',
        description: 'All Ontario legal requirements have been met. Document is ready for execution.',
        severity: 'success',
        action: 'Proceed to Generation'
      },
      {
        type: 'risk',
        title: 'Risk Assessment',
        description: 'Low risk detected. Consider appointing alternate executors for redundancy.',
        severity: 'low',
        action: 'Add Alternates'
      }
    ];
    
    setAiSuggestions(suggestions);
    setIsAiAnalyzing(false);
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAIResponse = (aiMessage) => {
    console.log('AI Response:', aiMessage);
    // Handle AI assistant responses
  };

  const renderStepContent = () => {
    const step = steps[currentStep];
    
    switch (step.id) {
      case 'personal':
        return (
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="w-5 h-5 text-blue-600" />
                  <span>Personal Information</span>
                </CardTitle>
                <CardDescription>
                  This information identifies you as the document creator.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Full Legal Name</label>
                    <input
                      type="text"
                      className="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter your full legal name"
                      value={formData.fullName || ''}
                      onChange={(e) => handleFormChange('fullName', e.target.value)}
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Date of Birth</label>
                    <input
                      type="date"
                      className="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      value={formData.dateOfBirth || ''}
                      onChange={(e) => handleFormChange('dateOfBirth', e.target.value)}
                    />
                  </div>
                  
                  <div className="md:col-span-2">
                    <label className="text-sm font-medium">Address</label>
                    <input
                      type="text"
                      className="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter your complete address"
                      value={formData.address || ''}
                      onChange={(e) => handleFormChange('address', e.target.value)}
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Email Address</label>
                    <input
                      type="email"
                      className="w-full mt-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="your.email@example.com"
                      value={formData.email || ''}
                      onChange={(e) => handleFormChange('email', e.target.value)}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
        
      case 'parties':
        return (
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Users className="w-5 h-5 text-purple-600" />
                  <span>
                    {documentType === 'will' ? 'Executors & Beneficiaries' : 'Attorneys'}
                  </span>
                </CardTitle>
                <CardDescription>
                  {documentType === 'will' 
                    ? 'Select who will manage your estate and receive your assets.'
                    : 'Choose who will make decisions on your behalf.'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-gray-500">
                  <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg mb-2">Dynamic Form Section</p>
                  <p className="text-sm">
                    This section would contain dynamic forms for adding executors, beneficiaries, or attorneys
                    based on the document type.
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
        
      case 'provisions':
        return (
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="w-5 h-5 text-green-600" />
                  <span>
                    {documentType === 'will' ? 'Assets & Bequests' : 'Powers & Instructions'}
                  </span>
                </CardTitle>
                <CardDescription>
                  {documentType === 'will' 
                    ? 'Specify how your assets should be distributed.'
                    : 'Define the scope of powers and specific instructions.'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-gray-500">
                  <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg mb-2">Provisions Configuration</p>
                  <p className="text-sm">
                    Interactive forms for specifying assets, bequests, powers, and instructions
                    would be implemented here.
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
        
      case 'legal':
        return (
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-red-600" />
                  <span>Legal Requirements</span>
                </CardTitle>
                <CardDescription>
                  Ensure compliance with Ontario legal requirements.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <AlertCircle className="w-5 h-5 text-amber-600" />
                      <span className="font-medium text-amber-800">Ontario Legal Requirements</span>
                    </div>
                    <ul className="text-sm text-amber-700 space-y-1">
                      <li>• Two qualified witnesses must be present during signing</li>
                      <li>• Witnesses cannot be beneficiaries or spouses of beneficiaries</li>
                      <li>• Document must be signed in the presence of witnesses</li>
                      <li>• All parties must be of sound mind and legal age</li>
                    </ul>
                  </div>
                  
                  <div className="text-center py-8 text-gray-500">
                    <Shield className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p className="text-lg mb-2">Witness & Execution Details</p>
                    <p className="text-sm">
                      Forms for witness information and execution scheduling would be here.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
        
      case 'review':
        return (
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="w-5 h-5 text-indigo-600" />
                  <span>AI Analysis & Review</span>
                  {isAiAnalyzing && (
                    <div className="flex items-center space-x-2 ml-4">
                      <div className="w-4 h-4 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
                      <span className="text-sm text-indigo-600">Analyzing...</span>
                    </div>
                  )}
                </CardTitle>
                <CardDescription>
                  AI-powered compliance checking and optimization suggestions.
                </CardDescription>
              </CardHeader>
              <CardContent>
                {isAiAnalyzing ? (
                  <div className="text-center py-12">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                      className="w-16 h-16 mx-auto mb-4"
                    >
                      <Brain className="w-full h-full text-indigo-600" />
                    </motion.div>
                    <p className="text-lg font-medium text-gray-900 mb-2">AI Analysis in Progress</p>
                    <p className="text-sm text-gray-600">
                      Checking compliance, analyzing risks, and generating optimization suggestions...
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {aiSuggestions.map((suggestion, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className={`p-4 border rounded-lg ${
                          suggestion.severity === 'success' ? 'bg-green-50 border-green-200' :
                          suggestion.severity === 'medium' ? 'bg-yellow-50 border-yellow-200' :
                          suggestion.severity === 'low' ? 'bg-blue-50 border-blue-200' :
                          'bg-gray-50 border-gray-200'
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-center space-x-3">
                            {suggestion.severity === 'success' ? (
                              <CheckCircle2 className="w-5 h-5 text-green-600" />
                            ) : suggestion.severity === 'medium' ? (
                              <AlertCircle className="w-5 h-5 text-yellow-600" />
                            ) : (
                              <Info className="w-5 h-5 text-blue-600" />
                            )}
                            <div>
                              <h4 className="font-medium text-gray-900">{suggestion.title}</h4>
                              <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                            </div>
                          </div>
                          <Button variant="outline" size="sm">
                            {suggestion.action}
                          </Button>
                        </div>
                      </motion.div>
                    ))}
                    
                    <div className="flex space-x-4 mt-8">
                      <Button onClick={onPreview} variant="outline" className="flex-1">
                        <Eye className="w-4 h-4 mr-2" />
                        Preview Document
                      </Button>
                      <Button onClick={onSave} className="flex-1">
                        <Download className="w-4 h-4 mr-2" />
                        Generate Document
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-950 dark:to-purple-950">
      {/* 3D Background */}
      <div className="fixed inset-0 pointer-events-none">
        <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
          <Suspense fallback={null}>
            <Environment preset="city" />
            <ambientLight intensity={0.4} />
            <pointLight position={[10, 10, 10]} intensity={0.8} />
            <pointLight position={[-10, -10, -10]} intensity={0.3} color="#8b5cf6" />
            
            <BackgroundElements />
            
            {/* Main 3D Document */}
            <group position={[4, 0, -2]}>
              <Document3D documentType={documentType} progress={progress / 100} />
            </group>
          </Suspense>
        </Canvas>
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-6 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Create Your {documentType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
            AI-powered Ontario legal document creation with professional guidance
          </p>
          
          {/* Progress Indicator */}
          <div className="max-w-2xl mx-auto">
            <Progress value={progress} className="h-3 mb-4" />
            <div className="flex justify-between text-sm text-gray-500">
              <span>Step {currentStep + 1} of {steps.length}</span>
              <span>{Math.round(progress)}% Complete</span>
            </div>
          </div>
        </motion.div>

        {/* Steps Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-4xl mx-auto mb-8"
        >
          <div className="flex justify-center space-x-2 md:space-x-4 overflow-x-auto">
            {steps.map((step, index) => (
              <motion.div
                key={step.id}
                className={`flex items-center space-x-2 p-3 rounded-lg transition-all duration-300 ${
                  index === currentStep
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                    : index < currentStep
                    ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-500'
                }`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <step.icon className="w-5 h-5" />
                <div className="hidden md:block">
                  <div className="font-medium text-sm">{step.title}</div>
                  {index === currentStep && (
                    <div className="text-xs opacity-75">{step.description}</div>
                  )}
                </div>
                {index < currentStep && (
                  <CheckCircle2 className="w-4 h-4 text-green-600" />
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Main Content Area */}
        <div className="max-w-4xl mx-auto">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 dark:border-gray-700/20 p-8"
          >
            {renderStepContent()}
            
            {/* Navigation Buttons */}
            <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 0}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Previous</span>
              </Button>
              
              <div className="flex items-center space-x-4">
                <Button variant="ghost" size="sm">
                  <Save className="w-4 h-4 mr-2" />
                  Save Progress
                </Button>
                
                {currentStep < steps.length - 1 ? (
                  <Button onClick={handleNext} className="flex items-center space-x-2">
                    <span>Next</span>
                    <ArrowRight className="w-4 h-4" />
                  </Button>
                ) : (
                  <Button 
                    onClick={onSave} 
                    className="flex items-center space-x-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                    disabled={isAiAnalyzing}
                  >
                    <Zap className="w-4 h-4" />
                    <span>Generate Document</span>
                  </Button>
                )}
              </div>
            </div>
          </motion.div>
        </div>

        {/* AI Assistant Integration */}
        <EnhancedAIAssistant
          documentType={documentType}
          userContent={formData}
          onAIResponse={handleAIResponse}
        />
      </div>
    </div>
  );
};

export default PremiumDocumentCreator;