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
  Mail,
  Moon,
  Sun,
  Monitor
} from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { useTheme } from './ThemeContext';

const ModernLandingPage = ({ onGetStarted, onLearnMore }) => {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [isVisible, setIsVisible] = useState({});
  const { theme, toggleTheme, isDark } = useTheme();

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
  <div className="min-h-screen bg-[var(--surface-bg)] text-[var(--text-strong)] transition-colors">
      {/* Header with Theme Toggle */}
      <header className="absolute top-0 left-0 right-0 z-50" role="banner">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-2"
            >
              <div className="p-2 bg-white/10 backdrop-blur-sm rounded-lg" aria-hidden="true">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-white font-semibold text-lg">Ontario Legal Docs</h1>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleTheme}
                className="text-white hover:bg-white/10 rounded-lg"
                aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
              >
                {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
            </motion.div>
          </div>
        </div>
      </header>

      {/* Hero Section with Enhanced Design */}
      <section className="relative overflow-hidden text-white" role="main" aria-labelledby="hero-heading">
        <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-brand-600)] via-[var(--color-brand-700)] to-[var(--color-accent-600)]"></div>
        <div className="absolute inset-0 opacity-30" style={{
          backgroundImage: `url("data:image/svg+xml,${encodeURIComponent('<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="#ffffff" fill-opacity="0.05"><circle cx="10" cy="10" r="1"/></g></g></svg>')}")`,
        }} aria-hidden="true"></div>
        
        {/* Floating elements for visual interest */}
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          {[...Array(12)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute bg-white/10 rounded-full blur-sm"
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

  <div className="relative container mx-auto px-6 py-24 lg:py-32 max-w-[var(--container-2xl)] hero-section">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <div className="space-y-4">
                <Badge variant="brand" className="px-4 py-2 text-sm font-medium">
                  <Zap className="h-4 w-4 mr-2" />
                  AI-Powered Legal Documents
                </Badge>
                <h2 id="hero-heading" className="text-5xl lg:text-7xl font-bold leading-tight tracking-tight font-semibold hero-text">
                  Create Legal Documents with
                  <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                    {" "}AI Precision
                  </span>
                </h2>
                <p className="text-xl lg:text-2xl text-blue-100 leading-relaxed max-w-2xl">
                  Generate Ontario-compliant wills and powers of attorney in minutes. 
                  Our AI analyzes your documents for legal compliance and provides 
                  intelligent suggestions.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 hero-buttons">
                <Button
                  variant="primary"
                  size="xl"
                  onClick={onGetStarted}
                  className="group bg-white text-[var(--color-brand-700)] hover:bg-gray-50 shadow-xl hover:shadow-2xl rounded-xl font-semibold"
                >
                  Start Creating Documents
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
                </Button>
                <Button
                  variant="outline"
                  size="xl"
                  onClick={onLearnMore}
                  className="group border-2 border-white/40 text-white hover:bg-white/10 hover:border-white/60 font-semibold backdrop-blur-sm"
                >
                  <Play className="mr-2 h-5 w-5 group-hover:scale-110 transition-transform duration-200" />
                  Watch Demo
                </Button>
              </div>

              <div className="flex items-center space-x-8 pt-4 stats-container" role="group" aria-label="Platform statistics">
                {stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                    whileHover={{ scale: 1.05 }}
                    className="text-center group cursor-default"
                    role="img"
                    aria-label={`${stat.number} ${stat.label}`}
                  >
                    <div className="text-2xl font-bold text-cyan-400 group-hover:text-cyan-300 transition-colors duration-200" aria-hidden="true">{stat.number}</div>
                    <div className="text-sm text-blue-200 group-hover:text-blue-100 transition-colors duration-200" aria-hidden="true">{stat.label}</div>
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
      <section id="features" className="py-24 bg-gradient-to-b from-gray-50 to-white" aria-labelledby="features-heading">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={isVisible.features ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <Badge variant="info" className="mb-4" aria-hidden="true">
              <Award className="h-4 w-4 mr-2" />
              Advanced Features
            </Badge>
            <h2 id="features-heading" className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Powered by Cutting-Edge Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Our platform combines artificial intelligence, legal expertise, and modern design 
              to deliver the most advanced legal document creation experience.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 features-grid" role="list">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                animate={isVisible.features ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                whileHover={{ y: -8 }}
                className="group"
                role="listitem"
              >
                <Card className="h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-2 bg-white border-gray-100" interactive>
                  <CardHeader className="pb-4">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`} aria-hidden="true">
                      {feature.icon}
                    </div>
                    <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-[var(--color-brand-700)] transition-colors">
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

      {/* Do
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)