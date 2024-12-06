'use client';

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FeeStructureManager } from '@/components/finance/FeeStructure';
import { PaymentHistory } from '@/components/finance/PaymentHistory';
import { FeeReports } from '@/components/finance/FeeReports';

export default function FinancePage() {
  const [activeTab, setActiveTab] = useState('structure');

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Finance Management</h1>
        <p className="text-muted-foreground">
          Manage fee structures, track payments, and view reports
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="structure">Fee Structure</TabsTrigger>
          <TabsTrigger value="payments">Payment History</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>
        <TabsContent value="structure">
          <FeeStructureManager />
        </TabsContent>
        <TabsContent value="payments">
          <PaymentHistory />
        </TabsContent>
        <TabsContent value="reports">
          <FeeReports />
        </TabsContent>
      </Tabs>
    </div>
  );
}