/**
 * Accessibility audit utility for WCAG 2.1 compliance checking
 */

class AccessibilityAuditor {
  constructor() {
    this.issues = [];
    this.warnings = [];
    this.suggestions = [];
    this.isSupported = typeof window !== 'undefined' && typeof document !== 'undefined';
  }

  // Main audit function
  audit(element = document.body) {
    if (!this.isSupported) {
      console.warn('Accessibility audit not supported in this environment');
      return this.generateReport();
    }

    this.reset();
    
    // Run all audit checks
    this.checkColorContrast(element);
    this.checkKeyboardNavigation(element);
    this.checkAriaLabels(element);
    this.checkHeadingStructure(element);
    this.checkImageAltText(element);
    this.checkFormLabels(element);
    this.checkFocusManagement(element);
    this.checkSemanticHTML(element);
    this.checkLinkAccessibility(element);
    this.checkTableAccessibility(element);
    this.checkMotionPreferences();
    this.checkTextScaling();
    this.checkLandmarks(element);

    return this.generateReport();
  }

  reset() {
    this.issues = [];
    this.warnings = [];
    this.suggestions = [];
  }

  // Color contrast checking (WCAG 2.1 AA)
  checkColorContrast(element) {
    const textElements = element.querySelectorAll('*');
    
    textElements.forEach((el) => {
      if (this.hasTextContent(el)) {
        const styles = window.getComputedStyle(el);
        const color = styles.color;
        const backgroundColor = styles.backgroundColor;
        const fontSize = parseFloat(styles.fontSize);
        const fontWeight = styles.fontWeight;
        
        if (color && backgroundColor && backgroundColor !== 'rgba(0, 0, 0, 0)') {
          const contrast = this.calculateContrast(color, backgroundColor);
          const isLargeText = fontSize >= 18 || (fontSize >= 14 && (fontWeight === 'bold' || parseInt(fontWeight) >= 700));
          const requiredRatio = isLargeText ? 3 : 4.5;
          
          if (contrast < requiredRatio) {
            this.addIssue('color-contrast', {
              element: el,
              message: `Insufficient color contrast ratio: ${contrast.toFixed(2)} (required: ${requiredRatio})`,
              severity: 'error',
              wcag: '1.4.3'
            });
          } else if (contrast < (isLargeText ? 4.5 : 7)) {
            this.addSuggestion('color-contrast-aaa', {
              element: el,
              message: `Consider improving contrast for AAA compliance: ${contrast.toFixed(2)}`,
              severity: 'suggestion'
            });
          }
        }
      }
    });
  }

  // Keyboard navigation checking
  checkKeyboardNavigation(element) {
    const interactiveElements = element.querySelectorAll(
      'button, a, input, select, textarea, [tabindex], [role="button"], [role="link"]'
    );
    
    interactiveElements.forEach((el) => {
      // Check if element is focusable
      if (!this.isFocusable(el)) {
        this.addIssue('keyboard-navigation', {
          element: el,
          message: 'Interactive element is not keyboard focusable',
          severity: 'error',
          wcag: '2.1.1'
        });
      }
      
      // Check for focus indicators
      if (!this.hasFocusIndicator(el)) {
        this.addWarning('focus-indicator', {
          element: el,
          message: 'Element may not have visible focus indicator',
          severity: 'warning',
          wcag: '2.4.7'
        });
      }
      
      // Check tabindex values
      const tabindex = el.getAttribute('tabindex');
      if (tabindex && parseInt(tabindex) > 0) {
        this.addWarning('positive-tabindex', {
          element: el,
          message: 'Avoid positive tabindex values',
          severity: 'warning',
          wcag: '2.4.3'
        });
      }
    });
  }

  // ARIA labels and attributes checking
  checkAriaLabels(element) {
    const elementsNeedingLabels = element.querySelectorAll(
      'button, input, select, textarea, [role="button"], [role="checkbox"], [role="radio"]'
    );
    
    elementsNeedingLabels.forEach((el) => {
      const hasLabel = this.hasAccessibleName(el);
      
      if (!hasLabel) {
        this.addIssue('missing-label', {
          element: el,
          message: 'Interactive element lacks accessible name',
          severity: 'error',
          wcag: '4.1.2'
        });
      }
    });

    // Check for invalid ARIA attributes
    const elementsWithAria = element.querySelectorAll('[aria-*]');
    elementsWithAria.forEach((el) => {
      Array.from(el.attributes).forEach((attr) => {
        if (attr.name.startsWith('aria-')) {
          if (!this.isValidAriaAttribute(attr.name, attr.value, el)) {
            this.addIssue('invalid-aria', {
              element: el,
              message: `Invalid ARIA attribute: ${attr.name}="${attr.value}"`,
              severity: 'error',
              wcag: '4.1.2'
            });
          }
        }
      });
    });
  }

  // Heading structure checking
  checkHeadingStructure(element) {
    const headings = element.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]');
    let previousLevel = 0;
    let hasH1 = false;
    
    headings.forEach((heading) => {
      const level = this.getHeadingLevel(heading);
      
      if (level === 1) {
        if (hasH1) {
          this.addWarning('multiple-h1', {
            element: heading,
            message: 'Multiple H1 elements found on page',
            severity: 'warning',
            wcag: '1.3.1'
          });
        }
        hasH1 = true;
      }
      
      if (previousLevel > 0 && level > previousLevel + 1) {
        this.addIssue('heading-skip', {
          element: heading,
          message: `Heading level skipped from H${previousLevel} to H${level}`,
          severity: 'error',
          wcag: '1.3.1'
        });
      }
      
      if (!heading.textContent.trim()) {
        this.addIssue('empty-heading', {
          element: heading,
          message: 'Heading element is empty',
          severity: 'error',
          wcag: '1.3.1'
        });
      }
      
      previousLevel = level;
    });
    
    if (!hasH1 && headings.length > 0) {
      this.addWarning('no-h1', {
        element: element,
        message: 'Page should have an H1 heading',
        severity: 'warning',
        wcag: '1.3.1'
      });
    }
  }

  // Image alt text checking
  checkImageAltText(element) {
    const images = element.querySelectorAll('img');
    
    images.forEach((img) => {
      const alt = img.getAttribute('alt');
      const role = img.getAttribute('role');
      
      if (role === 'presentation' || role === 'none') {
        if (alt && alt.trim()) {
          this.addWarning('decorative-alt', {
            element: img,
            message: 'Decorative image should have empty alt attribute',
            severity: 'warning',
            wcag: '1.1.1'
          });
        }
      } else if (alt === null) {
        this.addIssue('missing-alt', {
          element: img,
          message: 'Image missing alt attribute',
          severity: 'error',
          wcag: '1.1.1'
        });
      } else if (alt.trim() === '') {
        // Empty alt is okay for decorative images, but warn if it might be content
        const hasCaption = img.closest('figure')?.querySelector('figcaption');
        if (!hasCaption) {
          this.addWarning('empty-alt', {
            element: img,
            message: 'Image has empty alt - ensure it is decorative',
            severity: 'warning',
            wcag: '1.1.1'
          });
        }
      }
    });
  }

  // Form labels checking
  checkFormLabels(element) {
    const formControls = element.querySelectorAll('input, select, textarea');
    
    formControls.forEach((control) => {
      const type = control.type;
      
      // Skip hidden inputs
      if (type === 'hidden') return;
      
      const hasLabel = this.hasFormLabel(control);
      
      if (!hasLabel) {
        this.addIssue('missing-form-label', {
          element: control,
          message: 'Form control lacks associated label',
          severity: 'error',
          wcag: '1.3.1'
        });
      }
      
      // Check for required field indicators
      if (control.hasAttribute('required') || control.getAttribute('aria-required') === 'true') {
        const hasRequiredIndicator = this.hasRequiredIndicator(control);
        if (!hasRequiredIndicator) {
          this.addSuggestion('required-indicator', {
            element: control,
            message: 'Required field should have clear visual indicator',
            severity: 'suggestion'
          });
        }
      }
    });
  }

  // Focus management checking
  checkFocusManagement(element) {
    // Check for focus traps in modals
    const modals = element.querySelectorAll('[role="dialog"], [role="alertdialog"], .modal');
    
    modals.forEach((modal) => {
      const focusableElements = this.getFocusableElements(modal);
      
      if (focusableElements.length === 0) {
        this.addWarning('modal-no-focusable', {
          element: modal,
          message: 'Modal should contain focusable elements',
          severity: 'warning',
          wcag: '2.4.3'
        });
      }
    });
    
    // Check for skip links
    const skipLinks = element.querySelectorAll('a[href^="#"]');
    const hasSkipToMain = Array.from(skipLinks).some(link => 
      link.textContent.toLowerCase().includes('skip') && 
      link.textContent.toLowerCase().includes('main')
    );
    
    if (!hasSkipToMain) {
      this.addSuggestion('skip-link', {
        element: element,
        message: 'Consider adding skip to main content link',
        severity: 'suggestion',
        wcag: '2.4.1'
      });
    }
  }

  // Semantic HTML checking
  checkSemanticHTML(element) {
    // Check for generic div/span overuse
    const genericElements = element.querySelectorAll('div, span');
    const interactiveGeneric = Array.from(genericElements).filter(el => 
      el.onclick || el.getAttribute('tabindex') || el.getAttribute('role')
    );
    
    interactiveGeneric.forEach((el) => {
      this.addSuggestion('semantic-html', {
        element: el,
        message: 'Consider using semantic HTML elements instead of generic div/span',
        severity: 'suggestion'
      });
    });
    
    // Check for list structure
    const listItems = element.querySelectorAll('li');
    listItems.forEach((li) => {
      const parent = li.parentElement;
      if (!parent || !['ul', 'ol', 'menu'].includes(parent.tagName.toLowerCase())) {
        this.addIssue('invalid-list-structure', {
          element: li,
          message: 'List item must be child of ul, ol, or menu',
          severity: 'error',
          wcag: '1.3.1'
        });
      }
    });
  }

  // Link accessibility checking
  checkLinkAccessibility(element) {
    const links = element.querySelectorAll('a');
    
    links.forEach((link) => {
      const href = link.getAttribute('href');
      const text = link.textContent.trim();
      
      if (!href) {
        this.addIssue('link-no-href', {
          element: link,
          message: 'Link element missing href attribute',
          severity: 'error',
          wcag: '4.1.2'
        });
      }
      
      if (!text && !link.getAttribute('aria-label') && !link.querySelector('img[alt]')) {
        this.addIssue('link-no-text', {
          element: link,
          message: 'Link has no accessible text',
          severity: 'error',
          wcag: '2.4.4'
        });
      }
      
      // Check for vague link text
      const vagueTexts = ['click here', 'read more', 'here', 'more', 'link'];
      if (vagueTexts.includes(text.toLowerCase())) {
        this.addSuggestion('vague-link-text', {
          element: link,
          message: 'Link text should be descriptive of destination',
          severity: 'suggestion',
          wcag: '2.4.4'
        });
      }
      
      // Check for external links
      if (href && (href.startsWith('http') && !href.includes(window.location.hostname))) {
        const hasExternalIndicator = link.getAttribute('aria-label')?.includes('external') ||
                                   text.includes('external') ||
                                   link.querySelector('[aria-label*="external"]');
        
        if (!hasExternalIndicator) {
          this.addSuggestion('external-link-indicator', {
            element: link,
            message: 'External links should be clearly indicated',
            severity: 'suggestion'
          });
        }
      }
    });
  }

  // Table accessibility checking
  checkTableAccessibility(element) {
    const tables = element.querySelectorAll('table');
    
    tables.forEach((table) => {
      const caption = table.querySelector('caption');
      const headers = table.querySelectorAll('th');
      const hasHeaderRow = table.querySelector('thead tr') || table.querySelector('tr:first-child th');
      
      if (!caption && !table.getAttribute('aria-label') && !table.getAttribute('aria-labelledby')) {
        this.addWarning('table-no-caption', {
          element: table,
          message: 'Data table should have caption or accessible name',
          severity: 'warning',
          wcag: '1.3.1'
        });
      }
      
      if (headers.length === 0) {
        this.addIssue('table-no-headers', {
          element: table,
          message: 'Data table should have header cells',
          severity: 'error',
          wcag: '1.3.1'
        });
      }
      
      // Check for proper header associations
      const cells = table.querySelectorAll('td');
      cells.forEach((cell) => {
        if (!cell.getAttribute('headers') && !hasHeaderRow) {
          this.addWarning('table-header-association', {
            element: cell,
            message: 'Complex tables should use headers attribute',
            severity: 'warning',
            wcag: '1.3.1'
          });
        }
      });
    });
  }

  // Motion preferences checking
  checkMotionPreferences() {
    const hasReducedMotionCSS = Array.from(document.styleSheets).some(sheet => {
      try {
        return Array.from(sheet.cssRules).some(rule => 
          rule.media && rule.media.mediaText.includes('prefers-reduced-motion')
        );
      } catch (e) {
        return false;
      }
    });
    
    if (!hasReducedMotionCSS) {
      this.addSuggestion('reduced-motion', {
        element: document.body,
        message: 'Consider implementing prefers-reduced-motion media query',
        severity: 'suggestion',
        wcag: '2.3.3'
      });
    }
  }

  // Text scaling checking
  checkTextScaling() {
    const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
    const baseFontSize = 16; // Standard browser default
    
    if (rootFontSize < baseFontSize * 0.8) {
      this.addWarning('small-text', {
        element: document.documentElement,
        message: 'Root font size may be too small for accessibility',
        severity: 'warning',
        wcag: '1.4.4'
      });
    }
  }

  // Landmark checking
  checkLandmarks(element) {
    const landmarks = element.querySelectorAll('main, nav, header, footer, aside, section, [role="main"], [role="navigation"], [role="banner"], [role="contentinfo"], [role="complementary"]');
    
    const hasMain = element.querySelector('main, [role="main"]');
    if (!hasMain) {
      this.addSuggestion('missing-main', {
        element: element,
        message: 'Page should have a main landmark',
        severity: 'suggestion',
        wcag: '1.3.6'
      });
    }
    
    // Check for duplicate landmarks without labels
    const landmarkTypes = {};
    landmarks.forEach((landmark) => {
      const type = landmark.tagName.toLowerCase() === 'section' ? 
                   landmark.getAttribute('role') || 'section' : 
                   landmark.tagName.toLowerCase();
      
      if (!landmarkTypes[type]) {
        landmarkTypes[type] = [];
      }
      landmarkTypes[type].push(landmark);
    });
    
    Object.entries(landmarkTypes).forEach(([type, elements]) => {
      if (elements.length > 1) {
        elements.forEach((element) => {
          if (!this.hasAccessibleName(element)) {
            this.addWarning('duplicate-landmark', {
              element: element,
              message: `Multiple ${type} landmarks should have unique labels`,
              severity: 'warning',
              wcag: '1.3.6'
            });
          }
        });
      }
    });
  }

  // Helper methods
  hasTextContent(element) {
    return element.textContent && element.textContent.trim().length > 0;
  }

  calculateContrast(color1, color2) {
    // Simplified contrast calculation - in real implementation, use proper color parsing
    // This is a placeholder that returns a reasonable value
    return 4.5; // Placeholder
  }

  isFocusable(element) {
    const tabindex = element.getAttribute('tabindex');
    if (tabindex === '-1') return false;
    if (tabindex && parseInt(tabindex) >= 0) return true;
    
    const focusableElements = ['a', 'button', 'input', 'select', 'textarea'];
    return focusableElements.includes(element.tagName.toLowerCase()) && !element.disabled;
  }

  hasFocusIndicator(element) {
    const styles = getComputedStyle(element, ':focus');
    return styles.outline !== 'none' || styles.boxShadow !== 'none';
  }

  hasAccessibleName(element) {
    return !!(
      element.getAttribute('aria-label') ||
      element.getAttribute('aria-labelledby') ||
      element.getAttribute('title') ||
      element.textContent?.trim() ||
      (element.tagName.toLowerCase() === 'input' && element.getAttribute('placeholder'))
    );
  }

  hasFormLabel(control) {
    const id = control.getAttribute('id');
    if (id && document.querySelector(`label[for="${id}"]`)) return true;
    if (control.closest('label')) return true;
    if (control.getAttribute('aria-label')) return true;
    if (control.getAttribute('aria-labelledby')) return true;
    return false;
  }

  hasRequiredIndicator(control) {
    const label = document.querySelector(`label[for="${control.id}"]`) || control.closest('label');
    return !!(
      label?.textContent.includes('*') ||
      label?.textContent.toLowerCase().includes('required') ||
      control.getAttribute('aria-label')?.toLowerCase().includes('required')
    );
  }

  getFocusableElements(container) {
    return container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
  }

  getHeadingLevel(heading) {
    if (heading.tagName.match(/^H[1-6]$/)) {
      return parseInt(heading.tagName.charAt(1));
    }
    const ariaLevel = heading.getAttribute('aria-level');
    return ariaLevel ? parseInt(ariaLevel) : 1;
  }

  isValidAriaAttribute(name, value, element) {
    // Simplified validation - in real implementation, use comprehensive ARIA spec
    const validAttributes = [
      'aria-label', 'aria-labelledby', 'aria-describedby', 'aria-expanded',
      'aria-hidden', 'aria-live', 'aria-atomic', 'aria-relevant', 'aria-busy'
    ];
    return validAttributes.includes(name);
  }

  // Issue management
  addIssue(type, details) {
    this.issues.push({ type, ...details, timestamp: Date.now() });
  }

  addWarning(type, details) {
    this.warnings.push({ type, ...details, timestamp: Date.now() });
  }

  addSuggestion(type, details) {
    this.suggestions.push({ type, ...details, timestamp: Date.now() });
  }

  // Generate comprehensive report
  generateReport() {
    const totalIssues = this.issues.length + this.warnings.length;
    const score = Math.max(0, 100 - (this.issues.length * 10) - (this.warnings.length * 5));
    
    return {
      timestamp: Date.now(),
      score,
      summary: {
        issues: this.issues.length,
        warnings: this.warnings.length,
        suggestions: this.suggestions.length,
        total: totalIssues
      },
      details: {
        issues: this.issues,
        warnings: this.warnings,
        suggestions: this.suggestions
      },
      recommendations: this.generateRecommendations()
    };
  }

  generateRecommendations() {
    const recommendations = [];
    
    if (this.issues.length > 0) {
      recommendations.push('Address critical accessibility issues first - these prevent users from accessing content.');
    }
    
    if (this.warnings.length > 5) {
      recommendations.push('Review and fix accessibility warnings to improve user experience.');
    }
    
    if (this.suggestions.length > 0) {
      recommendations.push('Consider implementing suggestions for enhanced accessibility.');
    }
    
    return recommendations;
  }
}

// Create singleton instance
const accessibilityAuditor = new AccessibilityAuditor();

// React hook for accessibility auditing
export const useAccessibilityAudit = () => {
  const audit = (element) => accessibilityAuditor.audit(element);
  
  return { audit };
};

// Utility function for quick audits
export const quickAccessibilityCheck = (element = document.body) => {
  return accessibilityAuditor.audit(element);
};

export default accessibilityAuditor;
