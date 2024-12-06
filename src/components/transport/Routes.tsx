// src/components/transport/Routes.tsx

'use client';

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { useTransport } from '@/contexts/TransportContext';
import { Search, PlusCircle, Edit, Trash } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { Route } from '@/types/transport';

interface RouteFormData {
  name: string;
  startTime: string;
  endTime: string;
  students: string;
  stops: string; // Comma-separated
  vehicleId?: string;
  distance?: string;
  estimatedDuration?: string;
  type?: 'pickup' | 'drop' | 'both';
}

export default function Routes() {
  const { routes, addRoute, updateRoute, deleteRoute } = useTransport();
  const [searchTerm, setSearchTerm] = useState('');
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedRoute, setSelectedRoute] = useState<string | null>(null);

  // React Hook Form for Add/Edit
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors },
  } = useForm<RouteFormData>();

  const onAdd = (data: RouteFormData) => {
    addRoute({
      id: Math.random().toString(36).substr(2, 9),
      name: data.name,
      startTime: data.startTime,
      endTime: data.endTime,
      students: parseInt(data.students),
      stops: data.stops.split(',').map((s) => s.trim()),
      status: 'active',
      distance: data.distance ? parseFloat(data.distance) : 0,
      estimatedDuration: data.estimatedDuration ? parseFloat(data.estimatedDuration) : 0,
      type: data.type || 'pickup',
    });

    toast.success('Route added successfully');

    setIsAddOpen(false);
    reset();
  };

  const onEdit = (data: RouteFormData) => {
    if (!selectedRoute) return;

    updateRoute(selectedRoute, {
      name: data.name,
      startTime: data.startTime,
      endTime: data.endTime,
      students: parseInt(data.students),
      stops: data.stops.split(',').map((s) => s.trim()),
      distance: data.distance ? parseFloat(data.distance) : 0,
      estimatedDuration: data.estimatedDuration ? parseFloat(data.estimatedDuration) : 0,
      type: data.type,
      status: 'active',
    });

    toast.success('Route updated successfully');

    setIsEditOpen(false);
    setSelectedRoute(null);
    reset();
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this route?')) {
      deleteRoute(id);
      toast.success('Route deleted successfully');
    }
  };

  const handleEditClick = (route: Route) => {
    setSelectedRoute(route.id);
    setIsEditOpen(true);
    setValue('name', route.name);
    setValue('startTime', route.startTime || '');
    setValue('endTime', route.endTime || '');
    setValue('students', route.students.toString());
    setValue('stops', route.stops.join(', '));
    setValue('distance', route.distance?.toString() || '');
    setValue('estimatedDuration', route.estimatedDuration?.toString() || '');
    setValue('type', route.type || 'pickup');
  };

  const filteredRoutes = routes.filter((route) =>
    route.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Route Management</h1>
        <Button onClick={() => setIsAddOpen(true)} className="flex items-center gap-2">
          <PlusCircle className="h-4 w-4" />
          Add Route
        </Button>
      </div>

      {/* Routes Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Routes</CardTitle>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search routes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Route Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timings
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Students
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stops
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
                {filteredRoutes.map((route) => (
                  <tr key={route.id}>
                    <td className="px-6 py-4 whitespace-nowrap">{route.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {route.startTime} - {route.endTime}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {route.students !== undefined ? route.students : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {route.stops.join(', ')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          route.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {route.status.charAt(0).toUpperCase() + route.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center gap-2">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditClick(route)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(route.id)}
                        >
                          <Trash className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
                {filteredRoutes.length === 0 && (
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-center" colSpan={6}>
                      No routes found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Add Route Dialog */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Route</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(onAdd)} className="grid gap-4">
            <div>
              <Label htmlFor="name">Route Name*</Label>
              <Input
                id="name"
                {...register('name', { required: 'Route name is required' })}
                placeholder="Enter route name"
              />
              {errors.name && (
                <p className="text-red-600 text-xs mt-1">{errors.name.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="startTime">Start Time*</Label>
              <Input
                id="startTime"
                type="time"
                {...register('startTime', { required: 'Start time is required' })}
              />
              {errors.startTime && (
                <p className="text-red-600 text-xs mt-1">{errors.startTime.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="endTime">End Time*</Label>
              <Input
                id="endTime"
                type="time"
                {...register('endTime', { required: 'End time is required' })}
              />
              {errors.endTime && (
                <p className="text-red-600 text-xs mt-1">{errors.endTime.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="students">Number of Students</Label>
              <Input
                id="students"
                type="number"
                {...register('students', {
                  min: { value: 0, message: 'Number of students cannot be negative' },
                })}
                placeholder="Enter number of students"
              />
              {errors.students && (
                <p className="text-red-600 text-xs mt-1">{errors.students.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="stops">Stops (comma separated)</Label>
              <Input
                id="stops"
                {...register('stops', { required: 'At least one stop is required' })}
                placeholder="Enter stops separated by commas"
              />
              {errors.stops && (
                <p className="text-red-600 text-xs mt-1">{errors.stops.message}</p>
              )}
            </div>
            {/* Optional Fields */}
            <div>
              <Label htmlFor="distance">Distance (km)</Label>
              <Input
                id="distance"
                type="number"
                step="0.1"
                {...register('distance')}
                placeholder="Enter total distance"
              />
            </div>
            <div>
              <Label htmlFor="estimatedDuration">Estimated Duration (mins)</Label>
              <Input
                id="estimatedDuration"
                type="number"
                step="1"
                {...register('estimatedDuration')}
                placeholder="Enter estimated duration"
              />
            </div>
            <div>
              <Label htmlFor="type">Type</Label>
              <select
                id="type"
                {...register('type')}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="pickup">Pickup</option>
                <option value="drop">Drop</option>
                <option value="both">Both</option>
              </select>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsAddOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">Add Route</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Edit Route Dialog */}
      <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Route</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit(onEdit)} className="grid gap-4">
            <div>
              <Label htmlFor="name">Route Name*</Label>
              <Input
                id="name"
                {...register('name', { required: 'Route name is required' })}
                placeholder="Enter route name"
              />
              {errors.name && (
                <p className="text-red-600 text-xs mt-1">{errors.name.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="startTime">Start Time*</Label>
              <Input
                id="startTime"
                type="time"
                {...register('startTime', { required: 'Start time is required' })}
              />
              {errors.startTime && (
                <p className="text-red-600 text-xs mt-1">{errors.startTime.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="endTime">End Time*</Label>
              <Input
                id="endTime"
                type="time"
                {...register('endTime', { required: 'End time is required' })}
              />
              {errors.endTime && (
                <p className="text-red-600 text-xs mt-1">{errors.endTime.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="students">Number of Students</Label>
              <Input
                id="students"
                type="number"
                {...register('students', {
                  min: { value: 0, message: 'Number of students cannot be negative' },
                })}
                placeholder="Enter number of students"
              />
              {errors.students && (
                <p className="text-red-600 text-xs mt-1">{errors.students.message}</p>
              )}
            </div>
            <div>
              <Label htmlFor="stops">Stops (comma separated)</Label>
              <Input
                id="stops"
                {...register('stops', { required: 'At least one stop is required' })}
                placeholder="Enter stops separated by commas"
              />
              {errors.stops && (
                <p className="text-red-600 text-xs mt-1">{errors.stops.message}</p>
              )}
            </div>
            {/* Optional Fields */}
            <div>
              <Label htmlFor="distance">Distance (km)</Label>
              <Input
                id="distance"
                type="number"
                step="0.1"
                {...register('distance')}
                placeholder="Enter total distance"
              />
            </div>
            <div>
              <Label htmlFor="estimatedDuration">Estimated Duration (mins)</Label>
              <Input
                id="estimatedDuration"
                type="number"
                step="1"
                {...register('estimatedDuration')}
                placeholder="Enter estimated duration"
              />
            </div>
            <div>
              <Label htmlFor="type">Type</Label>
              <select
                id="type"
                {...register('type')}
                className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="pickup">Pickup</option>
                <option value="drop">Drop</option>
                <option value="both">Both</option>
              </select>
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
  );
}
