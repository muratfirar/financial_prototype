// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://financial-risk-api.onrender.com';

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: `${API_BASE_URL}/api/v1/auth/login`,
    REGISTER: `${API_BASE_URL}/api/v1/auth/register`,
  },
  COMPANIES: {
    LIST: `${API_BASE_URL}/api/v1/companies`,
    CREATE: `${API_BASE_URL}/api/v1/companies`,
    DETAIL: (id: string) => `${API_BASE_URL}/api/v1/companies/${id}`,
  },
  DASHBOARD: {
    STATS: `${API_BASE_URL}/api/v1/dashboard/stats`,
  },
};

export default API_BASE_URL;