// src/components/settings/SecuritySettings.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Shield,
  Smartphone,
  History,
  AlertTriangle,
  Key,
  LogOut,
  Globe,
  AlertCircle,
  ChevronRight
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import Enable2FAModal from './Enable2FAModal'
import DeleteAccountModal from './DeleteAccountModal'
import BackupCodesModal from './BackupCodesModal'

interface LoginSession {
  id: string
  device: string
  browser: string
  location: string
  ipAddress: string
  timestamp: string
  current: boolean
}

interface SecurityActivity {
  id: string
  action: string
  ipAddress: string
  location: string
  timestamp: string
  browser: string
  status: 'success' | 'warning' | 'error'
}

export default function SecuritySettings() {
  const [is2FAEnabled, setIs2FAEnabled] = React.useState(false)
  const [isEnable2FAModalOpen, setIsEnable2FAModalOpen] = React.useState(false)
  const [isBackupCodesModalOpen, setIsBackupCodesModalOpen] = React.useState(false)
  const [isDeleteAccountModalOpen, setIsDeleteAccountModalOpen] = React.useState(false)
  const { toast } = useToast()

  const [loginSessions, setLoginSessions] = React.useState<LoginSession[]>([
    {
      id: '1',
      device: 'Windows PC',
      browser: 'Chrome',
      location: 'Mumbai, India',
      ipAddress: '192.168.1.1',
      timestamp: new Date().toISOString(),
      current: true
    },
    {
      id: '2',
      device: 'iPhone 12',
      browser: 'Safari',
      location: 'Delhi, India',
      ipAddress: '192.168.1.2',
      timestamp: '2024-11-15T10:30:00',
      current: false
    },
    {
      id: '3',
      device: 'MacBook Pro',
      browser: 'Firefox',
      location: 'Bangalore, India',
      ipAddress: '192.168.1.3',
      timestamp: '2024-11-14T15:45:00',
      current: false
    }
  ])

  const [securityActivities] = React.useState<SecurityActivity[]>([
    {
      id: '1',
      action: 'Login successful',
      ipAddress: '192.168.1.1',
      location: 'Mumbai, India',
      timestamp: new Date().toISOString(),
      browser: 'Chrome',
      status: 'success'
    },
    {
      id: '2',
      action: 'Password changed',
      ipAddress: '192.168.1.1',
      location: 'Mumbai, India',
      timestamp: '2024-11-15T10:30:00',
      browser: 'Chrome',
      status: 'success'
    },
    {
      id: '3',
      action: 'Failed login attempt',
      ipAddress: '192.168.1.4',
      location: 'Unknown',
      timestamp: '2024-11-14T15:45:00',
      browser: 'Unknown',
      status: 'error'
    }
  ])

  const handleTerminateSession = async (sessionId: string) => {
    try {
      // Here you would make an API call to terminate the session
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setLoginSessions(prev => 
        prev.filter(session => session.id !== sessionId)
      )

      toast({
        title: "Session Terminated",
        description: "The selected session has been terminated successfully",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to terminate session. Please try again.",
        variant: "destructive"
      })
    }
  }

  const handleTerminateAllSessions = async () => {
    try {
      // Here you would make an API call to terminate all sessions except current
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setLoginSessions(prev => 
        prev.filter(session => session.current)
      )

      toast({
        title: "All Sessions Terminated",
        description: "All other sessions have been terminated successfully",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to terminate sessions. Please try again.",
        variant: "destructive"
      })
    }
  }

  const getStatusIcon = (status: SecurityActivity['status']) => {
    switch (status) {
      case 'success':
        return <div className="h-2 w-2 bg-green-400 rounded-full" />
      case 'warning':
        return <div className="h-2 w-2 bg-yellow-400 rounded-full" />
      case 'error':
        return <div className="h-2 w-2 bg-red-400 rounded-full" />
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short'
    }).format(date)
  }

  return (
    <div className="space-y-6">
      {/* Two-Factor Authentication */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Two-Factor Authentication
            </CardTitle>
            <Button
              variant={is2FAEnabled ? "outline" : "default"}
              onClick={() => setIsEnable2FAModalOpen(true)}
            >
              {is2FAEnabled ? 'Manage 2FA' : 'Enable 2FA'}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Add an extra layer of security to your account by enabling two-factor authentication.
              When 2FA is enabled, you'll need to enter a code from your authenticator app along
              with your password when signing in.
            </p>

            {is2FAEnabled && (
              <>
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <Shield className="h-4 w-4" />
                  Two-factor authentication is currently enabled
                </div>
                <Button
                  variant="outline"
                  onClick={() => setIsBackupCodesModalOpen(true)}
                  className="mt-2"
                >
                  <Key className="h-4 w-4 mr-2" />
                  View Backup Codes
                </Button>
              </>
            )}

            {!is2FAEnabled && (
              <div className="rounded-md bg-yellow-50 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <AlertCircle className="h-5 w-5 text-yellow-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      Recommended Security Setting
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      Enable two-factor authentication to better protect your account.
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Active Sessions */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5" />
              Active Sessions
            </CardTitle>
            {loginSessions.length > 1 && (
              <Button
                variant="outline"
                onClick={handleTerminateAllSessions}
              >
                Terminate All Other Sessions
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {loginSessions.map((session) => (
              <div
                key={session.id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Globe className="h-4 w-4 text-muted-foreground" />
                    <p className="font-medium">
                      {session.device} - {session.browser}
                      {session.current && (
                        <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                          Current Session
                        </span>
                      )}
                    </p>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {session.location} • {session.ipAddress}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Last active: {formatDate(session.timestamp)}
                  </div>
                </div>
                {!session.current && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleTerminateSession(session.id)}
                    className="text-red-600 hover:text-red-700"
                  >
                    <LogOut className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Security Log */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="h-5 w-5" />
            Security Activity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {securityActivities.map((activity) => (
              <div
                key={activity.id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-4">
                  {getStatusIcon(activity.status)}
                  <div className="space-y-1">
                    <p className="font-medium">{activity.action}</p>
                    <div className="text-sm text-muted-foreground">
                      {activity.browser} • {activity.location} • {activity.ipAddress}
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {formatDate(activity.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Account Deletion */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            Delete Account
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <Button
              variant="destructive"
              onClick={() => setIsDeleteAccountModalOpen(true)}
            >
              Delete Account
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Modals */}
      <Enable2FAModal
        open={isEnable2FAModalOpen}
        onOpenChange={setIsEnable2FAModalOpen}
        onSuccess={() => setIs2FAEnabled(true)}
      />

      <BackupCodesModal
        open={isBackupCodesModalOpen}
        onOpenChange={setIsBackupCodesModalOpen}
      />

      <DeleteAccountModal
        open={isDeleteAccountModalOpen}
        onOpenChange={setIsDeleteAccountModalOpen}
      />
    </div>
  )
}