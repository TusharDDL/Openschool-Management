import { useState, useEffect, useCallback } from 'react';
import { APIClient } from '@/services/api/client';

interface QueryOptions<T> {
  initialData?: T;
  enabled?: boolean;
  refetchInterval?: number;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface QueryResult<T> {
  data: T | undefined;
  error: Error | null;
  isLoading: boolean;
  isError: boolean;
  refetch: () => Promise<void>;
}

const apiClient = new APIClient();
const cache = new Map<string, any>();

export function useQuery<T>(
  endpoint: string,
  options: QueryOptions<T> = {}
): QueryResult<T> {
  const {
    initialData,
    enabled = true,
    refetchInterval,
    onSuccess,
    onError,
  } = options;

  const [data, setData] = useState<T | undefined>(initialData);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(!initialData && enabled);

  const fetchData = useCallback(async () => {
    if (!enabled) return;

    try {
      setIsLoading(true);
      setError(null);

      // Check cache first
      const cachedData = cache.get(endpoint);
      if (cachedData) {
        setData(cachedData);
        onSuccess?.(cachedData);
        setIsLoading(false);
        return;
      }

      const result = await apiClient.get<T>(endpoint);
      cache.set(endpoint, result);
      setData(result);
      onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('An error occurred');
      setError(error);
      onError?.(error);
    } finally {
      setIsLoading(false);
    }
  }, [endpoint, enabled, onSuccess, onError]);

  useEffect(() => {
    fetchData();

    if (refetchInterval) {
      const intervalId = setInterval(fetchData, refetchInterval);
      return () => clearInterval(intervalId);
    }
  }, [fetchData, refetchInterval]);

  return {
    data,
    error,
    isLoading,
    isError: !!error,
    refetch: fetchData,
  };
}

export function useMutation<T, V>(
  endpoint: string,
  options: {
    onSuccess?: (data: T) => void;
    onError?: (error: Error) => void;
    invalidateQueries?: string[];
  } = {}
) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const mutate = async (variables: V) => {
    try {
      setIsLoading(true);
      setError(null);

      const result = await apiClient.post<T>(endpoint, variables);

      // Invalidate related queries
      if (options.invalidateQueries) {
        options.invalidateQueries.forEach(query => cache.delete(query));
      }

      options.onSuccess?.(result);
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('An error occurred');
      setError(error);
      options.onError?.(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    mutate,
    isLoading,
    error,
    isError: !!error,
  };
}