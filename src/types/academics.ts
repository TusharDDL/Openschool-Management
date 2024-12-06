// src/types/academics.ts
// src/types/academics.ts
export interface Course {
    id: number
    name: string
    class: string
    subject: string
    teacher: string
    students: number
    schedule: string
    status: 'active' | 'upcoming' | 'completed'
    description?: string
    startDate?: string
    endDate?: string
    syllabus?: string
  }
  
  export interface Teacher {
    id: number
    name: string
    subject: string
    email: string
    phone: string
  }
  
  export interface Subject {
    id: number
    name: string
    code: string
    department: string
  }
  // src/types/academics.ts
export interface Assignment {
    id: number
    title: string
    courseId: number
    courseName: string
    dueDate: string
    totalMarks: number
    status: 'upcoming' | 'ongoing' | 'completed'
    description: string
    attachments?: string[]
    submissionCount?: number
    class: string
    subject: string
  }