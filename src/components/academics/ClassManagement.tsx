"use client";

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
import { academicService, AcademicYear, Class } from '@/services/academicService';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  description: z.string().optional(),
  academic_year_id: z.string().min(1, 'Academic year is required'),
  is_active: z.boolean().default(true),
});

export function ClassManagement() {
  const [classes, setClasses] = useState<Class[]>([]);
  const [academicYears, setAcademicYears] = useState<AcademicYear[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      description: '',
      is_active: true,
    },
  });

  useEffect(() => {
    loadAcademicYears();
    loadClasses();
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

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      setIsLoading(true);
      const data = {
        ...values,
        academic_year_id: parseInt(values.academic_year_id),
      };

      if (editingId) {
        await academicService.updateClass(editingId, data);
        toast({
          title: "Success",
          description: "Class updated successfully",
        });
      } else {
        await academicService.createClass(data);
        toast({
          title: "Success",
          description: "Class created successfully",
        });
      }

      form.reset();
      setEditingId(null);
      loadClasses();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save class",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (classObj: Class) => {
    setEditingId(classObj.id);
    form.reset({
      name: classObj.name,
      description: classObj.description || '',
      academic_year_id: classObj.academic_year_id.toString(),
      is_active: classObj.is_active,
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{editingId ? 'Edit' : 'Create'} Class</CardTitle>
          <CardDescription>
            Manage classes for your school
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
                    <FormDescription>
                      Select the academic year for this class
                    </FormDescription>
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
                      <Input placeholder="Class 10" {...field} />
                    </FormControl>
                    <FormDescription>
                      Enter the class name (e.g., Class 10, Grade 5)
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
                        placeholder="Enter class description"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Optional description for the class
                    </FormDescription>
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
                        Mark this class as active
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
          <CardTitle>Classes</CardTitle>
          <CardDescription>
            List of all classes
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {classes.map((classObj) => {
              const academicYear = academicYears.find(
                (year) => year.id === classObj.academic_year_id
              );

              return (
                <div
                  key={classObj.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div className="space-y-1">
                    <p className="font-medium">{classObj.name}</p>
                    {academicYear && (
                      <p className="text-sm text-muted-foreground">
                        Academic Year: {academicYear.name}
                      </p>
                    )}
                    {classObj.description && (
                      <p className="text-sm text-muted-foreground">
                        {classObj.description}
                      </p>
                    )}
                    <p className="text-sm">
                      Status: <span className={classObj.is_active ? "text-green-600" : "text-red-600"}>
                        {classObj.is_active ? "Active" : "Inactive"}
                      </span>
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleEdit(classObj)}
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
