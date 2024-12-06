'use client';

import { DashboardOverview } from '@/components/dashboard/Overview';

export default function DashboardPage() {
  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your school's performance and statistics
        </p>
      </div>

      <DashboardOverview />
    </div>
  );
}