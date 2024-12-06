// src/components/finance/FinanceOverview.tsx
'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  PlusCircle, 
  Search, 
  IndianRupee,
  CreditCard,
  Receipt,
  Download,
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import { cn } from '@/lib/utils'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'

interface FeeRecord {
  id: number
  studentName: string
  studentId: string
  class: string
  feeType: string
  amount: number
  dueDate: string
  status: 'paid' | 'pending' | 'overdue'
  paymentDate?: string
  paymentMethod?: string
  transactionId?: string
}

interface FeeType {
  id: number
  name: string
  amount: number
  frequency: 'monthly' | 'quarterly' | 'annually'
  description?: string
}

interface FormData {
  studentName: string
  studentId: string
  class: string
  feeType: string
  amount: number
  dueDate: string
}

const INITIAL_FEE_RECORDS: FeeRecord[] = [
  {
    id: 1,
    studentName: "John Doe",
    studentId: "STU001",
    class: "10th A",
    feeType: "Tuition Fee",
    amount: 15000,
    dueDate: "2024-01-15",
    status: "paid",
    paymentDate: "2024-01-10",
    paymentMethod: "Online",
    transactionId: "TXN123456"
  },
  {
    id: 2,
    studentName: "Jane Smith",
    studentId: "STU002",
    class: "9th B",
    feeType: "Tuition Fee",
    amount: 15000,
    dueDate: "2024-01-15",
    status: "pending"
  },
  {
    id: 3,
    studentName: "Mike Johnson",
    studentId: "STU003",
    class: "10th A",
    feeType: "Transport Fee",
    amount: 5000,
    dueDate: "2024-01-10",
    status: "overdue"
  },
  {
    id: 4,
    studentName: "Sarah Williams",
    studentId: "STU004",
    class: "8th C",
    feeType: "Library Fee",
    amount: 2000,
    dueDate: "2024-01-20",
    status: "paid",
    paymentDate: "2024-01-05",
    paymentMethod: "Cash",
    transactionId: "TXN123457"
  }
]

const FEE_TYPES: FeeType[] = [
  {
    id: 1,
    name: "Tuition Fee",
    amount: 15000,
    frequency: "monthly",
    description: "Regular monthly tuition fee"
  },
  {
    id: 2,
    name: "Transport Fee",
    amount: 5000,
    frequency: "monthly",
    description: "School bus service fee"
  },
  {
    id: 3,
    name: "Library Fee",
    amount: 2000,
    frequency: "annually",
    description: "Annual library membership fee"
  },
  {
    id: 4,
    name: "Laboratory Fee",
    amount: 3000,
    frequency: "quarterly",
    description: "Science lab usage fee"
  }
]

const INITIAL_FORM_DATA: FormData = {
  studentName: '',
  studentId: '',
  class: '',
  feeType: '',
  amount: 0,
  dueDate: new Date().toISOString().split('T')[0]
}

export default function FinanceOverview() {
  const [searchTerm, setSearchTerm] = React.useState('')
  const [selectedClass, setSelectedClass] = React.useState('')
  const [selectedStatus, setSelectedStatus] = React.useState('')
  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false)
  const [feeRecords, setFeeRecords] = React.useState<FeeRecord[]>(INITIAL_FEE_RECORDS)
  const [formData, setFormData] = React.useState<FormData>(INITIAL_FORM_DATA)
  const { toast } = useToast()

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) || 0 : value
    }))
  }

  const handleAddFeeRecord = async () => {
    if (!formData.studentName || !formData.studentId || !formData.class || !formData.feeType || !formData.amount || !formData.dueDate) {
      toast({
        title: "Error",
        description: "Please fill in all required fields",
        variant: "destructive"
      })
      return
    }

    try {
      const newRecord: FeeRecord = {
        id: Date.now(),
        ...formData,
        status: 'pending'
      }

      setFeeRecords(prev => [...prev, newRecord])
      setIsAddModalOpen(false)
      setFormData(INITIAL_FORM_DATA)

      toast({
        title: "Success",
        description: "Fee record added successfully"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add fee record",
        variant: "destructive"
      })
    }
  }

  const handlePaymentCollection = async (recordId: number) => {
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      setFeeRecords(prev => prev.map(record => 
        record.id === recordId
          ? { 
              ...record, 
              status: 'paid',
              paymentDate: new Date().toISOString().split('T')[0],
              paymentMethod: 'Online',
              transactionId: `TXN${Date.now()}`
            }
          : record
      ))

      toast({
        title: "Success",
        description: "Payment collected successfully"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to collect payment",
        variant: "destructive"
      })
    }
  }

  const handleGenerateReceipt = async (recordId: number) => {
    try {
      const record = feeRecords.find(r => r.id === recordId)
      if (!record) return

      const receiptContent = `
Receipt
-------
Student: ${record.studentName}
ID: ${record.studentId}
Amount: ₹${record.amount}
Date: ${record.paymentDate}
Transaction: ${record.transactionId}
`
      const blob = new Blob([receiptContent], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `receipt_${record.studentId}.txt`
      document.body.appendChild(a)
      a.click()
      URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast({
        title: "Success",
        description: "Receipt downloaded successfully"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate receipt",
        variant: "destructive"
      })
    }
  }

  const handleExportReport = async () => {
    try {
      const stats = calculateStats()
      const report = `
Financial Report
---------------
Total Collected: ₹${stats.totalCollected}
Pending Amount: ₹${stats.pendingAmount}
Overdue Payments: ${stats.overdueCount}
`
      const blob = new Blob([report], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'financial_report.txt'
      document.body.appendChild(a)
      a.click()
      URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast({
        title: "Success",
        description: "Financial report downloaded successfully"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate report",
        variant: "destructive"
      })
    }
  }

  const filteredRecords = feeRecords.filter(record => {
    const matchesSearch = 
      record.studentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.studentId.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesClass = selectedClass ? record.class === selectedClass : true
    const matchesStatus = selectedStatus ? record.status === selectedStatus : true
    return matchesSearch && matchesClass && matchesStatus
  })

  const calculateStats = () => ({
    totalCollected: feeRecords
      .filter(r => r.status === 'paid')
      .reduce((acc, curr) => acc + curr.amount, 0),
    pendingAmount: feeRecords
      .filter(r => r.status === 'pending' || r.status === 'overdue')
      .reduce((acc, curr) => acc + curr.amount, 0),
    overdueCount: feeRecords.filter(r => r.status === 'overdue').length
  })

  const stats = calculateStats()

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Finance</h1>
          <p className="text-muted-foreground">
            Manage fee collection and financial records
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            className="flex items-center gap-2"
            onClick={handleExportReport}
          >
            <Download className="h-4 w-4" />
            Export Report
          </Button>
          <Button
            className="flex items-center gap-2"
            onClick={() => setIsAddModalOpen(true)}
          >
            <PlusCircle className="h-4 w-4" />
            Add Fee Record
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Collected</CardTitle>
            <IndianRupee className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{stats.totalCollected.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              From {feeRecords.filter(r => r.status === 'paid').length} payments
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Amount</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">
              ₹{stats.pendingAmount.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              From {feeRecords.filter(r => r.status === 'pending').length} pending payments
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overdue Payments</CardTitle>
            <Receipt className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.overdueCount}</div>
            <p className="text-xs text-muted-foreground">
              Requiring immediate attention
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <CardTitle>Fee Records</CardTitle>
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search records..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8"
                />
              </div>
              <select
                value={selectedClass}
                onChange={(e) => setSelectedClass(e.target.value)}
                className="px-4 py-2 border rounded-md"
              >
                <option value="">All Classes</option>
                <option value="10th A">10th A</option>
                <option value="9th B">9th B</option>
                <option value="8th C">8th C</option>
              </select>
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-2 border rounded-md"
              >
                <option value="">All Status</option>
                <option value="paid">Paid</option>
                <option value="pending">Pending</option>
                <option value="overdue">Overdue</option>
              </select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-gray-50">
                <tr>
                  <th className="px-6 py-3">Student ID</th>
                  <th className="px-6 py-3">Name</th>
                  <th className="px-6 py-3">Class</th>
                  <th className="px-6 py-3">Fee Type</th>
                  <th className="px-6 py-3">Amount</th>
                  <th className="px-6 py-3">Due Date</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredRecords.map((record) => (
                  <tr key={record.id} className="bg-white border-b hover:bg-gray-50">
                    <td className="px-6 py-4">{record.studentId}</td>
                    <td className="px-6 py-4 font-medium">{record.studentName}</td>
                    <td className="px-6 py-4">{record.class}</td>
                    <td className="px-6 py-4">{record.feeType}</td>
                    <td className="px-6 py-4">₹{record.amount.toLocaleString()}</td>
                    <td className="px-6 py-4">
                      {new Date(record.dueDate).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={cn(
                          "px-2 py-1 text-xs font-semibold rounded-full",
                          {
                            "bg-green-100 text-green-800": record.status === "paid",
                            "bg-yellow-100 text-yellow-800": record.status === "pending",
                            "bg-red-100 text-red-800": record.status === "overdue"
                          }
                        )}
                      >
                        {record.status.charAt(0).toUpperCase() + record.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        {record.status !== 'paid' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handlePaymentCollection(record.id)}
                          >
                            Collect
                          </Button>
                        )}
                        {record.status === 'paid' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleGenerateReceipt(record.id)}
                          >
                            Receipt
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredRecords.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              No fee records found matching the search criteria
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Fee Structure</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-gray-50">
                <tr>
                  <th className="px-6 py-3">Fee Type</th>
                  <th className="px-6 py-3">Amount</th>
                  <th className="px-6 py-3">Frequency</th>
                  <th className="px-6 py-3">Description</th>
                </tr>
              </thead>
              <tbody>
                {FEE_TYPES.map((feeType) => (
                  <tr key={feeType.id} className="bg-white border-b hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium">{feeType.name}</td>
                    <td className="px-6 py-4">₹{feeType.amount.toLocaleString()}</td>
                    <td className="px-6 py-4">
                      {feeType.frequency.charAt(0).toUpperCase() + feeType.frequency.slice(1)}
                    </td>
                    <td className="px-6 py-4">{feeType.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <Dialog open={isAddModalOpen} onOpenChange={setIsAddModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Fee Record</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="studentId">Student ID</Label>
              <Input
                id="studentId"
                name="studentId"
                placeholder="Enter student ID"
                value={formData.studentId}
                onChange={handleInputChange}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="studentName">Student Name</Label>
              <Input
                id="studentName"
                name="studentName"
                placeholder="Enter student name"
                value={formData.studentName}
                onChange={handleInputChange}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="class">Class</Label>
              <select
                id="class"
                name="class"
                className="px-3 py-2 border rounded-md"
                value={formData.class}
                onChange={handleInputChange}
              >
                <option value="">Select Class</option>
                <option value="10th A">10th A</option>
                <option value="9th B">9th B</option>
                <option value="8th C">8th C</option>
              </select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="feeType">Fee Type</Label>
              <select
                id="feeType"
                name="feeType"
                className="px-3 py-2 border rounded-md"
                value={formData.feeType}
                onChange={handleInputChange}
              >
                <option value="">Select Fee Type</option>
                {FEE_TYPES.map(type => (
                  <option key={type.id} value={type.name}>{type.name}</option>
                ))}
              </select>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                name="amount"
                type="number"
                placeholder="Enter amount"
                value={formData.amount}
                onChange={handleInputChange}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="dueDate">Due Date</Label>
              <Input
                id="dueDate"
                name="dueDate"
                type="date"
                value={formData.dueDate}
                onChange={handleInputChange}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddModalOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAddFeeRecord}>Add Record</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}