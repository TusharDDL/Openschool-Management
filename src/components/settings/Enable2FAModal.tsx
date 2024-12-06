// src/components/settings/Enable2FAModal.tsx
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
import { Shield, Smartphone, Copy, RefreshCcw, Check } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import Link from 'next/link'
import Image from 'next/image'

interface Enable2FAModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess: () => void
}

interface VerificationStep {
  title: string
  description: string
}

const VERIFICATION_STEPS: VerificationStep[] = [
  {
    title: "Install authenticator app",
    description: "Download Google Authenticator or any other 2FA app on your phone"
  },
  {
    title: "Scan QR code",
    description: "Open your authenticator app and scan the QR code shown below"
  },
  {
    title: "Enter verification code",
    description: "Enter the 6-digit code shown in your authenticator app"
  }
]

export default function Enable2FAModal({
  open,
  onOpenChange,
  onSuccess
}: Enable2FAModalProps) {
  const [currentStep, setCurrentStep] = React.useState(0)
  const [verificationCode, setVerificationCode] = React.useState('')
  const [secretKey, setSecretKey] = React.useState('ABCD-EFGH-IJKL-MNOP')
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [isCopied, setIsCopied] = React.useState(false)
  const { toast } = useToast()

  React.useEffect(() => {
    if (!open) {
      setCurrentStep(0)
      setVerificationCode('')
      setIsCopied(false)
    }
  }, [open])

  const generateQRCode = () => {
    // This would typically make an API call to generate a new secret key
    setSecretKey('WXYZ-' + Math.random().toString(36).substring(7).toUpperCase())
  }

  const copySecretKey = async () => {
    try {
      await navigator.clipboard.writeText(secretKey)
      setIsCopied(true)
      setTimeout(() => setIsCopied(false), 2000)
      toast({
        title: "Copied",
        description: "Secret key copied to clipboard",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to copy secret key",
        variant: "destructive"
      })
    }
  }

  const handleVerificationCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, '').slice(0, 6)
    setVerificationCode(value)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (verificationCode.length !== 6) {
      toast({
        title: "Invalid Code",
        description: "Please enter a 6-digit verification code",
        variant: "destructive"
      })
      return
    }

    setIsSubmitting(true)
    try {
      // Here you would make an API call to verify the code
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      toast({
        title: "Success",
        description: "Two-factor authentication has been enabled",
        variant: "success"
      })
      
      onSuccess()
      onOpenChange(false)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to verify code. Please try again.",
        variant: "destructive"
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancel = () => {
    setCurrentStep(0)
    setVerificationCode('')
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Enable Two-Factor Authentication
          </DialogTitle>
        </DialogHeader>

        {/* Steps Indicator */}
        <div className="relative mt-4">
          <div className="absolute top-4 w-full h-0.5 bg-gray-200">
            <div
              className="absolute h-full bg-blue-600 transition-all duration-300"
              style={{ width: `${((currentStep + 1) / VERIFICATION_STEPS.length) * 100}%` }}
            />
          </div>
          <div className="relative flex justify-between">
            {VERIFICATION_STEPS.map((step, index) => (
              <div
                key={index}
                className={`flex flex-col items-center gap-2 ${
                  index <= currentStep ? 'text-blue-600' : 'text-gray-400'
                }`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center z-10 ${
                    index <= currentStep
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {index + 1}
                </div>
                <span className="text-xs text-center max-w-[80px]">
                  {step.title}
                </span>
              </div>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          {/* Step Content */}
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">
              {VERIFICATION_STEPS[currentStep].description}
            </p>

            {currentStep === 0 && (
              <div className="flex flex-col gap-4">
                <Link
                  href="https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2"
                  target="_blank"
                  className="flex items-center gap-2 p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                    <Smartphone className="h-5 w-5 text-gray-600" />
                  </div>
                  <div>
                    <p className="font-medium">Google Authenticator</p>
                    <p className="text-sm text-muted-foreground">
                      For Android & iOS
                    </p>
                  </div>
                </Link>
              </div>
            )}

            {currentStep === 1 && (
              <div className="space-y-4">
                <div className="flex justify-center">
                  {/* This would be your actual QR code */}
                  <div className="w-48 h-48 bg-gray-100 rounded-lg flex items-center justify-center text-sm text-gray-500">
                    QR Code Placeholder
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Secret Key
                  </label>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 p-2 bg-gray-100 rounded text-sm font-mono">
                      {secretKey}
                    </code>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={copySecretKey}
                    >
                      {isCopied ? (
                        <Check className="h-4 w-4 text-green-600" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={generateQRCode}
                    >
                      <RefreshCcw className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Verification Code
                  </label>
                  <input
                    type="text"
                    value={verificationCode}
                    onChange={handleVerificationCodeChange}
                    className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-center text-2xl tracking-widest font-mono"
                    placeholder="000000"
                    required
                    autoComplete="off"
                  />
                </div>
              </div>
            )}
          </div>

          <DialogFooter>
            {currentStep === 0 ? (
              <>
                <Button type="button" variant="outline" onClick={handleCancel}>
                  Cancel
                </Button>
                <Button type="button" onClick={() => setCurrentStep(1)}>
                  Next
                </Button>
              </>
            ) : currentStep === 1 ? (
              <>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setCurrentStep(0)}
                >
                  Back
                </Button>
                <Button type="button" onClick={() => setCurrentStep(2)}>
                  Next
                </Button>
              </>
            ) : (
              <>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setCurrentStep(1)}
                  disabled={isSubmitting}
                >
                  Back
                </Button>
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Verifying...
                    </div>
                  ) : (
                    'Enable 2FA'
                  )}
                </Button>
              </>
            )}
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}