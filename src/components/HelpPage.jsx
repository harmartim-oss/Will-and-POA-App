import React from 'react';
import PageHeader from './layout/PageHeader';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { HelpCircle, MessageCircle, Book, Mail } from 'lucide-react';
import { Button } from './ui/button';

const HelpPage = () => {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Help & Support"
        description="Get assistance with creating your legal documents and find answers to common questions."
        breadcrumbs={[
          { label: 'Home', href: '/' },
          { label: 'Help & Support' }
        ]}
      />

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <HelpCircle className="h-5 w-5 text-blue-600" />
              <CardTitle className="text-lg">Frequently Asked Questions</CardTitle>
            </div>
            <CardDescription>
              Find answers to the most common questions about wills and power of attorney.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-sm">Common Questions:</h4>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <li>• What makes a will legally valid in Ontario?</li>
                <li>• How many witnesses do I need?</li>
                <li>• Can I update my documents later?</li>
                <li>• What's the difference between POA types?</li>
              </ul>
            </div>
            <Button variant="outline" size="sm">
              View All FAQs
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Book className="h-5 w-5 text-green-600" />
              <CardTitle className="text-lg">User Guide</CardTitle>
            </div>
            <CardDescription>
              Step-by-step instructions for using the document creator.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h4 className="font-medium text-sm">Getting Started:</h4>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <li>• Understanding the wizard process</li>
                <li>• Preparing required information</li>
                <li>• Tips for completing forms</li>
                <li>• Reviewing and finalizing documents</li>
              </ul>
            </div>
            <Button variant="outline" size="sm">
              Read Guide
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <MessageCircle className="h-5 w-5 text-purple-600" />
              <CardTitle className="text-lg">Live Chat Support</CardTitle>
            </div>
            <CardDescription>
              Chat with our support team for immediate assistance.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Our support team is available to help you with any questions about using the platform or understanding legal requirements.
            </p>
            <Button variant="outline" size="sm" disabled>
              Start Chat (Coming Soon)
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Mail className="h-5 w-5 text-orange-600" />
              <CardTitle className="text-lg">Contact Support</CardTitle>
            </div>
            <CardDescription>
              Send us an email for detailed questions or technical issues.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              For complex questions or technical issues, email our support team and we'll get back to you within 24 hours.
            </p>
            <Button variant="outline" size="sm" disabled>
              Send Email (Coming Soon)
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Disclaimer */}
      <Card className="border-yellow-200 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-900/20">
        <CardContent className="pt-6">
          <div className="flex items-start space-x-3">
            <HelpCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
            <div className="space-y-2">
              <h4 className="font-medium text-yellow-800 dark:text-yellow-200">
                Important Legal Notice
              </h4>
              <p className="text-sm text-yellow-700 dark:text-yellow-300">
                This tool provides general information and document templates. For complex situations or specific legal advice, 
                please consult with a qualified lawyer. We are not liable for the legal validity or completeness of documents 
                created using this platform.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default HelpPage;