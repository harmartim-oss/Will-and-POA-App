import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Mail, Phone, MapPin, Github, Twitter, Linkedin } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    product: [
      { label: 'Features', path: '/#features' },
      { label: 'How It Works', path: '/#how-it-works' },
      { label: 'Pricing', path: '/#pricing' },
      { label: 'FAQ', path: '/#faq' }
    ],
    legal: [
      { label: 'Privacy Policy', path: '/privacy' },
      { label: 'Terms of Service', path: '/terms' },
      { label: 'Legal Disclaimer', path: '/disclaimer' },
      { label: 'Cookie Policy', path: '/cookies' }
    ],
    support: [
      { label: 'Help Center', path: '/help' },
      { label: 'Contact Us', path: '/contact' },
      { label: 'Documentation', path: '/docs' },
      { label: 'Community', path: '/community' }
    ]
  };

  const socialLinks = [
    { icon: Github, href: 'https://github.com/harmartim-oss/Will-and-POA-App', label: 'GitHub' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Linkedin, href: '#', label: 'LinkedIn' }
  ];

  return (
    <footer className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 border-t-2 border-gray-200 dark:border-gray-700 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 py-14">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <Link to="/" className="flex items-center space-x-2 group mb-5">
              <div className="p-2.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl group-hover:scale-110 transition-transform duration-200 shadow-lg">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <span className="text-lg font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Ontario Wills & POA
              </span>
            </Link>
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-5 leading-relaxed">
              Professional legal document creation with AI assistance. Create legally compliant wills 
              and power of attorney documents for Ontario with confidence and ease.
            </p>
            
            {/* Contact Info */}
            <div className="space-y-3 text-sm">
              <div className="flex items-center text-gray-600 dark:text-gray-400 group">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                  <Mail className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                </div>
                <a href="mailto:support@ontariowills.com" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium">
                  support@ontariowills.com
                </a>
              </div>
              <div className="flex items-center text-gray-600 dark:text-gray-400 group">
                <div className="w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                  <Phone className="h-4 w-4 text-green-600 dark:text-green-400" />
                </div>
                <a href="tel:+1234567890" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors font-medium">
                  +1 (234) 567-890
                </a>
              </div>
              <div className="flex items-center text-gray-600 dark:text-gray-400 group">
                <div className="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                  <MapPin className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                </div>
                <span className="font-medium">Toronto, Ontario, Canada</span>
              </div>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="text-gray-900 dark:text-white font-bold mb-5 text-base">Product</h3>
            <ul className="space-y-3">
              {footerLinks.product.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.path}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm transition-all duration-200 hover:translate-x-1 inline-block font-medium"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h3 className="text-gray-900 dark:text-white font-bold mb-5 text-base">Legal</h3>
            <ul className="space-y-3">
              {footerLinks.legal.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.path}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm transition-all duration-200 hover:translate-x-1 inline-block font-medium"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h3 className="text-gray-900 dark:text-white font-bold mb-5 text-base">Support</h3>
            <ul className="space-y-3">
              {footerLinks.support.map((link, index) => (
                <li key={index}>
                  <Link
                    to={link.path}
                    className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm transition-all duration-200 hover:translate-x-1 inline-block font-medium"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="py-8 border-t-2 border-gray-200 dark:border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0 pb-4">
            {/* Copyright */}
            <p className="text-gray-600 dark:text-gray-400 text-sm text-center md:text-left font-medium">
              © {currentYear} Ontario Wills & Power of Attorney Creator. All rights reserved.
            </p>

            {/* Social Links */}
            <div className="flex items-center space-x-3">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2.5 rounded-xl text-gray-600 dark:text-gray-400 hover:text-white bg-gray-200 dark:bg-gray-800 hover:bg-gradient-to-r hover:from-blue-600 hover:to-purple-600 transition-all duration-200 hover:scale-110 shadow-md hover:shadow-lg"
                  aria-label={social.label}
                >
                  <social.icon className="h-5 w-5" />
                </a>
              ))}
            </div>

            {/* Disclaimer */}
            <p className="text-xs text-gray-500 dark:text-gray-500 text-center md:text-right max-w-md font-medium bg-yellow-50 dark:bg-yellow-900/20 px-4 py-2 rounded-lg border border-yellow-200 dark:border-yellow-800">
              This tool provides information only. Consult with a licensed lawyer for legal advice.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
