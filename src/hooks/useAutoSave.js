import { useEffect, useRef, useCallback, useState } from 'react';
import { toast } from 'sonner';

/**
 * Custom hook for auto-saving form data with debouncing and conflict resolution
 * @param {Object} data - The data to auto-save
 * @param {Function} saveFunction - Function to call for saving (should return a Promise)
 * @param {Object} options - Configuration options
 * @returns {Object} - Auto-save status and controls
 */
export const useAutoSave = (data, saveFunction, options = {}) => {
  const {
    delay = 2000, // Debounce delay in milliseconds
    enabled = true, // Whether auto-save is enabled
    key = 'autosave', // Storage key for local backup
    showToasts = true, // Whether to show save status toasts
    onSaveSuccess = () => {}, // Callback on successful save
    onSaveError = () => {}, // Callback on save error
    maxRetries = 3, // Maximum retry attempts
    retryDelay = 1000, // Delay between retries
  } = options;

  const [saveStatus, setSaveStatus] = useState('idle'); // idle, saving, saved, error
  const [lastSaved, setLastSaved] = useState(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const timeoutRef = useRef(null);
  const lastDataRef = useRef(null);
  const saveInProgressRef = useRef(false);
  const retryTimeoutRef = useRef(null);

  // Save to localStorage as backup
  const saveToLocalStorage = useCallback((dataToSave) => {
    try {
      const backup = {
        data: dataToSave,
        timestamp: Date.now(),
        version: '1.0'
      };
      localStorage.setItem(`${key}_backup`, JSON.stringify(backup));
    } catch (error) {
      console.warn('Failed to save backup to localStorage:', error);
    }
  }, [key]);

  // Load from localStorage backup
  const loadFromLocalStorage = useCallback(() => {
    try {
      const backup = localStorage.getItem(`${key}_backup`);
      if (backup) {
        const parsed = JSON.parse(backup);
        return parsed;
      }
    } catch (error) {
      console.warn('Failed to load backup from localStorage:', error);
    }
    return null;
  }, [key]);

  // Clear localStorage backup
  const clearLocalStorage = useCallback(() => {
    try {
      localStorage.removeItem(`${key}_backup`);
    } catch (error) {
      console.warn('Failed to clear backup from localStorage:', error);
    }
  }, [key]);

  // Perform the actual save operation with retry logic
  const performSave = useCallback(async (dataToSave, attempt = 1) => {
    if (saveInProgressRef.current) return;
    
    saveInProgressRef.current = true;
    setSaveStatus('saving');
    
    try {
      await saveFunction(dataToSave);
      
      // Success
      setSaveStatus('saved');
      setLastSaved(new Date());
      setHasUnsavedChanges(false);
      setRetryCount(0);
      
      // Clear backup since we successfully saved
      clearLocalStorage();
      
      if (showToasts) {
        toast.success('Changes saved automatically', {
          duration: 2000,
          position: 'bottom-right'
        });
      }
      
      onSaveSuccess(dataToSave);
      
    } catch (error) {
      console.error('Auto-save failed:', error);
      
      if (attempt < maxRetries) {
        // Retry after delay
        setRetryCount(attempt);
        retryTimeoutRef.current = setTimeout(() => {
          performSave(dataToSave, attempt + 1);
        }, retryDelay * attempt); // Exponential backoff
        
        if (showToasts) {
          toast.warning(`Save failed, retrying... (${attempt}/${maxRetries})`, {
            duration: 3000,
            position: 'bottom-right'
          });
        }
      } else {
        // Max retries reached
        setSaveStatus('error');
        setRetryCount(0);
        
        // Keep backup in localStorage since save failed
        saveToLocalStorage(dataToSave);
        
        if (showToasts) {
          toast.error('Failed to save changes. Data backed up locally.', {
            duration: 5000,
            position: 'bottom-right',
            action: {
              label: 'Retry',
              onClick: () => performSave(dataToSave, 1)
            }
          });
        }
        
        onSaveError(error, dataToSave);
      }
    } finally {
      saveInProgressRef.current = false;
    }
  }, [saveFunction, maxRetries, retryDelay, showToasts, onSaveSuccess, onSaveError, saveToLocalStorage, clearLocalStorage]);

  // Debounced save function
  const debouncedSave = useCallback((dataToSave) => {
    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    // Clear retry timeout if exists
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
      retryTimeoutRef.current = null;
    }
    
    // Set new timeout
    timeoutRef.current = setTimeout(() => {
      performSave(dataToSave);
    }, delay);
    
    // Save backup immediately
    saveToLocalStorage(dataToSave);
    setHasUnsavedChanges(true);
    
  }, [delay, performSave, saveToLocalStorage]);

  // Effect to handle data changes
  useEffect(() => {
    if (!enabled || !data) return;
    
    // Skip if data hasn't changed
    const dataString = JSON.stringify(data);
    if (dataString === JSON.stringify(lastDataRef.current)) return;
    
    lastDataRef.current = data;
    debouncedSave(data);
    
  }, [data, enabled, debouncedSave]);

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, []);

  // Manual save function
  const saveNow = useCallback(async () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    if (data) {
      await performSave(data);
    }
  }, [data, performSave]);

  // Force save function (ignores debounce and saves immediately)
  const forceSave = useCallback(async (dataToSave = data) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    if (dataToSave) {
      await performSave(dataToSave);
    }
  }, [data, performSave]);

  // Get backup data
  const getBackup = useCallback(() => {
    return loadFromLocalStorage();
  }, [loadFromLocalStorage]);

  // Check if there's a backup available
  const hasBackup = useCallback(() => {
    const backup = loadFromLocalStorage();
    return backup && backup.data;
  }, [loadFromLocalStorage]);

  // Restore from backup
  const restoreFromBackup = useCallback(() => {
    const backup = loadFromLocalStorage();
    if (backup && backup.data) {
      return backup.data;
    }
    return null;
  }, [loadFromLocalStorage]);

  return {
    // Status
    saveStatus,
    lastSaved,
    hasUnsavedChanges,
    retryCount,
    
    // Actions
    saveNow,
    forceSave,
    
    // Backup utilities
    getBackup,
    hasBackup,
    restoreFromBackup,
    clearLocalStorage,
    
    // Computed values
    isSaving: saveStatus === 'saving',
    isSaved: saveStatus === 'saved',
    hasError: saveStatus === 'error',
    isIdle: saveStatus === 'idle'
  };
};

export default useAutoSave;
