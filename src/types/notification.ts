// src/types/notification.ts
export type NotificationType = 
  | 'assignment'
  | 'grade'
  | 'attendance'
  | 'announcement'
  | 'reminder'
  | 'message'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  timestamp: string
  read: boolean
  link?: string
  course?: {
    id: number
    name: string
  }
  actionRequired?: boolean
  priority?: 'low' | 'medium' | 'high'
}