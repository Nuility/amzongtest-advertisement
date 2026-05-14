import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const metricsAPI = {
  getCampaignMetrics: (params) => 
    apiClient.get('/metrics/campaigns', { params }),
  
  getKeywordMetrics: (params) => 
    apiClient.get('/metrics/keywords', { params }),
  
  getDashboardOverview: (params) => 
    apiClient.get('/metrics/dashboard/overview', { params }),
};

export const biddingAPI = {
  executeBidding: (data) => 
    apiClient.post('/bidding/execute', data),
  
  getBiddingLogs: (params) => 
    apiClient.get('/bidding/logs', { params }),
};

export const keywordsAPI = {
  getRecommendations: (params) => 
    apiClient.get('/keywords/recommend', { params }),
  
  addNegativeKeywords: (keywordIds) => 
    apiClient.post('/keywords/negative', keywordIds),
};

export default apiClient;
