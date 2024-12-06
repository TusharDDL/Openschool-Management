// src/components/transport/Reports.tsx

'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { useTransport } from '@/contexts/TransportContext'

export default function Reports() {
  const { vehicles, routes, maintenanceHistory } = useTransport()

  // Example: Maintenance cost per vehicle
  const data = vehicles.map(vehicle => {
    const totalCost = (vehicle.maintenanceHistory || []).reduce((acc, record) => acc + record.cost, 0)
    return {
      name: vehicle.number,
      cost: totalCost,
    }
  })

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Reports</h1>

      {/* Maintenance Cost Report */}
      <Card>
        <CardHeader>
          <CardTitle>Maintenance Cost per Vehicle</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cost" fill="#4ade80" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Additional Reports can be added here */}
    </div>
  )
}
