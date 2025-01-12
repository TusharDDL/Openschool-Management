import api from './api';

export interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_users: number;
  response_time: number;
  error_rate: number;
  uptime: number;
  last_updated: string;
}

export const monitoringService = {
  async getMetrics(): Promise<SystemMetrics> {
    try {
      console.log('Fetching system metrics...');
      const response = await api.get('/monitoring/metrics');
      console.log('Metrics response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching metrics:', error.response?.data || error.message);
      throw error;
    }
  },

  async getSystemStatus(): Promise<{
    status: 'operational' | 'degraded' | 'down';
    services: Array<{
      name: string;
      status: 'operational' | 'degraded' | 'down';
      latency?: number;
    }>;
  }> {
    try {
      console.log('Fetching system status...');
      const response = await api.get('/monitoring/status');
      console.log('Status response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching system status:', error.response?.data || error.message);
      throw error;
    }
  },

  async getLogs(limit: number = 100): Promise<Array<{
    timestamp: string;
    level: 'info' | 'warning' | 'error';
    message: string;
    service?: string;
  }>> {
    try {
      console.log('Fetching system logs...');
      const response = await api.get('/monitoring/logs', {
        params: { limit }
      });
      console.log('Logs response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching system logs:', error.response?.data || error.message);
      throw error;
    }
  }
};
