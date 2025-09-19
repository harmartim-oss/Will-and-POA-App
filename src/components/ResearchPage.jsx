import React from 'react';
import PageHeader from './layout/PageHeader';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { BookOpen, ExternalLink } from 'lucide-react';

const LegalResearchPanel = () => {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Legal Research"
        description="Browse legal resources and requirements for Ontario wills and power of attorney documents."
        breadcrumbs={[
          { label: 'Home', href: '/' },
          { label: 'Legal Research' }
        ]}
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <BookOpen className="h-5 w-5 text-blue-600" />
              <CardTitle className="text-lg">Ontario Requirements</CardTitle>
            </div>
            <CardDescription>
              Official requirements for creating valid legal documents in Ontario.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              This section will contain comprehensive legal research tools and resources.
            </p>
            <div className="mt-4 text-xs text-gray-500">
              <span className="inline-flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Coming Soon
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Case Law</CardTitle>
            <CardDescription>
              Relevant case law and precedents for estate planning.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Browse relevant legal precedents and case law.
            </p>
            <div className="mt-4 text-xs text-gray-500">
              <span className="inline-flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Coming Soon
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Forms & Templates</CardTitle>
            <CardDescription>
              Standard forms and document templates.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Access standard legal forms and document templates.
            </p>
            <div className="mt-4 text-xs text-gray-500">
              <span className="inline-flex items-center">
                <ExternalLink className="h-3 w-3 mr-1" />
                Coming Soon
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LegalResearchPanel;