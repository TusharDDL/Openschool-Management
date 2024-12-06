// src/components/layout/Sidebar.tsx
"use client"

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Home, 
  Users, 
  BookOpen, 
  Calculator, 
  Calendar, 
  MessageSquare, 
  Bus, 
  Library, 
  Settings 
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { SidebarItem } from '@/types/layout'

interface SidebarProps {
  isOpen: boolean
}

const menuItems: SidebarItem[] = [
  { icon: Home, label: 'Dashboard', href: '/dashboard' },
  { icon: Users, label: 'Students', href: '/dashboard/students' },
  { icon: BookOpen, label: 'Academics', href: '/dashboard/academics' },
  { icon: Calculator, label: 'Finance', href: '/dashboard/finance' },
  { icon: Calendar, label: 'Attendance', href: '/dashboard/attendance' },
  { icon: MessageSquare, label: 'Communication', href: '/dashboard/communication' },
  { icon: Bus, label: 'Transport', href: '/dashboard/transport' },
  { icon: Library, label: 'Library', href: '/dashboard/library' },
  { icon: Settings, label: 'Settings', href: '/dashboard/settings' }
]

const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        "fixed left-0 top-16 h-[calc(100vh-4rem)] bg-white shadow-lg transition-all duration-300",
        isOpen ? 'w-64' : 'w-20'
      )}
    >
      <nav className="mt-8">
        <div className="px-2 space-y-1">
          {menuItems.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.label}
                href={item.href}
                className={cn(
                  "flex items-center px-4 py-3 text-gray-600 rounded-lg transition-colors group",
                  isActive ? "bg-blue-50 text-blue-600" : "hover:bg-blue-50 hover:text-blue-600"
                )}
              >
                <item.icon className="h-5 w-5" />
                {isOpen && (
                  <span className="ml-3 text-sm font-medium">{item.label}</span>
                )}
                {!isOpen && (
                  <span className="sr-only">{item.label}</span>
                )}
              </Link>
            )
          })}
        </div>
      </nav>
    </aside>
  )
}

export default Sidebar