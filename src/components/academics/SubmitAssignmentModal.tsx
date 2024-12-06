// src/components/academics/SubmitAssignmentModal.tsx
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
import { Upload, X, FileText, AlertCircle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import { cn } from '@/lib/utils'

interface SubmitAssignmentModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  assignment: {
    id: number
    title: string
    courseId: number
    courseName: string
    dueDate: string
    totalMarks: number
  } | null
}

interface FormData {
  files: File[]
  comments?: string
}

const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB
const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'image/jpeg',
  'image/png'
]

export default function SubmitAssignmentModal({
  open,
  onOpenChange,
  assignment
}: SubmitAssignmentModalProps) {
  const [formData, setFormData] = React.useState<FormData>({
    files: [],
    comments: ''
  })
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [errors, setErrors] = React.useState<string[]>([])
  const [isDragging, setIsDragging] = React.useState(false)
  const fileInputRef = React.useRef<HTMLInputElement>(null)
  const { toast } = useToast()
  const dragCounter = React.useRef(0)

  React.useEffect(() => {
    if (!open) {
      setFormData({ files: [], comments: '' })
      setErrors([])
      setIsDragging(false)
      dragCounter.current = 0
    }
  }, [open])

  const validateFiles = (files: File[]): string[] => {
    const newErrors: string[] = []

    if (files.length === 0) {
      newErrors.push('At least one file is required')
      return newErrors
    }

    for (const file of files) {
      if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        newErrors.push(`${file.name} is not a supported file type`)
      }
      if (file.size > MAX_FILE_SIZE) {
        newErrors.push(`${file.name} exceeds the maximum file size of 10MB`)
      }
    }

    return newErrors
  }

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    dragCounter.current += 1
    if (dragCounter.current === 1) {
      setIsDragging(true)
    }
  }

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    dragCounter.current -= 1
    if (dragCounter.current === 0) {
      setIsDragging(false)
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    
    setIsDragging(false)
    dragCounter.current = 0
    
    const droppedFiles = Array.from(e.dataTransfer.files)
    const newErrors = validateFiles(droppedFiles)
    setErrors(newErrors)
    
    if (newErrors.length === 0) {
      setFormData(prev => ({
        ...prev,
        files: [...prev.files, ...droppedFiles]
      }))
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])
    const newErrors = validateFiles(selectedFiles)
    setErrors(newErrors)
    
    if (newErrors.length === 0) {
      setFormData(prev => ({
        ...prev,
        files: [...prev.files, ...selectedFiles]
      }))
    }

    // Reset the input value to allow selecting the same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleCommentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData(prev => ({ ...prev, comments: e.target.value }))
  }

  const removeFile = (index: number) => {
    setFormData(prev => ({
      ...prev,
      files: prev.files.filter((_, i) => i !== index)
    }))
    setErrors([])
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const newErrors = validateFiles(formData.files)
    if (newErrors.length > 0) {
      setErrors(newErrors)
      return
    }

    setIsSubmitting(true)
    try {
      // Here you would typically make an API call to submit the assignment
      const formDataToSubmit = new FormData()
      formData.files.forEach((file, index) => {
        formDataToSubmit.append(`file-${index}`, file)
      })
      if (formData.comments) {
        formDataToSubmit.append('comments', formData.comments)
      }

      await new Promise(resolve => setTimeout(resolve, 1500)) // Simulate API call
      
      toast({
        title: "Success",
        description: "Assignment submitted successfully!",
        variant: "success"
      })
      
      onOpenChange(false)
    } catch (error) {
      console.error('Error submitting assignment:', error)
      toast({
        title: "Error",
        description: "Failed to submit assignment. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const isOverdue = assignment ? new Date(assignment.dueDate) < new Date() : false

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Submit Assignment
          </DialogTitle>
        </DialogHeader>

        {assignment && (
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Assignment Details */}
            <div className="space-y-2">
              <h3 className="font-medium">{assignment.title}</h3>
              <p className="text-sm text-muted-foreground">
                {assignment.courseName}
              </p>
              <div className="flex items-center gap-2">
                <p className="text-sm text-muted-foreground">
                  Due: {new Date(assignment.dueDate).toLocaleString()}
                </p>
                {isOverdue && (
                  <span className="text-xs font-medium text-red-600">Overdue</span>
                )}
              </div>
            </div>

            {/* File Upload Area */}
            <div
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={cn(
                "border-2 border-dashed rounded-lg p-8 text-center transition-colors",
                isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300",
                "cursor-pointer"
              )}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                accept={ALLOWED_FILE_TYPES.join(',')}
              />
              <div className="space-y-4">
                <div className="flex justify-center">
                  <Upload className={cn(
                    "h-8 w-8 transition-colors",
                    isDragging ? "text-blue-500" : "text-gray-400"
                  )} />
                </div>
                <div>
                  <p className="text-sm font-medium">
                    {isDragging ? 'Drop files to upload' : 'Drop files here or click to upload'}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Supported files: PDF, DOC, DOCX, JPG, PNG (max 10MB each)
                  </p>
                </div>
              </div>
            </div>

            {/* File List */}
            {formData.files.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium">Selected Files:</p>
                <div className="space-y-2">
                  {formData.files.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-2 bg-gray-50 rounded-md"
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <FileText className="h-4 w-4 text-blue-500 flex-shrink-0" />
                        <div className="min-w-0">
                          <p className="text-sm font-medium truncate">
                            {file.name}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {formatFileSize(file.size)}
                          </p>
                        </div>
                      </div>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Error Messages */}
            {errors.length > 0 && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      Upload Errors
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      <ul className="list-disc pl-5 space-y-1">
                        {errors.map((error, index) => (
                          <li key={index}>{error}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Comments */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Additional Comments
              </label>
              <textarea
                value={formData.comments}
                onChange={handleCommentChange}
                rows={3}
                className="mt-1 w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Any additional notes for your teacher..."
              />
            </div>

            {/* Overdue Warning */}
            {isOverdue && (
              <div className="rounded-md bg-yellow-50 p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-yellow-400" />
                  <div className="ml-3">
                    <p className="text-sm text-yellow-700">
                      This assignment is past its due date. Late submissions may affect your grade.
                    </p>
                  </div>
                </div>
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
              <Button
                type="submit"
                disabled={isSubmitting || formData.files.length === 0}
                className="min-w-[100px]"
              >
                {isSubmitting ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Submitting...
                  </div>
                ) : (
                  'Submit'
                )}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  )
}