// src/app/(dashboard)/dashboard/profile/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  User, 
  Mail, 
  Phone, 
  Calendar,
  MapPin,
  Book,
  GraduationCap,
  Edit,
  Upload
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import EditProfileModal from '@/components/profile/EditProfileModal'

interface UserProfile {
  id: string
  firstName: string
  lastName: string
  email: string
  phone: string
  dateOfBirth: string
  address: string
  class: string
  section: string
  rollNumber: string
  admissionDate: string
  parentName: string
  parentPhone: string
  parentEmail: string
  bloodGroup: string
  emergencyContact: string
  avatar?: string
}

export default function ProfilePage() {
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
  const [isUploading, setIsUploading] = React.useState(false)
  const fileInputRef = React.useRef<HTMLInputElement>(null)
  const { toast } = useToast()

  // This would typically come from your API or auth context
  const userProfile: UserProfile = {
    id: "1",
    firstName: "John",
    lastName: "Doe",
    email: "john.doe@example.com",
    phone: "+91 9876543210",
    dateOfBirth: "2005-05-15",
    address: "123 School Street, City, State - 12345",
    class: "10th",
    section: "A",
    rollNumber: "1001",
    admissionDate: "2020-04-01",
    parentName: "Robert Doe",
    parentPhone: "+91 9876543211",
    parentEmail: "robert.doe@example.com",
    bloodGroup: "A+",
    emergencyContact: "+91 9876543212"
  }

  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.type.startsWith('image/')) {
      toast({
        title: "Error",
        description: "Please select an image file",
        variant: "destructive"
      })
      return
    }

    setIsUploading(true)
    try {
      // Here you would typically upload the file to your storage
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate upload
      
      toast({
        title: "Success",
        description: "Profile picture updated successfully",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update profile picture",
        variant: "destructive"
      })
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
          <p className="text-muted-foreground">
            Manage your personal information and preferences
          </p>
        </div>
        <Button
          onClick={() => setIsEditModalOpen(true)}
          className="flex items-center gap-2"
        >
          <Edit className="h-4 w-4" />
          Edit Profile
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Profile Overview */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Profile Picture Section */}
            <div className="flex items-center space-x-6">
              <div className="relative">
                <div className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
                  {userProfile.avatar ? (
                    <img 
                      src={userProfile.avatar} 
                      alt="Profile"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <User className="h-12 w-12 text-gray-400" />
                  )}
                </div>
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  accept="image/*"
                  onChange={handleAvatarChange}
                />
                <Button
                  variant="outline"
                  size="sm"
                  className="absolute bottom-0 right-0 rounded-full"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                >
                  <Upload className="h-4 w-4" />
                </Button>
              </div>
              <div>
                <h3 className="text-xl font-semibold">
                  {userProfile.firstName} {userProfile.lastName}
                </h3>
                <p className="text-sm text-muted-foreground">
                  Class {userProfile.class} - {userProfile.section}
                </p>
                <p className="text-sm text-muted-foreground">
                  Roll Number: {userProfile.rollNumber}
                </p>
              </div>
            </div>

            {/* Contact Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm text-muted-foreground">Email</label>
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <span>{userProfile.email}</span>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-sm text-muted-foreground">Phone</label>
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <span>{userProfile.phone}</span>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-sm text-muted-foreground">Date of Birth</label>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span>{new Date(userProfile.dateOfBirth).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-sm text-muted-foreground">Address</label>
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>{userProfile.address}</span>
                </div>
              </div>
            </div>

            {/* Academic Information */}
            <div className="border-t pt-4">
              <h4 className="font-medium mb-3">Academic Information</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-sm text-muted-foreground">Class & Section</label>
                  <div className="flex items-center gap-2">
                    <Book className="h-4 w-4 text-muted-foreground" />
                    <span>Class {userProfile.class} - {userProfile.section}</span>
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-sm text-muted-foreground">Admission Date</label>
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-4 w-4 text-muted-foreground" />
                    <span>{new Date(userProfile.admissionDate).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Parent Information */}
        <Card>
          <CardHeader>
            <CardTitle>Parent/Guardian Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1">
              <label className="text-sm text-muted-foreground">Parent Name</label>
              <p className="font-medium">{userProfile.parentName}</p>
            </div>

            <div className="space-y-1">
              <label className="text-sm text-muted-foreground">Parent Phone</label>
              <p className="font-medium">{userProfile.parentPhone}</p>
            </div>

            <div className="space-y-1">
              <label className="text-sm text-muted-foreground">Parent Email</label>
              <p className="font-medium">{userProfile.parentEmail}</p>
            </div>

            <div className="border-t pt-4">
              <h4 className="font-medium mb-3">Emergency Information</h4>
              <div className="space-y-2">
                <div className="space-y-1">
                  <label className="text-sm text-muted-foreground">Blood Group</label>
                  <p className="font-medium">{userProfile.bloodGroup}</p>
                </div>

                <div className="space-y-1">
                  <label className="text-sm text-muted-foreground">Emergency Contact</label>
                  <p className="font-medium">{userProfile.emergencyContact}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <EditProfileModal 
        open={isEditModalOpen}
        onOpenChange={setIsEditModalOpen}
        profile={userProfile}
      />
    </div>
  )
}