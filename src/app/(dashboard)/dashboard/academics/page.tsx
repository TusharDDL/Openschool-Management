// src/app/(dashboard)/dashboard/academics/page.tsx
'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { PlusCircle, Search, BookOpen, Users, Clock } from 'lucide-react'
import { cn } from '@/lib/utils'
import AddCourseModal from '@/components/academics/AddCourseModal'
import EditCourseModal from '@/components/academics/EditCourseModal'
import DeleteCourseDialog from '@/components/academics/DeleteCourseDialog'

interface Course {
  id: number
  name: string
  class: string
  subject: string
  teacher: string
  students: number
  schedule: string
  status: 'active' | 'upcoming' | 'completed'
  description?: string
  startDate?: string
  endDate?: string
  syllabus?: string
}

export default function AcademicsPage() {
  const [searchTerm, setSearchTerm] = React.useState('')
  const [selectedClass, setSelectedClass] = React.useState('')
  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false)
  const [selectedCourse, setSelectedCourse] = React.useState<Course | null>(null)
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = React.useState(false)

  const [courses, setCourses] = React.useState<Course[]>([
    {
      id: 1,
      name: "Mathematics Advanced",
      class: "10th",
      subject: "Mathematics",
      teacher: "Dr. Sarah Wilson",
      students: 35,
      schedule: "Mon, Wed, Fri - 9:00 AM",
      status: "active",
      description: "Advanced mathematics covering calculus and algebra",
      startDate: "2024-01-01",
      endDate: "2024-12-31"
    },
    {
      id: 2,
      name: "English Literature",
      class: "9th",
      subject: "English",
      teacher: "Prof. John Smith",
      students: 40,
      schedule: "Tue, Thu - 10:30 AM",
      status: "active",
      description: "Comprehensive English literature course",
      startDate: "2024-01-01",
      endDate: "2024-12-31"
    },
    {
      id: 3,
      name: "Physics Foundation",
      class: "10th",
      subject: "Science",
      teacher: "Mr. Robert Brown",
      students: 38,
      schedule: "Mon, Wed - 11:45 AM",
      status: "upcoming",
      description: "Fundamental physics concepts",
      startDate: "2024-01-15",
      endDate: "2024-12-15"
    },
    {
      id: 4,
      name: "Computer Science",
      class: "9th",
      subject: "Computer Science",
      teacher: "Ms. Emily Chen",
      students: 32,
      schedule: "Tue, Thu - 2:00 PM",
      status: "active",
      description: "Introduction to programming and algorithms",
      startDate: "2024-01-01",
      endDate: "2024-12-31"
    },
    {
      id: 5,
      name: "Biology Advanced",
      class: "10th",
      subject: "Science",
      teacher: "Dr. Michael Lee",
      students: 36,
      schedule: "Wed, Fri - 1:15 PM",
      status: "active",
      description: "Advanced biology concepts and lab work",
      startDate: "2024-01-01",
      endDate: "2024-12-31"
    }
  ])

  const handleEditCourse = (courseId: number) => {
    const course = courses.find(c => c.id === courseId)
    if (course) {
      setSelectedCourse(course)
      setIsEditModalOpen(true)
    }
  }

  const handleDeleteCourse = (courseId: number) => {
    const course = courses.find(c => c.id === courseId)
    if (course) {
      setSelectedCourse(course)
      setIsDeleteDialogOpen(true)
    }
  }

  const handleDeleteConfirm = async () => {
    if (!selectedCourse) return

    try {
      // Here you would typically make an API call to delete the course
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
      
      // Update local state to remove the deleted course
      setCourses(prevCourses => 
        prevCourses.filter(course => course.id !== selectedCourse.id)
      )
      
      setIsDeleteDialogOpen(false)
    } catch (error) {
      console.error('Error deleting course:', error)
    }
  }

  const filteredCourses = courses.filter(course => {
    const matchesSearch = 
      course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.teacher.toLowerCase().includes(searchTerm.toLowerCase()) ||
      course.subject.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesClass = selectedClass ? course.class === selectedClass : true
    return matchesSearch && matchesClass
  })

  const totalActiveStudents = courses
    .filter(course => course.status === 'active')
    .reduce((total, course) => total + course.students, 0)

  const totalTeachers = new Set(courses.map(course => course.teacher)).size

  const weeklyClasses = courses
    .filter(course => course.status === 'active')
    .length * 3 // Assuming average of 3 classes per course per week
    return (
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Academics</h1>
            <p className="text-muted-foreground">
              Manage courses, subjects, and academic schedules
            </p>
          </div>
    
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Courses</CardTitle>
                <BookOpen className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {courses.filter(course => course.status === 'active').length}
                </div>
                <p className="text-xs text-muted-foreground">
                  {courses.filter(course => course.status === 'upcoming').length} upcoming courses
                </p>
              </CardContent>
            </Card>
    
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Teachers</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalTeachers}</div>
                <p className="text-xs text-muted-foreground">
                  Teaching {courses.length} courses
                </p>
              </CardContent>
            </Card>
    
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Weekly Classes</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{weeklyClasses}</div>
                <p className="text-xs text-muted-foreground">
                  {totalActiveStudents} active students
                </p>
              </CardContent>
            </Card>
          </div>
    
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Course List</CardTitle>
                <div className="flex gap-4">
                  <div className="relative">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <input
                      type="text"
                      placeholder="Search courses..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-8 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <select
                    value={selectedClass}
                    onChange={(e) => setSelectedClass(e.target.value)}
                    className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Classes</option>
                    <option value="10th">10th</option>
                    <option value="9th">9th</option>
                    <option value="8th">8th</option>
                  </select>
                  <Button 
                    className="flex items-center gap-2"
                    onClick={() => setIsAddModalOpen(true)}
                  >
                    <PlusCircle className="h-4 w-4" />
                    Add Course
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="relative overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs uppercase bg-gray-50">
                    <tr>
                      <th className="px-6 py-3">Course Name</th>
                      <th className="px-6 py-3">Class</th>
                      <th className="px-6 py-3">Subject</th>
                      <th className="px-6 py-3">Teacher</th>
                      <th className="px-6 py-3">Students</th>
                      <th className="px-6 py-3">Schedule</th>
                      <th className="px-6 py-3">Status</th>
                      <th className="px-6 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredCourses.map((course) => (
                      <tr key={course.id} className="bg-white border-b hover:bg-gray-50">
                        <td className="px-6 py-4 font-medium">
                          <Link 
                            href={`/dashboard/academics/${course.id}`}
                            className="hover:text-blue-600 hover:underline"
                          >
                            {course.name}
                          </Link>
                        </td>
                        <td className="px-6 py-4">{course.class}</td>
                        <td className="px-6 py-4">{course.subject}</td>
                        <td className="px-6 py-4">{course.teacher}</td>
                        <td className="px-6 py-4">{course.students}</td>
                        <td className="px-6 py-4">{course.schedule}</td>
                        <td className="px-6 py-4">
                          <span
                            className={cn(
                              "px-2 py-1 text-xs font-semibold rounded-full",
                              {
                                "bg-green-100 text-green-800": course.status === "active",
                                "bg-yellow-100 text-yellow-800": course.status === "upcoming",
                                "bg-gray-100 text-gray-800": course.status === "completed"
                              }
                            )}
                          >
                            {course.status.charAt(0).toUpperCase() + course.status.slice(1)}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => handleEditCourse(course.id)}
                          >
                            Edit
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="text-red-600 hover:text-red-700"
                            onClick={() => handleDeleteCourse(course.id)}
                          >
                            Delete
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
    
          <AddCourseModal 
            open={isAddModalOpen}
            onOpenChange={setIsAddModalOpen}
          />
    
          <EditCourseModal 
            open={isEditModalOpen}
            onOpenChange={setIsEditModalOpen}
            courseData={selectedCourse}
          />
    
          <DeleteCourseDialog 
            open={isDeleteDialogOpen}
            onOpenChange={setIsDeleteDialogOpen}
            courseName={selectedCourse?.name || ''}
            onConfirm={handleDeleteConfirm}
          />
        </div>
      )
    }