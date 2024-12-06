import { api } from './api';

export interface FeeStructure {
  id: number;
  name: string;
  description?: string;
  amount: number;
  frequency: 'MONTHLY' | 'QUARTERLY' | 'YEARLY' | 'ONE_TIME';
  class_id?: number;
  academic_year_id: number;
  due_day?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface FeePayment {
  id: number;
  student_id: number;
  fee_structure_id: number;
  amount_paid: number;
  payment_date: string;
  payment_mode: 'CASH' | 'CHEQUE' | 'ONLINE';
  reference_number?: string;
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export interface FeeReport {
  total_collected: number;
  total_pending: number;
  collection_by_class: {
    class_name: string;
    collected: number;
    pending: number;
  }[];
  collection_by_month: {
    month: string;
    amount: number;
  }[];
}

class FeeService {
  // Fee Structure
  async createFeeStructure(data: Omit<FeeStructure, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<FeeStructure>('/fees/structures', data);
    return response.data;
  }

  async getFeeStructures(params?: {
    class_id?: number;
    academic_year_id?: number;
    is_active?: boolean;
  }) {
    const response = await api.get<FeeStructure[]>('/fees/structures', { params });
    return response.data;
  }

  async updateFeeStructure(id: number, data: Partial<FeeStructure>) {
    const response = await api.put<FeeStructure>(`/fees/structures/${id}`, data);
    return response.data;
  }

  // Fee Payments
  async recordPayment(data: Omit<FeePayment, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<FeePayment>('/fees/payments', data);
    return response.data;
  }

  async getStudentPayments(studentId: number, params?: {
    academic_year_id?: number;
    from_date?: string;
    to_date?: string;
  }) {
    const response = await api.get<FeePayment[]>(`/fees/students/${studentId}/payments`, {
      params,
    });
    return response.data;
  }

  async generateReceipt(paymentId: number) {
    const response = await api.get(`/fees/payments/${paymentId}/receipt`, {
      responseType: 'blob',
    });
    return response.data;
  }

  // Reports
  async getFeeReport(params: {
    academic_year_id: number;
    from_date?: string;
    to_date?: string;
    class_id?: number;
  }) {
    const response = await api.get<FeeReport>('/fees/reports', { params });
    return response.data;
  }

  async getStudentDues(studentId: number, params?: { academic_year_id?: number }) {
    const response = await api.get(`/fees/students/${studentId}/dues`, { params });
    return response.data;
  }
}

export const feeService = new FeeService();