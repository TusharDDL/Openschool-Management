"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AcademicYearManagement } from "@/components/academics/AcademicYearManagement";
import { ClassManagement } from "@/components/academics/ClassManagement";
import { SectionManagement } from "@/components/academics/SectionManagement";

export default function AcademicPage() {
  const [activeTab, setActiveTab] = useState("academic-years");

  return (
    <div className="container mx-auto py-6">
      <h1 className="text-3xl font-bold mb-6">Academic Management</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="academic-years">Academic Years</TabsTrigger>
          <TabsTrigger value="classes">Classes</TabsTrigger>
          <TabsTrigger value="sections">Sections</TabsTrigger>
        </TabsList>
        <TabsContent value="academic-years">
          <AcademicYearManagement />
        </TabsContent>
        <TabsContent value="classes">
          <ClassManagement />
        </TabsContent>
        <TabsContent value="sections">
          <SectionManagement />
        </TabsContent>
      </Tabs>
    </div>
  );
}
