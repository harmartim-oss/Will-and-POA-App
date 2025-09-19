import React, { createContext, useContext, useState, useEffect } from 'react';
import { documentService } from '../services/documentService';
import { useAuth } from './AuthContext';

const DocumentContext = createContext();

export const useDocument = () => {
  const context = useContext(DocumentContext);
  if (!context) {
    throw new Error('useDocument must be used within a DocumentProvider');
  }
  return context;
};

export const DocumentProvider = ({ children }) => {
  const { user } = useAuth();
  const [documents, setDocuments] = useState([]);
  const [currentDocument, setCurrentDocument] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      loadUserDocuments();
    } else {
      setDocuments([]);
      setCurrentDocument(null);
    }
  }, [user]);

  const loadUserDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.getUserDocuments();
      
      if (result.success) {
        setDocuments(result.documents || []);
      } else {
        setError(result.error || 'Failed to load documents');
      }
    } catch (error) {
      console.error('Error loading documents:', error);
      setError('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const createDocument = async (documentType, formData) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.createDocument(documentType, formData);
      
      if (result.success) {
        const newDocument = result.document;
        setDocuments(prev => [newDocument, ...prev]);
        setCurrentDocument(newDocument);
        return { success: true, document: newDocument };
      } else {
        setError(result.error || 'Failed to create document');
        return { success: false, error: result.error || 'Failed to create document' };
      }
    } catch (error) {
      console.error('Error creating document:', error);
      const errorMessage = 'Failed to create document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const updateDocument = async (documentId, updates) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.updateDocument(documentId, updates);
      
      if (result.success) {
        const updatedDocument = result.document;
        
        // Update documents list
        setDocuments(prev => 
          prev.map(doc => doc.id === documentId ? updatedDocument : doc)
        );
        
        // Update current document if it's the one being updated
        if (currentDocument?.id === documentId) {
          setCurrentDocument(updatedDocument);
        }
        
        return { success: true, document: updatedDocument };
      } else {
        setError(result.error || 'Failed to update document');
        return { success: false, error: result.error || 'Failed to update document' };
      }
    } catch (error) {
      console.error('Error updating document:', error);
      const errorMessage = 'Failed to update document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const deleteDocument = async (documentId) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.deleteDocument(documentId);
      
      if (result.success) {
        // Remove from documents list
        setDocuments(prev => prev.filter(doc => doc.id !== documentId));
        
        // Clear current document if it's the one being deleted
        if (currentDocument?.id === documentId) {
          setCurrentDocument(null);
        }
        
        return { success: true };
      } else {
        setError(result.error || 'Failed to delete document');
        return { success: false, error: result.error || 'Failed to delete document' };
      }
    } catch (error) {
      console.error('Error deleting document:', error);
      const errorMessage = 'Failed to delete document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const loadDocument = async (documentId) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.getDocument(documentId);
      
      if (result.success) {
        setCurrentDocument(result.document);
        return { success: true, document: result.document };
      } else {
        setError(result.error || 'Failed to load document');
        return { success: false, error: result.error || 'Failed to load document' };
      }
    } catch (error) {
      console.error('Error loading document:', error);
      const errorMessage = 'Failed to load document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const generateDocument = async (documentId, includeAI = true) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.generateDocument(documentId, includeAI);
      
      if (result.success) {
        const updatedDocument = result.document;
        
        // Update documents list
        setDocuments(prev => 
          prev.map(doc => doc.id === documentId ? updatedDocument : doc)
        );
        
        // Update current document
        if (currentDocument?.id === documentId) {
          setCurrentDocument(updatedDocument);
        }
        
        return { success: true, document: updatedDocument, analysis: result.analysis };
      } else {
        setError(result.error || 'Failed to generate document');
        return { success: false, error: result.error || 'Failed to generate document' };
      }
    } catch (error) {
      console.error('Error generating document:', error);
      const errorMessage = 'Failed to generate document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const analyzeDocument = async (documentId) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.analyzeDocument(documentId);
      
      if (result.success) {
        return { success: true, analysis: result.analysis };
      } else {
        setError(result.error || 'Failed to analyze document');
        return { success: false, error: result.error || 'Failed to analyze document' };
      }
    } catch (error) {
      console.error('Error analyzing document:', error);
      const errorMessage = 'Failed to analyze document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const exportDocument = async (documentId, format = 'pdf') => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.exportDocument(documentId, format);
      
      if (result.success) {
        return { success: true, downloadUrl: result.downloadUrl };
      } else {
        setError(result.error || 'Failed to export document');
        return { success: false, error: result.error || 'Failed to export document' };
      }
    } catch (error) {
      console.error('Error exporting document:', error);
      const errorMessage = 'Failed to export document';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const sendForSignature = async (documentId, signers, options = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.sendForSignature(documentId, signers, options);
      
      if (result.success) {
        // Update document status
        const updatedDocument = { ...currentDocument, status: 'sent_for_signature' };
        setCurrentDocument(updatedDocument);
        
        setDocuments(prev => 
          prev.map(doc => doc.id === documentId ? updatedDocument : doc)
        );
        
        return { success: true, envelopeId: result.envelopeId };
      } else {
        setError(result.error || 'Failed to send for signature');
        return { success: false, error: result.error || 'Failed to send for signature' };
      }
    } catch (error) {
      console.error('Error sending for signature:', error);
      const errorMessage = 'Failed to send for signature';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const submitForReview = async (documentId, reviewOptions = {}) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await documentService.submitForReview(documentId, reviewOptions);
      
      if (result.success) {
        // Update document status
        const updatedDocument = { ...currentDocument, status: 'under_review' };
        setCurrentDocument(updatedDocument);
        
        setDocuments(prev => 
          prev.map(doc => doc.id === documentId ? updatedDocument : doc)
        );
        
        return { success: true, reviewId: result.reviewId };
      } else {
        setError(result.error || 'Failed to submit for review');
        return { success: false, error: result.error || 'Failed to submit for review' };
      }
    } catch (error) {
      console.error('Error submitting for review:', error);
      const errorMessage = 'Failed to submit for review';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => {
    setError(null);
  };

  const clearCurrentDocument = () => {
    setCurrentDocument(null);
  };

  const value = {
    documents,
    currentDocument,
    loading,
    error,
    loadUserDocuments,
    createDocument,
    updateDocument,
    deleteDocument,
    loadDocument,
    generateDocument,
    analyzeDocument,
    exportDocument,
    sendForSignature,
    submitForReview,
    clearError,
    clearCurrentDocument,
    setCurrentDocument
  };

  return (
    <DocumentContext.Provider value={value}>
      {children}
    </DocumentContext.Provider>
  );
};

