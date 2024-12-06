// src/components/students/StudentBulkImport.tsx

import React from 'react';
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardContent 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Upload,
  Download,
  AlertCircle,
  CheckCircle,
  X,
  FileSpreadsheet,
  RefreshCw
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface StudentData {
  firstName: string;
  lastName: string;
  email: string;
  class: string;
  section: string;
  rollNumber: string;
  parentName: string;
  parentEmail: string;
  parentPhone: string;
  address: string;
}

interface ValidationError {
  row: number;
  column: string;
  message: string;
}

export default function StudentBulkImport() {
  const [file, setFile] = React.useState<File | null>(null);
  const [isUploading, setIsUploading] = React.useState(false);
  const [isValidating, setIsValidating] = React.useState(false);
  const [validationErrors, setValidationErrors] = React.useState<ValidationError[]>([]);
  const [parsedData, setParsedData] = React.useState<StudentData[]>([]);
  const [uploadProgress, setUploadProgress] = React.useState(0);
  const fileInputRef = React.useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  // Download sample template
  const downloadTemplate = () => {
    const template = `First Name,Last Name,Email,Class,Section,Roll Number,Parent Name,Parent Email,Parent Phone,Address
John,Doe,john@example.com,10,A,1001,Jane Doe,jane@example.com,+1234567890,123 Main St
`;
    const blob = new Blob([template], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'student_import_template.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const validateData = async (data: StudentData[]): Promise<ValidationError[]> => {
    const errors: ValidationError[] = [];

    data.forEach((student, index) => {
      // Required fields
      if (!student.firstName?.trim()) {
        errors.push({
          row: index + 1,
          column: 'First Name',
          message: 'First name is required'
        });
      }

      if (!student.lastName?.trim()) {
        errors.push({
          row: index + 1,
          column: 'Last Name',
          message: 'Last name is required'
        });
      }

      // Email validation
      if (!student.email?.trim()) {
        errors.push({
          row: index + 1,
          column: 'Email',
          message: 'Email is required'
        });
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(student.email)) {
        errors.push({
          row: index + 1,
          column: 'Email',
          message: 'Invalid email format'
        });
      }

      // Phone number validation
      if (student.parentPhone && !/^\+?[\d\s-]{10,}$/.test(student.parentPhone)) {
        errors.push({
          row: index + 1,
          column: 'Parent Phone',
          message: 'Invalid phone number format'
        });
      }

      // Class validation
      if (!student.class?.trim()) {
        errors.push({
          row: index + 1,
          column: 'Class',
          message: 'Class is required'
        });
      }

      // Section validation
      if (!student.section?.trim()) {
        errors.push({
          row: index + 1,
          column: 'Section',
          message: 'Section is required'
        });
      }
    });

    return errors;
  };

  const parseCSV = (content: string): StudentData[] => {
    const lines = content.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const data: StudentData[] = [];

    for (let i = 1; i < lines.length; i++) {
      if (!lines[i].trim()) continue;
      
      const values = lines[i].split(',').map(v => v.trim());
      const student: any = {};
      
      headers.forEach((header, index) => {
        const key = header.toLowerCase().replace(/\s+/g, '');
        student[key] = values[index] || '';
      });

      data.push(student as StudentData);
    }

    return data;
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    if (selectedFile.type !== 'text/csv') {
      toast({
        title: "Invalid File",
        description: "Please upload a CSV file",
        variant: "destructive"
      });
      return;
    }

    setFile(selectedFile);
    setValidationErrors([]);
    setParsedData([]);
    setUploadProgress(0);

    // Read and validate file
    setIsValidating(true);
    try {
      const content = await selectedFile.text();
      const data = parseCSV(content);
      const errors = await validateData(data);
      
      setValidationErrors(errors);
      setParsedData(data);

      if (errors.length > 0) {
        toast({
          title: "Validation Failed",
          description: `Found ${errors.length} errors in the file`,
          variant: "destructive"
        });
      } else {
        toast({
          title: "File Validated",
          description: `Successfully validated ${data.length} records`,
          variant: "success"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to parse CSV file",
        variant: "destructive"
      });
    } finally {
      setIsValidating(false);
    }
  };

  const handleUpload = async () => {
    if (!file || validationErrors.length > 0) return;

    setIsUploading(true);
    try {
      // Simulate upload progress
      for (let i = 0; i <= 100; i += 10) {
        setUploadProgress(i);
        await new Promise(resolve => setTimeout(resolve, 200));
      }

      // Here you would typically make an API call to upload the data
      await new Promise(resolve => setTimeout(resolve, 1000));

      toast({
        title: "Success",
        description: `Successfully imported ${parsedData.length} students`,
        variant: "success"
      });

      // Reset form
      setFile(null);
      setParsedData([]);
      setValidationErrors([]);
      setUploadProgress(0);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to import students",
        variant: "destructive"
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Bulk Import Students
          </CardTitle>
          <Button
            variant="outline"
            onClick={downloadTemplate}
            className="flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Download Template
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Upload Area */}
          <div
            className={cn(
              "border-2 border-dashed rounded-lg p-8 text-center transition-colors",
              "hover:border-blue-500 hover:bg-blue-50",
              "cursor-pointer"
            )}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              className="hidden"
            />
            <div className="space-y-4">
              <div className="flex justify-center">
                <FileSpreadsheet className="h-12 w-12 text-blue-500" />
              </div>
              <div>
                <p className="text-lg font-medium">
                  Drop your CSV file here or click to browse
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Upload a CSV file containing student information
                </p>
              </div>
            </div>
          </div>

          {/* File Details */}
          {file && (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <FileSpreadsheet className="h-6 w-6 text-blue-500" />
                  <div>
                    <p className="font-medium">{file.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {parsedData.length} records found
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setFile(null);
                    setParsedData([]);
                    setValidationErrors([]);
                    if (fileInputRef.current) {
                      fileInputRef.current.value = '';
                    }
                  }}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              {/* Validation Status */}
              {isValidating ? (
                <div className="flex items-center justify-center gap-2 p-4">
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  <span>Validating file...</span>
                </div>
              ) : validationErrors.length > 0 ? (
                <div className="rounded-lg border border-red-200 bg-red-50">
                  <div className="p-4">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5 text-red-500" />
                      <h3 className="font-medium text-red-900">
                        Validation Errors
                      </h3>
                    </div>
                    <div className="mt-4 space-y-2">
                      {validationErrors.map((error, index) => (
                        <div
                          key={index}
                          className="flex items-start gap-2 text-sm text-red-800"
                        >
                          <span>•</span>
                          <span>
                            Row {error.row}: {error.column} - {error.message}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : parsedData.length > 0 && (
                <div className="rounded-lg border border-green-200 bg-green-50 p-4">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="font-medium text-green-900">
                      File validated successfully
                    </span>
                  </div>
                </div>
              )}

              {/* Upload Progress */}
              {isUploading && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div
                      className="h-full bg-blue-500 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Upload Button */}
              <div className="flex justify-end">
                <Button
                  onClick={handleUpload}
                  disabled={isUploading || validationErrors.length > 0}
                  className="min-w-[120px]"
                >
                  {isUploading ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    'Upload'
                  )}
                </Button>
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="rounded-md bg-blue-50 p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <AlertCircle className="h-5 w-5 text-blue-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Import Instructions
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <ul className="list-disc space-y-1 pl-5">
                    <li>Download the template file for the correct format</li>
                    <li>Ensure all required fields are filled</li>
                    <li>Save the file in CSV format</li>
                    <li>Upload the file to import students</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}