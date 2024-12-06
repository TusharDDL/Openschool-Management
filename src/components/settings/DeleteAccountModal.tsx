// src/components/settings/DeleteAccountModal.tsx
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
import { AlertTriangle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface DeleteAccountModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export default function DeleteAccountModal({
  open,
  onOpenChange
}: DeleteAccountModalProps) {
  const [confirmation, setConfirmation] = React.useState('')
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const { toast } = useToast()

  const CONFIRMATION_TEXT = "delete my account"

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (confirmation.toLowerCase() !== CONFIRMATION_TEXT) {
      toast({
        title: "Invalid Confirmation",
        description: `Please type "${CONFIRMATION_TEXT}" to confirm`,
        variant: "destructive"
      })
      return
    }

    setIsSubmitting(true)
    try {
      // Here you would make an API call to delete the account
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      toast({
        title: "Account Deleted",
        description: "Your account has been permanently deleted",
        variant: "success"
      })
      
      // Redirect to login page or home page
      window.location.href = '/login'
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete account. Please try again.",
        variant: "destructive"
      })
      setIsSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            Delete Account
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-5 w-5 text-red-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Warning: This action cannot be undone
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  <ul className="list-disc space-y-1 pl-5">
                    <li>Your account will be permanently deleted</li>
                    <li>All your data will be removed</li>
                    <li>You won't be able to recover your account</li>
                    <li>Active subscriptions will be cancelled</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Confirmation
              </label>
              <p className="text-sm text-muted-foreground mt-1">
                Please type <span className="font-medium">"{CONFIRMATION_TEXT}"</span> to confirm
              </p>
              <input
                type="text"
                value={confirmation}
                onChange={(e) => setConfirmation(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                placeholder={CONFIRMATION_TEXT}
                required
              />
            </div>
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
            <Button
              type="submit"
              variant="destructive"
              disabled={isSubmitting || confirmation.toLowerCase() !== CONFIRMATION_TEXT}
            >
              {isSubmitting ? (
                <div className="flex items-center">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                  Deleting...
                </div>
              ) : (
                'Delete Account'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}