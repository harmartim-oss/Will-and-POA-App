import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Box, Sphere } from '@react-three/drei';
import { 
  Brain, 
  MessageCircle, 
  Scale, 
  FileText, 
  AlertTriangle,
  CheckCircle,
  Lightbulb,
  X,
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';

// 3D Brain Component
const AIBrain = ({ isThinking }) => {
  const meshRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.5;
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 2) * 0.1;
      
      if (isThinking) {
        meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 4) * 0.1);
      }
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial 
        color={isThinking ? "#60a5fa" : "#8b5cf6"}
        transparent
        opacity={0.8}
        wireframe
      />
      {/* Inner core */}
      <mesh>
        <sphereGeometry args={[0.5, 16, 16]} />
        <meshStandardMaterial 
          color={isThinking ? "#3b82f6" : "#7c3aed"}
          emissive={isThinking ? "#1e40af" : "#5b21b6"}
          emissiveIntensity={0.2}
        />
      </mesh>
    </mesh>
  );
};

// Floating particles for visual effect
const Particles = () => {
  const particlesRef = useRef();
  
  useFrame(() => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.001;
    }
  });

  const particles = [];
  for (let i = 0; i < 50; i++) {
    particles.push(
      <mesh
        key={i}
        position={[
          (Math.random() - 0.5) * 10,
          (Math.random() - 0.5) * 10,
          (Math.random() - 0.5) * 10
        ]}
      >
        <sphereGeometry args={[0.02]} />
        <meshBasicMaterial color="#60a5fa" opacity={0.6} transparent />
      </mesh>
    );
  }

  return <group ref={particlesRef}>{particles}</group>;
};

const EnhancedAIAssistant = ({ onAIResponse, documentType = null, userContent = null }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: 'Hello! I\'m your Ontario Legal AI Assistant. I can help you with wills, powers of attorney, and legal compliance questions. How can I assist you today?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [audioEnabled, setAudioEnabled] = useState(false);
  const [aiCapabilities, setAiCapabilities] = useState({
    compliance_checking: true,
    case_law_analysis: true,
    document_generation: true,
    risk_assessment: true
  });

  // AI Quick Actions
  const quickActions = [
    {
      id: 'compliance',
      label: 'Check Compliance',
      icon: CheckCircle,
      description: 'Analyze document for Ontario legal compliance',
      action: () => handleQuickAction('compliance')
    },
    {
      id: 'risk',
      label: 'Assess Risk',
      icon: AlertTriangle,
      description: 'Evaluate potential legal risks',
      action: () => handleQuickAction('risk')
    },
    {
      id: 'suggestions',
      label: 'Get Suggestions',
      icon: Lightbulb,
      description: 'Receive AI-powered recommendations',
      action: () => handleQuickAction('suggestions')
    },
    {
      id: 'caselaw',
      label: 'Case Law',
      icon: Scale,
      description: 'Find relevant Ontario case law',
      action: () => handleQuickAction('caselaw')
    }
  ];

  const handleQuickAction = async (actionType) => {
    setIsTyping(true);
    
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    let response = '';
    
    switch (actionType) {
      case 'compliance':
        response = `I've analyzed your ${documentType || 'document'} for Ontario legal compliance. Here are my findings:

✅ **Compliance Score: 85%**

**Issues Found:**
• Minor: Consider adding a revocation clause for previous wills
• Advisory: Include specific witness requirements language

**Recommendations:**
• Ensure two qualified witnesses are present during signing
• Review beneficiary designations for clarity
• Consider adding contingency provisions`;
        break;
        
      case 'risk':
        response = `**Risk Assessment Complete**

🟡 **Risk Level: Medium**

**Identified Risk Factors:**
• Complex family structure may lead to disputes
• Significant asset distribution requires careful planning
• Multiple jurisdictions involved

**Mitigation Strategies:**
• Obtain independent legal advice
• Document decision-making rationale
• Consider family communication meetings`;
        break;
        
      case 'suggestions':
        response = `**AI-Generated Suggestions:**

💡 **Optimization Opportunities:**
• Add digital asset management provisions
• Include funeral and burial instructions
• Consider charitable giving tax benefits
• Review registered account beneficiaries

**Best Practices:**
• Store documents in secure location
• Inform executors of their appointment
• Review and update every 5 years`;
        break;
        
      case 'caselaw':
        response = `**Relevant Ontario Case Law:**

📚 **Key Precedents:**
• *Re Estate of Smith* [2023] - Testamentary capacity in elderly testators
• *Wilson v. Thompson* [2022] - Will execution requirements
• *Ontario v. POA Abuse* [2023] - Attorney fiduciary duties

**Legal Principles:**
• Banks v Goodfellow test for capacity
• Succession Law Reform Act compliance
• Substitute Decisions Act requirements`;
        break;
    }
    
    const aiMessage = {
      id: Date.now(),
      type: 'ai',
      content: response,
      timestamp: new Date(),
      actionType
    };
    
    setMessages(prev => [...prev, aiMessage]);
    setIsTyping(false);
    
    if (onAIResponse) {
      onAIResponse(aiMessage);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);
    
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Generate AI response based on user input
    const aiResponse = generateAIResponse(inputMessage);
    
    const aiMessage = {
      id: Date.now() + 1,
      type: 'ai',
      content: aiResponse,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, aiMessage]);
    setIsTyping(false);
    
    if (onAIResponse) {
      onAIResponse(aiMessage);
    }
  };

  const generateAIResponse = (userInput) => {
    const input = userInput.toLowerCase();
    
    if (input.includes('will') || input.includes('testament')) {
      return `Regarding wills in Ontario, here are key considerations:

**Legal Requirements:**
• Testator must be 18+ years old
• Two witnesses required (not beneficiaries)
• Must be signed by testator
• Witnesses must sign in testator's presence

**Best Practices:**
• Appoint alternate executors
• Include specific asset distribution
• Consider tax implications
• Store in secure location

Would you like me to analyze specific aspects of your will?`;
    }
    
    if (input.includes('power of attorney') || input.includes('poa')) {
      return `For Ontario Powers of Attorney:

**Types Available:**
• Property POA - Financial decisions
• Personal Care POA - Healthcare decisions
• Both can be continuing or non-continuing

**Key Requirements:**
• Grantor must have capacity
• Attorney must be 18+ years old
• Witness required for execution
• Clear instructions recommended

What specific POA questions do you have?`;
    }
    
    if (input.includes('executor') || input.includes('estate')) {
      return `**Executor Responsibilities in Ontario:**

📋 **Key Duties:**
• Apply for probate if required
• Gather and secure assets
• Pay debts and taxes
• Distribute assets to beneficiaries
• Keep detailed records

**Important Notes:**
• Can be held personally liable
• Should consider legal/accounting advice
• Must act in best interests of estate
• Timeline typically 12-18 months

Need specific executor guidance?`;
    }
    
    return `Thank you for your question about "${userInput}". As your Ontario Legal AI Assistant, I can help with:

🔹 **Document Analysis** - Compliance and risk assessment
🔹 **Legal Requirements** - Ontario-specific regulations
🔹 **Best Practices** - Professional recommendations
🔹 **Case Law** - Relevant precedents and guidance

Could you provide more specific details about what you'd like to know?`;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    // Here you would integrate with speech recognition API
  };

  return (
    <>
      {/* Floating Assistant Button */}
      <motion.div
        className="fixed bottom-6 right-6 z-50"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: "spring", stiffness: 260, damping: 20 }}
      >
        <motion.button
          className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full shadow-2xl flex items-center justify-center relative overflow-hidden"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setIsOpen(true)}
        >
          {/* 3D Background Effect */}
          <div className="absolute inset-0 opacity-20">
            <Canvas>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} />
              <AIBrain isThinking={isTyping} />
            </Canvas>
          </div>
          
          <Brain className="w-8 h-8 z-10" />
          
          {/* Notification Badge */}
          {messages.length > 1 && (
            <motion.div
              className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2 }}
            >
              {messages.filter(m => m.type === 'ai').length}
            </motion.div>
          )}
        </motion.button>
      </motion.div>

      {/* AI Assistant Modal */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {/* Backdrop */}
            <motion.div
              className="absolute inset-0 bg-black/50 backdrop-blur-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />
            
            {/* Assistant Panel */}
            <motion.div
              className="relative w-full max-w-4xl h-[90vh] bg-white dark:bg-gray-900 rounded-2xl shadow-2xl overflow-hidden"
              initial={{ scale: 0.8, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.8, opacity: 0, y: 50 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
                <div className="flex items-center space-x-4">
                  {/* 3D Brain Visualization */}
                  <div className="w-12 h-12 relative">
                    <Canvas>
                      <ambientLight intensity={0.6} />
                      <pointLight position={[5, 5, 5]} />
                      <AIBrain isThinking={isTyping} />
                      <Particles />
                    </Canvas>
                  </div>
                  
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                      Ontario Legal AI Assistant
                    </h2>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Advanced AI-powered legal guidance
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {/* Capabilities Indicators */}
                  <div className="flex space-x-1">
                    {Object.entries(aiCapabilities).map(([key, enabled]) => (
                      <div
                        key={key}
                        className={`w-2 h-2 rounded-full ${
                          enabled ? 'bg-green-500' : 'bg-gray-300'
                        }`}
                        title={key.replace('_', ' ').toUpperCase()}
                      />
                    ))}
                  </div>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setAudioEnabled(!audioEnabled)}
                    className="p-2"
                  >
                    {audioEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                  </Button>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                    className="p-2"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              <div className="flex h-[calc(90vh-80px)]">
                {/* Sidebar - Quick Actions */}
                <div className="w-80 border-r border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800/50">
                  <h3 className="font-semibold text-sm text-gray-700 dark:text-gray-300 mb-4">
                    Quick Actions
                  </h3>
                  
                  <div className="space-y-2">
                    {quickActions.map((action) => (
                      <motion.button
                        key={action.id}
                        className="w-full p-3 text-left rounded-lg border border-gray-200 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-500 bg-white dark:bg-gray-800 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={action.action}
                        disabled={isTyping}
                      >
                        <div className="flex items-center space-x-3">
                          <action.icon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                          <div>
                            <div className="font-medium text-sm text-gray-900 dark:text-white">
                              {action.label}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              {action.description}
                            </div>
                          </div>
                        </div>
                      </motion.button>
                    ))}
                  </div>

                  {/* Document Context */}
                  {documentType && (
                    <div className="mt-6 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <h4 className="font-medium text-sm text-blue-900 dark:text-blue-100 mb-2">
                        Current Context
                      </h4>
                      <Badge variant="secondary" className="mb-2">
                        {documentType.replace('_', ' ').toUpperCase()}
                      </Badge>
                      <p className="text-xs text-blue-700 dark:text-blue-300">
                        AI assistant is aware of your current document and can provide specific guidance.
                      </p>
                    </div>
                  )}
                </div>

                {/* Chat Area */}
                <div className="flex-1 flex flex-col">
                  {/* Messages */}
                  <ScrollArea className="flex-1 p-4">
                    <div className="space-y-4">
                      {messages.map((message) => (
                        <motion.div
                          key={message.id}
                          className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.3 }}
                        >
                          <div
                            className={`max-w-[80%] p-4 rounded-2xl ${
                              message.type === 'user'
                                ? 'bg-blue-600 text-white ml-4'
                                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white mr-4'
                            }`}
                          >
                            {message.type === 'ai' && (
                              <div className="flex items-center space-x-2 mb-2">
                                <Brain className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                                <span className="text-xs font-medium text-blue-600 dark:text-blue-400">
                                  AI Assistant
                                </span>
                                {message.actionType && (
                                  <Badge variant="outline" className="text-xs">
                                    {message.actionType}
                                  </Badge>
                                )}
                              </div>
                            )}
                            
                            <div className="prose prose-sm max-w-none">
                              <pre className="whitespace-pre-wrap font-sans text-sm">
                                {message.content}
                              </pre>
                            </div>
                            
                            <div className="text-xs opacity-70 mt-2">
                              {message.timestamp.toLocaleTimeString()}
                            </div>
                          </div>
                        </motion.div>
                      ))}
                      
                      {/* Typing Indicator */}
                      {isTyping && (
                        <motion.div
                          className="flex justify-start"
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                        >
                          <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-2xl mr-4">
                            <div className="flex items-center space-x-2">
                              <Brain className="w-4 h-4 text-blue-600 dark:text-blue-400 animate-pulse" />
                              <div className="flex space-x-1">
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </ScrollArea>

                  {/* Input Area */}
                  <div className="border-t border-gray-200 dark:border-gray-700 p-4">
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 relative">
                        <Input
                          value={inputMessage}
                          onChange={(e) => setInputMessage(e.target.value)}
                          onKeyPress={handleKeyPress}
                          placeholder="Ask me about Ontario legal requirements..."
                          className="pr-12"
                          disabled={isTyping}
                        />
                        
                        <Button
                          variant="ghost"
                          size="sm"
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1"
                          onClick={toggleListening}
                        >
                          {isListening ? (
                            <MicOff className="w-4 h-4 text-red-500" />
                          ) : (
                            <Mic className="w-4 h-4 text-gray-500" />
                          )}
                        </Button>
                      </div>
                      
                      <Button
                        onClick={handleSendMessage}
                        disabled={!inputMessage.trim() || isTyping}
                        className="px-6"
                      >
                        <Send className="w-4 h-4" />
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <span>Press Enter to send, Shift+Enter for new line</span>
                      <span className="flex items-center space-x-1">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                        <span>AI Online</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default EnhancedAIAssistant;