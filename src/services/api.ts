// File: src/services/api.ts
// API service configuration and endpoints

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
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

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token expiration
      localStorage.removeItem('token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  logout: async () => {
    localStorage.removeItem('token');
    return api.post('/auth/logout');
  },
};

// Student API
export const studentAPI = {
  getDashboard: async () => {
    const response = await api.get('/student/dashboard');
    return response.data;
  },
  getAssignments: async () => {
    const response = await api.get('/student/assignments');
    return response.data;
  },
  submitAssignment: async (assignmentId: number, formData: FormData) => {
    const response = await api.post(
      `/student/assignments/${assignmentId}/submit`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },
  getResults: async () => {
    const response = await api.get('/student/results');
    return response.data;
  },
};

// Academic API
export const academicAPI = {
  getTimetable: async (params?: any) => {
    const response = await api.get('/academic/timetable', { params });
    return response.data;
  },
  createAssessment: async (data: any) => {
    const response = await api.post('/academic/assessments', data);
    return response.data;
  },
  getResults: async (studentId: number) => {
    const response = await api.get(`/academic/results/student/${studentId}`);
    return response.data;
  },
  createNote: async (data: any) => {
    const response = await api.post('/academic/notes', data);
    return response.data;
  },
};

// Fee API
export const feeAPI = {
  createFeeStructure: async (data: any) => {
    const response = await api.post('/fees', data);
    return response.data;
  },
  getFeeStructures: async (params?: any) => {
    const response = await api.get('/fees', { params });
    return response.data;
  },
  createDiscount: async (data: any) => {
    const response = await api.post('/fees/discounts', data);
    return response.data;
  },
  recordPayment: async (data: any) => {
    const response = await api.post('/fees/pay', data);
    return response.data;
  },
  generateReport: async (data: any) => {
    const response = await api.post('/fees/report', data, {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Admin API
export const adminAPI = {
  createSchool: async (data: any) => {
    const response = await api.post('/schools', data);
    return response.data;
  },
  getSchools: async () => {
    const response = await api.get('/schools');
    return response.data;
  },
  createTenant: async (data: any) => {
    const response = await api.post('/tenants', data);
    return response.data;
  },
  getTenants: async () => {
    const response = await api.get('/tenants');
    return response.data;
  },
};

// Announcement API
export const announcementAPI = {
  getAnnouncements: async (params?: any) => {
    const response = await api.get('/announcements', { params });
    return response.data;
  },
  createAnnouncement: async (data: any) => {
    const response = await api.post('/announcements', data);
    return response.data;
  },
  updateAnnouncement: async (id: number, data: any) => {
    const response = await api.put(`/announcements/${id}`, data);
    return response.data;
  },
  deleteAnnouncement: async (id: number) => {
    const response = await api.delete(`/announcements/${id}`);
    return response.data;
  },
};

export default api;