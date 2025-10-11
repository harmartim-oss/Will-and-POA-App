/**
 * Performance monitoring utility for tracking Core Web Vitals and custom metrics
 */

class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.observers = new Map();
    this.isSupported = this.checkSupport();
    
    if (this.isSupported) {
      this.initializeObservers();
    }
  }

  checkSupport() {
    return (
      typeof window !== 'undefined' &&
      'performance' in window &&
      'PerformanceObserver' in window
    );
  }

  initializeObservers() {
    // Core Web Vitals
    this.observeLCP(); // Largest Contentful Paint
    this.observeFID(); // First Input Delay
    this.observeCLS(); // Cumulative Layout Shift
    this.observeFCP(); // First Contentful Paint
    this.observeTTFB(); // Time to First Byte
    
    // Custom metrics
    this.observeResourceTiming();
    this.observeNavigationTiming();
  }

  // Largest Contentful Paint (LCP)
  observeLCP() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        
        this.recordMetric('LCP', {
          value: lastEntry.startTime,
          rating: this.rateLCP(lastEntry.startTime),
          timestamp: Date.now(),
          element: lastEntry.element?.tagName || 'unknown'
        });
      });
      
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
      this.observers.set('lcp', observer);
    } catch (error) {
      console.warn('LCP observation failed:', error);
    }
  }

  // First Input Delay (FID)
  observeFID() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          this.recordMetric('FID', {
            value: entry.processingStart - entry.startTime,
            rating: this.rateFID(entry.processingStart - entry.startTime),
            timestamp: Date.now(),
            eventType: entry.name
          });
        });
      });
      
      observer.observe({ entryTypes: ['first-input'] });
      this.observers.set('fid', observer);
    } catch (error) {
      console.warn('FID observation failed:', error);
    }
  }

  // Cumulative Layout Shift (CLS)
  observeCLS() {
    try {
      let clsValue = 0;
      let sessionValue = 0;
      let sessionEntries = [];
      
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        
        entries.forEach((entry) => {
          if (!entry.hadRecentInput) {
            const firstSessionEntry = sessionEntries[0];
            const lastSessionEntry = sessionEntries[sessionEntries.length - 1];
            
            if (sessionValue &&
                entry.startTime - lastSessionEntry.startTime < 1000 &&
                entry.startTime - firstSessionEntry.startTime < 5000) {
              sessionValue += entry.value;
              sessionEntries.push(entry);
            } else {
              sessionValue = entry.value;
              sessionEntries = [entry];
            }
            
            if (sessionValue > clsValue) {
              clsValue = sessionValue;
              this.recordMetric('CLS', {
                value: clsValue,
                rating: this.rateCLS(clsValue),
                timestamp: Date.now(),
                entries: sessionEntries.length
              });
            }
          }
        });
      });
      
      observer.observe({ entryTypes: ['layout-shift'] });
      this.observers.set('cls', observer);
    } catch (error) {
      console.warn('CLS observation failed:', error);
    }
  }

  // First Contentful Paint (FCP)
  observeFCP() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.name === 'first-contentful-paint') {
            this.recordMetric('FCP', {
              value: entry.startTime,
              rating: this.rateFCP(entry.startTime),
              timestamp: Date.now()
            });
          }
        });
      });
      
      observer.observe({ entryTypes: ['paint'] });
      this.observers.set('fcp', observer);
    } catch (error) {
      console.warn('FCP observation failed:', error);
    }
  }

  // Time to First Byte (TTFB)
  observeTTFB() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.entryType === 'navigation') {
            const ttfb = entry.responseStart - entry.requestStart;
            this.recordMetric('TTFB', {
              value: ttfb,
              rating: this.rateTTFB(ttfb),
              timestamp: Date.now()
            });
          }
        });
      });
      
      observer.observe({ entryTypes: ['navigation'] });
      this.observers.set('ttfb', observer);
    } catch (error) {
      console.warn('TTFB observation failed:', error);
    }
  }

  // Resource timing
  observeResourceTiming() {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (entry.initiatorType === 'script' || entry.initiatorType === 'css') {
            this.recordMetric('ResourceTiming', {
              name: entry.name,
              type: entry.initiatorType,
              duration: entry.duration,
              size: entry.transferSize || 0,
              timestamp: Date.now()
            });
          }
        });
      });
      
      observer.observe({ entryTypes: ['resource'] });
      this.observers.set('resource', observer);
    } catch (error) {
      console.warn('Resource timing observation failed:', error);
    }
  }

  // Navigation timing
  observeNavigationTiming() {
    try {
      if (performance.getEntriesByType) {
        const navEntries = performance.getEntriesByType('navigation');
        if (navEntries.length > 0) {
          const entry = navEntries[0];
          this.recordMetric('NavigationTiming', {
            domContentLoaded: entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart,
            loadComplete: entry.loadEventEnd - entry.loadEventStart,
            domInteractive: entry.domInteractive - entry.fetchStart,
            timestamp: Date.now()
          });
        }
      }
    } catch (error) {
      console.warn('Navigation timing observation failed:', error);
    }
  }

  // Custom metric tracking
  startTiming(name) {
    if (!this.isSupported) return;
    
    const startTime = performance.now();
    this.metrics.set(`${name}_start`, startTime);
    
    return {
      end: () => {
        const endTime = performance.now();
        const duration = endTime - startTime;
        this.recordMetric('CustomTiming', {
          name,
          duration,
          timestamp: Date.now()
        });
        this.metrics.delete(`${name}_start`);
        return duration;
      }
    };
  }

  // Record a metric
  recordMetric(type, data) {
    const metricKey = `${type}_${Date.now()}`;
    this.metrics.set(metricKey, {
      type,
      ...data
    });

    // Send to analytics if available
    this.sendToAnalytics(type, data);
    
    // Log in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[Performance] ${type}:`, data);
    }
  }

  // Send metrics to analytics service
  sendToAnalytics(type, data) {
    try {
      // Google Analytics 4
      if (typeof gtag !== 'undefined') {
        gtag('event', 'web_vital', {
          event_category: 'Performance',
          event_label: type,
          value: Math.round(data.value || data.duration || 0),
          custom_parameter_1: data.rating || 'unknown'
        });
      }

      // Custom analytics endpoint
      if (window.analytics && typeof window.analytics.track === 'function') {
        window.analytics.track('Performance Metric', {
          metric: type,
          value: data.value || data.duration || 0,
          rating: data.rating || 'unknown',
          timestamp: data.timestamp
        });
      }
    } catch (error) {
      console.warn('Failed to send analytics:', error);
    }
  }

  // Rating functions for Core Web Vitals
  rateLCP(value) {
    if (value <= 2500) return 'good';
    if (value <= 4000) return 'needs-improvement';
    return 'poor';
  }

  rateFID(value) {
    if (value <= 100) return 'good';
    if (value <= 300) return 'needs-improvement';
    return 'poor';
  }

  rateCLS(value) {
    if (value <= 0.1) return 'good';
    if (value <= 0.25) return 'needs-improvement';
    return 'poor';
  }

  rateFCP(value) {
    if (value <= 1800) return 'good';
    if (value <= 3000) return 'needs-improvement';
    return 'poor';
  }

  rateTTFB(value) {
    if (value <= 800) return 'good';
    if (value <= 1800) return 'needs-improvement';
    return 'poor';
  }

  // Get all metrics
  getMetrics() {
    const metrics = {};
    this.metrics.forEach((value, key) => {
      metrics[key] = value;
    });
    return metrics;
  }

  // Get metrics by type
  getMetricsByType(type) {
    const metrics = [];
    this.metrics.forEach((value, key) => {
      if (value.type === type) {
        metrics.push(value);
      }
    });
    return metrics;
  }

  // Get Core Web Vitals summary
  getCoreWebVitals() {
    return {
      LCP: this.getLatestMetric('LCP'),
      FID: this.getLatestMetric('FID'),
      CLS: this.getLatestMetric('CLS'),
      FCP: this.getLatestMetric('FCP'),
      TTFB: this.getLatestMetric('TTFB')
    };
  }

  getLatestMetric(type) {
    const metrics = this.getMetricsByType(type);
    return metrics.length > 0 ? metrics[metrics.length - 1] : null;
  }

  // Generate performance report
  generateReport() {
    const cwv = this.getCoreWebVitals();
    const customMetrics = this.getMetricsByType('CustomTiming');
    const resourceMetrics = this.getMetricsByType('ResourceTiming');

    return {
      timestamp: Date.now(),
      coreWebVitals: cwv,
      customMetrics: customMetrics.slice(-10), // Last 10 custom metrics
      resourceMetrics: resourceMetrics.slice(-20), // Last 20 resource metrics
      summary: {
        lcp: cwv.LCP?.rating || 'unknown',
        fid: cwv.FID?.rating || 'unknown',
        cls: cwv.CLS?.rating || 'unknown',
        fcp: cwv.FCP?.rating || 'unknown',
        ttfb: cwv.TTFB?.rating || 'unknown'
      }
    };
  }

  // Clean up observers
  disconnect() {
    this.observers.forEach((observer) => {
      try {
        observer.disconnect();
      } catch (error) {
        console.warn('Failed to disconnect observer:', error);
      }
    });
    this.observers.clear();
    this.metrics.clear();
  }
}

// Create singleton instance
const performanceMonitor = new PerformanceMonitor();

// React hook for using performance monitoring
export const usePerformanceMonitor = () => {
  const startTiming = (name) => performanceMonitor.startTiming(name);
  const getMetrics = () => performanceMonitor.getMetrics();
  const getCoreWebVitals = () => performanceMonitor.getCoreWebVitals();
  const generateReport = () => performanceMonitor.generateReport();

  return {
    startTiming,
    getMetrics,
    getCoreWebVitals,
    generateReport
  };
};

// Utility functions
export const measureFunction = (fn, name) => {
  const timer = performanceMonitor.startTiming(name);
  const result = fn();
  timer.end();
  return result;
};

export const measureAsyncFunction = async (fn, name) => {
  const timer = performanceMonitor.startTiming(name);
  try {
    const result = await fn();
    timer.end();
    return result;
  } catch (error) {
    timer.end();
    throw error;
  }
};

// Initialize performance monitoring
export const initPerformanceMonitoring = (config = {}) => {
  const {
    enableConsoleLogging = process.env.NODE_ENV === 'development',
    enableAnalytics = true,
    reportInterval = 30000 // 30 seconds
  } = config;

  if (enableConsoleLogging) {
    // Log performance report periodically
    setInterval(() => {
      const report = performanceMonitor.generateReport();
      console.group('Performance Report');
      console.table(report.summary);
      console.groupEnd();
    }, reportInterval);
  }

  // Send initial page load metrics after a delay
  setTimeout(() => {
    const report = performanceMonitor.generateReport();
    if (enableAnalytics && typeof gtag !== 'undefined') {
      gtag('event', 'page_performance', {
        event_category: 'Performance',
        lcp_rating: report.summary.lcp,
        fid_rating: report.summary.fid,
        cls_rating: report.summary.cls
      });
    }
  }, 5000);

  return performanceMonitor;
};

export default performanceMonitor;
