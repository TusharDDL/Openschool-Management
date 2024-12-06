// src/components/transport/Overview.tsx

'use client';

import React from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { AlertTriangle } from 'lucide-react';
import { useTransport } from '@/contexts/TransportContext';

export default function Overview() {
  const { vehicles, routes, students } = useTransport();

  // Statistics
  const stats = {
    totalVehicles: vehicles.length,
    activeVehicles: vehicles.filter((v) => v.status === 'active').length,
    totalRoutes: routes.length,
    activeRoutes: routes.filter((r) => r.status === 'active').length,
    totalStudents: students.length,
    maintenanceDue: vehicles.filter((v) => {
      if (!v.nextMaintenance) return false;
      const nextDate = new Date(v.nextMaintenance);
      return nextDate <= new Date();
    }).length,
    insuranceExpired: vehicles.filter((v) => {
      if (!v.insuranceExpiry) return false;
      const insuranceDate = new Date(v.insuranceExpiry);
      return insuranceDate <= new Date();
    }).length,
    pollutionExpired: vehicles.filter((v) => {
      if (!v.pollutionExpiry) return false;
      const pollutionDate = new Date(v.pollutionExpiry);
      return pollutionDate <= new Date();
    }).length,
  };

  // Upcoming Maintenance
  const upcomingMaintenance = vehicles
    .filter((v) => v.nextMaintenance)
    .sort(
      (a, b) =>
        new Date(a.nextMaintenance!).getTime() - new Date(b.nextMaintenance!).getTime()
    )
    .slice(0, 3);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Transport Overview</h1>

      {/* Statistics Cards */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-3">
        {/* Total Vehicles */}
        <Card>
          <CardHeader>
            <CardTitle>Total Vehicles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.totalVehicles}</div>
          </CardContent>
        </Card>

        {/* Active Vehicles */}
        <Card>
          <CardHeader>
            <CardTitle>Active Vehicles</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.activeVehicles}</div>
          </CardContent>
        </Card>

        {/* Maintenance Due */}
        <Card>
          <CardHeader>
            <CardTitle>Maintenance Due</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.maintenanceDue}</div>
          </CardContent>
        </Card>

        {/* Total Routes */}
        <Card>
          <CardHeader>
            <CardTitle>Total Routes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.totalRoutes}</div>
          </CardContent>
        </Card>

        {/* Active Routes */}
        <Card>
          <CardHeader>
            <CardTitle>Active Routes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.activeRoutes}</div>
          </CardContent>
        </Card>

        {/* Total Students */}
        <Card>
          <CardHeader>
            <CardTitle>Total Students</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-semibold">{stats.totalStudents}</div>
          </CardContent>
        </Card>
      </div>

      {/* Upcoming Maintenance */}
      <Card>
        <CardHeader>
          <CardTitle>Upcoming Maintenance</CardTitle>
        </CardHeader>
        <CardContent>
          {upcomingMaintenance.length > 0 ? (
            <ul className="list-disc list-inside">
              {upcomingMaintenance.map((vehicle) => (
                <li key={vehicle.id}>
                  {vehicle.number} - Due on {vehicle.nextMaintenance}
                </li>
              ))}
            </ul>
          ) : (
            <div>No upcoming maintenance.</div>
          )}
        </CardContent>
      </Card>

      {/* Alerts */}
      <Card>
        <CardHeader>
          <CardTitle>Alerts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {stats.maintenanceDue > 0 && (
              <div className="flex items-center text-yellow-600">
                <AlertTriangle className="h-5 w-5 mr-2" />
                {stats.maintenanceDue} vehicle(s) due for maintenance.
              </div>
            )}
            {stats.insuranceExpired > 0 && (
              <div className="flex items-center text-red-600">
                <AlertTriangle className="h-5 w-5 mr-2" />
                {stats.insuranceExpired} vehicle(s) have expired insurance.
              </div>
            )}
            {stats.pollutionExpired > 0 && (
              <div className="flex items-center text-red-600">
                <AlertTriangle className="h-5 w-5 mr-2" />
                {stats.pollutionExpired} vehicle(s) have expired pollution certificates.
              </div>
            )}
            {/* Add more alerts as needed */}
            {stats.maintenanceDue === 0 &&
              stats.insuranceExpired === 0 &&
              stats.pollutionExpired === 0 && (
                <div>No alerts at the moment.</div>
              )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
