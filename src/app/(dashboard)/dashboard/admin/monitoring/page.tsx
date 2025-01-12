'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { monitoringService } from '@/services/monitoring';

interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  active_users: number;
  response_time: number;
  error_rate: number;
}

export default function SystemMonitoringPage() {
  const [metrics, setMetrics] = React.useState<SystemMetrics>({
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
    active_users: 0,
    response_time: 0,
    error_rate: 0
  });
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const [systemStatus, setSystemStatus] = React.useState<{
    status: 'operational' | 'degraded' | 'down';
    services: Array<{
      name: string;
      status: 'operational' | 'degraded' | 'down';
      latency?: number;
    }>;
  } | null>(null);

  const fetchData = React.useCallback(async () => {
    try {
      setLoading(true);
      const [metricsData, statusData] = await Promise.all([
        monitoringService.getMetrics(),
        monitoringService.getSystemStatus()
      ]);
      setMetrics(metricsData);
      setSystemStatus(statusData);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching monitoring data:', err);
      setError(err.message || 'Failed to fetch monitoring data');
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    fetchData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-lg">Loading system metrics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 p-4">
        Error loading metrics: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">System Monitoring</h1>
        <button 
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Refresh Metrics
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* CPU Usage */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">CPU Usage</h3>
          <div className="flex items-end space-x-2">
            <span className="text-2xl font-bold">{metrics.cpu_usage}%</span>
            <div className="flex-1 bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className="bg-blue-500 rounded-full h-2" 
                style={{ width: `${metrics.cpu_usage}%` }}
              />
            </div>
          </div>
        </Card>

        {/* Memory Usage */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Memory Usage</h3>
          <div className="flex items-end space-x-2">
            <span className="text-2xl font-bold">{metrics.memory_usage}%</span>
            <div className="flex-1 bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className="bg-green-500 rounded-full h-2" 
                style={{ width: `${metrics.memory_usage}%` }}
              />
            </div>
          </div>
        </Card>

        {/* Disk Usage */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Disk Usage</h3>
          <div className="flex items-end space-x-2">
            <span className="text-2xl font-bold">{metrics.disk_usage}%</span>
            <div className="flex-1 bg-gray-200 rounded-full h-2 mb-2">
              <div 
                className="bg-yellow-500 rounded-full h-2" 
                style={{ width: `${metrics.disk_usage}%` }}
              />
            </div>
          </div>
        </Card>

        {/* Active Users */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Active Users</h3>
          <p className="text-2xl font-bold">{metrics.active_users}</p>
        </Card>

        {/* Response Time */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Avg Response Time</h3>
          <p className="text-2xl font-bold">{metrics.response_time}ms</p>
        </Card>

        {/* Error Rate */}
        <Card className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-sm font-medium text-gray-500 mb-2">Error Rate</h3>
          <p className="text-2xl font-bold">{metrics.error_rate}%</p>
        </Card>
      </div>

      {/* System Status */}
      <Card className="p-6 bg-white rounded-lg shadow-sm mt-6">
        <h2 className="text-lg font-semibold mb-4">System Status</h2>
        <div className="space-y-4">
          {systemStatus ? (
            <>
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  systemStatus.status === 'operational' ? 'bg-green-500' :
                  systemStatus.status === 'degraded' ? 'bg-yellow-500' :
                  'bg-red-500'
                }`} />
                <span className="capitalize">
                  System {systemStatus.status}
                </span>
              </div>
              {systemStatus.services.map((service, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${
                    service.status === 'operational' ? 'bg-green-500' :
                    service.status === 'degraded' ? 'bg-yellow-500' :
                    'bg-red-500'
                  }`} />
                  <span>{service.name}</span>
                  {service.latency && (
                    <span className="text-sm text-gray-500">
                      ({service.latency}ms)
                    </span>
                  )}
                </div>
              ))}
            </>
          ) : (
            <div>Loading system status...</div>
          )}
        </div>
      </Card>
    </div>
  );
}
