// src/components/settings/PasswordPolicyCard.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Lock,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Clock,
  RefreshCw
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface PasswordPolicy {
  minLength: number
  requireUppercase: boolean
  requireLowercase: boolean
  requireNumbers: boolean
  requireSpecialChars: boolean
  preventReuse: number
  expiryDays: number
  enforceHistory: number
}

export default function PasswordPolicyCard() {
  const { toast } = useToast()
  const [isEditing, setIsEditing] = React.useState(false)
  const [isSaving, setIsSaving] = React.useState(false)

  const [policy, setPolicy] = React.useState<PasswordPolicy>({
    minLength: 8,
    requireUppercase: true,
    requireLowercase: true,
    requireNumbers: true,
    requireSpecialChars: true,
    preventReuse: 5,
    expiryDays: 90,
    enforceHistory: 3
  })

  const handlePolicyChange = (
    key: keyof PasswordPolicy,
    value: number | boolean
  ) => {
    setPolicy(prev => ({ ...prev, [key]: value }))
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      // Here you would make an API call to update the password policy
      await new Promise(resolve => setTimeout(resolve, 1000))

      toast({
        title: "Success",
        description: "Password policy has been updated",
        variant: "success"
      })
      setIsEditing(false)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update password policy",
        variant: "destructive"
      })
    } finally {
      setIsSaving(false)
    }
  }

  const requirements = [
    {
      label: 'Minimum length',
      value: policy.minLength,
      type: 'number',
      min: 8,
      max: 128
    },
    {
      label: 'Uppercase letters required',
      checked: policy.requireUppercase,
      type: 'boolean'
    },
    {
      label: 'Lowercase letters required',
      checked: policy.requireLowercase,
      type: 'boolean'
    },
    {
      label: 'Numbers required',
      checked: policy.requireNumbers,
      type: 'boolean'
    },
    {
      label: 'Special characters required',
      checked: policy.requireSpecialChars,
      type: 'boolean'
    }
  ]

  const additionalSettings = [
    {
      label: 'Password expires after (days)',
      value: policy.expiryDays,
      type: 'number',
      min: 0,
      max: 365,
      icon: Clock
    },
    {
      label: 'Previous passwords prevented',
      value: policy.preventReuse,
      type: 'number',
      min: 0,
      max: 24,
      icon: RefreshCw
    }
  ]

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Lock className="h-5 w-5" />
            Password Policy
          </CardTitle>
          <Button
            variant="outline"
            onClick={() => {
              if (isEditing) {
                handleSave()
              } else {
                setIsEditing(true)
              }
            }}
            disabled={isSaving}
          >
            {isSaving ? (
              <>
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                Saving...
              </>
            ) : isEditing ? (
              'Save Changes'
            ) : (
              'Edit Policy'
            )}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Password Requirements */}
          <div className="space-y-4">
            <h4 className="text-sm font-medium text-muted-foreground">
              Password Requirements
            </h4>
            <div className="grid gap-4">
              {requirements.map((req) => (
                <div
                  key={req.label}
                  className="flex items-center justify-between"
                >
                  <span className="text-sm">{req.label}</span>
                  {req.type === 'number' ? (
                    <input
                      type="number"
                      value={req.value}
                      onChange={(e) => handlePolicyChange(
                        'minLength',
                        parseInt(e.target.value)
                      )}
                      min={req.min}
                      max={req.max}
                      className={`w-20 px-2 py-1 text-right border rounded-md ${
                        isEditing ? '' : 'bg-gray-50'
                      }`}
                      disabled={!isEditing}
                    />
                  ) : (
                    <button
                      type="button"
                      onClick={() => handlePolicyChange(
                        req.label.toLowerCase().replace(/ /g, '') as keyof PasswordPolicy,
                        !req.checked
                      )}
                      className={`p-2 rounded-full transition-colors ${
                        isEditing ? 'hover:bg-gray-100' : ''
                      }`}
                      disabled={!isEditing}
                    >
                      {req.checked ? (
                        <CheckCircle2 className="h-5 w-5 text-green-500" />
                      ) : (
                        <XCircle className="h-5 w-5 text-gray-300" />
                      )}
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Additional Settings */}
          <div className="space-y-4">
            <h4 className="text-sm font-medium text-muted-foreground">
              Additional Settings
            </h4>
            <div className="grid gap-4">
              {additionalSettings.map((setting) => (
                <div
                  key={setting.label}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center gap-2">
                    <setting.icon className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm">{setting.label}</span>
                  </div>
                  <input
                    type="number"
                    value={setting.value}
                    onChange={(e) => handlePolicyChange(
                      setting.label.includes('expires') ? 'expiryDays' : 'preventReuse',
                      parseInt(e.target.value)
                    )}
                    min={setting.min}
                    max={setting.max}
                    className={`w-20 px-2 py-1 text-right border rounded-md ${
                      isEditing ? '' : 'bg-gray-50'
                    }`}
                    disabled={!isEditing}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Warning Message */}
          <div className="rounded-md bg-yellow-50 p-4">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Important Note
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>Changes to password policy will:</p>
                  <ul className="list-disc pl-5 space-y-1 mt-2">
                    <li>Apply to all new passwords</li>
                    <li>Not affect existing passwords until they are changed</li>
                    <li>Trigger password reset for non-compliant accounts</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}