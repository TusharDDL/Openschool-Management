// src/types/transport.ts

export interface MaintenanceRecord {
    id: string
    vehicleId: string
    type: 'regular' | 'repair' | 'emergency'
    description: string
    cost: number
    date: string
    status: 'completed' | 'pending'
  }
  
  export interface Vehicle {
    id: string
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
    nextMaintenance?: string
    maintenanceHistory?: MaintenanceRecord[]
  }
  
  export interface Route {
    id: string
    name: string
    vehicleId: string
    stops: string[]
    distance: number
    students: number
    status: 'active' | 'inactive'
    startTime?: string
    endTime?: string
    estimatedDuration?: number
  }
  
  export interface Student {
    id: string
    name: string
    stopId: string
  }
  
  export interface VehicleLocation {
    id: string
    latitude: number
    longitude: number
    speed: number
    lastUpdated: string
    status: 'moving' | 'stopped' | 'idle'
    nextStop?: string
    estimatedArrival?: string
  }
  
  export interface TransportContextProps {
    vehicles: Vehicle[]
    routes: Route[]
    students: Student[]
    addVehicle: (vehicle: Vehicle) => void
    updateVehicle: (number: string, updatedVehicle: Partial<Vehicle>) => void
    deleteVehicle: (id: string) => void
    addMaintenanceRecord: (record: MaintenanceRecord) => void
    addRoute: (route: Route) => void
    updateRoute: (id: string, updatedRoute: Partial<Route>) => void
    deleteRoute: (id: string) => void
  }
  