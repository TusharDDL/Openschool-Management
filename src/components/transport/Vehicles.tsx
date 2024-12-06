// src/components/transport/Vehicles.tsx

'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { useTransport } from '@/contexts/TransportContext'
import { Edit, Trash, PlusCircle } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { toast } from 'react-toastify'
import { Vehicle } from '@/types/transport'

interface VehicleFormData {
  number: string
  capacity: number
  driver: string
  driverPhone: string
  route: string
  status: 'active' | 'maintenance' | 'inactive'
  insuranceExpiry?: string
  pollutionExpiry?: string
  fuelEfficiency?: number
  driverLicense?: string
  driverLicenseExpiry?: string
  manufactureYear?: string
  model?: string
  engineNumber?: string
  chassisNumber?: string
}

export default function Vehicles() {
  const { vehicles, addVehicle, updateVehicle, deleteVehicle } = useTransport()
  const [isAddOpen, setIsAddOpen] = useState(false)
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [selectedVehicle, setSelectedVehicle] = useState<string | null>(null)

  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm<VehicleFormData>()

  const onAdd = (data: VehicleFormData) => {
    addVehicle({
      id: Math.random().toString(36).substr(2, 9),
      number: data.number,
      capacity: data.capacity,
      driver: data.driver,
      driverPhone: data.driverPhone,
      route: data.route,
      status: data.status,
      insuranceExpiry: data.insuranceExpiry,
      pollutionExpiry: data.pollutionExpiry,
      fuelEfficiency: data.fuelEfficiency,
      driverLicense: data.driverLicense,
      driverLicenseExpiry: data.driverLicenseExpiry,
      manufactureYear: data.manufactureYear,
      model: data.model,
      engineNumber: data.engineNumber,
      chassisNumber: data.chassisNumber,
      maintenanceHistory: [],
    })

    toast.success('Vehicle added successfully')
    setIsAddOpen(false)
    reset()
  }

  const onEdit = (data: VehicleFormData) => {
    if (!selectedVehicle) return

    updateVehicle(data.number, {
      capacity: data.capacity,
      driver: data.driver,
      driverPhone: data.driverPhone,
      route: data.route,
      status: data.status,
      insuranceExpiry: data.insuranceExpiry,
      pollutionExpiry: data.pollutionExpiry,
      fuelEfficiency: data.fuelEfficiency,
      driverLicense: data.driverLicense,
      driverLicenseExpiry: data.driverLicenseExpiry,
      manufactureYear: data.manufactureYear,
      model: data.model,
      engineNumber: data.engineNumber,
      chassisNumber: data.chassisNumber,
    })

    toast.success('Vehicle updated successfully')
    setIsEditOpen(false)
    setSelectedVehicle(null)
    reset()
  }

  const handleEditClick = (vehicle: Vehicle) => {
    setSelectedVehicle(vehicle.id)
    setIsEditOpen(true)
    setValue('number', vehicle.number)
    setValue('capacity', vehicle.capacity)
    setValue('driver', vehicle.driver)
    setValue('driverPhone', vehicle.driverPhone)
    setValue('route', vehicle.route)
    setValue('status', vehicle.status)
    setValue('insuranceExpiry', vehicle.insuranceExpiry || '')
    setValue('pollutionExpiry', vehicle.pollutionExpiry || '')
    setValue('fuelEfficiency', vehicle.fuelEfficiency || 0)
    setValue('driverLicense', vehicle.driverLicense || '')
    setValue('driverLicenseExpiry', vehicle.driverLicenseExpiry || '')
    setValue('manufactureYear', vehicle.manufactureYear || '')
    setValue('model', vehicle.model || '')
    setValue('engineNumber', vehicle.engineNumber || '')
    setValue('chassisNumber', vehicle.chassisNumber || '')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Vehicle Management</h1>
        <Button onClick={() => setIsAddOpen(true)} className="flex items-center gap-2">
          <PlusCircle className="h-4 w-4" />
          Add Vehicle
        </Button>
      </div>

      {/* Vehicles Table */}
      <Card>
        <CardHeader>
          <CardTitle>Vehicles</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Number
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Driver
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Route
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {vehicles.map((vehicle) => (
                  <tr key={vehicle.id}>
                    <td className="px-6 py-4 whitespace-nowrap">{vehicle.number}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{vehicle.driver}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{vehicle.route}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          vehicle.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : vehicle.status === 'maintenance'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {vehicle.status.charAt(0).toUpperCase() + vehicle.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditClick(vehicle)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => deleteVehicle(vehicle.id)}
                        >
                          <Trash className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
                {vehicles.length === 0 && (
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-center" colSpan={5}>
                      No vehicles found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Add Vehicle Dialog */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Vehicle</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(onAdd)} className="grid gap-4">
            <div>
              <Label htmlFor="number">Number*</Label>
              <Input
                id="number"
                {...register('number', { required: 'Vehicle number is required' })}
                placeholder="Enter vehicle number"
              />
              {errors.number && (
                <p className="text-red-600 text-xs mt-1">{errors.number.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="capacity">Capacity*</Label>
              <Input
                id="capacity"
                type="number"
                {...register('capacity', { required: 'Capacity is required', min: { value: 1, message: 'Capacity must be at least 1' } })}
                placeholder="Enter capacity"
              />
              {errors.capacity && (
                <p className="text-red-600 text-xs mt-1">{errors.capacity.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="driver">Driver*</Label>
              <Input
                id="driver"
                {...register('driver', { required: 'Driver name is required' })}
                placeholder="Enter driver name"
              />
              {errors.driver && (
                <p className="text-red-600 text-xs mt-1">{errors.driver.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="driverPhone">Driver Phone*</Label>
              <Input
                id="driverPhone"
                type="tel"
                {...register('driverPhone', { required: 'Driver phone is required' })}
                placeholder="Enter driver phone number"
              />
              {errors.driverPhone && (
                <p className="text-red-600 text-xs mt-1">{errors.driverPhone.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="route">Route*</Label>
              <Input
                id="route"
                {...register('route', { required: 'Route is required' })}
                placeholder="Enter route name"
              />
              {errors.route && (
                <p className="text-red-600 text-xs mt-1">{errors.route.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="status">Status*</Label>
              <select
                id="status"
                {...register('status', { required: 'Status is required' })}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="active">Active</option>
                <option value="maintenance">Maintenance</option>
                <option value="inactive">Inactive</option>
              </select>
              {errors.status && (
                <p className="text-red-600 text-xs mt-1">{errors.status.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="insuranceExpiry">Insurance Expiry</Label>
              <Input
                id="insuranceExpiry"
                type="date"
                {...register('insuranceExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="pollutionExpiry">Pollution Expiry</Label>
              <Input
                id="pollutionExpiry"
                type="date"
                {...register('pollutionExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="fuelEfficiency">Fuel Efficiency (km/l)</Label>
              <Input
                id="fuelEfficiency"
                type="number"
                step="0.1"
                {...register('fuelEfficiency')}
                placeholder="Enter fuel efficiency"
              />
            </div>
            <div>
              <Label htmlFor="driverLicense">Driver License</Label>
              <Input
                id="driverLicense"
                {...register('driverLicense')}
                placeholder="Enter driver license number"
              />
            </div>
            <div>
              <Label htmlFor="driverLicenseExpiry">Driver License Expiry</Label>
              <Input
                id="driverLicenseExpiry"
                type="date"
                {...register('driverLicenseExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="manufactureYear">Manufacture Year</Label>
              <Input
                id="manufactureYear"
                type="number"
                {...register('manufactureYear')}
                placeholder="Enter manufacture year"
              />
            </div>
            <div>
              <Label htmlFor="model">Model</Label>
              <Input
                id="model"
                {...register('model')}
                placeholder="Enter vehicle model"
              />
            </div>
            <div>
              <Label htmlFor="engineNumber">Engine Number</Label>
              <Input
                id="engineNumber"
                {...register('engineNumber')}
                placeholder="Enter engine number"
              />
            </div>
            <div>
              <Label htmlFor="chassisNumber">Chassis Number</Label>
              <Input
                id="chassisNumber"
                {...register('chassisNumber')}
                placeholder="Enter chassis number"
              />
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsAddOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Add Vehicle</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Edit Vehicle Dialog */}
      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Vehicle</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(onEdit)} className="grid gap-4">
            <div>
              <Label htmlFor="number">Number*</Label>
              <Input
                id="number"
                {...register('number', { required: 'Vehicle number is required' })}
                placeholder="Enter vehicle number"
              />
              {errors.number && (
                <p className="text-red-600 text-xs mt-1">{errors.number.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="capacity">Capacity*</Label>
              <Input
                id="capacity"
                type="number"
                {...register('capacity', { required: 'Capacity is required', min: { value: 1, message: 'Capacity must be at least 1' } })}
                placeholder="Enter capacity"
              />
              {errors.capacity && (
                <p className="text-red-600 text-xs mt-1">{errors.capacity.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="driver">Driver*</Label>
              <Input
                id="driver"
                {...register('driver', { required: 'Driver name is required' })}
                placeholder="Enter driver name"
              />
              {errors.driver && (
                <p className="text-red-600 text-xs mt-1">{errors.driver.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="driverPhone">Driver Phone*</Label>
              <Input
                id="driverPhone"
                type="tel"
                {...register('driverPhone', { required: 'Driver phone is required' })}
                placeholder="Enter driver phone number"
              />
              {errors.driverPhone && (
                <p className="text-red-600 text-xs mt-1">{errors.driverPhone.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="route">Route*</Label>
              <Input
                id="route"
                {...register('route', { required: 'Route is required' })}
                placeholder="Enter route name"
              />
              {errors.route && (
                <p className="text-red-600 text-xs mt-1">{errors.route.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="status">Status*</Label>
              <select
                id="status"
                {...register('status', { required: 'Status is required' })}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="active">Active</option>
                <option value="maintenance">Maintenance</option>
                <option value="inactive">Inactive</option>
              </select>
              {errors.status && (
                <p className="text-red-600 text-xs mt-1">{errors.status.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="insuranceExpiry">Insurance Expiry</Label>
              <Input
                id="insuranceExpiry"
                type="date"
                {...register('insuranceExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="pollutionExpiry">Pollution Expiry</Label>
              <Input
                id="pollutionExpiry"
                type="date"
                {...register('pollutionExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="fuelEfficiency">Fuel Efficiency (km/l)</Label>
              <Input
                id="fuelEfficiency"
                type="number"
                step="0.1"
                {...register('fuelEfficiency')}
                placeholder="Enter fuel efficiency"
              />
            </div>
            <div>
              <Label htmlFor="driverLicense">Driver License</Label>
              <Input
                id="driverLicense"
                {...register('driverLicense')}
                placeholder="Enter driver license number"
              />
            </div>
            <div>
              <Label htmlFor="driverLicenseExpiry">Driver License Expiry</Label>
              <Input
                id="driverLicenseExpiry"
                type="date"
                {...register('driverLicenseExpiry')}
              />
            </div>
            <div>
              <Label htmlFor="manufactureYear">Manufacture Year</Label>
              <Input
                id="manufactureYear"
                type="number"
                {...register('manufactureYear')}
                placeholder="Enter manufacture year"
              />
            </div>
            <div>
              <Label htmlFor="model">Model</Label>
              <Input
                id="model"
                {...register('model')}
                placeholder="Enter vehicle model"
              />
            </div>
            <div>
              <Label htmlFor="engineNumber">Engine Number</Label>
              <Input
                id="engineNumber"
                {...register('engineNumber')}
                placeholder="Enter engine number"
              />
            </div>
            <div>
              <Label htmlFor="chassisNumber">Chassis Number</Label>
              <Input
                id="chassisNumber"
                {...register('chassisNumber')}
                placeholder="Enter chassis number"
              />
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Save Changes</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  )
}
