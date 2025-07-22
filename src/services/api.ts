// API Service for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// Debug log to see what URL is being used
console.log('API_BASE_URL:', API_BASE_URL);
console.log('VITE_API_URL env var:', import.meta.env.VITE_API_URL);


// Auth token management
let authToken: string | null = localStorage.getItem('authToken');

const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('authToken');
      authToken = null;
      window.location.href = '/login';
      return null;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    authToken = data.access_token;
    localStorage.setItem('authToken', authToken!);
    return data;
  },

  logout: () => {
    authToken = null;
    localStorage.removeItem('authToken');
  },

  getCurrentUser: () => {
    return apiRequest('/api/v1/auth/me');
  }
};

// Companies API
export const companiesAPI = {
  getAll: (params?: { search?: string; risk_level?: string; sector?: string }) => {
    const searchParams = new URLSearchParams();
    if (params?.search) searchParams.append('search', params.search);
    if (params?.risk_level) searchParams.append('risk_level', params.risk_level);
    if (params?.sector) searchParams.append('sector', params.sector);
    
    const queryString = searchParams.toString();
    return apiRequest(`/api/v1/companies${queryString ? `?${queryString}` : ''}`);
  },

  getById: (id: string) => {
    return apiRequest(`/api/v1/companies/${id}`);
  },

  create: (companyData: any) => {
    return apiRequest('/api/v1/companies', {
      method: 'POST',
      body: JSON.stringify(companyData),
    });
  },

  update: (id: string, companyData: any) => {
    return apiRequest(`/api/v1/companies/${id}`, {
      method: 'PUT',
      body: JSON.stringify(companyData),
    });
  },

  delete: (id: string) => {
    return apiRequest(`/api/v1/companies/${id}`, {
      method: 'DELETE',
    });
  }
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => {
    return apiRequest('/api/v1/dashboard/stats');
  }
};

// Health check
export const healthCheck = async () => {
  try {
    console.log('Health check URL:', `${API_BASE_URL}/health`);
    const response = await fetch(`${API_BASE_URL}/health`);
    console.log('Health check response:', response.status, response.ok);
    return response.ok;
  } catch {
    console.error('Health check failed');
    return false;
  }
};

export { authToken };