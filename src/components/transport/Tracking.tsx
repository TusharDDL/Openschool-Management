// src/components/transport/Tracking.tsx

'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useTransport } from '@/contexts/TransportContext'
import { 
  MapPin, 
  Clock, 
  AlertTriangle,
  PhoneCall,
  Navigation,
  MessageSquare,
  Bus,
  RefreshCcw,
  Tool, // Changed from 'Tools' to 'Tool'
} from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'react-toastify'
import { VehicleLocation, Vehicle } from '@/types/transport'

export default function Tracking() {
  const { vehicles, routes, students } = useTransport()
  const [selectedVehicle, setSelectedVehicle] = React.useState<string | null>(null)
  const [locationData, setLocationData] = React.useState<Record<string, VehicleLocation>>({})
  const [isTracking, setIsTracking] = React.useState(true)

  // Simulated real-time updates
  React.useEffect(() => {
    if (!isTracking) return

    const interval = setInterval(() => {
      const updates: Record<string, VehicleLocation> = {}

      vehicles.forEach(vehicle => {
        const route = routes.find(r => r.vehicleId === vehicle.id)
        updates[vehicle.id] = {
          id: vehicle.id,
          latitude: 28.6139 + (Math.random() - 0.5) * 0.1,
          longitude: 77.2090 + (Math.random() - 0.5) * 0.1,
          speed: Math.floor(Math.random() * 60),
          lastUpdated: new Date().toISOString(),
          status: Math.random() > 0.3 ? 'moving' : 'stopped',
          nextStop: route?.stops[0],
          estimatedArrival: new Date(Date.now() + 15 * 60000).toLocaleTimeString()
        }
      })

      setLocationData(updates)
    }, 5000)

    return () => clearInterval(interval)
  }, [vehicles, routes, isTracking])

  const handleAlert = (vehicleId: string) => {
    const vehicle = vehicles.find(v => v.id === vehicleId)
    toast.info(`Alert sent to ${vehicle?.driver}'s device`)
  }

  const handleCall = (vehicleId: string) => {
    const vehicle = vehicles.find(v => v.id === vehicleId)
    if (vehicle?.driverPhone) {
      window.open(`tel:${vehicle.driverPhone}`)
    } else {
      toast.error('Driver phone number not available.')
    }
  }

  const handleMessage = (vehicleId: string) => {
    // Implement SMS/notification functionality
    toast.info("Status update requested from driver")
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Live Tracking</h2>
        <div className="flex gap-2">
          <Button
            variant={isTracking ? "default" : "outline"}
            onClick={() => setIsTracking(!isTracking)}
          >
            <RefreshCcw className={`mr-2 h-4 w-4 ${isTracking ? 'animate-spin' : ''}`} />
            {isTracking ? 'Tracking Active' : 'Start Tracking'}
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Active Vehicles */}
        <Card>
          <CardHeader>
            <CardTitle>Active Vehicles</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {vehicles
              .filter(v => v.status === 'active')
              .map(vehicle => {
                const location = locationData[vehicle.id]
                const route = routes.find(r => r.vehicleId === vehicle.id)
                
                return (
                  <div 
                    key={vehicle.id} 
                    className={`p-4 rounded-lg border ${
                      selectedVehicle === vehicle.id ? 'border-blue-500 bg-blue-50' : ''
                    } cursor-pointer`}
                    onClick={() => setSelectedVehicle(vehicle.id)}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold flex items-center">
                          <Bus className="h-4 w-4 mr-2" />
                          {vehicle.number}
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          Route: {route?.name || 'N/A'}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button 
                          size="sm" 
                          variant="ghost"
                          onClick={(e) => { 
                            e.stopPropagation()
                            handleAlert(vehicle.id) 
                          }}
                        >
                          <AlertTriangle className="h-4 w-4 text-yellow-500" />
                        </Button>
                        <Button 
                          size="sm" 
                          variant="ghost"
                          onClick={(e) => { 
                            e.stopPropagation()
                            handleCall(vehicle.id) 
                          }}
                        >
                          <PhoneCall className="h-4 w-4 text-green-500" />
                        </Button>
                        <Button 
                          size="sm" 
                          variant="ghost"
                          onClick={(e) => { 
                            e.stopPropagation()
                            handleMessage(vehicle.id) 
                          }}
                        >
                          <MessageSquare className="h-4 w-4 text-blue-500" />
                        </Button>
                      </div>
                    </div>

                    {location && (
                      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4 text-muted-foreground" />
                          <span>
                            Last Updated: {new Date(location.lastUpdated).toLocaleTimeString()}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Navigation className="h-4 w-4 text-muted-foreground" />
                          <span>Speed: {location.speed} km/h</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <MapPin className="h-4 w-4 text-muted-foreground" />
                          <span>Next Stop: {location.nextStop || 'N/A'}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4 text-muted-foreground" />
                          <span>ETA: {location.estimatedArrival || 'N/A'}</span>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
          </CardContent>
        </Card>

        {/* Map View */}
        <Card>
          <CardHeader>
            <CardTitle>Map View</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[600px] rounded-lg bg-gray-100 flex items-center justify-center">
              {/* Integrate with your preferred maps provider (Google Maps, Mapbox, etc.) */}
              <p className="text-muted-foreground">Map integration required</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Route Details */}
      {selectedVehicle && (
        <Card>
          <CardHeader>
            <CardTitle>Route Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {routes
                .filter(route => route.vehicleId === selectedVehicle)
                .map(route => (
                  <div key={route.id} className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="font-semibold">{route.name}</h3>
                      <span className="text-sm text-muted-foreground">
                        {route.startTime || 'N/A'} - {route.endTime || 'N/A'}
                      </span>
                    </div>
                    
                    <div className="relative">
                      {route.stops.map((stop, index) => (
                        <div 
                          key={stop} 
                          className="flex items-center gap-4 pb-8 relative"
                        >
                          <div className="absolute left-[11px] h-full w-0.5 bg-gray-200" />
                          <div className="z-10 w-6 h-6 rounded-full bg-white border-2 border-blue-500 flex items-center justify-center">
                            {index + 1}
                          </div>
                          <div className="flex-1">
                            <div className="font-medium">{stop}</div>
                            <div className="text-sm text-muted-foreground">
                              Scheduled: {route.startTime || 'N/A'}
                            </div>
                          </div>
                          <div className="text-sm font-medium">
                            {students.filter(s => s.stopId === stop).length} students
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
