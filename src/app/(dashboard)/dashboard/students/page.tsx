// src/app/(dashboard)/dashboard/students/page.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { UserPlus, Search } from 'lucide-react'
import AddStudentModal from '@/components/students/AddStudentModal'

interface Student {
  id: number
  name: string
  class: string
  rollNo: string
  gender: string
  contact: string
  status: string
}

export default function StudentsPage() {
  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false)
  const [searchTerm, setSearchTerm] = React.useState('')
  const [selectedClass, setSelectedClass] = React.useState('')

  const students: Student[] = [
    {
      id: 1,
      name: "Alex Johnson",
      class: "10th A",
      rollNo: "101",
      gender: "Male",
      contact: "+91 9876543210",
      status: "Active"
    },
    {
      id: 2,
      name: "Sarah Williams",
      class: "9th B",
      rollNo: "102",
      gender: "Female",
      contact: "+91 9876543211",
      status: "Active"
    },
    {
      id: 3,
      name: "Michael Brown",
      class: "10th A",
      rollNo: "103",
      gender: "Male",
      contact: "+91 9876543212",
      status: "Active"
    },
    {
      id: 4,
      name: "Emily Davis",
      class: "8th C",
      rollNo: "104",
      gender: "Female",
      contact: "+91 9876543213",
      status: "Active"
    }
  ]

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value)
  }

  const handleClassChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedClass(event.target.value)
  }

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.rollNo.includes(searchTerm)
    const matchesClass = selectedClass ? student.class.includes(selectedClass) : true
    return matchesSearch && matchesClass
  })

  const handleEdit = (studentId: number) => {
    console.log('Edit student:', studentId)
    // Implement edit functionality
  }

  const handleDelete = (studentId: number) => {
    console.log('Delete student:', studentId)
    // Implement delete functionality
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Students</h1>
          <p className="text-muted-foreground">Manage your student records</p>
        </div>
        <Button 
          className="flex items-center gap-2"
          onClick={() => setIsAddModalOpen(true)}
        >
          <UserPlus className="h-4 w-4" />
          Add New Student
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Student List</CardTitle>
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search students..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  className="pl-8 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <select 
                className="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={selectedClass}
                onChange={handleClassChange}
              >
                <option value="">All Classes</option>
                <option value="10th">10th</option>
                <option value="9th">9th</option>
                <option value="8th">8th</option>
              </select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-gray-50">
                <tr>
                  <th className="px-6 py-3">Roll No</th>
                  <th className="px-6 py-3">Name</th>
                  <th className="px-6 py-3">Class</th>
                  <th className="px-6 py-3">Gender</th>
                  <th className="px-6 py-3">Contact</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="bg-white border-b hover:bg-gray-50">
                    <td className="px-6 py-4">{student.rollNo}</td>
                    <td className="px-6 py-4 font-medium">{student.name}</td>
                    <td className="px-6 py-4">{student.class}</td>
                    <td className="px-6 py-4">{student.gender}</td>
                    <td className="px-6 py-4">{student.contact}</td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                        {student.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => handleEdit(student.id)}
                      >
                        Edit
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-red-600 hover:text-red-700"
                        onClick={() => handleDelete(student.id)}
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

      <AddStudentModal 
        open={isAddModalOpen} 
        onOpenChange={setIsAddModalOpen} 
      />
    </div>
  )
}