import axios, { AxiosResponse } from 'axios';

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

// Type definitions
interface CampaignMetricsParams {
  account_id: string;
  start_date?: string;
  end_date?: string;
}

interface KeywordMetricsParams {
  campaign_id: string;
  start_date?: string;
  end_date?: string;
}

interface DashboardParams {
  account_id: string;
  start_date?: string;
  end_date?: string;
}

interface BiddingData {
  strategy_name: string;
  keyword_ids: string[];
  target_acos?: number;
  target_cvr?: number;
}

interface BiddingLogsParams {
  account_id?: string;
  limit?: number;
}

interface RecommendationsParams {
  asin: string;
  limit?: number;
}

export const metricsAPI = {
  getCampaignMetrics: (params: CampaignMetricsParams): Promise<AxiosResponse<any>> => 
    apiClient.get('/metrics/campaigns', { params }),
  
  getKeywordMetrics: (params: KeywordMetricsParams): Promise<AxiosResponse<any>> => 
    apiClient.get('/metrics/keywords', { params }),
  
  getDashboardOverview: (params: DashboardParams): Promise<AxiosResponse<any>> => 
    apiClient.get('/metrics/dashboard/overview', { params }),
};

export const biddingAPI = {
  executeBidding: (data: BiddingData): Promise<AxiosResponse<any>> => 
    apiClient.post('/bidding/execute', data),
  
  getBiddingLogs: (params: BiddingLogsParams): Promise<AxiosResponse<any>> => 
    apiClient.get('/bidding/logs', { params }),
};

export const keywordsAPI = {
  getRecommendations: (params: RecommendationsParams): Promise<AxiosResponse<any>> => 
    apiClient.get('/keywords/recommend', { params }),
  
  addNegativeKeywords: (keywordIds: string[]): Promise<AxiosResponse<any>> => 
    apiClient.post('/keywords/negative', keywordIds),
};

export default apiClient;
