import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const sessionToken = localStorage.getItem('session_token');
      
      if (token || sessionToken) {
        const userData = await authService.verifyAuth();
        if (userData.success) {
          setUser(userData.user);
        } else {
          // Clear invalid tokens
          localStorage.removeItem('auth_token');
          localStorage.removeItem('session_token');
        }
      }
    } catch (err) {
      setError('Authentication check failed');
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await authService.login(credentials);
      
      if (result.success) {
        setUser(result.user);
        
        // Store tokens
        if (result.token) {
          localStorage.setItem('auth_token', result.token);
        }
        if (result.session?.session_token) {
          localStorage.setItem('session_token', result.session.session_token);
        }
        
        return { success: true };
      } else {
        setError(result.errors?.[0] || 'Login failed');
        return { success: false, error: result.errors?.[0] || 'Login failed' };
      }
    } catch (err) {
      const errorMessage = 'Login failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await authService.register(userData);
      
      if (result.success) {
        // Auto-login after successful registration
        const loginResult = await login({
          username: userData.username,
          password: userData.password
        });
        
        return loginResult;
      } else {
        setError(result.errors?.[0] || 'Registration failed');
        return { success: false, error: result.errors?.[0] || 'Registration failed' };
      }
    } catch (err) {
      const errorMessage = 'Registration failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      
      const sessionToken = localStorage.getItem('session_token');
      if (sessionToken) {
        await authService.logout(sessionToken);
      }
      
      // Clear local state and storage
      setUser(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('session_token');
      
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local state even if API call fails
      setUser(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('session_token');
      return { success: true };
    } finally {
      setLoading(false);
    }
  };

  const updateUser = (updatedUser) => {
    setUser(prevUser => ({ ...prevUser, ...updatedUser }));
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      setError(null);
      
      const result = await authService.changePassword({
        current_password: currentPassword,
        new_password: newPassword
      });
      
      if (result.success) {
        return { success: true };
      } else {
        setError(result.errors?.[0] || 'Password change failed');
        return { success: false, error: result.errors?.[0] || 'Password change failed' };
      }
    } catch (error) {
      const errorMessage = 'Password change failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const requestPasswordReset = async (email) => {
    try {
      setError(null);
      
      const result = await authService.requestPasswordReset(email);
      
      if (result.success) {
        return { success: true, message: result.message };
      } else {
        setError(result.errors?.[0] || 'Password reset request failed');
        return { success: false, error: result.errors?.[0] || 'Password reset request failed' };
      }
    } catch (error) {
      const errorMessage = 'Password reset request failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      setError(null);
      
      const result = await authService.resetPassword(token, newPassword);
      
      if (result.success) {
        return { success: true };
      } else {
        setError(result.errors?.[0] || 'Password reset failed');
        return { success: false, error: result.errors?.[0] || 'Password reset failed' };
      }
    } catch (error) {
      const errorMessage = 'Password reset failed. Please try again.';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updateUser,
    changePassword,
    requestPasswordReset,
    resetPassword,
    clearError,
    isAuthenticated: !!user,
    hasSubscription: (level) => {
      if (!user) return false;
      const levels = { free: 0, premium: 1, professional: 2 };
      const userLevel = levels[user.subscription_type] || 0;
      const requiredLevel = levels[level] || 1;
      return userLevel >= requiredLevel;
    }
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

