import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/hooks/use-toast';
import { feeService, FeeStructure } from '@/services/feeService';
import { academicService } from '@/services/academicService';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  description: z.string().optional(),
  amount: z.number().min(0, 'Amount must be positive'),
  frequency: z.enum(['MONTHLY', 'QUARTERLY', 'YEARLY', 'ONE_TIME']),
  class_id: z.string().optional(),
  academic_year_id: z.string().min(1, 'Academic year is required'),
  due_day: z.number().min(1).max(31).optional(),
  is_active: z.boolean().default(true),
});

export function FeeStructureManager() {
  const [feeStructures, setFeeStructures] = useState<FeeStructure[]>([]);
  const [academicYears, setAcademicYears] = useState<any[]>([]);
  const [classes, setClasses] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      description: '',
      amount: 0,
      frequency: 'MONTHLY',
      is_active: true,
    },
  });

  useEffect(() => {
    loadAcademicYears();
    loadClasses();
    loadFeeStructures();
  }, []);

  const loadAcademicYears = async () => {
    try {
      const data = await academicService.getAcademicYears({ is_active: true });
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
      const data = await academicService.getClasses({ is_active: true });
      setClasses(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load classes",
        variant: "destructive",
      });
    }
  };

  const loadFeeStructures = async () => {
    try {
      const data = await feeService.getFeeStructures();
      setFeeStructures(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load fee structures",
        variant: "destructive",
      });
    }
  };

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      setIsLoading(true);
      const data = {
        ...values,
        academic_year_id: parseInt(values.academic_year_id),
        class_id: values.class_id ? parseInt(values.class_id) : undefined,
      };

      if (editingId) {
        await feeService.updateFeeStructure(editingId, data);
        toast({
          title: "Success",
          description: "Fee structure updated successfully",
        });
      } else {
        await feeService.createFeeStructure(data);
        toast({
          title: "Success",
          description: "Fee structure created successfully",
        });
      }

      form.reset();
      setEditingId(null);
      loadFeeStructures();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save fee structure",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (feeStructure: FeeStructure) => {
    setEditingId(feeStructure.id);
    form.reset({
      name: feeStructure.name,
      description: feeStructure.description,
      amount: feeStructure.amount,
      frequency: feeStructure.frequency,
      class_id: feeStructure.class_id?.toString(),
      academic_year_id: feeStructure.academic_year_id.toString(),
      due_day: feeStructure.due_day,
      is_active: feeStructure.is_active,
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{editingId ? 'Edit' : 'Create'} Fee Structure</CardTitle>
          <CardDescription>
            Define fee structures for your school
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="academic_year_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Academic Year</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select academic year" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {academicYears.map((year) => (
                          <SelectItem
                            key={year.id}
                            value={year.id.toString()}
                          >
                            {year.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Tuition Fee" {...field} />
                    </FormControl>
                    <FormDescription>
                      Enter the fee name (e.g., Tuition Fee, Lab Fee)
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="amount"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Amount</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        placeholder="0"
                        {...field}
                        onChange={(e) => field.onChange(parseFloat(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="frequency"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Frequency</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select frequency" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="MONTHLY">Monthly</SelectItem>
                        <SelectItem value="QUARTERLY">Quarterly</SelectItem>
                        <SelectItem value="YEARLY">Yearly</SelectItem>
                        <SelectItem value="ONE_TIME">One Time</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="class_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Class (Optional)</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select class" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="">All Classes</SelectItem>
                        {classes.map((cls) => (
                          <SelectItem
                            key={cls.id}
                            value={cls.id.toString()}
                          >
                            {cls.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormDescription>
                      Leave empty to apply to all classes
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="due_day"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Due Day</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min="1"
                        max="31"
                        placeholder="10"
                        {...field}
                        onChange={(e) => field.onChange(parseInt(e.target.value))}
                      />
                    </FormControl>
                    <FormDescription>
                      Day of the month when fee is due
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Enter fee description"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="is_active"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                    <div className="space-y-0.5">
                      <FormLabel className="text-base">
                        Active
                      </FormLabel>
                      <FormDescription>
                        Mark this fee structure as active
                      </FormDescription>
                    </div>
                    <FormControl>
                      <Switch
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />

              <div className="flex justify-end space-x-4">
                {editingId && (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      setEditingId(null);
                      form.reset();
                    }}
                  >
                    Cancel
                  </Button>
                )}
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? "Saving..." : editingId ? "Update" : "Create"}
                </Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Fee Structures</CardTitle>
          <CardDescription>
            List of all fee structures
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {feeStructures.map((fee) => {
              const academicYear = academicYears.find(
                (year) => year.id === fee.academic_year_id
              );
              const cls = classes.find(
                (c) => c.id === fee.class_id
              );

              return (
                <div
                  key={fee.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div className="space-y-1">
                    <p className="font-medium">{fee.name}</p>
                    <p className="text-sm">
                      Amount: ₹{fee.amount} ({fee.frequency.toLowerCase()})
                    </p>
                    {academicYear && (
                      <p className="text-sm text-muted-foreground">
                        Academic Year: {academicYear.name}
                      </p>
                    )}
                    {cls && (
                      <p className="text-sm text-muted-foreground">
                        Class: {cls.name}
                      </p>
                    )}
                    {fee.description && (
                      <p className="text-sm text-muted-foreground">
                        {fee.description}
                      </p>
                    )}
                    <p className="text-sm">
                      Status: <span className={fee.is_active ? "text-green-600" : "text-red-600"}>
                        {fee.is_active ? "Active" : "Inactive"}
                      </span>
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleEdit(fee)}
                  >
                    Edit
                  </Button>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}