// src/components/students/StudentAttendance.tsx

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Calendar,
  Users,
  CheckCircle2,
  XCircle,
  Clock,
  Download,
  Upload,
  Filter,
  AlertTriangle,
  Search
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface Student {
  id: string;
  name: string;
  rollNumber: string;
  class: string;
  section: string;
}

interface AttendanceRecord {
  date: string;
  studentId: string;
  status: 'present' | 'absent' | 'late';
  notes?: string;
}

interface AttendanceStats {
  totalStudents: number;
  present: number;
  absent: number;
  late: number;
}

export default function StudentAttendance() {
  const [selectedDate, setSelectedDate] = React.useState<string>(
    new Date().toISOString().split('T')[0]
  );
  const [selectedClass, setSelectedClass] = React.useState('');
  const [selectedSection, setSelectedSection] = React.useState('');
  const [searchTerm, setSearchTerm] = React.useState('');
  const [isMarking, setIsMarking] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const { toast } = useToast();

  // Sample data - would come from API
  const [students] = React.useState<Student[]>([
    { id: '1', name: 'John Doe', rollNumber: '101', class: '10', section: 'A' },
    { id: '2', name: 'Jane Smith', rollNumber: '102', class: '10', section: 'A' },
    { id: '3', name: 'Mike Johnson', rollNumber: '103', class: '10', section: 'A' },
    { id: '4', name: 'Sarah Williams', rollNumber: '104', class: '10', section: 'B' },
  ]);

  const [attendance, setAttendance] = React.useState<AttendanceRecord[]>([]);

  const calculateStats = (): AttendanceStats => {
    const todayAttendance = attendance.filter(
      record => record.date === selectedDate
    );

    return {
      totalStudents: students.length,
      present: todayAttendance.filter(record => record.status === 'present').length,
      absent: todayAttendance.filter(record => record.status === 'absent').length,
      late: todayAttendance.filter(record => record.status === 'late').length
    };
  };

  const handleMarkAttendance = async (
    studentId: string,
    status: 'present' | 'absent' | 'late',
    notes?: string
  ) => {
    setIsMarking(true);
    try {
      // Here you would make an API call to save the attendance
      await new Promise(resolve => setTimeout(resolve, 500));

      setAttendance(prev => {
        // Remove any existing attendance for this student on this date
        const filtered = prev.filter(
          record => !(record.date === selectedDate && record.studentId === studentId)
        );

        // Add new attendance record
        return [...filtered, {
          date: selectedDate,
          studentId,
          status,
          notes
        }];
      });

      toast({
        title: "Success",
        description: "Attendance marked successfully",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to mark attendance",
        variant: "destructive"
      });
    } finally {
      setIsMarking(false);
    }
  };

  const handleBulkMarkAttendance = async (status: 'present' | 'absent' | 'late') => {
    setIsMarking(true);
    try {
      // Here you would make an API call to save bulk attendance
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newRecords = filteredStudents.map(student => ({
        date: selectedDate,
        studentId: student.id,
        status
      }));

      setAttendance(prev => {
        // Remove existing records for these students on this date
        const filtered = prev.filter(
          record => !(
            record.date === selectedDate && 
            filteredStudents.some(s => s.id === record.studentId)
          )
        );

        return [...filtered, ...newRecords];
      });

      toast({
        title: "Success",
        description: `Marked ${filteredStudents.length} students as ${status}`,
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to mark bulk attendance",
        variant: "destructive"
      });
    } finally {
      setIsMarking(false);
    }
  };

  const exportAttendance = async () => {
    setIsLoading(true);
    try {
      // Here you would typically generate and download a report
      await new Promise(resolve => setTimeout(resolve, 1000));

      const stats = calculateStats();
      const date = new Date(selectedDate).toLocaleDateString();
      const report = `Attendance Report - ${date}
Total Students: ${stats.totalStudents}
Present: ${stats.present}
Absent: ${stats.absent}
Late: ${stats.late}
`;

      const blob = new Blob([report], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `attendance_report_${selectedDate}.txt`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast({
        title: "Success",
        description: "Attendance report downloaded",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to export attendance",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getStudentAttendance = (studentId: string): AttendanceRecord | undefined => {
    return attendance.find(
      record => record.date === selectedDate && record.studentId === studentId
    );
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.rollNumber.includes(searchTerm);
    const matchesClass = selectedClass ? student.class === selectedClass : true;
    const matchesSection = selectedSection ? student.section === selectedSection : true;
    return matchesSearch && matchesClass && matchesSection;
  });

  const stats = calculateStats();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Attendance</h1>
          <p className="text-muted-foreground">
            Mark and manage student attendance
          </p>
        </div>
        <Button
          onClick={exportAttendance}
          disabled={isLoading}
          className="flex items-center gap-2"
        >
          <Download className="h-4 w-4" />
          Export Report
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Students</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalStudents}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Present</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {stats.present}
              <span className="text-sm text-muted-foreground ml-2">
                ({((stats.present / stats.totalStudents) * 100).toFixed(1)}%)
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Absent</CardTitle>
            <XCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {stats.absent}
              <span className="text-sm text-muted-foreground ml-2">
                ({((stats.absent / stats.totalStudents) * 100).toFixed(1)}%)
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Late</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">
              {stats.late}
              <span className="text-sm text-muted-foreground ml-2">
                ({((stats.late / stats.totalStudents) * 100).toFixed(1)}%)
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="px-3 py-2 border rounded-md"
              />
              <select
                value={selectedClass}
                onChange={(e) => setSelectedClass(e.target.value)}
                className="px-3 py-2 border rounded-md"
              >
                <option value="">All Classes</option>
                <option value="10">Class 10</option>
                <option value="9">Class 9</option>
              </select>
              <select
                value={selectedSection}
                onChange={(e) => setSelectedSection(e.target.value)}
                className="px-3 py-2 border rounded-md"
              >
                <option value="">All Sections</option>
                <option value="A">Section A</option>
                <option value="B">Section B</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search students..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8 pr-4 py-2 border rounded-md"
                />
              </div>
              <Button
                variant="outline"
                onClick={() => handleBulkMarkAttendance('present')}
                disabled={isMarking}
              >
                Mark All Present
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="relative overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-gray-50">
                <tr>
                  <th className="px-6 py-3">Roll No</th>
                  <th className="px-6 py-3">Name</th>
                  <th className="px-6 py-3">Class</th>
                  <th className="px-6 py-3">Section</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.map((student) => {
                  const attendanceRecord = getStudentAttendance(student.id);
                  return (
                    <tr key={student.id} className="bg-white border-b hover:bg-gray-50">
                      <td className="px-6 py-4">{student.rollNumber}</td>
                      <td className="px-6 py-4 font-medium">{student.name}</td>
                      <td className="px-6 py-4">Class {student.class}</td>
                      <td className="px-6 py-4">Section {student.section}</td>
                      <td className="px-6 py-4">
                        <span
                          className={cn(
                            "px-2 py-1 text-xs font-semibold rounded-full",
                            {
                              "bg-green-100 text-green-800": attendanceRecord?.status === "present",
                              "bg-red-100 text-red-800": attendanceRecord?.status === "absent",
                              "bg-yellow-100 text-yellow-800": attendanceRecord?.status === "late",
                              "bg-gray-100 text-gray-800": !attendanceRecord
                            }
                          )}
                        >
                          {attendanceRecord?.status 
                            ? attendanceRecord.status.charAt(0).toUpperCase() + 
                              attendanceRecord.status.slice(1)
                            : "Not Marked"
                          }
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-green-600"
                            onClick={() => handleMarkAttendance(student.id, 'present')}
                            disabled={isMarking}
                          >
                            Present
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-red-600"
                            onClick={() => handleMarkAttendance(student.id, 'absent')}
                            disabled={isMarking}
                          >
                            Absent
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-yellow-600"
                            onClick={() => handleMarkAttendance(student.id, 'late')}
                            disabled={isMarking}
                          >
                            Late
                          </Button>
                        </div>
                      </td>
                      </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {filteredStudents.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              No students found matching the search criteria
            </div>
          )}
        </CardContent>
      </Card>

      {/* Attendance Summary Card */}
      <Card>
        <CardHeader>
          <CardTitle>Daily Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {stats.absent > 0 && (
              <div className="rounded-md bg-yellow-50 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <AlertTriangle className="h-5 w-5 text-yellow-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      Absence Alert
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      <p>{stats.absent} students are marked absent today.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border rounded-lg">
                <div className="text-sm font-medium text-muted-foreground">
                  Attendance Rate
                </div>
                <div className="mt-2 text-2xl font-semibold">
                  {((stats.present / stats.totalStudents) * 100).toFixed(1)}%
                </div>
                <div className="mt-1 text-xs text-muted-foreground">
                  Overall attendance for selected date
                </div>
              </div>

              <div className="p-4 border rounded-lg">
                <div className="text-sm font-medium text-muted-foreground">
                  Late Arrivals
                </div>
                <div className="mt-2 text-2xl font-semibold">
                  {stats.late}
                </div>
                <div className="mt-1 text-xs text-muted-foreground">
                  Students marked late today
                </div>
              </div>

              <div className="p-4 border rounded-lg">
                <div className="text-sm font-medium text-muted-foreground">
                  Follow-up Required
                </div>
                <div className="mt-2 text-2xl font-semibold">
                  {stats.absent > 2 ? 'Yes' : 'No'}
                </div>
                <div className="mt-1 text-xs text-muted-foreground">
                  Based on absence threshold
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}