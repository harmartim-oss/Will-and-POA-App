import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Lightbulb, 
  ShieldCheck, 
  Rocket, 
  Users, 
  FileText, 
  Settings
} from 'lucide-react';

const features = [
  {
    icon: <Lightbulb className="h-8 w-8 text-white" />,
    title: "Intuitive Guided Process",
    description: "Our step-by-step questionnaire makes creating complex legal documents simple and straightforward.",
    color: "bg-gradient-to-br from-yellow-500 to-orange-500"
  },
  {
    icon: <ShieldCheck className="h-8 w-8 text-white" />,
    title: "Bank-Grade Security",
    description: "Your sensitive information is protected with end-to-end encryption and secure cloud storage.",
    color: "bg-gradient-to-br from-green-500 to-emerald-500"
  },
  {
    icon: <Rocket className="h-8 w-8 text-white" />,
    title: "Rapid Document Generation",
    description: "Generate complete, legally compliant documents in a fraction of the time it takes manually.",
    color: "bg-gradient-to-br from-purple-500 to-pink-500"
  },
  {
    icon: <Users className="h-8 w-8 text-white" />,
    title: "User-Friendly Interface",
    description: "Designed for clarity and ease of use, ensuring a smooth experience for all users, regardless of technical skill.",
    color: "bg-gradient-to-br from-blue-500 to-cyan-500"
  },
  {
    icon: <FileText className="h-8 w-8 text-white" />,
    title: "Comprehensive Document Library",
    description: "Access a wide range of templates for Wills, Powers of Attorney, and other essential legal forms.",
    color: "bg-gradient-to-br from-red-500 to-orange-500"
  },
  {
    icon: <Settings className="h-8 w-8 text-white" />,
    title: "Customizable Options",
    description: "Tailor each document to your specific needs with flexible options and personalized clauses.",
    color: "bg-gradient-to-br from-indigo-500 to-purple-500"
  }
];

const FeatureSpotlight = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  return (
    <section className="py-24 bg-gray-100 dark:bg-gray-800" aria-labelledby="feature-spotlight-heading">
      <div className="container mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <Badge variant="default" className="mb-4 bg-blue-600 text-white">
            Key Advantages
          </Badge>
          <h2 id="feature-spotlight-heading" className="text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Why Choose Our Platform?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Discover the core benefits that make our legal document creation platform stand out.
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => (
            <motion.div key={index} variants={itemVariants}>
              <Card className="h-full shadow-lg hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700">
                <CardHeader className="flex flex-row items-center space-x-4 pb-4">
                  <div className={`p-3 rounded-lg ${feature.color}`} aria-hidden="true">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl font-bold text-gray-900 dark:text-white">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default FeatureSpotlight;

