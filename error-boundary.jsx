import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, RefreshCw, Home, Mail } from 'lucide-react';
import { Button } from './button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './card';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null,
      retryCount: 0 
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // Log error to monitoring service
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'exception', {
        description: error.toString(),
        fatal: false
      });
    }

    console.error('Error caught by boundary:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState(prevState => ({
      hasError: false,
      error: null,
      errorInfo: null,
      retryCount: prevState.retryCount + 1
    }));
  };

  handleGoHome = () => {
    window.location.href = '/';
  };

  handleReportError = () => {
    const errorReport = {
      error: this.state.error?.toString(),
      stack: this.state.error?.stack,
      componentStack: this.state.errorInfo?.componentStack,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };

    const mailtoLink = `mailto:support@ontariowills.ai?subject=Error Report&body=${encodeURIComponent(
      `Error Report:\n\n${JSON.stringify(errorReport, null, 2)}`
    )}`;
    
    window.location.href = mailtoLink;
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950 dark:to-orange-950 flex items-center justify-center p-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            className="w-full max-w-2xl"
          >
            <Card className="border-red-200 dark:border-red-800 shadow-xl">
              <CardHeader className="text-center pb-6">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: "spring" }}
                  className="w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mx-auto mb-4"
                >
                  <AlertTriangle className="w-8 h-8 text-red-600 dark:text-red-400" />
                </motion.div>
                
                <CardTitle className="text-2xl text-red-900 dark:text-red-100">
                  Something went wrong
                </CardTitle>
                <CardDescription className="text-red-700 dark:text-red-300 text-base">
                  We apologize for the inconvenience. An unexpected error has occurred.
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* Error details for development */}
                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    transition={{ delay: 0.3 }}
                    className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4"
                  >
                    <h4 className="font-semibold text-red-900 dark:text-red-100 mb-2">
                      Error Details (Development Mode)
                    </h4>
                    <pre className="text-xs text-red-800 dark:text-red-200 overflow-auto max-h-32">
                      {this.state.error.toString()}
                    </pre>
                  </motion.div>
                )}

                {/* Action buttons */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="flex flex-col sm:flex-row gap-3 justify-center"
                >
                  <Button
                    onClick={this.handleRetry}
                    className="bg-red-600 hover:bg-red-700 text-white"
                    disabled={this.state.retryCount >= 3}
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    {this.state.retryCount >= 3 ? 'Max retries reached' : 'Try Again'}
                  </Button>

                  <Button
                    onClick={this.handleGoHome}
                    variant="outline"
                    className="border-red-300 text-red-700 hover:bg-red-50 dark:border-red-700 dark:text-red-300 dark:hover:bg-red-950"
                  >
                    <Home className="w-4 h-4 mr-2" />
                    Go Home
                  </Button>

                  <Button
                    onClick={this.handleReportError}
                    variant="ghost"
                    className="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-950"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    Report Error
                  </Button>
                </motion.div>

                {/* Help text */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.6 }}
                  className="text-center text-sm text-gray-600 dark:text-gray-400"
                >
                  <p>
                    If this problem persists, please contact our support team at{' '}
                    <a 
                      href="mailto:support@ontariowills.ai" 
                      className="text-red-600 dark:text-red-400 hover:underline"
                    >
                      support@ontariowills.ai
                    </a>
                  </p>
                </motion.div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
