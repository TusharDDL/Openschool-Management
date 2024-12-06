import { toast } from 'react-toastify';

export interface APIError {
  detail: string;
  type: string;
}

export class APIClient {
  private baseUrl: string;
  private defaultHeaders: HeadersInit;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || '') {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private getHeaders(): HeadersInit {
    const token = localStorage.getItem('token');
    return {
      ...this.defaultHeaders,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  }

  private handleError(error: any): never {
    let message = 'An unexpected error occurred';
    
    if (error instanceof Response) {
      message = `HTTP error! status: ${error.status}`;
    } else if (error instanceof Error) {
      message = error.message;
    }

    toast.error(message);
    throw error;
  }

  async get<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        const error: APIError = await response.json();
        throw new Error(error.detail || 'Request failed');
      }

      return response.json();
    } catch (error) {
      return this.handleError(error);
    }
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: data ? JSON.stringify(data) : undefined,
      });

      if (!response.ok) {
        const error: APIError = await response.json();
        throw new Error(error.detail || 'Request failed');
      }

      return response.json();
    } catch (error) {
      return this.handleError(error);
    }
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error: APIError = await response.json();
        throw new Error(error.detail || 'Request failed');
      }

      return response.json();
    } catch (error) {
      return this.handleError(error);
    }
  }

  async delete(endpoint: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'DELETE',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        const error: APIError = await response.json();
        throw new Error(error.detail || 'Request failed');
      }
    } catch (error) {
      return this.handleError(error);
    }
  }

  async upload(endpoint: string, file: File): Promise<any> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          Authorization: this.getHeaders().Authorization,
        },
        body: formData,
      });

      if (!response.ok) {
        const error: APIError = await response.json();
        throw new Error(error.detail || 'Upload failed');
      }

      return response.json();
    } catch (error) {
      return this.handleError(error);
    }
  }
}