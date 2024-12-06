// src/components/settings/BackupCodesModal.tsx
'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogDescription,
} from '@/components/ui/dialog'
import { Key, Download, Copy, RefreshCw, Printer, AlertTriangle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface BackupCodesModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

interface BackupCode {
  code: string
  used: boolean
}

export default function BackupCodesModal({
  open,
  onOpenChange
}: BackupCodesModalProps) {
  const [codes, setCodes] = React.useState<BackupCode[]>([])
  const [isGenerating, setIsGenerating] = React.useState(false)
  const [isCopied, setIsCopied] = React.useState(false)
  const { toast } = useToast()

  // Generate codes when modal opens
  React.useEffect(() => {
    if (open && codes.length === 0) {
      generateCodes()
    }
  }, [open])

  const generateCodes = async () => {
    setIsGenerating(true)
    try {
      // In a real app, this would be an API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Generate 10 random codes
      const newCodes: BackupCode[] = Array.from({ length: 10 }, () => ({
        code: Array.from({ length: 4 }, () => 
          Math.random().toString(36).substring(2, 6)
        ).join('-').toUpperCase(),
        used: false
      }))
      
      setCodes(newCodes)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate backup codes",
        variant: "destructive"
      })
    } finally {
      setIsGenerating(false)
    }
  }

  const copyAllCodes = async () => {
    try {
      const codesText = codes.map(code => code.code).join('\n')
      await navigator.clipboard.writeText(codesText)
      setIsCopied(true)
      setTimeout(() => setIsCopied(false), 2000)
      toast({
        title: "Success",
        description: "Backup codes copied to clipboard",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to copy codes",
        variant: "destructive"
      })
    }
  }

  const downloadCodes = () => {
    try {
      const codesText = codes.map(code => code.code).join('\n')
      const blob = new Blob([codesText], { type: 'text/plain' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'backup-codes.txt'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      toast({
        title: "Success",
        description: "Backup codes downloaded successfully",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download codes",
        variant: "destructive"
      })
    }
  }

  const printCodes = () => {
    const printWindow = window.open('', '', 'width=600,height=600')
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>2FA Backup Codes</title>
            <style>
              body {
                font-family: system-ui, -apple-system, sans-serif;
                padding: 2rem;
                max-width: 600px;
                margin: 0 auto;
              }
              h1 { font-size: 1.5rem; margin-bottom: 1rem; }
              .code {
                font-family: monospace;
                padding: 0.5rem;
                margin: 0.5rem 0;
                background: #f1f5f9;
                border-radius: 0.25rem;
              }
              .warning {
                margin-top: 2rem;
                padding: 1rem;
                background: #fef2f2;
                border-radius: 0.5rem;
                color: #991b1b;
              }
              @media print {
                body { padding: 0; }
                .warning { break-inside: avoid; }
              }
            </style>
          </head>
          <body>
            <h1>2FA Backup Codes</h1>
            <div>${codes.map(code => 
              `<div class="code">${code.code}</div>`
            ).join('')}</div>
            <div class="warning">
              <strong>Important:</strong>
              <ul>
                <li>Keep these codes safe and secure</li>
                <li>Each code can only be used once</li>
                <li>Generate new codes if they are lost or compromised</li>
              </ul>
            </div>
          </body>
        </html>
      `)
      printWindow.document.close()
      printWindow.print()
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            Backup Codes
          </DialogTitle>
          <DialogDescription>
            Save these backup codes in a secure place to regain access to your account if you lose your authentication device.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Warning Message */}
          <div className="rounded-md bg-yellow-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertTriangle className="h-5 w-5 text-yellow-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Important Security Information
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <ul className="list-disc space-y-1 pl-5">
                    <li>Each code can only be used once</li>
                    <li>Save these codes somewhere safe but accessible</li>
                    <li>Generate new codes if they become compromised</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Backup Codes */}
          <div className="grid grid-cols-2 gap-2">
            {codes.map((code, index) => (
              <div
                key={index}
                className="p-2 bg-gray-50 rounded-md text-center font-mono text-sm"
              >
                {code.code}
              </div>
            ))}
          </div>

          {/* Actions */}
          <div className="flex flex-col gap-2">
            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={copyAllCodes}
              disabled={isGenerating}
            >
              <Copy className="h-4 w-4 mr-2" />
              {isCopied ? 'Copied!' : 'Copy Codes'}
            </Button>
            
            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={downloadCodes}
              disabled={isGenerating}
            >
              <Download className="h-4 w-4 mr-2" />
              Download Codes
            </Button>

            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={printCodes}
              disabled={isGenerating}
            >
              <Printer className="h-4 w-4 mr-2" />
              Print Codes
            </Button>

            <Button
              type="button"
              variant="outline"
              className="w-full"
              onClick={generateCodes}
              disabled={isGenerating}
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isGenerating ? 'animate-spin' : ''}`} />
              Generate New Codes
            </Button>
          </div>
        </div>

        <DialogFooter>
          <Button
            type="button"
            variant="default"
            onClick={() => onOpenChange(false)}
            disabled={isGenerating}
          >
            Done
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}