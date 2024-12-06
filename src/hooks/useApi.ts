import { useState, useCallback } from 'react';
import { AxiosError } from 'axios';

interface UseApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  execute: (...args: any[]) => Promise<T | null>;
}

export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>,
  options = { immediate: false }
): UseApiResponse<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: any[]) => {
      try {
        setLoading(true);
        setError(null);
        const response = await apiFunction(...args);
        setData(response);
        return response;
      } catch (err) {
        const error = err as AxiosError;
        const errorMessage =
          error.response?.data?.detail || error.message || 'An error occurred';
        setError(errorMessage);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  // Execute immediately if option is set
  if (options.immediate) {
    execute();
  }

  return { data, loading, error, execute };
}