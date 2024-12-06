// src/app/(dashboard)/dashboard/transport/page.tsx

'use client'

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import Overview from '@/components/transport/Overview'
import Vehicles from '@/components/transport/Vehicles'
import Routes from '@/components/transport/Routes'
import Tracking from '@/components/transport/Tracking'
import Alerts from '@/components/transport/Alerts'
import Reports from '@/components/transport/Reports'
import Students from '@/components/transport/Students'
import React from 'react'

export default function TransportPage() {
  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Transport Management</h1>
          <p className="text-muted-foreground">
            Manage vehicles, routes, and student transportation
          </p>
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="tracking">Live Tracking</TabsTrigger>
          <TabsTrigger value="vehicles">Vehicles</TabsTrigger>
          <TabsTrigger value="routes">Routes</TabsTrigger>
          <TabsTrigger value="students">Students</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview">
          <Overview />
        </TabsContent>
        <TabsContent value="tracking">
          <Tracking />
        </TabsContent>
        <TabsContent value="vehicles">
          <Vehicles />
        </TabsContent>
        <TabsContent value="routes">
          <Routes />
        </TabsContent>
        <TabsContent value="students">
          <Students />
        </TabsContent>
        <TabsContent value="alerts">
          <Alerts />
        </TabsContent>
        <TabsContent value="reports">
          <Reports />
        </TabsContent>
      </Tabs>
    </div>
  )
}
