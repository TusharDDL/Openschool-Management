import React from 'react';
import { cn } from '@/lib/utils';
import { Label } from '@radix-ui/react-label';
import { LoadingButton } from './loading';

interface FormFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  className?: string;
}

export function FormField({
  label,
  error,
  className,
  id,
  ...props
}: FormFieldProps) {
  return (
    <div className={cn('space-y-2', className)}>
      <Label
        htmlFor={id}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
      </Label>
      <input
        id={id}
        className={cn(
          'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
          props.disabled && 'bg-gray-100 cursor-not-allowed'
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}

interface TextAreaFieldProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
  className?: string;
}

export function TextAreaField({
  label,
  error,
  className,
  id,
  ...props
}: TextAreaFieldProps) {
  return (
    <div className={cn('space-y-2', className)}>
      <Label
        htmlFor={id}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
      </Label>
      <textarea
        id={id}
        className={cn(
          'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
          props.disabled && 'bg-gray-100 cursor-not-allowed'
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}

interface SelectFieldProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: Array<{ value: string; label: string }>;
  className?: string;
}

export function SelectField({
  label,
  error,
  options,
  className,
  id,
  ...props
}: SelectFieldProps) {
  return (
    <div className={cn('space-y-2', className)}>
      <Label
        htmlFor={id}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
      </Label>
      <select
        id={id}
        className={cn(
          'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-500',
          props.disabled && 'bg-gray-100 cursor-not-allowed'
        )}
        {...props}
      >
        <option value="">Select an option</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}

interface CheckboxFieldProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  className?: string;
}

export function CheckboxField({
  label,
  error,
  className,
  id,
  ...props
}: CheckboxFieldProps) {
  return (
    <div className={cn('relative flex items-start', className)}>
      <div className="flex h-5 items-center">
        <input
          id={id}
          type="checkbox"
          className={cn(
            'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500',
            error && 'border-red-300 focus:ring-red-500',
            props.disabled && 'bg-gray-100 cursor-not-allowed'
          )}
          {...props}
        />
      </div>
      <div className="ml-3 text-sm">
        <Label
          htmlFor={id}
          className="font-medium text-gray-700"
        >
          {label}
        </Label>
        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}
      </div>
    </div>
  );
}

interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {
  onSubmit: (e: React.FormEvent) => void;
  loading?: boolean;
  error?: string;
  submitText?: string;
  className?: string;
}

export function Form({
  onSubmit,
  loading = false,
  error,
  submitText = 'Submit',
  className,
  children,
  ...props
}: FormProps) {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(e);
      }}
      className={cn('space-y-6', className)}
      {...props}
    >
      {children}
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}
      <div className="flex justify-end">
        <LoadingButton
          type="submit"
          loading={loading}
          loadingText="Submitting..."
        >
          {submitText}
        </LoadingButton>
      </div>
    </form>
  );
}