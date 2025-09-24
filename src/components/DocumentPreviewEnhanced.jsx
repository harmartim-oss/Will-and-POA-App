import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Document, Page, pdfjs } from 'react-pdf';
import html2canvas from 'html2canvas';
import { 
  FileText, 
  Download, 
  Share2, 
  Printer, 
  ZoomIn, 
  ZoomOut, 
  RotateCw,
  Eye,
  AlertCircle,
  CheckCircle,
  Brain,
  Sparkles,
  X,
  Maximize2,
  Minimize2
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { ScrollArea } from './ui/scroll-area';
import { Progress } from './ui/progress';

// Set PDF.js worker source
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

const DocumentPreviewEnhanced = ({ 
  documentData, 
  documentType = 'will', 
  onClose, 
  onDownload, 
  onShare 
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [numPages, setNumPages] = useState(null);
  const [scale, setScale] = useState(1.0);
  const [rotation, setRotation] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [complianceScore, setComplianceScore] = useState(92);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(true);
  
  const previewRef = useRef();
  const documentRef = useRef();

  // Sample document content for demonstration
  const sampleDocumentContent = {
    will: {
      title: "LAST WILL AND TESTAMENT",
      content: `I, [TESTATOR NAME], of [ADDRESS], Ontario, being of sound mind and disposing memory, do hereby make, publish and declare this to be my Last Will and Testament, hereby revoking all former Wills and Codicils by me at any time heretofore made.

1. APPOINTMENT OF EXECUTOR
I APPOINT [EXECUTOR NAME] of [EXECUTOR ADDRESS] to be the Executor and Trustee of this my Will.

2. PAYMENT OF DEBTS
I DIRECT my Executor to pay my just debts, funeral expenses, and testamentary expenses.

3. SPECIFIC BEQUESTS
I GIVE, DEVISE AND BEQUEATH [SPECIFIC ITEMS] to [BENEFICIARY NAME].

4. RESIDUARY CLAUSE
I GIVE, DEVISE AND BEQUEATH all the rest, residue and remainder of my estate, both real and personal, wheresoever situate, unto [RESIDUARY BENEFICIARY] absolutely.

IN WITNESS WHEREOF I have to this my Last Will and Testament, subscribed my name this _____ day of ____________, 2024.

_________________________________
[TESTATOR NAME]
Testator

WITNESSES:
_________________________________    _________________________________
Witness Signature                     Date
[WITNESS 1 NAME]
[WITNESS 1 ADDRESS]

_________________________________    _________________________________
Witness Signature                     Date  
[WITNESS 2 NAME]
[WITNESS 2 ADDRESS]`
    },
    poa_property: {
      title: "POWER OF ATTORNEY FOR PROPERTY",
      content: `I, [GRANTOR NAME], of [ADDRESS], Ontario, APPOINT [ATTORNEY NAME] of [ATTORNEY ADDRESS] to be my attorney for property.

I GIVE my attorney the authority to do on my behalf anything in respect of property that I could do if capable of managing property, except make a will, subject to the law and to any conditions or restrictions contained in this document.

CONDITIONS AND RESTRICTIONS:
[CONDITIONS IF ANY]

This Power of Attorney for Property shall commence immediately.

SIGNED this _____ day of ____________, 2024.

_________________________________
[GRANTOR NAME]
Grantor

WITNESS:
_________________________________    _________________________________
Witness Signature                     Date
[WITNESS NAME]
[WITNESS ADDRESS]`
    }
  };

  useEffect(() => {
    // Simulate AI analysis
    const performAnalysis = async () => {
      setIsAnalyzing(true);
      
      // Simulate analysis delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const analysis = {
        complianceScore: 92,
        issues: [
          {
            type: 'minor',
            message: 'Consider adding specific instructions for digital assets',
            suggestion: 'Add a clause covering online accounts and digital properties'
          }
        ],
        strengths: [
          'All required legal elements present',
          'Clear beneficiary designations',
          'Proper execution requirements included'
        ],
        recommendations: [
          'Review beneficiary information annually',
          'Ensure witnesses are not beneficiaries',
          'Store in secure, accessible location'
        ]
      };
      
      setAiAnalysis(analysis);
      setComplianceScore(analysis.complianceScore);
      setIsAnalyzing(false);
    };
    
    performAnalysis();
  }, []);

  const generatePDF = async () => {
    setIsGeneratingPdf(true);
    
    try {
      // Capture the document content as canvas
      const canvas = await html2canvas(documentRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff'
      });
      
      // Convert canvas to blob
      canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
        setIsGeneratingPdf(false);
      }, 'image/png');
      
    } catch (error) {
      console.error('PDF generation failed:', error);
      setIsGeneratingPdf(false);
    }
  };

  const handleDownload = () => {
    if (pdfUrl) {
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `ontario_${documentType}_${new Date().toISOString().split('T')[0]}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      generatePDF();
    }
    
    if (onDownload) onDownload();
  };

  const handlePrint = () => {
    window.print();
  };

  const handleShare = () => {
    if (navigator.share && pdfUrl) {
      navigator.share({
        title: `Ontario ${documentType.replace('_', ' ').toUpperCase()}`,
        text: 'Legal document generated with AI assistance',
        url: pdfUrl
      });
    }
    
    if (onShare) onShare();
  };

  const zoomIn = () => setScale(prev => Math.min(prev + 0.2, 2.0));
  const zoomOut = () => setScale(prev => Math.max(prev - 0.2, 0.5));
  const rotate = () => setRotation(prev => (prev + 90) % 360);

  const getComplianceColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getComplianceIcon = (score) => {
    if (score >= 90) return CheckCircle;
    if (score >= 80) return AlertCircle;
    return AlertCircle;
  };

  const ComplianceIcon = getComplianceIcon(complianceScore);

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <motion.div
          className={`bg-white dark:bg-gray-900 rounded-2xl shadow-2xl overflow-hidden ${
            isFullscreen ? 'w-full h-full' : 'w-full max-w-7xl h-[90vh]'
          }`}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.8, opacity: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              
              <div>
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Document Preview
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {documentType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())} • Ontario Legal Document
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Compliance Score */}
              <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${getComplianceColor(complianceScore)}`}>
                <ComplianceIcon className="w-4 h-4" />
                <span className="font-medium text-sm">
                  {isAnalyzing ? 'Analyzing...' : `${complianceScore}% Compliant`}
                </span>
              </div>
              
              {/* Action Buttons */}
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsFullscreen(!isFullscreen)}
                >
                  {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                </Button>
                
                <Button variant="outline" size="sm" onClick={handlePrint}>
                  <Printer className="w-4 h-4" />
                </Button>
                
                <Button variant="outline" size="sm" onClick={handleShare}>
                  <Share2 className="w-4 h-4" />
                </Button>
                
                <Button size="sm" onClick={handleDownload} disabled={isGeneratingPdf}>
                  {isGeneratingPdf ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <Download className="w-4 h-4" />
                  )}
                  <span className="ml-2">Download</span>
                </Button>
                
                <Button variant="ghost" size="sm" onClick={onClose}>
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>

          <div className="flex h-[calc(90vh-80px)]">
            {/* Sidebar - AI Analysis */}
            <div className="w-80 border-r border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
              <div className="p-4">
                <h3 className="font-semibold text-sm text-gray-700 dark:text-gray-300 mb-4 flex items-center">
                  <Brain className="w-4 h-4 mr-2 text-purple-600" />
                  AI Analysis
                </h3>
                
                {isAnalyzing ? (
                  <div className="text-center py-8">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                      className="w-12 h-12 mx-auto mb-4"
                    >
                      <Brain className="w-full h-full text-purple-600" />
                    </motion.div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Analyzing document compliance and quality...
                    </p>
                  </div>
                ) : (
                  <ScrollArea className="h-[calc(90vh-160px)]">
                    <div className="space-y-4">
                      {/* Compliance Score */}
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm flex items-center">
                            <ComplianceIcon className="w-4 h-4 mr-2" />
                            Compliance Score
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-2xl font-bold">{complianceScore}%</span>
                            <Badge variant={complianceScore >= 90 ? 'default' : 'secondary'}>
                              {complianceScore >= 90 ? 'Excellent' : 'Good'}
                            </Badge>
                          </div>
                          <Progress value={complianceScore} className="h-2" />
                        </CardContent>
                      </Card>

                      {/* Issues */}
                      {aiAnalysis?.issues?.length > 0 && (
                        <Card>
                          <CardHeader className="pb-2">
                            <CardTitle className="text-sm flex items-center">
                              <AlertCircle className="w-4 h-4 mr-2 text-yellow-600" />
                              Issues Found
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-2">
                            {aiAnalysis.issues.map((issue, index) => (
                              <div key={index} className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                                <div className="font-medium text-sm text-yellow-800 dark:text-yellow-200">
                                  {issue.message}
                                </div>
                                <div className="text-xs text-yellow-600 dark:text-yellow-400 mt-1">
                                  {issue.suggestion}
                                </div>
                              </div>
                            ))}
                          </CardContent>
                        </Card>
                      )}

                      {/* Strengths */}
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm flex items-center">
                            <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                            Strengths
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-1">
                            {aiAnalysis?.strengths?.map((strength, index) => (
                              <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                                <div className="w-1.5 h-1.5 bg-green-500 rounded-full mr-2" />
                                {strength}
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>

                      {/* Recommendations */}
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm flex items-center">
                            <Sparkles className="w-4 h-4 mr-2 text-blue-600" />
                            Recommendations
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <ul className="space-y-1">
                            {aiAnalysis?.recommendations?.map((rec, index) => (
                              <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2" />
                                {rec}
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                    </div>
                  </ScrollArea>
                )}
              </div>
            </div>

            {/* Document Preview */}
            <div className="flex-1 flex flex-col">
              {/* Toolbar */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-2">
                  <Button variant="outline" size="sm" onClick={zoomOut}>
                    <ZoomOut className="w-4 h-4" />
                  </Button>
                  <span className="text-sm font-medium px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded">
                    {Math.round(scale * 100)}%
                  </span>
                  <Button variant="outline" size="sm" onClick={zoomIn}>
                    <ZoomIn className="w-4 h-4" />
                  </Button>
                  <Separator orientation="vertical" className="h-6" />
                  <Button variant="outline" size="sm" onClick={rotate}>
                    <RotateCw className="w-4 h-4" />
                  </Button>
                </div>
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Page 1 of 1
                  </span>
                </div>
              </div>

              {/* Document Content */}
              <ScrollArea className="flex-1 p-8 bg-gray-100 dark:bg-gray-800">
                <motion.div
                  className="max-w-[8.5in] mx-auto bg-white shadow-2xl"
                  style={{ 
                    transform: `scale(${scale}) rotate(${rotation}deg)`,
                    transformOrigin: 'center'
                  }}
                  animate={{ scale, rotate: rotation }}
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                >
                  <div 
                    ref={documentRef}
                    className="w-full min-h-[11in] p-16 font-serif text-gray-900 leading-relaxed"
                    style={{ 
                      fontFamily: 'Times New Roman, serif',
                      fontSize: '12pt',
                      lineHeight: '1.5'
                    }}
                  >
                    {/* Document Header */}
                    <div className="text-center mb-12">
                      <h1 className="text-2xl font-bold mb-4 uppercase tracking-wider">
                        {sampleDocumentContent[documentType]?.title}
                      </h1>
                      <div className="w-32 h-0.5 bg-gray-400 mx-auto" />
                    </div>

                    {/* Document Content */}
                    <div className="whitespace-pre-line text-justify">
                      {sampleDocumentContent[documentType]?.content}
                    </div>

                    {/* Footer */}
                    <div className="mt-16 pt-8 border-t border-gray-300 text-center text-sm text-gray-600">
                      <p>This document was generated using AI-assisted legal document creation</p>
                      <p>Generated on {new Date().toLocaleDateString()}</p>
                    </div>
                  </div>
                </motion.div>
              </ScrollArea>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default DocumentPreviewEnhanced;