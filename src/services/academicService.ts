import { api } from './api';

export interface AcademicYear {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Class {
  id: number;
  name: string;
  description?: string;
  academic_year_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Section {
  id: number;
  name: string;
  class_id: number;
  capacity: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentSection {
  id: number;
  student_id: number;
  section_id: number;
  roll_number?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TeacherSection {
  id: number;
  teacher_id: number;
  section_id: number;
  is_class_teacher: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClassStudent {
  student_id: number;
  roll_number?: string;
  section_name: string;
  is_active: boolean;
}

export interface TeacherClass {
  class_id: number;
  class_name: string;
  section_id: number;
  section_name: string;
  is_class_teacher: boolean;
}

class AcademicService {
  // Academic Year
  async createAcademicYear(data: Omit<AcademicYear, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<AcademicYear>('/academic/years', data);
    return response.data;
  }

  async getAcademicYears(params?: { is_active?: boolean; skip?: number; limit?: number }) {
    const response = await api.get<AcademicYear[]>('/academic/years', { params });
    return response.data;
  }

  async getAcademicYear(id: number) {
    const response = await api.get<AcademicYear>(`/academic/years/${id}`);
    return response.data;
  }

  async updateAcademicYear(id: number, data: Partial<AcademicYear>) {
    const response = await api.put<AcademicYear>(`/academic/years/${id}`, data);
    return response.data;
  }

  // Class
  async createClass(data: Omit<Class, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<Class>('/academic/classes', data);
    return response.data;
  }

  async getClasses(params?: {
    academic_year_id?: number;
    is_active?: boolean;
    skip?: number;
    limit?: number;
  }) {
    const response = await api.get<Class[]>('/academic/classes', { params });
    return response.data;
  }

  async getClass(id: number) {
    const response = await api.get<Class>(`/academic/classes/${id}`);
    return response.data;
  }

  async updateClass(id: number, data: Partial<Class>) {
    const response = await api.put<Class>(`/academic/classes/${id}`, data);
    return response.data;
  }

  // Section
  async createSection(data: Omit<Section, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<Section>('/academic/sections', data);
    return response.data;
  }

  async getSections(params?: {
    class_id?: number;
    is_active?: boolean;
    skip?: number;
    limit?: number;
  }) {
    const response = await api.get<Section[]>('/academic/sections', { params });
    return response.data;
  }

  async getSection(id: number) {
    const response = await api.get<Section>(`/academic/sections/${id}`);
    return response.data;
  }

  async updateSection(id: number, data: Partial<Section>) {
    const response = await api.put<Section>(`/academic/sections/${id}`, data);
    return response.data;
  }

  // Student Section Assignment
  async assignStudentToSection(data: Omit<StudentSection, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<StudentSection>('/academic/student-sections', data);
    return response.data;
  }

  // Teacher Section Assignment
  async assignTeacherToSection(data: Omit<TeacherSection, 'id' | 'created_at' | 'updated_at'>) {
    const response = await api.post<TeacherSection>('/academic/teacher-sections', data);
    return response.data;
  }

  // Utility
  async getClassStudents(classId: number, params?: { is_active?: boolean }) {
    const response = await api.get<ClassStudent[]>(`/academic/classes/${classId}/students`, {
      params,
    });
    return response.data;
  }

  async getTeacherClasses(teacherId: number, params?: { academic_year_id?: number }) {
    const response = await api.get<TeacherClass[]>(`/academic/teachers/${teacherId}/classes`, {
      params,
    });
    return response.data;
  }
}

export const academicService = new AcademicService();
