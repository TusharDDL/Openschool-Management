// src/components/layout/DashboardLayout.tsx
"use client"

import React, { useState } from 'react'
import { cn } from '@/lib/utils'
import { useAuth } from '@/contexts/AuthContext'
import Navbar from './Navbar'
import Sidebar, { teacherMenuItems, studentMenuItems } from './Sidebar'

interface DashboardLayoutProps {
  children: React.ReactNode
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const { user, currentRole } = useAuth()

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  // Get appropriate menu items based on role
  const getMenuItems = () => {
    if (!currentRole) return []
    
    switch (currentRole.toUpperCase()) {
      case 'TEACHER':
        return teacherMenuItems
      case 'STUDENT':
        return studentMenuItems
      default:
        console.error('Invalid role for DashboardLayout:', currentRole)
        return []
    }
  }

  // Format role for display (e.g., "TEACHER" -> "Teacher")
  const formatRole = (role: string | null): string => {
    if (!role) return 'Dashboard'
    return role.charAt(0).toUpperCase() + role.slice(1).toLowerCase()
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar onMenuClick={toggleSidebar} />
      <Sidebar 
        isOpen={isSidebarOpen}
        menuItems={getMenuItems()}
        title={`${formatRole(currentRole)} Portal`}
        onMenuClick={toggleSidebar}
      />
      <main
        className={cn(
          "transition-all duration-300 min-h-screen bg-gray-50",
          "pt-20 pb-8", // Increased top padding for better spacing
          "relative z-0", // Ensure proper stacking context
          isSidebarOpen ? 'sm:ml-64' : 'sm:ml-20',
          'ml-0' // Default margin on mobile
        )}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8 lg:px-10">
          {children}
        </div>
      </main>
    </div>
  )
}

export default DashboardLayout
