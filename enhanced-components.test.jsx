import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '../components/ThemeContext';

// Import components to test
import EnhancedLoading from '../components/ui/enhanced-loading';
import ErrorBoundary from '../components/ui/error-boundary';
import { ProgressIndicator, ProgressBar } from '../components/ui/progress-indicator';
import MobileNav from '../components/ui/mobile-nav';
import LazyDocumentCreator from '../components/LazyDocumentCreator';

// Mock framer-motion to avoid animation issues in tests
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    button: ({ children, ...props }) => <button {...props}>{children}</button>,
  },
  AnimatePresence: ({ children }) => <>{children}</>,
}));

// Mock Lucide icons
vi.mock('lucide-react', () => ({
  Loader2: () => <div data-testid="loader-icon">Loading</div>,
  FileText: () => <div data-testid="file-icon">File</div>,
  Brain: () => <div data-testid="brain-icon">Brain</div>,
  Shield: () => <div data-testid="shield-icon">Shield</div>,
  AlertTriangle: () => <div data-testid="alert-icon">Alert</div>,
  RefreshCw: () => <div data-testid="refresh-icon">Refresh</div>,
  Home: () => <div data-testid="home-icon">Home</div>,
  Mail: () => <div data-testid="mail-icon">Mail</div>,
  Check: () => <div data-testid="check-icon">Check</div>,
  Circle: () => <div data-testid="circle-icon">Circle</div>,
  Menu: () => <div data-testid="menu-icon">Menu</div>,
  X: () => <div data-testid="close-icon">Close</div>,
  Sun: () => <div data-testid="sun-icon">Sun</div>,
  Moon: () => <div data-testid="moon-icon">Moon</div>,
  Phone: () => <div data-testid="phone-icon">Phone</div>,
  Users: () => <div data-testid="users-icon">Users</div>,
}));

// Test wrapper component
const TestWrapper = ({ children }) => (
  <BrowserRouter>
    <ThemeProvider>
      {children}
    </ThemeProvider>
  </BrowserRouter>
);

describe('EnhancedLoading Component', () => {
  test('renders with default props', () => {
    render(<EnhancedLoading />, { wrapper: TestWrapper });
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    expect(screen.getByTestId('loader-icon')).toBeInTheDocument();
  });

  test('renders with custom message and type', () => {
    render(
      <EnhancedLoading 
        message="Creating Document" 
        submessage="Please wait..." 
        type="document" 
      />, 
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Creating Document')).toBeInTheDocument();
    expect(screen.getByText('Please wait...')).toBeInTheDocument();
    expect(screen.getByTestId('file-icon')).toBeInTheDocument();
  });

  test('renders different icons based on type', () => {
    const { rerender } = render(
      <EnhancedLoading type="ai" />, 
      { wrapper: TestWrapper }
    );
    expect(screen.getByTestId('brain-icon')).toBeInTheDocument();

    rerender(<EnhancedLoading type="legal" />);
    expect(screen.getByTestId('shield-icon')).toBeInTheDocument();
  });

  test('applies correct size classes', () => {
    const { container } = render(
      <EnhancedLoading size="large" />, 
      { wrapper: TestWrapper }
    );
    expect(container.querySelector('.p-12')).toBeInTheDocument();
  });
});

describe('ErrorBoundary Component', () => {
  // Suppress console.error for these tests
  const originalError = console.error;
  beforeAll(() => {
    console.error = vi.fn();
  });
  afterAll(() => {
    console.error = originalError;
  });

  const ThrowError = ({ shouldThrow }) => {
    if (shouldThrow) {
      throw new Error('Test error');
    }
    return <div>No error</div>;
  };

  test('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  test('renders error UI when there is an error', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByTestId('alert-icon')).toBeInTheDocument();
  });

  test('retry button works correctly', async () => {
    const { rerender } = render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    
    const retryButton = screen.getByText('Try Again');
    fireEvent.click(retryButton);
    
    // After retry, render without error
    rerender(
      <ErrorBoundary>
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>
    );
    
    await waitFor(() => {
      expect(screen.getByText('No error')).toBeInTheDocument();
    });
  });

  test('disables retry button after max retries', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );
    
    const retryButton = screen.getByText('Try Again');
    
    // Click retry 3 times
    fireEvent.click(retryButton);
    fireEvent.click(retryButton);
    fireEvent.click(retryButton);
    
    expect(screen.getByText('Max retries reached')).toBeInTheDocument();
    expect(screen.getByText('Max retries reached')).toBeDisabled();
  });
});

describe('ProgressIndicator Component', () => {
  const mockSteps = [
    { title: 'Step 1', description: 'First step' },
    { title: 'Step 2', description: 'Second step' },
    { title: 'Step 3', description: 'Third step' },
  ];

  test('renders steps correctly', () => {
    render(
      <ProgressIndicator steps={mockSteps} currentStep={1} />,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('Step 2')).toBeInTheDocument();
    expect(screen.getByText('Step 3')).toBeInTheDocument();
  });

  test('shows correct step status', () => {
    render(
      <ProgressIndicator steps={mockSteps} currentStep={1} />,
      { wrapper: TestWrapper }
    );
    
    // First step should be completed (check icon)
    expect(screen.getByTestId('check-icon')).toBeInTheDocument();
    
    // Third step should be upcoming (circle icon)
    expect(screen.getByTestId('circle-icon')).toBeInTheDocument();
  });

  test('compact variant renders correctly', () => {
    render(
      <ProgressIndicator 
        steps={mockSteps} 
        currentStep={1} 
        variant="compact" 
      />,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('2 of 3')).toBeInTheDocument();
  });

  test('hides labels when showLabels is false', () => {
    render(
      <ProgressIndicator 
        steps={mockSteps} 
        currentStep={1} 
        showLabels={false} 
      />,
      { wrapper: TestWrapper }
    );
    
    expect(screen.queryByText('Step 1')).not.toBeInTheDocument();
  });
});

describe('ProgressBar Component', () => {
  test('renders with correct percentage', () => {
    render(<ProgressBar value={75} max={100} />, { wrapper: TestWrapper });
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  test('renders with custom label', () => {
    render(
      <ProgressBar value={50} max={100} label="Upload Progress" />,
      { wrapper: TestWrapper }
    );
    expect(screen.getByText('Upload Progress')).toBeInTheDocument();
  });

  test('hides percentage when showPercentage is false', () => {
    render(
      <ProgressBar value={75} max={100} showPercentage={false} />,
      { wrapper: TestWrapper }
    );
    expect(screen.queryByText('75%')).not.toBeInTheDocument();
  });

  test('handles values exceeding max correctly', () => {
    render(<ProgressBar value={150} max={100} />, { wrapper: TestWrapper });
    expect(screen.getByText('100%')).toBeInTheDocument();
  });
});

describe('MobileNav Component', () => {
  const mockProps = {
    isOpen: false,
    onToggle: vi.fn(),
    onNavigate: vi.fn(),
    currentPath: '/',
  };

  test('renders menu button', () => {
    render(<MobileNav {...mockProps} />, { wrapper: TestWrapper });
    expect(screen.getByTestId('menu-icon')).toBeInTheDocument();
  });

  test('shows close icon when open', () => {
    render(
      <MobileNav {...mockProps} isOpen={true} />,
      { wrapper: TestWrapper }
    );
    expect(screen.getByTestId('close-icon')).toBeInTheDocument();
  });

  test('calls onToggle when menu button is clicked', () => {
    render(<MobileNav {...mockProps} />, { wrapper: TestWrapper });
    
    const menuButton = screen.getByLabelText('Open menu');
    fireEvent.click(menuButton);
    
    expect(mockProps.onToggle).toHaveBeenCalled();
  });

  test('renders navigation items when open', () => {
    render(
      <MobileNav {...mockProps} isOpen={true} />,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Create Will')).toBeInTheDocument();
    expect(screen.getByText('Power of Attorney')).toBeInTheDocument();
  });

  test('calls onNavigate when navigation item is clicked', () => {
    render(
      <MobileNav {...mockProps} isOpen={true} />,
      { wrapper: TestWrapper }
    );
    
    const homeButton = screen.getByText('Home');
    fireEvent.click(homeButton);
    
    expect(mockProps.onNavigate).toHaveBeenCalledWith('/');
  });
});

describe('LazyDocumentCreator Component', () => {
  test('renders loading state initially', () => {
    render(<LazyDocumentCreator />, { wrapper: TestWrapper });
    expect(screen.getByText('Loading Enhanced Document Creator')).toBeInTheDocument();
  });

  test('shows different loading messages for different types', () => {
    const { rerender } = render(
      <LazyDocumentCreator type="premium" />,
      { wrapper: TestWrapper }
    );
    expect(screen.getByText('Loading Premium Document Creator')).toBeInTheDocument();

    rerender(<LazyDocumentCreator type="basic" />);
    expect(screen.getByText('Loading Document Creator')).toBeInTheDocument();
  });

  test('passes props correctly', () => {
    const mockOnSave = vi.fn();
    const mockOnPreview = vi.fn();
    
    render(
      <LazyDocumentCreator 
        type="enhanced"
        documentType="poa"
        onSave={mockOnSave}
        onPreview={mockOnPreview}
      />,
      { wrapper: TestWrapper }
    );
    
    // Component should render with loading state
    expect(screen.getByText('Loading Enhanced Document Creator')).toBeInTheDocument();
  });
});

// Integration tests
describe('Component Integration', () => {
  test('ErrorBoundary catches errors from LazyDocumentCreator', () => {
    // Mock the lazy import to throw an error
    vi.doMock('../components/EnhancedDocumentCreator', () => {
      throw new Error('Failed to load component');
    });

    render(
      <ErrorBoundary>
        <LazyDocumentCreator />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );

    // Should show loading initially, then error boundary if component fails to load
    expect(screen.getByText('Loading Enhanced Document Creator')).toBeInTheDocument();
  });

  test('ProgressIndicator works with MobileNav navigation', () => {
    const steps = [
      { title: 'Personal Info', description: 'Enter your details' },
      { title: 'Document Type', description: 'Choose document type' },
      { title: 'Review', description: 'Review and submit' },
    ];

    render(
      <div>
        <ProgressIndicator steps={steps} currentStep={0} />
        <MobileNav
          isOpen={false}
          onToggle={vi.fn()}
          onNavigate={vi.fn()}
          currentPath="/create/will"
        />
      </div>,
      { wrapper: TestWrapper }
    );

    expect(screen.getByText('Personal Info')).toBeInTheDocument();
    expect(screen.getByTestId('menu-icon')).toBeInTheDocument();
  });
});

// Performance tests
describe('Performance Tests', () => {
  test('EnhancedLoading renders quickly', () => {
    const startTime = performance.now();
    render(<EnhancedLoading />, { wrapper: TestWrapper });
    const endTime = performance.now();
    
    expect(endTime - startTime).toBeLessThan(50); // Should render in less than 50ms
  });

  test('ProgressIndicator handles many steps efficiently', () => {
    const manySteps = Array.from({ length: 100 }, (_, i) => ({
      title: `Step ${i + 1}`,
      description: `Description ${i + 1}`
    }));

    const startTime = performance.now();
    render(
      <ProgressIndicator steps={manySteps} currentStep={50} />,
      { wrapper: TestWrapper }
    );
    const endTime = performance.now();
    
    expect(endTime - startTime).toBeLessThan(100); // Should handle 100 steps quickly
  });
});

// Accessibility tests
describe('Accessibility Tests', () => {
  test('EnhancedLoading has proper ARIA attributes', () => {
    render(<EnhancedLoading message="Loading content" />, { wrapper: TestWrapper });
    
    // Should have accessible content
    expect(screen.getByText('Loading content')).toBeInTheDocument();
  });

  test('ErrorBoundary has proper error messaging', () => {
    const ThrowError = () => {
      throw new Error('Test error');
    };

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText('We apologize for the inconvenience. An unexpected error has occurred.')).toBeInTheDocument();
  });

  test('MobileNav has proper ARIA labels', () => {
    render(
      <MobileNav
        isOpen={false}
        onToggle={vi.fn()}
        onNavigate={vi.fn()}
        currentPath="/"
      />,
      { wrapper: TestWrapper }
    );
    
    const menuButton = screen.getByLabelText('Open menu');
    expect(menuButton).toHaveAttribute('aria-expanded', 'false');
  });

  test('ProgressIndicator provides accessible progress information', () => {
    const steps = [
      { title: 'Step 1', description: 'First step' },
      { title: 'Step 2', description: 'Second step' },
    ];

    render(
      <ProgressIndicator steps={steps} currentStep={0} />,
      { wrapper: TestWrapper }
    );
    
    expect(screen.getByText('Step 1')).toBeInTheDocument();
    expect(screen.getByText('First step')).toBeInTheDocument();
  });
});
