// src/components/academics/GradeSubmissionModal.tsx
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
import { CheckCircle, Download } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface GradeSubmissionModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  submission: {
    id: number
    studentName: string
    studentId: string
    submittedAt: string
    status: 'submitted' | 'late' | 'graded'
    grade?: number
    feedback?: string
    attachments: string[]
  } | null
  totalMarks: number
}

interface GradeFormData {
  grade: string
  feedback: string
}

export default function GradeSubmissionModal({
  open,
  onOpenChange,
  submission,
  totalMarks
}: GradeSubmissionModalProps) {
  const [formData, setFormData] = React.useState<GradeFormData>({
    grade: submission?.grade?.toString() || '',
    feedback: submission?.feedback || ''
  })
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [errors, setErrors] = React.useState<Partial<GradeFormData>>({})
  const { toast } = useToast()

  React.useEffect(() => {
    if (submission) {
      setFormData({
        grade: submission.grade?.toString() || '',
        feedback: submission.feedback || ''
      })
    }
  }, [submission])

  const validateForm = (): boolean => {
    const newErrors: Partial<GradeFormData> = {}

    if (!formData.grade) {
      newErrors.grade = 'Grade is required'
    } else {
      const gradeNum = parseFloat(formData.grade)
      if (isNaN(gradeNum)) {
        newErrors.grade = 'Grade must be a number'
      } else if (gradeNum < 0) {
        newErrors.grade = 'Grade cannot be negative'
      } else if (gradeNum > totalMarks) {
        newErrors.grade = `Grade cannot exceed ${totalMarks}`
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name as keyof GradeFormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      toast({
        title: "Validation Error",
        description: "Please check all required fields.",
        variant: "destructive"
      })
      return
    }

    setIsSubmitting(true)
    try {
      // Here you would typically make an API call to save the grade
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
      
      toast({
        title: "Success",
        description: "Grade has been saved successfully.",
        variant: "success"
      })
      
      onOpenChange(false)
    } catch (error) {
      console.error('Error saving grade:', error)
      toast({
        title: "Error",
        description: "Failed to save grade. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDownload = (filename: string) => {
    // Implement download functionality
    toast({
      title: "Download Started",
      description: `Downloading ${filename}`,
      variant: "success"
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted':
        return 'text-blue-600'
      case 'late':
        return 'text-yellow-600'
      case 'graded':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  if (!submission) return null

  const submissionDate = new Date(submission.submittedAt)
  const isLate = submission.status === 'late'

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5" />
            Grade Submission
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Student Information */}
          <div className="space-y-2">
            <h3 className="font-medium">{submission.studentName}</h3>
            <p className="text-sm text-muted-foreground">ID: {submission.studentId}</p>
            <div className="flex items-center gap-2">
              <p className="text-sm text-muted-foreground">
                Submitted: {submissionDate.toLocaleDateString()} at {submissionDate.toLocaleTimeString()}
              </p>
              <span className={`text-xs font-medium ${getStatusColor(submission.status)}`}>
                ({submission.status.charAt(0).toUpperCase() + submission.status.slice(1)})
              </span>
            </div>
          </div>

          {/* Submission Files */}
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Submitted Files</h4>
            <div className="space-y-2">
              {submission.attachments.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-2 bg-gray-50 rounded-md"
                >
                  <span className="text-sm truncate">{file}</span>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDownload(file)}
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Grading Form */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Grade <span className="text-red-500">*</span>
              </label>
              <div className="mt-1 flex items-center gap-2">
                <input
                  type="number"
                  name="grade"
                  value={formData.grade}
                  onChange={handleChange}
                  min="0"
                  max={totalMarks}
                  step="0.5"
                  className="w-24 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
                <span className="text-sm text-muted-foreground">
                  / {totalMarks}
                </span>
              </div>
              {errors.grade && (
                <p className="text-sm text-red-500 mt-1">{errors.grade}</p>
              )}
              {formData.grade && (
                <p className="text-sm text-muted-foreground mt-1">
                  Percentage: {((parseFloat(formData.grade) / totalMarks) * 100).toFixed(1)}%
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Feedback
              </label>
              <textarea
                name="feedback"
                value={formData.feedback}
                onChange={handleChange}
                rows={4}
                className="mt-1 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Provide feedback to the student..."
              />
              <p className="text-sm text-muted-foreground mt-1">
                Provide constructive feedback to help the student understand their grade
              </p>
            </div>
          </div>

          {isLate && (
            <div className="rounded-md bg-yellow-50 p-4">
              <p className="text-sm text-yellow-700">
                This submission was received after the due date. Consider any late submission policies when grading.
              </p>
            </div>
          )}

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
              {isSubmitting ? 'Saving...' : 'Save Grade'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}