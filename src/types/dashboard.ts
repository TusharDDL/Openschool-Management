// src/types/dashboard.ts
export interface ChartData {
    subject: string
    grade: number
    classAverage: number
  }
  
  export interface AttendanceChartData {
    month: string
    attendance: number
    classAverage: number
  }
  
  export interface CourseStats {
    id: number
    name: string
    attendance: number
    nextClass: string
    currentGrade?: number
    teacher: string
  }
  
  export interface AssignmentStats {
    id: number
    title: string
    courseName: string
    dueDate: string
    status: 'pending' | 'submitted' | 'late' | 'graded'
  }