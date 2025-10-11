import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, FileText, Zap } from 'lucide-react';
import { Button } from './ui/button';

const CallToAction = ({ onGetStarted }) => {
  return (
    <section className="py-24 bg-gradient-to-br from-[var(--color-brand-600)] to-[var(--color-accent-600)] text-white relative overflow-hidden" aria-labelledby="cta-heading">
      <div className="absolute inset-0 opacity-20" style={{
        backgroundImage: `url("data:image/svg+xml,${encodeURIComponent('<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="#ffffff" fill-opacity="0.05"><circle cx="10" cy="10" r="1"/></g></g></svg>')}")`,
      }} aria-hidden="true"></div>
      
      <div className="container mx-auto px-6 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8 }}
        >
          <h2 id="cta-heading" className="text-4xl lg:text-5xl font-bold mb-6 leading-tight">
            Ready to Secure Your Future?
          </h2>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed mb-10">
            Create your legally-binding Ontario Will and Power of Attorney documents in minutes. 
            Our AI-powered platform makes it simple, secure, and affordable.
          </p>
          <Button
            variant="primary"
            size="xl"
            onClick={onGetStarted}
            className="group bg-white text-[var(--color-brand-700)] hover:bg-gray-50 shadow-xl hover:shadow-2xl rounded-xl font-semibold px-8 py-6 text-lg"
          >
            <Zap className="h-5 w-5 mr-2" />
            Start Creating Documents Now
            <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default CallToAction;

