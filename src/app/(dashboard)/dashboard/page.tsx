// src/app/(dashboard)/dashboard/page.tsx
'use client'

import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Users, BookOpen, DollarSign, Calendar } from 'lucide-react'

interface StatItem {
  title: string
  value: string
  icon: React.ElementType
  change: string
  description: string
}

export default function DashboardPage() {
  const stats: StatItem[] = [
    {
      title: 'Total Students',
      value: '1,234',
      icon: Users,
      change: '+12%',
      description: 'from last month'
    },
    {
      title: 'Active Courses',
      value: '42',
      icon: BookOpen,
      change: '+3',
      description: 'new this month'
    },
    {
      title: 'Revenue',
      value: '₹12.5L',
      icon: DollarSign,
      change: '+18%',
      description: 'from last month'
    },
    {
      title: 'Attendance',
      value: '92%',
      icon: Calendar,
      change: '+2%',
      description: 'from last week'
    }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to your school management dashboard
        </p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600">{stat.change}</span> {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}