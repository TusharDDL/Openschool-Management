// src/components/academics/CourseDetails.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  BookOpen, 
  Users, 
  Calendar,
  Clock,
  GraduationCap,
  FileText,
  PlusCircle,
  Download
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface Assignment {
  id: number
  title: string
  dueDate: string
  status: 'upcoming' | 'ongoing' | 'completed'
  totalMarks: number
}

interface Student {
  id: number
  name: string
  rollNo: string
  attendance: number
  performance: number
}

interface CourseDetailsProps {
  courseId: number
}

export default function CourseDetails({ courseId }: CourseDetailsProps) {
  // This would typically come from an API
  const courseData = {
    id: courseId,
    name: "Mathematics Advanced",
    class: "10th",
    subject: "Mathematics",
    teacher: "Dr. Sarah Wilson",
    students: 35,
    schedule: "Mon, Wed, Fri - 9:00 AM",
    status: "active" as const,
    description: "Advanced mathematics course covering calculus, algebra, and trigonometry.",
    syllabus: "path/to/syllabus.pdf",
    completionPercentage: 65,
    nextClass: "Monday, 10:00 AM",
    room: "Room 201"
  }

  const assignments: Assignment[] = [
    {
      id: 1,
      title: "Quadratic Equations Problem Set",
      dueDate: "2024-11-20",
      status: "upcoming",
      totalMarks: 50
    },
    {
      id: 2,
      title: "Trigonometry Assignment",
      dueDate: "2024-11-25",
      status: "ongoing",
      totalMarks: 100
    },
    {
      id: 3,
      title: "Basic Calculus Test",
      dueDate: "2024-11-15",
      status: "completed",
      totalMarks: 75
    }
  ]

  const students: Student[] = [
    {
      id: 1,
      name: "John Doe",
      rollNo: "10A01",
      attendance: 95,
      performance: 88
    },
    {
      id: 2,
      name: "Jane Smith",
      rollNo: "10A02",
      attendance: 92,
      performance: 94
    },
    {
      id: 3,
      name: "Mike Johnson",
      rollNo: "10A03",
      attendance: 88,
      performance: 82
    }
  ]

  const renderStatusBadge = (status: string) => (
    <span
      className={cn(
        "px-2 py-1 text-xs font-semibold rounded-full",
        {
          "bg-green-100 text-green-800": status === "active",
          "bg-yellow-100 text-yellow-800": status === "upcoming",
          "bg-gray-100 text-gray-800": status === "completed"
        }
      )}
    >
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  )

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{courseData.name}</h1>
          <p className="text-muted-foreground">
            {courseData.class} | {courseData.subject}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="flex items-center gap-2">
            <Download className="h-4 w-4" />
            Download Syllabus
          </Button>
          <Button className="flex items-center gap-2">
            <PlusCircle className="h-4 w-4" />
            Add Assignment
          </Button>
        </div>
      </div>

      {/* Course Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Students</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{courseData.students}</div>
            <p className="text-xs text-muted-foreground">Active enrolled</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Next Class</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{courseData.nextClass}</div>
            <p className="text-xs text-muted-foreground">{courseData.room}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completion</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{courseData.completionPercentage}%</div>
            <div className="w-full h-2 bg-gray-200 rounded-full mt-2">
              <div 
                className="h-full bg-blue-600 rounded-full"
                style={{ width: `${courseData.completionPercentage}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Performance</CardTitle>
            <GraduationCap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(students.reduce((acc, student) => acc + student.performance, 0) / students.length)}%
            </div>
            <p className="text-xs text-muted-foreground">Class average</p>
          </CardContent>
        </Card>
      </div>

      {/* Course Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Assignments Section */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Assignments</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {assignments.map((assignment) => (
                <div
                  key={assignment.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div className="space-y-1">
                    <p className="font-medium">{assignment.title}</p>
                    <p className="text-sm text-muted-foreground">
                      Due: {new Date(assignment.dueDate).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm font-medium">
                      {assignment.totalMarks} marks
                    </span>
                    {renderStatusBadge(assignment.status)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Student Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Top Performers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {students
                .sort((a, b) => b.performance - a.performance)
                .slice(0, 5)
                .map((student) => (
                  <div
                    key={student.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">{student.name}</p>
                      <p className="text-sm text-muted-foreground">
                        Roll No: {student.rollNo}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">{student.performance}%</p>
                      <p className="text-sm text-muted-foreground">
                        Attendance: {student.attendance}%
                      </p>
                    </div>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}