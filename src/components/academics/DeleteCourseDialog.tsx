// src/components/academics/DeleteCourseDialog.tsx
'use client'

import React from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { AlertTriangle } from 'lucide-react'

interface DeleteCourseDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  courseName: string
  onConfirm: () => Promise<void>
}

export default function DeleteCourseDialog({
  open,
  onOpenChange,
  courseName,
  onConfirm
}: DeleteCourseDialogProps) {
  const [isDeleting, setIsDeleting] = React.useState(false)

  const handleDelete = async () => {
    setIsDeleting(true)
    try {
      await onConfirm()
      onOpenChange(false)
    } catch (error) {
      console.error('Error deleting course:', error)
    } finally {
      setIsDeleting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            Delete Course
          </DialogTitle>
        </DialogHeader>

        <DialogDescription className="space-y-3">
          <p>
            Are you sure you want to delete <span className="font-medium">{courseName}</span>?
          </p>
          <p className="text-sm text-red-600">
            This action cannot be undone. This will permanently delete the course
            and remove all associated data including assignments, grades, and attendance records.
          </p>
        </DialogDescription>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button 
            type="button" 
            variant="destructive"
            onClick={handleDelete}
            disabled={isDeleting}
          >
            {isDeleting ? 'Deleting...' : 'Delete Course'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}