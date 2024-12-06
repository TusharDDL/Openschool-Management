import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import { feeService, FeeReport } from '@/services/feeService';
import { academicService } from '@/services/academicService';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export function FeeReports() {
  const [report, setReport] = useState<FeeReport | null>(null);
  const [academicYears, setAcademicYears] = useState<any[]>([]);
  const [classes, setClasses] = useState<any[]>([]);
  const [filters, setFilters] = useState({
    academic_year_id: '',
    class_id: '',
    from_date: '',
    to_date: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadAcademicYears();
    loadClasses();
  }, []);

  useEffect(() => {
    if (filters.academic_year_id) {
      loadReport();
    }
  }, [filters]);

  const loadAcademicYears = async () => {
    try {
      const data = await academicService.getAcademicYears();
      setAcademicYears(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load academic years",
        variant: "destructive",
      });
    }
  };

  const loadClasses = async () => {
    try {
      const data = await academicService.getClasses();
      setClasses(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load classes",
        variant: "destructive",
      });
    }
  };

  const loadReport = async () => {
    try {
      setIsLoading(true);
      const data = await feeService.getFeeReport({
        academic_year_id: parseInt(filters.academic_year_id),
        class_id: filters.class_id ? parseInt(filters.class_id) : undefined,
        from_date: filters.from_date || undefined,
        to_date: filters.to_date || undefined,
      });
      setReport(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load fee report",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Fee Collection Reports</CardTitle>
          <CardDescription>
            View fee collection statistics and trends
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Select
                value={filters.academic_year_id}
                onValueChange={(value) =>
                  setFilters((prev) => ({ ...prev, academic_year_id: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select academic year" />
                </SelectTrigger>
                <SelectContent>
                  {academicYears.map((year) => (
                    <SelectItem key={year.id} value={year.id.toString()}>
                      {year.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select
                value={filters.class_id}
                onValueChange={(value) =>
                  setFilters((prev) => ({ ...prev, class_id: value }))
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select class" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">All Classes</SelectItem>
                  {classes.map((cls) => (
                    <SelectItem key={cls.id} value={cls.id.toString()}>
                      {cls.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Input
                type="date"
                value={filters.from_date}
                onChange={(e) =>
                  setFilters((prev) => ({ ...prev, from_date: e.target.value }))
                }
                placeholder="From date"
              />

              <Input
                type="date"
                value={filters.to_date}
                onChange={(e) =>
                  setFilters((prev) => ({ ...prev, to_date: e.target.value }))
                }
                placeholder="To date"
              />
            </div>

            {isLoading ? (
              <div className="text-center py-4">Loading...</div>
            ) : report ? (
              <div className="space-y-6">
                {/* Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Total Collection</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold">₹{report.total_collected}</p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Total Pending</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-red-600">
                        ₹{report.total_pending}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                {/* Class-wise Collection Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle>Class-wise Collection</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-[300px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={report.collection_by_class}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="class_name" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="collected" name="Collected" fill="#4CAF50" />
                          <Bar dataKey="pending" name="Pending" fill="#f44336" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>

                {/* Monthly Collection Trend */}
                <Card>
                  <CardHeader>
                    <CardTitle>Monthly Collection Trend</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-[300px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={report.collection_by_month}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="month" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Bar
                            dataKey="amount"
                            name="Collection"
                            fill="#2196F3"
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>
              </div>
            ) : (
              <div className="text-center py-4 text-muted-foreground">
                Select filters to view report
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}