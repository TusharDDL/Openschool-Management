import { api } from './api';

export interface StudentProfile {
  id: number;
  admission_number: string;
  admission_date: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'male' | 'female' | 'other';
  blood_group?: string;
  address: string;
  phone?: string;
  emergency_contact: string;
  medical_conditions?: string;
  previous_school?: string;
  is_active: boolean;
  guardians: Guardian[];
  documents?: StudentDocument[];
  created_at: string;
  updated_at: string;
}

export interface Guardian {
  id: number;
  student_id: number;
  relationship: string;
  first_name: string;
  last_name: string;
  occupation?: string;
  phone: string;
  email?: string;
  address?: string;
  is_emergency_contact: boolean;
  is_authorized_pickup: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentDocument {
  id: number;
  student_id: number;
  document_type: string;
  document_url: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  is_verified: boolean;
  verified_by?: number;
  verification_date?: string;
  created_at: string;
  updated_at: string;
}

export interface StudentNote {
  id: number;
  student_id: number;
  note_type: string;
  title: string;
  content: string;
  is_confidential: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface StudentAttendanceSummary {
  total_days: number;
  present_days: number;
  absent_days: number;
  late_days: number;
  excused_days: number;
  attendance_percentage: number;
}

export interface StudentBasicInfo {
  id: number;
  admission_number: string;
  first_name: string;
  last_name: string;
  section_name?: string;
  roll_number?: string;
  is_active: boolean;
}

export interface StudentDetailedInfo extends StudentProfile {
  attendance_summary?: StudentAttendanceSummary;
  current_section?: string;
  current_class?: string;
  academic_year?: string;
}

class StudentService {
  // Student Profile
  async createStudent(data: Omit<StudentProfile, 'id' | 'created_at' | 'updated_at' | 'documents'>) {
    const response = await api.post<StudentProfile>('/students', data);
    return response.data;
  }

  async getStudents(params?: {
    search?: string;
    class_id?: number;
    section_id?: number;
    is_active?: boolean;
    skip?: number;
    limit?: number;
  }) {
    const response = await api.get<StudentBasicInfo[]>('/students', { params });
    return response.data;
  }

  async getStudent(id: number) {
    const response = await api.get<StudentDetailedInfo>(`/students/${id}`);
    return response.data;
  }

  async updateStudent(id: number, data: Partial<StudentProfile>) {
    const response = await api.put<StudentProfile>(`/students/${id}`, data);
    return response.data;
  }

  // Guardian Management
  async addGuardian(studentId: number, data: Omit<Guardian, 'id' | 'student_id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<Guardian>(`/students/${studentId}/guardians`, data);
    return response.data;
  }

  async updateGuardian(guardianId: number, data: Partial<Guardian>) {
    const response = await api.put<Guardian>(`/students/guardians/${guardianId}`, data);
    return response.data;
  }

  // Document Management
  async uploadDocument(studentId: number, documentType: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    const response = await api.post<StudentDocument>(
      `/students/${studentId}/documents`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  async verifyDocument(documentId: number) {
    const response = await api.post<StudentDocument>(`/students/documents/${documentId}/verify`);
    return response.data;
  }

  // Notes Management
  async addNote(studentId: number, data: Omit<StudentNote, 'id' | 'student_id' | 'created_by' | 'created_at' | 'updated_at'>) {
    const response = await api.post<StudentNote>(`/students/${studentId}/notes`, data);
    return response.data;
  }

  async getStudentNotes(studentId: number, noteType?: string) {
    const response = await api.get<StudentNote[]>(`/students/${studentId}/notes`, {
      params: { note_type: noteType },
    });
    return response.data;
  }

  // Attendance
  async getAttendanceSummary(studentId: number, params?: {
    start_date?: string;
    end_date?: string;
  }) {
    const response = await api.get<StudentAttendanceSummary>(
      `/students/${studentId}/attendance`,
      { params }
    );
    return response.data;
  }
}

export const studentService = new StudentService();
