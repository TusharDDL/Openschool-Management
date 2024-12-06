// src/components/transport/Maintenance.tsx

'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useTransport } from '@/contexts/TransportContext'
import { 
  Tool, // Changed from 'Tools' to 'Tool'
  AlertTriangle, 
  Calendar,
  Plus,
  IndianRupee
} from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { useForm } from 'react-hook-form'
import { format } from 'date-fns'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'react-toastify'
import { MaintenanceRecord, Vehicle } from '@/types/transport'

interface MaintenanceFormData {
  type: 'regular' | 'repair' | 'emergency'
  description: string
  cost: number
  nextDueDate: string
  notes?: string
  servicedBy?: string
  partsReplaced?: string
}

export default function Maintenance() {
  const { vehicles, addMaintenanceRecord } = useTransport()
  const [selectedVehicle, setSelectedVehicle] = React.useState<string>('')
  const [isAddOpen, setIsAddOpen] = React.useState(false)
  const { register, handleSubmit, reset, formState: { errors } } = useForm<MaintenanceFormData>()

  const upcomingMaintenance = vehicles
    .filter(v => v.nextMaintenance && new Date(v.nextMaintenance) > new Date())
    .sort((a, b) => new Date(a.nextMaintenance!).getTime() - new Date(b.nextMaintenance!).getTime())

  const overdueMaintenance = vehicles
    .filter(v => v.nextMaintenance && new Date(v.nextMaintenance) <= new Date())

  const maintenanceHistory = vehicles
    .flatMap(v => (v.maintenanceHistory || [])
      .map(m => ({ ...m, vehicleNumber: v.number })))
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())

  const onSubmit = (data: MaintenanceFormData) => {
    if (!selectedVehicle) {
      toast.error('Please select a vehicle.')
      return
    }

    const newRecord: MaintenanceRecord = {
      id: Math.random().toString(36).substr(2, 9),
      vehicleId: selectedVehicle,
      type: data.type,
      description: data.description,
      cost: data.cost,
      date: new Date().toISOString(),
      status: 'completed'
    }

    addMaintenanceRecord(newRecord)
    setIsAddOpen(false)
    reset()
    toast.success('Maintenance record added successfully')
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Due This Week</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {upcomingMaintenance.filter(v => 
                new Date(v.nextMaintenance!).getTime() - new Date().getTime() <= 7 * 24 * 60 * 60 * 1000
              ).length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overdue</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {overdueMaintenance.length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">This Month's Cost</CardTitle>
            <IndianRupee className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ₹{maintenanceHistory
                .filter(m => new Date(m.date).getMonth() === new Date().getMonth())
                .reduce((acc, curr) => acc + curr.cost, 0)
                .toLocaleString()}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Services</CardTitle>
            <Tool className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {vehicles.filter(v => v.status === 'maintenance').length}
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="upcoming" className="space-y-4">
        <TabsList>
          <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
          <TabsTrigger value="overdue">Overdue</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Upcoming Maintenance</CardTitle>
                <Button onClick={() => setIsAddOpen(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  Schedule Maintenance
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {upcomingMaintenance.map(vehicle => (
                  <div key={vehicle.id} className="flex items-center justify-between border-b pb-4">
                    <div>
                      <h3 className="font-semibold">{vehicle.number}</h3>
                      <p className="text-sm text-muted-foreground">Due: {format(new Date(vehicle.nextMaintenance!), 'PP')}</p>
                    </div>
                    <Button variant="outline" size="sm">Mark Complete</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="overdue">
          <Card>
            <CardHeader>
              <CardTitle>Overdue Maintenance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {overdueMaintenance.map(vehicle => (
                  <div key={vehicle.id} className="flex items-center justify-between border-b pb-4 text-red-600">
                    <div>
                      <h3 className="font-semibold">{vehicle.number}</h3>
                      <p className="text-sm">Overdue since: {format(new Date(vehicle.nextMaintenance!), 'PP')}</p>
                    </div>
                    <Button variant="destructive" size="sm">Schedule Now</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>Maintenance History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead>
                    <tr className="bg-muted">
                      <th className="p-4">Date</th>
                      <th className="p-4">Vehicle</th>
                      <th className="p-4">Type</th>
                      <th className="p-4">Cost</th>
                      <th className="p-4">Description</th>
                      <th className="p-4">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {maintenanceHistory.map(record => (
                      <tr key={record.id} className="border-b">
                        <td className="p-4">{format(new Date(record.date), 'PP')}</td>
                        <td className="p-4">{record.vehicleNumber}</td>
                        <td className="p-4">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            record.type === 'emergency' 
                              ? 'bg-red-100 text-red-800'
                              : record.type === 'repair'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-green-100 text-green-800'
                          }`}>
                            {record.type.charAt(0).toUpperCase() + record.type.slice(1)}
                          </span>
                        </td>
                        <td className="p-4">₹{record.cost.toLocaleString()}</td>
                        <td className="p-4">{record.description}</td>
                        <td className="p-4">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            record.status === 'completed'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-blue-100 text-blue-800'
                          }`}>
                            {record.status.charAt(0).toUpperCase() + record.status.slice(1)}
                          </span>
                        </td>
                      </tr>
                    ))}
                    {maintenanceHistory.length === 0 && (
                      <tr>
                        <td className="p-4 text-center" colSpan={6}>
                          No maintenance history found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Add Maintenance Dialog */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Schedule Maintenance</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(onSubmit)} className="grid gap-4">
            <div className="space-y-2">
              <Label htmlFor="vehicleId">Vehicle*</Label>
              <Select
                value={selectedVehicle}
                onValueChange={setSelectedVehicle}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select vehicle" />
                </SelectTrigger>
                <SelectContent>
                  {vehicles.map(vehicle => (
                    <SelectItem key={vehicle.id} value={vehicle.id}>
                      {vehicle.number}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {!selectedVehicle && (
                <p className="text-red-600 text-xs mt-1">Vehicle is required</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="type">Maintenance Type*</Label>
              <Select
                {...register('type', { required: 'Maintenance type is required' })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="regular">Regular</SelectItem>
                  <SelectItem value="repair">Repair</SelectItem>
                  <SelectItem value="emergency">Emergency</SelectItem>
                </SelectContent>
              </Select>
              {errors.type && (
                <p className="text-red-600 text-xs mt-1">{errors.type.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description*</Label>
              <Input
                {...register('description', { required: 'Description is required' })}
                placeholder="Maintenance details"
              />
              {errors.description && (
                <p className="text-red-600 text-xs mt-1">{errors.description.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="cost">Estimated Cost*</Label>
              <Input
                type="number"
                {...register('cost', { required: 'Cost is required', min: { value: 0, message: 'Cost cannot be negative' } })}
                placeholder="Enter cost"
              />
              {errors.cost && (
                <p className="text-red-600 text-xs mt-1">{errors.cost.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="nextDueDate">Next Due Date*</Label>
              <Input
                type="date"
                {...register('nextDueDate', { required: 'Next due date is required' })}
              />
              {errors.nextDueDate && (
                <p className="text-red-600 text-xs mt-1">{errors.nextDueDate.message}</p>
              )}
            </div>

            {/* Optional Fields */}
            <div className="space-y-2">
              <Label htmlFor="servicedBy">Serviced By</Label>
              <Input
                {...register('servicedBy')}
                placeholder="Name of the service provider"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="partsReplaced">Parts Replaced</Label>
              <Input
                {...register('partsReplaced')}
                placeholder="List of parts replaced"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="notes">Notes</Label>
              <Input
                {...register('notes')}
                placeholder="Additional notes"
              />
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsAddOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Schedule</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
