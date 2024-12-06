// src/components/notifications/NotificationCenter.tsx
'use client'

import React from 'react'
import {
  Bell,
  Book,
  CheckCircle,
  Calendar,
  MessageSquare,
  AlertCircle,
  Megaphone,
  X
} from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { Notification, NotificationType } from '@/types/notification'
import Link from 'next/link'

interface NotificationCenterProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const NOTIFICATION_ICONS: Record<NotificationType, React.ElementType> = {
  assignment: Book,
  grade: CheckCircle,
  attendance: Calendar,
  message: MessageSquare,
  announcement: Megaphone,
  reminder: AlertCircle,
}

const NOTIFICATION_COLORS: Record<NotificationType, string> = {
  assignment: 'bg-blue-500',
  grade: 'bg-green-500',
  attendance: 'bg-yellow-500',
  message: 'bg-purple-500',
  announcement: 'bg-orange-500',
  reminder: 'bg-red-500',
}

export default function NotificationCenter({ 
  open, 
  onOpenChange 
}: NotificationCenterProps) {
  const [notifications, setNotifications] = React.useState<Notification[]>([
    {
      id: '1',
      type: 'assignment',
      title: 'New Assignment Posted',
      message: 'Mathematics Problem Set 1 has been posted. Due date: Nov 20, 2024',
      timestamp: '2024-11-15T10:30:00',
      read: false,
      link: '/dashboard/student/assignments/1',
      course: {
        id: 1,
        name: 'Mathematics Advanced'
      },
      actionRequired: true,
      priority: 'high'
    },
    {
      id: '2',
      type: 'grade',
      title: 'Grade Posted',
      message: 'Your grade for Physics Lab Report has been posted',
      timestamp: '2024-11-14T15:45:00',
      read: true,
      link: '/dashboard/student/grades',
      course: {
        id: 3,
        name: 'Physics Foundation'
      }
    },
    {
      id: '3',
      type: 'announcement',
      title: 'School Event',
      message: 'Annual Science Fair will be held on December 1st, 2024',
      timestamp: '2024-11-13T09:00:00',
      read: false,
      priority: 'medium'
    }
  ])
  const [filter, setFilter] = React.useState<NotificationType | 'all'>('all')

  const markAsRead = (notificationId: string) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === notificationId
          ? { ...notification, read: true }
          : notification
      )
    )
  }

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification => ({ ...notification, read: true }))
    )
  }

  const deleteNotification = (notificationId: string) => {
    setNotifications(prev =>
      prev.filter(notification => notification.id !== notificationId)
    )
  }

  const filteredNotifications = notifications.filter(notification =>
    filter === 'all' ? true : notification.type === filter
  )

  const unreadCount = notifications.filter(n => !n.read).length

  const renderNotificationIcon = (type: NotificationType) => {
    const Icon = NOTIFICATION_ICONS[type]
    return (
      <div className={cn(
        "p-2 rounded-full",
        NOTIFICATION_COLORS[type],
        "bg-opacity-10"
      )}>
        <Icon className={cn(
          "h-5 w-5",
          NOTIFICATION_COLORS[type].replace('bg-', 'text-')
        )} />
      </div>
    )
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 24) {
      return diffInHours === 0 
        ? 'Just now'
        : `${diffInHours}h ago`
    }
    
    const diffInDays = Math.floor(diffInHours / 24)
    if (diffInDays < 7) {
      return `${diffInDays}d ago`
    }
    
    return date.toLocaleDateString()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md sm:max-w-xl">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notifications
              {unreadCount > 0 && (
                <span className="inline-flex items-center justify-center w-6 h-6 text-xs font-bold text-white bg-red-500 rounded-full">
                  {unreadCount}
                </span>
              )}
            </DialogTitle>
            {unreadCount > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={markAllAsRead}
              >
                Mark all as read
              </Button>
            )}
          </div>
        </DialogHeader>

        <div className="flex gap-2 pb-4 overflow-x-auto">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            All
          </Button>
          {Object.entries(NOTIFICATION_ICONS).map(([type, Icon]) => (
            <Button
              key={type}
              variant={filter === type ? 'default' : 'outline'}
              size="sm"
              onClick={() => setFilter(type as NotificationType)}
              className="flex items-center gap-1"
            >
              <Icon className="h-4 w-4" />
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </Button>
          ))}
        </div>

        <div className="space-y-4 max-h-[60vh] overflow-y-auto">
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              No notifications to show
            </div>
          ) : (
            filteredNotifications.map(notification => (
              <div
                key={notification.id}
                className={cn(
                  "relative flex gap-4 p-4 rounded-lg transition-colors",
                  notification.read ? "bg-gray-50" : "bg-blue-50",
                  "hover:bg-gray-100"
                )}
              >
                {renderNotificationIcon(notification.type)}
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <h4 className={cn(
                        "text-sm font-medium",
                        !notification.read && "font-semibold"
                      )}>
                        {notification.title}
                      </h4>
                      {notification.course && (
                        <p className="text-xs text-muted-foreground">
                          {notification.course.name}
                        </p>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground flex-shrink-0">
                      {formatTimestamp(notification.timestamp)}
                    </p>
                  </div>
                  
                  <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                    {notification.message}
                  </p>
                  
                  <div className="mt-2 flex items-center gap-3">
                    {notification.link && (
                      <Link 
                        href={notification.link}
                        className="text-sm text-blue-600 hover:text-blue-800"
                      >
                        View Details
                      </Link>
                    )}
                    {!notification.read && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => markAsRead(notification.id)}
                        className="text-sm"
                      >
                        Mark as Read
                      </Button>
                    )}
                    {notification.actionRequired && (
                      <span className="text-xs text-red-600 font-medium">
                        Action Required
                      </span>
                    )}
                  </div>
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => deleteNotification(notification.id)}
                >
                  <X className="h-4 w-4" />
                </Button>

                {notification.priority && (
                  <div className="absolute top-2 right-2">
                    <div className={cn(
                      "w-2 h-2 rounded-full",
                      {
                        'bg-red-500': notification.priority === 'high',
                        'bg-yellow-500': notification.priority === 'medium',
                        'bg-blue-500': notification.priority === 'low'
                      }
                    )} />
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}