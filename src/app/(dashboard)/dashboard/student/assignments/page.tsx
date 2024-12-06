// src/app/(dashboard)/dashboard/student/assignments/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  Clock, 
  Calendar,
  AlertCircle,
  Download,
  Upload,
  CheckCircle,
  XCircle,
  Filter
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useToast } from '@/hooks/use-toast'
import SubmitAssignmentModal from '@/components/academics/SubmitAssignmentModal'

interface Assignment {
  id: number
  title: string
  courseId: number
  courseName: string
  dueDate: string
  totalMarks: number
  status: 'pending' | 'submitted' | 'late' | 'graded'
  description: string
  attachments: string[]
  submittedAt?: string
  grade?: number
  feedback?: string
}

export default function StudentAssignmentsPage() {
  const [filter, setFilter] = React.useState<'all' | 'pending' | 'submitted' | 'graded'>('all')
  const [isSubmitModalOpen, setIsSubmitModalOpen] = React.useState(false)
  const [selectedAssignment, setSelectedAssignment] = React.useState<Assignment | null>(null)
  const { toast } = useToast()

  // This would typically come from an API
  const assignments: Assignment[] = [
    {
      id: 1,
      title: "Mathematics Problem Set 1",
      courseId: 1,
      courseName: "Mathematics Advanced",
      dueDate: "2024-11-20T23:59:59",
      totalMarks: 50,
      status: "pending",
      description: "Complete exercises from Chapter 3: Quadratic Equations",
      attachments: ["problem_set_1.pdf"]
    },
    {
      id: 2,
      title: "English Essay Writing",
      courseId: 2,
      courseName: "English Literature",
      dueDate: "2024-11-18T23:59:59",
      totalMarks: 100,
      status: "submitted",
      description: "Write a 1000-word essay on the theme of identity in The Great Gatsby",
      attachments: ["essay_guidelines.pdf"],
      submittedAt: "2024-11-17T14:30:00"
    },
    {
      id: 3,
      title: "Physics Lab Report",
      courseId: 3,
      courseName: "Physics Foundation",
      dueDate: "2024-11-15T23:59:59",
      totalMarks: 75,
      status: "graded",
      description: "Submit detailed lab report on the pendulum experiment",
      attachments: ["lab_report_template.pdf"],
      submittedAt: "2024-11-15T10:00:00",
      grade: 68,
      feedback: "Good analysis but need more detailed error calculations."
    }
  ]

  const filteredAssignments = assignments.filter(assignment => {
    if (filter === 'all') return true
    return assignment.status === filter
  })

  const handleDownload = (filename: string) => {
    toast({
      title: "Download Started",
      description: `Downloading ${filename}`,
      variant: "success"
    })
  }

  const handleSubmit = (assignment: Assignment) => {
    setSelectedAssignment(assignment)
    setIsSubmitModalOpen(true)
  }

  const getStatusBadge = (status: Assignment['status']) => {
    const styles = {
      pending: "bg-yellow-100 text-yellow-800",
      submitted: "bg-blue-100 text-blue-800",
      late: "bg-red-100 text-red-800",
      graded: "bg-green-100 text-green-800"
    }

    const icons = {
      pending: Clock,
      submitted: CheckCircle,
      late: AlertCircle,
      graded: CheckCircle
    }

    const Icon = icons[status]

    return (
      <span className={cn("flex items-center gap-1 px-2 py-1 text-xs font-semibold rounded-full", styles[status])}>
        <Icon className="h-3 w-3" />
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    )
  }

  const getDueStatus = (dueDate: string) => {
    const now = new Date()
    const due = new Date(dueDate)
    const diffDays = Math.ceil((due.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))

    if (diffDays < 0) {
      return <span className="text-red-600">Overdue</span>
    } else if (diffDays === 0) {
      return <span className="text-yellow-600">Due today</span>
    } else {
      return <span className="text-green-600">{diffDays} days left</span>
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">My Assignments</h1>
        <p className="text-muted-foreground">
          View and submit your assignments
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {assignments.filter(a => a.status === 'pending').length}
            </div>
            <p className="text-xs text-muted-foreground">
              Assignments to complete
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Submitted</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {assignments.filter(a => a.status === 'submitted' || a.status === 'graded').length}
            </div>
            <p className="text-xs text-muted-foreground">
              Total submissions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Grade</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(
                assignments
                  .filter(a => a.grade !== undefined)
                  .reduce((acc, curr) => acc + ((curr.grade || 0) / curr.totalMarks) * 100, 0) /
                assignments.filter(a => a.grade !== undefined).length
              )}%
            </div>
            <p className="text-xs text-muted-foreground">
              Across all graded assignments
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Assignment List</CardTitle>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as typeof filter)}
              className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Assignments</option>
              <option value="pending">Pending</option>
              <option value="submitted">Submitted</option>
              <option value="graded">Graded</option>
            </select>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredAssignments.map((assignment) => (
              <div
                key={assignment.id}
                className="border rounded-lg p-4 space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <h3 className="font-medium">{assignment.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {assignment.courseName}
                    </p>
                  </div>
                  {getStatusBadge(assignment.status)}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Due Date</p>
                    <p className="font-medium">
                      {new Date(assignment.dueDate).toLocaleDateString()}{' '}
                      {new Date(assignment.dueDate).toLocaleTimeString()}
                    </p>
                    <p className="text-sm mt-1">
                      {getDueStatus(assignment.dueDate)}
                    </p>
                  </div>

                  <div>
                    <p className="text-sm text-muted-foreground">Total Marks</p>
                    <p className="font-medium">{assignment.totalMarks}</p>
                    {assignment.grade !== undefined && (
                      <p className="text-sm mt-1">
                        Your grade: <span className="font-medium">{assignment.grade}</span>
                        {' '}({((assignment.grade / assignment.totalMarks) * 100).toFixed(1)}%)
                      </p>
                    )}
                  </div>
                </div>

                {assignment.description && (
                  <div>
                    <p className="text-sm text-muted-foreground">Description</p>
                    <p className="text-sm mt-1">{assignment.description}</p>
                  </div>
                )}

                {assignment.feedback && (
                  <div className="bg-blue-50 p-3 rounded-md">
                    <p className="text-sm font-medium text-blue-900">Teacher's Feedback</p>
                    <p className="text-sm text-blue-800 mt-1">{assignment.feedback}</p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2">
                    {assignment.attachments.map((file, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => handleDownload(file)}
                        className="flex items-center gap-2"
                      >
                        <Download className="h-4 w-4" />
                        Download
                      </Button>
                    ))}
                  </div>

                  {assignment.status === 'pending' && (
                    <Button
                      onClick={() => handleSubmit(assignment)}
                      className="flex items-center gap-2"
                    >
                      <Upload className="h-4 w-4" />
                      Submit Assignment
                    </Button>
                  )}

                  {assignment.submittedAt && (
                    <p className="text-sm text-muted-foreground">
                      Submitted: {new Date(assignment.submittedAt).toLocaleString()}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <SubmitAssignmentModal
        open={isSubmitModalOpen}
        onOpenChange={setIsSubmitModalOpen}
        assignment={selectedAssignment}
      />
    </div>
  )
}