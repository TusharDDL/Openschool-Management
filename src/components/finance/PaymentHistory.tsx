import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import { feeService, FeePayment } from '@/services/feeService';
import { academicService } from '@/services/academicService';

export function PaymentHistory() {
  const [payments, setPayments] = useState<FeePayment[]>([]);
  const [students, setStudents] = useState<any[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<string>('');
  const [dateRange, setDateRange] = useState({
    from: '',
    to: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadStudents();
  }, []);

  useEffect(() => {
    if (selectedStudent) {
      loadPayments();
    }
  }, [selectedStudent, dateRange]);

  const loadStudents = async () => {
    try {
      // Assuming there's a method to get students
      const data = await academicService.getStudents();
      setStudents(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load students",
        variant: "destructive",
      });
    }
  };

  const loadPayments = async () => {
    if (!selectedStudent) return;

    try {
      setIsLoading(true);
      const data = await feeService.getStudentPayments(parseInt(selectedStudent), {
        from_date: dateRange.from || undefined,
        to_date: dateRange.to || undefined,
      });
      setPayments(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load payments",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadReceipt = async (paymentId: number) => {
    try {
      const blob = await feeService.generateReceipt(paymentId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `receipt-${paymentId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to download receipt",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Payment History</CardTitle>
          <CardDescription>
            View and download payment receipts
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-1">
                <Select
                  value={selectedStudent}
                  onValueChange={setSelectedStudent}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select student" />
                  </SelectTrigger>
                  <SelectContent>
                    {students.map((student) => (
                      <SelectItem
                        key={student.id}
                        value={student.id.toString()}
                      >
                        {student.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex-1">
                <Input
                  type="date"
                  value={dateRange.from}
                  onChange={(e) => setDateRange(prev => ({
                    ...prev,
                    from: e.target.value
                  }))}
                  placeholder="From date"
                />
              </div>
              <div className="flex-1">
                <Input
                  type="date"
                  value={dateRange.to}
                  onChange={(e) => setDateRange(prev => ({
                    ...prev,
                    to: e.target.value
                  }))}
                  placeholder="To date"
                />
              </div>
            </div>

            {isLoading ? (
              <div className="text-center py-4">Loading...</div>
            ) : payments.length > 0 ? (
              <div className="space-y-4">
                {payments.map((payment) => (
                  <div
                    key={payment.id}
                    className="flex items-center justify-between p-4 border rounded-lg"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">
                        Amount: ₹{payment.amount_paid}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Date: {format(new Date(payment.payment_date), 'PPP')}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Mode: {payment.payment_mode}
                      </p>
                      {payment.reference_number && (
                        <p className="text-sm text-muted-foreground">
                          Ref: {payment.reference_number}
                        </p>
                      )}
                      {payment.remarks && (
                        <p className="text-sm text-muted-foreground">
                          {payment.remarks}
                        </p>
                      )}
                    </div>
                    <Button
                      variant="outline"
                      onClick={() => handleDownloadReceipt(payment.id)}
                    >
                      Download Receipt
                    </Button>
                  </div>
                ))}
              </div>
            ) : selectedStudent ? (
              <div className="text-center py-4 text-muted-foreground">
                No payments found
              </div>
            ) : (
              <div className="text-center py-4 text-muted-foreground">
                Select a student to view payment history
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}