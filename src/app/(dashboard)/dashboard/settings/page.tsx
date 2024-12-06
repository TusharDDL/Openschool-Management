// src/app/(dashboard)/dashboard/settings/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Bell,
  Lock,
  Shield,
  Mail,
  Smartphone,
  Eye,
  Book,
  AlertCircle,
  Globe,
  ChevronRight,
  Download
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import ChangePasswordModal from '@/components/settings/ChangePasswordModal'

interface NotificationSetting {
  id: string
  title: string
  description: string
  email: boolean
  push: boolean
  type: 'academic' | 'attendance' | 'grades' | 'events' | 'announcements'
}

interface PrivacySetting {
  id: string
  title: string
  description: string
  value: 'public' | 'private' | 'school'
}

export default function SettingsPage() {
  const [isPasswordModalOpen, setIsPasswordModalOpen] = React.useState(false)
  const { toast } = useToast()
  
  const [notificationSettings, setNotificationSettings] = React.useState<NotificationSetting[]>([
    {
      id: '1',
      title: 'Assignment Updates',
      description: 'Notifications about new assignments, due dates, and submissions',
      email: true,
      push: true,
      type: 'academic'
    },
    {
      id: '2',
      title: 'Attendance Marking',
      description: 'Daily attendance status and reports',
      email: true,
      push: false,
      type: 'attendance'
    },
    {
      id: '3',
      title: 'Grade Updates',
      description: 'New grades and assessment results',
      email: true,
      push: true,
      type: 'grades'
    },
    {
      id: '4',
      title: 'School Events',
      description: 'Updates about upcoming school events and activities',
      email: true,
      push: true,
      type: 'events'
    },
    {
      id: '5',
      title: 'Announcements',
      description: 'Important school announcements and notices',
      email: true,
      push: true,
      type: 'announcements'
    }
  ])

  const [privacySettings, setPrivacySettings] = React.useState<PrivacySetting[]>([
    {
      id: '1',
      title: 'Profile Visibility',
      description: 'Control who can see your profile information',
      value: 'school'
    },
    {
      id: '2',
      title: 'Grade Visibility',
      description: 'Control who can see your grades and academic performance',
      value: 'private'
    },
    {
      id: '3',
      title: 'Attendance Records',
      description: 'Control who can see your attendance records',
      value: 'school'
    }
  ])

  const [preferredLanguage, setPreferredLanguage] = React.useState('en')
  const [darkMode, setDarkMode] = React.useState(false)

  const handleNotificationToggle = (
    settingId: string, 
    type: 'email' | 'push'
  ) => {
    setNotificationSettings(prev =>
      prev.map(setting =>
        setting.id === settingId
          ? { ...setting, [type]: !setting[type] }
          : setting
      )
    )

    toast({
      title: "Settings Updated",
      description: "Your notification preferences have been saved",
      variant: "success"
    })
  }

  const handlePrivacyChange = (
    settingId: string,
    value: 'public' | 'private' | 'school'
  ) => {
    setPrivacySettings(prev =>
      prev.map(setting =>
        setting.id === settingId
          ? { ...setting, value }
          : setting
      )
    )

    toast({
      title: "Privacy Setting Updated",
      description: "Your privacy preferences have been saved",
      variant: "success"
    })
  }

  const handleExportData = async () => {
    try {
      // Here you would typically make an API call to request data export
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      toast({
        title: "Data Export Requested",
        description: "You will receive an email with your data soon",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to request data export",
        variant: "destructive"
      })
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Account Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Account Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button
              variant="outline"
              className="w-full flex items-center justify-between"
              onClick={() => setIsPasswordModalOpen(true)}
            >
              <div className="flex items-center gap-2">
                <Lock className="h-4 w-4" />
                <span>Change Password</span>
              </div>
              <ChevronRight className="h-4 w-4" />
            </Button>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Preferred Language
              </label>
              <select
                value={preferredLanguage}
                onChange={(e) => setPreferredLanguage(e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="te">Telugu</option>
                <option value="ta">Tamil</option>
                <option value="kn">Kannada</option>
              </select>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Eye className="h-4 w-4" />
                <span>Dark Mode</span>
              </div>
              <button
                type="button"
                role="switch"
                aria-checked={darkMode}
                onClick={() => setDarkMode(!darkMode)}
                className={`
                  relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent 
                  transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 
                  ${darkMode ? 'bg-blue-600' : 'bg-gray-200'}
                `}
              >
                <span
                  aria-hidden="true"
                  className={`
                    pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow 
                    ring-0 transition duration-200 ease-in-out
                    ${darkMode ? 'translate-x-5' : 'translate-x-0'}
                  `}
                />
              </button>
            </div>

            <Button
              variant="outline"
              className="w-full flex items-center justify-between"
              onClick={handleExportData}
            >
              <div className="flex items-center gap-2">
                <Download className="h-4 w-4" />
                <span>Export My Data</span>
              </div>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </CardContent>
        </Card>

        {/* Privacy Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Privacy Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {privacySettings.map(setting => (
              <div key={setting.id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-medium">{setting.title}</h4>
                    <p className="text-sm text-muted-foreground">
                      {setting.description}
                    </p>
                  </div>
                </div>
                <select
                  value={setting.value}
                  onChange={(e) => handlePrivacyChange(
                    setting.id,
                    e.target.value as 'public' | 'private' | 'school'
                  )}
                  className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="public">Public</option>
                  <option value="school">School Only</option>
                  <option value="private">Private</option>
                </select>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Notification Preferences</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {notificationSettings.map(setting => (
                <div
                  key={setting.id}
                  className="flex items-start justify-between p-4 border rounded-lg"
                >
                  <div>
                    <h4 className="text-sm font-medium">{setting.title}</h4>
                    <p className="text-sm text-muted-foreground">
                      {setting.description}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <label className="text-sm text-muted-foreground">Email</label>
                      <button
                        type="button"
                        role="switch"
                        aria-checked={setting.email}
                        onClick={() => handleNotificationToggle(setting.id, 'email')}
                        className={`
                          relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full 
                          border-2 border-transparent transition-colors duration-200 ease-in-out 
                          focus:outline-none focus:ring-2 focus:ring-blue-500
                          ${setting.email ? 'bg-blue-600' : 'bg-gray-200'}
                        `}
                      >
                        <span
                          aria-hidden="true"
                          className={`
                            pointer-events-none inline-block h-5 w-5 transform rounded-full 
                            bg-white shadow ring-0 transition duration-200 ease-in-out
                            ${setting.email ? 'translate-x-5' : 'translate-x-0'}
                          `}
                        />
                      </button>
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-sm text-muted-foreground">Push</label>
                      <button
                        type="button"
                        role="switch"
                        aria-checked={setting.push}
                        onClick={() => handleNotificationToggle(setting.id, 'push')}
                        className={`
                          relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full 
                          border-2 border-transparent transition-colors duration-200 ease-in-out 
                          focus:outline-none focus:ring-2 focus:ring-blue-500
                          ${setting.push ? 'bg-blue-600' : 'bg-gray-200'}
                        `}
                      >
                        <span
                          aria-hidden="true"
                          className={`
                            pointer-events-none inline-block h-5 w-5 transform rounded-full 
                            bg-white shadow ring-0 transition duration-200 ease-in-out
                            ${setting.push ? 'translate-x-5' : 'translate-x-0'}
                          `}
                        />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <ChangePasswordModal
        open={isPasswordModalOpen}
        onOpenChange={setIsPasswordModalOpen}
      />
    </div>
  )
}