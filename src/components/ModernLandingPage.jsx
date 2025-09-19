import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  Shield, 
  Users, 
  CheckCircle, 
  ArrowRight, 
  Star,
  Zap,
  Brain,
  Lock,
  Award,
  ChevronDown,
  Play,
  BookOpen,
  MessageCircle,
  Phone,
  Mail
} from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

const ModernLandingPage = ({ onGetStarted, onLearnMore }) => {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [isVisible, setIsVisible] = useState({});

  const features = [
    {
      icon: <Brain className="h-8 w-8" />,
      title: "AI-Powered Legal Analysis",
      description: "Advanced NLP technology analyzes your documents for compliance and suggests improvements using spaCy and machine learning.",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Ontario Legal Compliance",
      description: "Ensures full compliance with Ontario's Succession Law Reform Act and Substitute Decisions Act requirements.",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: <FileText className="h-8 w-8" />,
      title: "Professional Document Generation",
      description: "Creates legally formatted documents in PDF and Word formats with professional layouts and proper legal language.",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: <BookOpen className="h-8 w-8" />,
      title: "Legal Research Integration",
      description: "Access to CanLII database and relevant case law to ensure your documents reflect current legal standards.",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: <Lock className="h-8 w-8" />,
      title: "Secure & Private",
      description: "End-to-end encryption and secure cloud storage ensure your sensitive legal documents remain confidential.",
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "Instant Generation",
      description: "Generate complete legal documents in minutes with our guided questionnaire and intelligent automation.",
      color: "from-yellow-500 to-orange-500"
    }
  ];

  const documentTypes = [
    {
      title: "Last Will & Testament",
      description: "Comprehensive wills with executor appointments, beneficiary designations, and asset distribution.",
      features: ["Executor Appointment", "Asset Distribution", "Guardian Designation", "Witness Requirements"],
      icon: <FileText className="h-12 w-12" />,
      popular: true
    },
    {
      title: "Power of Attorney for Property",
      description: "Continuing or non-continuing POAs for financial and property management decisions.",
      features: ["Financial Management", "Property Decisions", "Investment Authority", "Banking Powers"],
      icon: <Shield className="h-12 w-12" />,
      popular: false
    },
    {
      title: "Power of Attorney for Personal Care",
      description: "Healthcare and personal care decision-making authority for trusted individuals.",
      features: ["Healthcare Decisions", "Personal Care", "Medical Consent", "Living Arrangements"],
      icon: <Users className="h-12 w-12" />,
      popular: false
    }
  ];

  const testimonials = [
    {
      name: "Sarah Mitchell",
      role: "Estate Planning Client",
      content: "The AI-powered suggestions helped me understand legal requirements I never knew existed. The process was incredibly smooth and professional.",
      rating: 5,
      avatar: "SM"
    },
    {
      name: "Dr. James Chen",
      role: "Medical Professional",
      content: "As a busy physician, I needed a quick but thorough solution for my estate planning. This platform delivered exactly what I needed.",
      rating: 5,
      avatar: "JC"
    },
    {
      name: "Margaret Thompson",
      role: "Retiree",
      content: "The step-by-step guidance made creating my Power of Attorney documents stress-free. Highly recommend for anyone needing legal documents.",
      rating: 5,
      avatar: "MT"
    }
  ];

  const stats = [
    { number: "10,000+", label: "Documents Created" },
    { number: "99.9%", label: "Legal Compliance" },
    { number: "4.9/5", label: "User Rating" },
    { number: "24/7", label: "Support Available" }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials.length]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setIsVisible(prev => ({
            ...prev,
            [entry.target.id]: entry.isIntersecting
          }));
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll('[id]').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
        
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute bg-white/5 rounded-full"
              style={{
                width: Math.random() * 100 + 50,
                height: Math.random() * 100 + 50,
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.3, 0.6, 0.3],
              }}
              transition={{
                duration: Math.random() * 3 + 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
          ))}
        </div>

        <div className="relative container mx-auto px-6 py-24 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <Badge className="bg-blue-500/20 text-blue-100 border-blue-400/30 px-4 py-2">
                  <Zap className="h-4 w-4 mr-2" />
                  AI-Powered Legal Documents
                </Badge>
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  Create Legal Documents with
                  <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                    {" "}AI Precision
                  </span>
                </h1>
                <p className="text-xl lg:text-2xl text-blue-100 leading-relaxed">
                  Generate Ontario-compliant wills and powers of attorney in minutes. 
                  Our AI analyzes your documents for legal compliance and provides 
                  intelligent suggestions.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  size="lg"
                  onClick={onGetStarted}
                  className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                >
                  Start Creating Documents
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
                <Button
                  variant="outline"
                  size="lg"
                  onClick={onLearnMore}
                  className="border-2 border-white/30 text-white hover:bg-white/10 px-8 py-4 text-lg font-semibold rounded-xl backdrop-blur-sm"
                >
                  <Play className="mr-2 h-5 w-5" />
                  Watch Demo
                </Button>
              </div>

              <div className="flex items-center space-x-8 pt-4">
                {stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-2xl font-bold text-cyan-400">{stat.number}</div>
                    <div className="text-sm text-blue-200">{stat.label}</div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="relative bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xl font-semibold">Document Preview</h3>
                    <Badge className="bg-green-500/20 text-green-100 border-green-400/30">
                      <CheckCircle className="h-4 w-4 mr-1" />
                      AI Verified
                    </Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-white/5 rounded-lg p-4 border-l-4 border-blue-400">
                      <p className="text-sm text-blue-100">
                        "I, John Smith, of sound mind and understanding..."
                      </p>
                    </div>
                    <div className="bg-white/5 rounded-lg p-4 border-l-4 border-green-400">
                      <p className="text-sm text-green-100">
                        ✓ Witness requirements verified
                      </p>
                    </div>
                    <div className="bg-white/5 rounded-lg p-4 border-l-4 border-purple-400">
                      <p className="text-sm text-purple-100">
                        ✓ Ontario legal compliance confirmed
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <ChevronDown className="h-8 w-8 text-white/60" />
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible.features ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <Badge className="mb-4 bg-blue-50 text-blue-600 border-blue-200">
              <Award className="h-4 w-4 mr-2" />
              Advanced Features
            </Badge>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Powered by Cutting-Edge Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform combines artificial intelligence, legal expertise, and modern design 
              to deliver the most advanced legal document creation experience.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                animate={isVisible.features ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className="group"
              >
                <Card className="h-full border-0 shadow-lg hover:shadow-2xl transition-all duration-300 bg-gradient-to-br from-white to-gray-50 group-hover:from-white group-hover:to-blue-50">
                  <CardHeader className="pb-4">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform duration-300`}>
                      {feature.icon}
                    </div>
                    <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-blue-900 transition-colors">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-gray-600 leading-relaxed">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Document Types Section */}
      <section id="documents" className="py-24 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible.documents ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <Badge className="mb-4 bg-green-50 text-green-600 border-green-200">
              <FileText className="h-4 w-4 mr-2" />
              Document Types
            </Badge>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Complete Legal Document Suite
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Create all essential legal documents with Ontario-specific compliance 
              and professional formatting.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-3 gap-8">
            {documentTypes.map((doc, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                animate={isVisible.documents ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                whileHover={{ y: -10 }}
                className="relative group"
              >
                <Card className={`h-full border-0 shadow-xl hover:shadow-2xl transition-all duration-500 ${
                  doc.popular 
                    ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white' 
                    : 'bg-white hover:bg-gradient-to-br hover:from-white hover:to-blue-50'
                }`}>
                  {doc.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <Badge className="bg-yellow-400 text-yellow-900 px-4 py-1 font-semibold">
                        <Star className="h-4 w-4 mr-1" />
                        Most Popular
                      </Badge>
                    </div>
                  )}
                  
                  <CardHeader className="text-center pb-4">
                    <div className={`w-20 h-20 mx-auto rounded-2xl flex items-center justify-center mb-4 ${
                      doc.popular 
                        ? 'bg-white/20 text-white' 
                        : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                    } group-hover:scale-110 transition-transform duration-300`}>
                      {doc.icon}
                    </div>
                    <CardTitle className={`text-2xl font-bold mb-2 ${
                      doc.popular ? 'text-white' : 'text-gray-900'
                    }`}>
                      {doc.title}
                    </CardTitle>
                    <CardDescription className={`${
                      doc.popular ? 'text-blue-100' : 'text-gray-600'
                    }`}>
                      {doc.description}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      {doc.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center space-x-3">
                          <CheckCircle className={`h-5 w-5 ${
                            doc.popular ? 'text-green-300' : 'text-green-500'
                          }`} />
                          <span className={`${
                            doc.popular ? 'text-blue-100' : 'text-gray-700'
                          }`}>
                            {feature}
                          </span>
                        </div>
                      ))}
                    </div>
                    
                    <Button
                      className={`w-full mt-6 ${
                        doc.popular
                          ? 'bg-white text-blue-600 hover:bg-blue-50'
                          : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600'
                      } font-semibold py-3 rounded-xl transition-all duration-300 transform hover:scale-105`}
                      onClick={onGetStarted}
                    >
                      Create {doc.title.split(' ')[0]} Document
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible.testimonials ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <Badge className="mb-4 bg-purple-50 text-purple-600 border-purple-200">
              <MessageCircle className="h-4 w-4 mr-2" />
              Client Testimonials
            </Badge>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Trusted by Thousands
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              See what our clients say about their experience creating legal documents 
              with our AI-powered platform.
            </p>
          </motion.div>

          <div className="max-w-4xl mx-auto">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentTestimonial}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.5 }}
                className="text-center"
              >
                <Card className="border-0 shadow-2xl bg-gradient-to-br from-white to-gray-50 p-8">
                  <CardContent className="space-y-6">
                    <div className="flex justify-center space-x-1 mb-4">
                      {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                        <Star key={i} className="h-6 w-6 text-yellow-400 fill-current" />
                      ))}
                    </div>
                    
                    <blockquote className="text-2xl font-medium text-gray-900 leading-relaxed">
                      "{testimonials[currentTestimonial].content}"
                    </blockquote>
                    
                    <div className="flex items-center justify-center space-x-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                        {testimonials[currentTestimonial].avatar}
                      </div>
                      <div className="text-left">
                        <div className="font-semibold text-gray-900">
                          {testimonials[currentTestimonial].name}
                        </div>
                        <div className="text-gray-600">
                          {testimonials[currentTestimonial].role}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </AnimatePresence>

            <div className="flex justify-center space-x-2 mt-8">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentTestimonial
                      ? 'bg-blue-500 w-8'
                      : 'bg-gray-300 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative container mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible.cta ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto space-y-8"
          >
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2 mb-6">
              <Zap className="h-4 w-4 mr-2" />
              Ready to Get Started?
            </Badge>
            
            <h2 className="text-4xl lg:text-6xl font-bold leading-tight">
              Create Your Legal Documents
              <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                {" "}Today
              </span>
            </h2>
            
            <p className="text-xl lg:text-2xl text-blue-100 leading-relaxed max-w-3xl mx-auto">
              Join thousands of Ontarians who have created their wills and powers of attorney 
              with confidence using our AI-powered platform.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center pt-8">
              <Button
                size="lg"
                onClick={onGetStarted}
                className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-12 py-6 text-xl font-semibold rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-105"
              >
                Start Creating Now
                <ArrowRight className="ml-3 h-6 w-6" />
              </Button>
              
              <div className="flex items-center space-x-4 text-blue-200">
                <div className="flex items-center space-x-2">
                  <Phone className="h-5 w-5" />
                  <span>1-800-LEGAL-AI</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Mail className="h-5 w-5" />
                  <span>support@ontariowills.ai</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default ModernLandingPage;

