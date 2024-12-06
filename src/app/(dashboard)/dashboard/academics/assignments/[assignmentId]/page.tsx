// src/app/(dashboard)/dashboard/academics/assignments/[assignmentId]/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  FileText, 
  Users, 
  Clock, 
  Download,
  Upload,
  CheckCircle,
  XCircle,
  Calendar,
  Edit,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useToast } from '@/hooks/use-toast'
import EditAssignmentModal from '@/components/academics/EditAssignmentModal'
import GradeSubmissionModal from '@/components/academics/GradeSubmissionModal'

interface Submission {
  id: number
  studentName: string
  studentId: string
  submittedAt: string
  status: 'submitted' | 'late' | 'graded'
  grade?: number
  feedback?: string
  attachments: string[]
}

export default function AssignmentDetailsPage({ 
  params 
}: { 
  params: { assignmentId: string } 
}) {
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
  const [isGradeModalOpen, setIsGradeModalOpen] = React.useState(false)
  const [selectedSubmission, setSelectedSubmission] = React.useState<Submission | null>(null)
  const { toast } = useToast()

  // This would typically come from an API
  const assignment = {
    id: parseInt(params.assignmentId),
    title: "Mathematics Problem Set 1",
    courseId: 1,
    courseName: "Mathematics Advanced",
    dueDate: "2024-11-20T23:59:59",
    totalMarks: 50,
    status: "ongoing" as const,
    description: "Complete exercises from Chapter 3: Quadratic Equations",
    instructions: "Show all your work. Partial credit will be given for correct working even if the final answer is wrong.",
    attachments: ["problem_set_1.pdf"],
    class: "10th",
    subject: "Mathematics",
    submissionCount: 15,
    totalStudents: 35
  }

  const submissions: Submission[] = [
    {
      id: 1,
      studentName: "John Doe",
      studentId: "10A001",
      submittedAt: "2024-11-18T14:30:00",
      status: "graded",
      grade: 45,
      feedback: "Excellent work! Clear working shown for all problems.",
      attachments: ["john_doe_submission.pdf"]
    },
    {
      id: 2,
      studentName: "Jane Smith",
      studentId: "10A002",
      submittedAt: "2024-11-19T09:15:00",
      status: "submitted",
      attachments: ["jane_smith_submission.pdf"]
    },
    {
      id: 3,
      studentName: "Mike Johnson",
      studentId: "10A003",
      submittedAt: "2024-11-20T23:59:59",
      status: "late",
      attachments: ["mike_johnson_submission.pdf"]
    }
  ]

  const handleDownload = (filename: string) => {
    // Implement download functionality
    toast({
      title: "Download Started",
      description: `Downloading ${filename}`,
      variant: "success"
    })
  }

  const handleGrade = (submission: Submission) => {
    setSelectedSubmission(submission)
    setIsGradeModalOpen(true)
  }

  const getStatusBadgeStyles = (status: Submission['status']) => {
    switch (status) {
      case 'submitted':
        return "bg-blue-100 text-blue-800"
      case 'late':
        return "bg-yellow-100 text-yellow-800"
      case 'graded':
        return "bg-green-100 text-green-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{assignment.title}</h1>
          <p className="text-muted-foreground">
            {assignment.courseName} | {assignment.class}
          </p>
        </div>
        <Button 
          variant="outline"
          className="flex items-center gap-2"
          onClick={() => setIsEditModalOpen(true)}
        >
          <Edit className="h-4 w-4" />
          Edit Assignment
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Due Date</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {new Date(assignment.dueDate).toLocaleDateString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {new Date(assignment.dueDate).toLocaleTimeString()}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Marks</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assignment.totalMarks}</div>
            <p className="text-xs text-muted-foreground">Maximum points</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Submissions</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {assignment.submissionCount}/{assignment.totalStudents}
            </div>
            <p className="text-xs text-muted-foreground">
              {((assignment.submissionCount / assignment.totalStudents) * 100).toFixed(1)}% submitted
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Time Remaining</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {new Date(assignment.dueDate) > new Date() 
                ? Math.ceil((new Date(assignment.dueDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
                : 0} days
            </div>
            <p className="text-xs text-muted-foreground">Until deadline</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose max-w-none">
                <p>{assignment.description}</p>
                {assignment.instructions && (
                  <>
                    <h4 className="text-lg font-semibold mt-4">Instructions</h4>
                    <p>{assignment.instructions}</p>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Submissions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {submissions.map((submission) => (
                  <div
                    key={submission.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">{submission.studentName}</p>
                      <p className="text-sm text-muted-foreground">
                        ID: {submission.studentId}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Submitted: {new Date(submission.submittedAt).toLocaleString()}
                      </p>
                    </div>

                    <div className="flex items-center gap-4">
                      {submission.grade !== undefined && (
                        <div className="text-right">
                          <p className="font-medium">{submission.grade}/{assignment.totalMarks}</p>
                          <p className="text-sm text-muted-foreground">
                            {((submission.grade / assignment.totalMarks) * 100).toFixed(1)}%
                          </p>
                        </div>
                      )}
                      <span
                        className={cn(
                          "px-2 py-1 text-xs font-semibold rounded-full",
                          getStatusBadgeStyles(submission.status)
                        )}
                      >
                        {submission.status.charAt(0).toUpperCase() + submission.status.slice(1)}
                      </span>
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDownload(submission.attachments[0])}
                        >
                          <Download className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleGrade(submission)}
                        >
                          Grade
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Resources</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {assignment.attachments.map((attachment, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <span>{attachment}</span>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDownload(attachment)}
                    >
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">On Time</span>
                  <span className="font-medium">
                    {submissions.filter(s => s.status === 'submitted' || s.status === 'graded').length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Late</span>
                  <span className="font-medium">
                    {submissions.filter(s => s.status === 'late').length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Graded</span>
                  <span className="font-medium">
                    {submissions.filter(s => s.status === 'graded').length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Average Score</span>
                  <span className="font-medium">
                    {submissions
                      .filter(s => s.grade !== undefined)
                      .reduce((acc, curr) => acc + (curr.grade || 0), 0) / 
                      submissions.filter(s => s.grade !== undefined).length || 0}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <EditAssignmentModal
        open={isEditModalOpen}
        onOpenChange={setIsEditModalOpen}
        assignment={assignment}
      />

      <GradeSubmissionModal
        open={isGradeModalOpen}
        onOpenChange={setIsGradeModalOpen}
        submission={selectedSubmission}
        totalMarks={assignment.totalMarks}
      />
    </div>
  )
}