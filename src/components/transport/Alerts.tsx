// src/components/transport/Alerts.tsx

'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { AlertCircle } from 'lucide-react'
import { useTransport } from '@/contexts/TransportContext'

export default function Alerts() {
  const { vehicles, routes, students } = useTransport()

  const expiredInsurance = vehicles.filter(v => {
    if (!v.insuranceExpiry) return false
    const expiryDate = new Date(v.insuranceExpiry)
    return expiryDate <= new Date()
  })

  const expiredPollution = vehicles.filter(v => {
    if (!v.pollutionExpiry) return false
    const expiryDate = new Date(v.pollutionExpiry)
    return expiryDate <= new Date()
  })

  const maintenanceDue = vehicles.filter(v => {
    if (!v.nextMaintenance) return false
    const dueDate = new Date(v.nextMaintenance)
    return dueDate <= new Date()
  })

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>

      {/* Insurance Expiry Alerts */}
      <Card>
        <CardHeader className="flex items-center">
          <AlertCircle className="h-6 w-6 text-red-500 mr-2" />
          <CardTitle>Insurance Expiry</CardTitle>
        </CardHeader>
        <CardContent>
          {expiredInsurance.length > 0 ? (
            <ul className="list-disc list-inside">
              {expiredInsurance.map(v => (
                <li key={v.id}>
                  Vehicle {v.number} has expired insurance on {v.insuranceExpiry}
                </li>
              ))}
            </ul>
          ) : (
            <div>No insurance expiries.</div>
          )}
        </CardContent>
      </Card>

      {/* Pollution Expiry Alerts */}
      <Card>
        <CardHeader className="flex items-center">
          <AlertCircle className="h-6 w-6 text-red-500 mr-2" />
          <CardTitle>Pollution Expiry</CardTitle>
        </CardHeader>
        <CardContent>
          {expiredPollution.length > 0 ? (
            <ul className="list-disc list-inside">
              {expiredPollution.map(v => (
                <li key={v.id}>
                  Vehicle {v.number} has expired pollution certificate on {v.pollutionExpiry}
                </li>
              ))}
            </ul>
          ) : (
            <div>No pollution expiries.</div>
          )}
        </CardContent>
      </Card>

      {/* Maintenance Due Alerts */}
      <Card>
        <CardHeader className="flex items-center">
          <AlertCircle className="h-6 w-6 text-red-500 mr-2" />
          <CardTitle>Maintenance Due</CardTitle>
        </CardHeader>
        <CardContent>
          {maintenanceDue.length > 0 ? (
            <ul className="list-disc list-inside">
              {maintenanceDue.map(v => (
                <li key={v.id}>
                  Vehicle {v.number} is due for maintenance on {v.nextMaintenance}
                </li>
              ))}
            </ul>
          ) : (
            <div>No maintenance due.</div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
