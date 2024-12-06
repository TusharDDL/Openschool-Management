// src/app/(dashboard)/dashboard/student/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  BookOpen, 
  Calendar, 
  Clock, 
  TrendingUp, 
  AlertCircle,
  ChevronRight,
  GraduationCap,
  BarChart3
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  Legend
} from 'recharts'
import Link from 'next/link'

interface Assignment {
  id: number
  title: string
  courseName: string
  dueDate: string
  status: 'pending' | 'submitted' | 'late' | 'graded'
}

interface Course {
  id: number
  name: string
  attendance: number
  nextClass: string
  currentGrade?: number
  teacher: string
}

interface GradeData {
  subject: string
  grade: number
  classAverage: number
}

interface AttendanceData {
  month: string
  attendance: number
  classAverage: number
}

export default function StudentDashboard() {
  // Sample data - would typically come from an API
  const recentAssignments: Assignment[] = [
    {
      id: 1,
      title: "Mathematics Problem Set 1",
      courseName: "Mathematics Advanced",
      dueDate: "2024-11-20",
      status: "pending"
    },
    {
      id: 2,
      title: "English Essay Writing",
      courseName: "English Literature",
      dueDate: "2024-11-18",
      status: "submitted"
    },
    {
      id: 3,
      title: "Physics Lab Report",
      courseName: "Physics Foundation",
      dueDate: "2024-11-15",
      status: "graded"
    }
  ]

  const courses: Course[] = [
    {
      id: 1,
      name: "Mathematics Advanced",
      attendance: 92,
      nextClass: "Monday, 9:00 AM",
      currentGrade: 88,
      teacher: "Dr. Sarah Wilson"
    },
    {
      id: 2,
      name: "English Literature",
      attendance: 95,
      nextClass: "Tuesday, 10:30 AM",
      currentGrade: 85,
      teacher: "Prof. John Smith"
    },
    {
      id: 3,
      name: "Physics Foundation",
      attendance: 88,
      nextClass: "Wednesday, 11:45 AM",
      currentGrade: 82,
      teacher: "Mr. Robert Brown"
    }
  ]

  const gradeData: GradeData[] = [
    { subject: "Mathematics", grade: 88, classAverage: 82 },
    { subject: "English", grade: 85, classAverage: 78 },
    { subject: "Physics", grade: 82, classAverage: 75 },
    { subject: "Chemistry", grade: 90, classAverage: 80 },
    { subject: "Biology", grade: 87, classAverage: 79 }
  ]

  const attendanceData: AttendanceData[] = [
    { month: "Aug", attendance: 95, classAverage: 88 },
    { month: "Sep", attendance: 92, classAverage: 87 },
    { month: "Oct", attendance: 88, classAverage: 85 },
    { month: "Nov", attendance: 94, classAverage: 86 }
  ]

  const getStatusColor = (status: Assignment['status']) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-600'
      case 'submitted':
        return 'text-blue-600'
      case 'late':
        return 'text-red-600'
      case 'graded':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  const getAttendanceColor = (percentage: number) => {
    if (percentage >= 90) return 'text-green-600'
    if (percentage >= 80) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Student Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back, John Doe
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overall Grade</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85.4%</div>
            <p className="text-xs text-muted-foreground">
              +2.5% from last term
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Attendance</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">92%</div>
            <p className="text-xs text-muted-foreground">
              Current semester
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Due Assignments</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">
              Within next 7 days
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Courses</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{courses.length}</div>
            <p className="text-xs text-muted-foreground">
              Current semester
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* Recent Assignments */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Recent Assignments</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/dashboard/student/assignments" className="flex items-center gap-1">
                  View All
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentAssignments.map((assignment) => (
                <div
                  key={assignment.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div>
                    <h4 className="font-medium">{assignment.title}</h4>
                    <p className="text-sm text-muted-foreground">
                      {assignment.courseName}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Due: {new Date(assignment.dueDate).toLocaleDateString()}
                    </p>
                  </div>
                  <span className={`text-sm font-medium ${getStatusColor(assignment.status)}`}>
                    {assignment.status.charAt(0).toUpperCase() + assignment.status.slice(1)}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Current Courses */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Current Courses</CardTitle>
              <Button variant="ghost" size="sm" asChild>
                <Link href="/dashboard/student/courses" className="flex items-center gap-1">
                  View All
                  <ChevronRight className="h-4 w-4" />
                </Link>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {courses.map((course) => (
                <div
                  key={course.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div>
                    <h4 className="font-medium">{course.name}</h4>
                    <p className="text-sm text-muted-foreground">
                      {course.teacher}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Next Class: {course.nextClass}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-medium ${getAttendanceColor(course.attendance)}`}>
                      {course.attendance}% attendance
                    </span>
                    {course.currentGrade && (
                      <p className="text-sm text-muted-foreground mt-1">
                        Current Grade: {course.currentGrade}%
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Grade Performance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GraduationCap className="h-5 w-5" />
              Grade Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={gradeData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="subject" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="grade" fill="#3b82f6" name="Your Grade" />
                  <Bar dataKey="classAverage" fill="#93c5fd" name="Class Average" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Attendance Trend */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Attendance Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={attendanceData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="attendance" 
                    stroke="#3b82f6" 
                    name="Your Attendance"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="classAverage" 
                    stroke="#93c5fd" 
                    name="Class Average"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}