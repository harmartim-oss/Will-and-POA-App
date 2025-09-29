// Simple API configuration for deployment
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://ontario-wills-backend.onrender.com/api'
  : 'http://localhost:5000/api';

export default {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
};