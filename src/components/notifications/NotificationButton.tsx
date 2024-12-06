// src/components/notifications/NotificationButton.tsx
'use client'

import React from 'react'
import { Button } from '@/components/ui/button'
import { Bell } from 'lucide-react'
import NotificationCenter from './NotificationCenter'

export default function NotificationButton() {
  const [isOpen, setIsOpen] = React.useState(false)
  const [unreadCount, setUnreadCount] = React.useState(3) // This would come from your API

  return (
    <>
      <Button
        variant="ghost"
        size="icon"
        className="relative"
        onClick={() => setIsOpen(true)}
      >
        <Bell className="h-5 w-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full">
            {unreadCount}
          </span>
        )}
      </Button>

      <NotificationCenter
        open={isOpen}
        onOpenChange={setIsOpen}
      />
    </>
  )
}