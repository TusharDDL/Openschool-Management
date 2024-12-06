// File: src/types/index.ts
// Core TypeScript type definitions for the application

// User related types
export interface User {
  id: string;
  email: string;
  role: 'super_admin' | 'school_admin' | 'teacher' | 'student' | 'parent';
  firstName?: string;
  lastName?: string;
  createdAt: string;
  updatedAt: string;
}

// Authentication types
export interface AuthState {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// School related types
export interface School {
  id: string;
  name: string;
  code: string;
  address: string;
  phone: string;
  email: string;
  website?: string;
  status: 'active' | 'inactive';
}

// Student related types
export interface Student {
  id: string;
  userId: string;
  schoolId: string;
  rollNumber: string;
  class: string;
  section: string;
  admissionDate: string;
  status: 'active' | 'inactive' | 'graduated';
}

// Academic types
export interface Course {
  id: string;
  name: string;
  code: string;
  description?: string;
  credits: number;
}

export interface Grade {
  id: string;
  studentId: string;
  courseId: string;
  marks: number;
  grade: string;
  semester: string;
  academicYear: string;
}

// Fee related types
export interface FeeStructure {
  id: string;
  name: string;
  amount: number;
  frequency: 'monthly' | 'quarterly' | 'yearly';
  dueDay: number;
}

export interface Payment {
  id: string;
  studentId: string;
  amount: number;
  status: 'pending' | 'paid' | 'failed';
  transactionId?: string;
  paidAt?: string;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Form types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'select' | 'date' | 'number';
  required?: boolean;
  options?: { label: string; value: string | number }[];
  validation?: {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    message?: string;
  };
}