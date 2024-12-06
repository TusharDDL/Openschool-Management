// src/components/layout/Navbar.tsx
'use client';

import React from 'react';
import { Menu, Search, User, Settings, LogOut } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';  // Updated import path
import { Button } from '@/components/ui/button';
import { NavbarProps } from '@/types/layout';
import NotificationButton from '@/components/notifications/NotificationButton';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

export default function Navbar({ onMenuClick }: NavbarProps) {
  const { user, logout } = useAuth()
  const pathname = usePathname()
  const [isSearchFocused, setIsSearchFocused] = React.useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = React.useState(false)
  const userMenuRef = React.useRef<HTMLDivElement>(null)

  // Close user menu when clicking outside
  React.useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setIsUserMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  return (
    <nav className="bg-white shadow-sm fixed w-full z-10">
      <div className="mx-auto px-4">
        <div className="flex justify-between h-16">
          {/* Left Section */}
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={onMenuClick}
              className="p-2"
            >
              <Menu className="h-6 w-6" />
            </Button>
            <Link href="/dashboard" className="ml-4 flex items-center">
              <span className="text-xl font-bold text-blue-600">EduManager</span>
            </Link>
          </div>

          {/* Middle Section - Search */}
          <div className="hidden md:flex flex-1 items-center justify-center px-6">
            <div className="relative w-full max-w-lg">
              <input
                type="text"
                placeholder="Search..."
                className={cn(
                  "w-full px-4 py-2 pl-10 pr-4 rounded-lg text-sm border transition-all duration-200",
                  isSearchFocused
                    ? "border-blue-500 ring-2 ring-blue-200"
                    : "border-gray-200 hover:border-gray-300"
                )}
                onFocus={() => setIsSearchFocused(true)}
                onBlur={() => setIsSearchFocused(false)}
              />
              <div className="absolute left-3 top-2.5">
                <Search className={cn(
                  "h-5 w-5",
                  isSearchFocused ? "text-blue-500" : "text-gray-400"
                )} />
              </div>
            </div>
          </div>

          {/* Right Section */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <NotificationButton />

            {/* User Menu */}
            <div className="relative" ref={userMenuRef}>
              <Button
                variant="ghost"
                size="icon"
                className="relative"
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
              >
                <User className="h-5 w-5" />
              </Button>

              {/* User Dropdown Menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                  <div className="p-2">
                    {/* User Info */}
                    <div className="px-4 py-2">
                      <p className="text-sm font-semibold">{user?.name || 'User'}</p>
                      <p className="text-xs text-gray-500">{user?.email}</p>
                    </div>
                    
                    <div className="border-t my-1"></div>
                    
                    {/* Menu Items */}
                    <Link
                      href="/dashboard/profile"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <User className="h-4 w-4 mr-2" />
                      Profile
                    </Link>

                    <Link
                      href="/dashboard/settings"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <Settings className="h-4 w-4 mr-2" />
                      Settings
                    </Link>
                    
                    <div className="border-t my-1"></div>

                    <button
                      className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md"
                      onClick={async () => {
                        setIsUserMenuOpen(false)
                        await logout()
                      }}
                    >
                      <LogOut className="h-4 w-4 mr-2" />
                      Log out
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Mobile Search Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
            >
              <Search className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Search (Hidden by default) */}
      <div className="md:hidden border-t">
        <div className="p-2">
          <div className="relative">
            <input
              type="text"
              placeholder="Search..."
              className="w-full px-4 py-2 pl-10 pr-4 rounded-lg text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="absolute left-3 top-2.5">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}