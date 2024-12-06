// src/components/transport/Students.tsx

'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useTransport } from '@/contexts/TransportContext'

export default function Students() {
  const { students, routes } = useTransport()

  const getRouteName = (stopId: string) => {
    const route = routes.find(r => r.stops.includes(stopId))
    return route ? route.name : 'N/A'
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Students</h1>

      {/* Students Table */}
      <Card>
        <CardHeader>
          <CardTitle>Student List</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stop
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Route
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {students.map(student => (
                  <tr key={student.id}>
                    <td className="px-6 py-4 whitespace-nowrap">{student.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{student.stopId}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{getRouteName(student.stopId)}</td>
                  </tr>
                ))}
                {students.length === 0 && (
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-center" colSpan={3}>
                      No students found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
