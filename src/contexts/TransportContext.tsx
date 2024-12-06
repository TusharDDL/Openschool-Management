// src/contexts/TransportContext.tsx

'use client'

import React, { createContext, useContext, useState, ReactNode } from 'react'
import { TransportContextProps, Vehicle, Route, Student, MaintenanceRecord } from '@/types/transport'

const TransportContext = createContext<TransportContextProps | undefined>(undefined)

export const TransportProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [routes, setRoutes] = useState<Route[]>([])
  const [students, setStudents] = useState<Student[]>([])

  const addVehicle = (vehicle: Vehicle) => {
    setVehicles((prev) => [...prev, vehicle])
  }

  const updateVehicle = (number: string, updatedVehicle: Partial<Vehicle>) => {
    setVehicles((prev) =>
      prev.map((v) => (v.number === number ? { ...v, ...updatedVehicle } : v))
    )
  }

  const deleteVehicle = (id: string) => {
    setVehicles((prev) => prev.filter((v) => v.id !== id))
    setRoutes((prev) => prev.filter((r) => r.vehicleId !== id))
  }

  const addMaintenanceRecord = (record: MaintenanceRecord) => {
    setVehicles((prev) =>
      prev.map((v) =>
        v.id === record.vehicleId
          ? {
              ...v,
              maintenanceHistory: v.maintenanceHistory
                ? [...v.maintenanceHistory, record]
                : [record],
              ...(record.type === 'regular'
                ? {
                    nextMaintenance: new Date(
                      new Date().setMonth(new Date().getMonth() + 6)
                    ).toISOString().split('T')[0],
                  }
                : {}),
            }
          : v
      )
    )
  }

  const addRoute = (route: Route) => {
    setRoutes((prev) => [...prev, route])
  }

  const updateRoute = (id: string, updatedRoute: Partial<Route>) => {
    setRoutes((prev) =>
      prev.map((r) => (r.id === id ? { ...r, ...updatedRoute } : r))
    )
  }

  const deleteRoute = (id: string) => {
    setRoutes((prev) => prev.filter((r) => r.id !== id))
  }

  return (
    <TransportContext.Provider
      value={{
        vehicles,
        routes,
        students,
        addVehicle,
        updateVehicle,
        deleteVehicle,
        addMaintenanceRecord,
        addRoute,
        updateRoute,
        deleteRoute,
      }}
    >
      {children}
    </TransportContext.Provider>
  )
}

export const useTransport = (): TransportContextProps => {
  const context = useContext(TransportContext)
  if (!context) {
    throw new Error('useTransport must be used within a TransportProvider')
  }
  return context
}
