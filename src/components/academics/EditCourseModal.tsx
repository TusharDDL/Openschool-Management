// src/components/academics/EditCourseModal.tsx
'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { BookOpen } from 'lucide-react'
import { Course } from '@/types/academics'

interface EditCourseModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  courseData: Course | null
}

interface CourseFormData {
  name: string
  class: string
  subject: string
  teacher: string
  schedule: string
  maxStudents: string
  description: string
  status: string
  startDate: string
  endDate: string
  syllabus: string
}

const CLASS_OPTIONS = [
  { value: '1', label: 'Class 1' },
  { value: '2', label: 'Class 2' },
  { value: '3', label: 'Class 3' },
  { value: '4', label: 'Class 4' },
  { value: '5', label: 'Class 5' },
  { value: '6', label: 'Class 6' },
  { value: '7', label: 'Class 7' },
  { value: '8', label: 'Class 8' },
  { value: '9', label: 'Class 9' },
  { value: '10', label: 'Class 10' },
  { value: '11', label: 'Class 11' },
  { value: '12', label: 'Class 12' }
]

const SUBJECT_OPTIONS = [
  { value: 'mathematics', label: 'Mathematics' },
  { value: 'english', label: 'English' },
  { value: 'science', label: 'Science' },
  { value: 'social_studies', label: 'Social Studies' },
  { value: 'computer_science', label: 'Computer Science' },
  { value: 'physics', label: 'Physics' },
  { value: 'chemistry', label: 'Chemistry' },
  { value: 'biology', label: 'Biology' }
]

const TEACHER_OPTIONS = [
  { value: '1', label: 'Dr. Sarah Wilson' },
  { value: '2', label: 'Prof. John Smith' },
  { value: '3', label: 'Mr. Robert Brown' },
  { value: '4', label: 'Ms. Emily Chen' },
  { value: '5', label: 'Dr. Michael Lee' }
]

const STATUS_OPTIONS = [
  { value: 'upcoming', label: 'Upcoming' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' }
]

export default function EditCourseModal({ open, onOpenChange, courseData }: EditCourseModalProps) {
  const [formData, setFormData] = React.useState<CourseFormData>({
    name: courseData?.name || '',
    class: courseData?.class || '',
    subject: courseData?.subject || '',
    teacher: courseData?.teacher || '',
    schedule: courseData?.schedule || '',
    maxStudents: courseData?.students.toString() || '',
    description: courseData?.description || '',
    status: courseData?.status || 'active',
    startDate: courseData?.startDate || '',
    endDate: courseData?.endDate || '',
    syllabus: courseData?.syllabus || ''
  })

  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [errors, setErrors] = React.useState<Partial<CourseFormData>>({})

  // Update form data when courseData changes
  React.useEffect(() => {
    if (courseData) {
      setFormData({
        name: courseData.name,
        class: courseData.class,
        subject: courseData.subject,
        teacher: courseData.teacher,
        schedule: courseData.schedule,
        maxStudents: courseData.students.toString(),
        description: courseData.description || '',
        status: courseData.status,
        startDate: courseData.startDate || '',
        endDate: courseData.endDate || '',
        syllabus: courseData.syllabus || ''
      })
    }
  }, [courseData])

  const validateForm = (): boolean => {
    const newErrors: Partial<CourseFormData> = {}

    if (!formData.name) newErrors.name = 'Course name is required'
    if (!formData.class) newErrors.class = 'Class is required'
    if (!formData.subject) newErrors.subject = 'Subject is required'
    if (!formData.teacher) newErrors.teacher = 'Teacher is required'
    if (!formData.schedule) newErrors.schedule = 'Schedule is required'
    if (!formData.maxStudents) newErrors.maxStudents = 'Maximum students is required'
    if (!formData.startDate) newErrors.startDate = 'Start date is required'
    if (!formData.endDate) newErrors.endDate = 'End date is required'

    if (formData.startDate && formData.endDate) {
      if (new Date(formData.startDate) >= new Date(formData.endDate)) {
        newErrors.endDate = 'End date must be after start date'
      }
    }

    if (formData.maxStudents && parseInt(formData.maxStudents) <= 0) {
      newErrors.maxStudents = 'Maximum students must be a positive number'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name as keyof CourseFormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsSubmitting(true)
    try {
      // Here you would typically make an API call to update the course
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
      console.log('Form submitted:', formData)
      onOpenChange(false)
    } catch (error) {
      console.error('Error updating course:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!courseData) return null

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            Edit Course
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Course Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              error={errors.name}
              required
            />

            <Select
              label="Class"
              name="class"
              value={formData.class}
              onChange={handleChange}
              options={CLASS_OPTIONS}
              error={errors.class}
              required
            />

            <Select
              label="Subject"
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              options={SUBJECT_OPTIONS}
              error={errors.subject}
              required
            />

            <Select
              label="Teacher"
              name="teacher"
              value={formData.teacher}
              onChange={handleChange}
              options={TEACHER_OPTIONS}
              error={errors.teacher}
              required
            />

            <Input
              label="Schedule"
              name="schedule"
              value={formData.schedule}
              onChange={handleChange}
              error={errors.schedule}
              required
            />

            <Input
              label="Maximum Students"
              name="maxStudents"
              type="number"
              min="1"
              value={formData.maxStudents}
              onChange={handleChange}
              error={errors.maxStudents}
              required
            />

            <Input
              label="Start Date"
              name="startDate"
              type="date"
              value={formData.startDate}
              onChange={handleChange}
              error={errors.startDate}
              required
            />

            <Input
              label="End Date"
              name="endDate"
              type="date"
              value={formData.endDate}
              onChange={handleChange}
              error={errors.endDate}
              required
            />

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                rows={3}
                value={formData.description}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter course description..."
              />
            </div>

            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleChange}
              options={STATUS_OPTIONS}
              required
            />
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : 'Save Changes'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}