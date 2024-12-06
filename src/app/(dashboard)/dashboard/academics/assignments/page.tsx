// src/app/(dashboard)/dashboard/academics/assignments/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  PlusCircle, 
  Search, 
  FileText, 
  Calendar,
  CheckCircle2,
  Clock
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Assignment } from '@/types/academics'
import AddAssignmentModal from '@/components/academics/AddAssignmentModal'
import { useToast } from '@/hooks/use-toast'

export default function AssignmentsPage() {
  const [searchTerm, setSearchTerm] = React.useState('')
  const [selectedClass, setSelectedClass] = React.useState('')
  const [selectedSubject, setSelectedSubject] = React.useState('')
  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false)
  const { toast } = useToast()

  const assignments: Assignment[] = [
    {
      id: 1,
      title: "Mathematics Problem Set 1",
      courseId: 1,
      courseName: "Mathematics Advanced",
      dueDate: "2024-11-20",
      totalMarks: 50,
      status: "upcoming",
      description: "Complete exercises from Chapter 3: Quadratic Equations",
      submissionCount: 0,
      class: "10th",
      subject: "Mathematics"
    },
    {
      id: 2,
      title: "English Essay Writing",
      courseId: 2,
      courseName: "English Literature",
      dueDate: "2024-11-18",
      totalMarks: 100,
      status: "ongoing",
      description: "Write a 1000-word essay on the theme of identity in The Great Gatsby",
      submissionCount: 15,
      class: "9th",
      subject: "English"
    },
    {
      id: 3,
      title: "Physics Lab Report",
      courseId: 3,
      courseName: "Physics Foundation",
      dueDate: "2024-11-15",
      totalMarks: 75,
      status: "completed",
      description: "Submit detailed lab report on the pendulum experiment",
      submissionCount: 38,
      class: "10th",
      subject: "Physics"
    }
  ]

  const filteredAssignments = assignments.filter(assignment => {
    const matchesSearch = 
      assignment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      assignment.courseName.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesClass = selectedClass ? assignment.class === selectedClass : true
    const matchesSubject = selectedSubject ? assignment.subject === selectedSubject : true
    return matchesSearch && matchesClass && matchesSubject
  })

  const handleViewSubmissions = (assignmentId: number) => {
    // Implement view submissions functionality
    console.log('View submissions for assignment:', assignmentId)
  }

  const handleDeleteAssignment = async (assignmentId: number) => {
    try {
      // Here you would make an API call to delete the assignment
      await new Promise(resolve => setTimeout(resolve, 1000))
      toast({
        title: "Success",
        description: "Assignment deleted successfully",
        variant: "success"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete assignment",
        variant: "destructive"
      })
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Assignments</h1>
        <p className="text-muted-foreground">
          Manage and track student assignments
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assignments</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assignments.length}</div>
            <p className="text-xs text-muted-foreground">
              {assignments.filter(a => a.status === 'upcoming').length} upcoming
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Due This Week</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {assignments.filter(a => 
                new Date(a.dueDate) <= new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
              ).length}
            </div>
            <p className="text-xs text-muted-foreground">
              Across all subjects
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {assignments.filter(a => a.status === 'completed').length}
            </div>
            <p className="text-xs text-muted-foreground">
              Total completed assignments
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Assignment List</CardTitle>
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search assignments..."
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
              <select
                value={selectedSubject}
                onChange={(e) => setSelectedSubject(e.target.value)}
                className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Subjects</option>
                <option value="Mathematics">Mathematics</option>
                <option value="English">English</option>
                <option value="Physics">Physics</option>
              </select>
              <Button 
                className="flex items-center gap-2"
                onClick={() => setIsAddModalOpen(true)}
              >
                <PlusCircle className="h-4 w-4" />
                Add Assignment
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-gray-50">
                <tr>
                  <th className="px-6 py-3">Title</th>
                  <th className="px-6 py-3">Course</th>
                  <th className="px-6 py-3">Class</th>
                  <th className="px-6 py-3">Due Date</th>
                  <th className="px-6 py-3">Total Marks</th>
                  <th className="px-6 py-3">Submissions</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredAssignments.map((assignment) => (
                  <tr key={assignment.id} className="bg-white border-b hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium">
                      {assignment.title}
                    </td>
                    <td className="px-6 py-4">{assignment.courseName}</td>
                    <td className="px-6 py-4">{assignment.class}</td>
                    <td className="px-6 py-4">
                      {new Date(assignment.dueDate).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">{assignment.totalMarks}</td>
                    <td className="px-6 py-4">{assignment.submissionCount || 0}</td>
                    <td className="px-6 py-4">
                      <span
                        className={cn(
                          "px-2 py-1 text-xs font-semibold rounded-full",
                          {
                            "bg-yellow-100 text-yellow-800": assignment.status === "upcoming",
                            "bg-blue-100 text-blue-800": assignment.status === "ongoing",
                            "bg-green-100 text-green-800": assignment.status === "completed"
                          }
                        )}
                      >
                        {assignment.status.charAt(0).toUpperCase() + assignment.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleViewSubmissions(assignment.id)}
                      >
                        View
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                        onClick={() => handleDeleteAssignment(assignment.id)}
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

      <AddAssignmentModal
        open={isAddModalOpen}
        onOpenChange={setIsAddModalOpen}
      />
    </div>
  )
}