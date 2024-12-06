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
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/hooks/use-toast';
import { academicService, Class, Section } from '@/services/academicService';

const formSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  class_id: z.string().min(1, 'Class is required'),
  capacity: z.string().transform((val) => parseInt(val, 10)).refine((val) => val > 0, {
    message: "Capacity must be greater than 0",
  }),
  is_active: z.boolean().default(true),
});

export function SectionManagement() {
  const [sections, setSections] = useState<Section[]>([]);
  const [classes, setClasses] = useState<Class[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      capacity: '30',
      is_active: true,
    },
  });

  useEffect(() => {
    loadClasses();
    loadSections();
  }, []);

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

  const loadSections = async () => {
    try {
      const data = await academicService.getSections();
      setSections(data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load sections",
        variant: "destructive",
      });
    }
  };

  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      setIsLoading(true);
      const data = {
        ...values,
        class_id: parseInt(values.class_id),
        capacity: parseInt(values.capacity),
      };

      if (editingId) {
        await academicService.updateSection(editingId, data);
        toast({
          title: "Success",
          description: "Section updated successfully",
        });
      } else {
        await academicService.createSection(data);
        toast({
          title: "Success",
          description: "Section created successfully",
        });
      }

      form.reset();
      setEditingId(null);
      loadSections();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save section",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (section: Section) => {
    setEditingId(section.id);
    form.reset({
      name: section.name,
      class_id: section.class_id.toString(),
      capacity: section.capacity.toString(),
      is_active: section.is_active,
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{editingId ? 'Edit' : 'Create'} Section</CardTitle>
          <CardDescription>
            Manage sections for your classes
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="class_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Class</FormLabel>
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
                        {classes.map((classObj) => (
                          <SelectItem
                            key={classObj.id}
                            value={classObj.id.toString()}
                          >
                            {classObj.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormDescription>
                      Select the class for this section
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
                      <Input placeholder="Section A" {...field} />
                    </FormControl>
                    <FormDescription>
                      Enter the section name (e.g., A, B, Red, Blue)
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="capacity"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Capacity</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min="1"
                        placeholder="30"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Maximum number of students in this section
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
                        Mark this section as active
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
          <CardTitle>Sections</CardTitle>
          <CardDescription>
            List of all sections
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {sections.map((section) => {
              const classObj = classes.find(
                (c) => c.id === section.class_id
              );

              return (
                <div
                  key={section.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div className="space-y-1">
                    <p className="font-medium">Section {section.name}</p>
                    {classObj && (
                      <p className="text-sm text-muted-foreground">
                        Class: {classObj.name}
                      </p>
                    )}
                    <p className="text-sm text-muted-foreground">
                      Capacity: {section.capacity} students
                    </p>
                    <p className="text-sm">
                      Status: <span className={section.is_active ? "text-green-600" : "text-red-600"}>
                        {section.is_active ? "Active" : "Inactive"}
                      </span>
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleEdit(section)}
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
