import { useState, useCallback } from 'react';
import { useMutation } from './useQuery';
import { toast } from 'react-toastify';

interface FormOptions<T, R> {
  endpoint: string;
  onSuccess?: (data: R) => void;
  onError?: (error: Error) => void;
  transform?: (data: T) => any;
  successMessage?: string;
  invalidateQueries?: string[];
}

export function useForm<T extends object, R = any>(
  initialValues: T,
  options: FormOptions<T, R>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const { mutate, isLoading } = useMutation<R, any>(options.endpoint, {
    onSuccess: (data) => {
      toast.success(options.successMessage || 'Success!');
      options.onSuccess?.(data);
      setValues(initialValues);
      setErrors({});
      setTouched({});
    },
    onError: (error) => {
      toast.error(error.message);
      options.onError?.(error);
    },
    invalidateQueries: options.invalidateQueries,
  });

  const handleChange = useCallback((
    name: keyof T,
    value: any
  ) => {
    setValues((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: '' }));
  }, []);

  const handleBlur = useCallback((name: keyof T) => {
    setTouched((prev) => ({ ...prev, [name]: true }));
  }, []);

  const validate = useCallback((values: T): boolean => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let isValid = true;

    // Add your validation rules here
    Object.entries(values).forEach(([key, value]) => {
      if (value === undefined || value === null || value === '') {
        newErrors[key as keyof T] = 'This field is required';
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, []);

  const handleSubmit = useCallback(async (
    e?: React.FormEvent
  ) => {
    e?.preventDefault();

    if (!validate(values)) {
      toast.error('Please fix the form errors');
      return;
    }

    const data = options.transform ? options.transform(values) : values;
    await mutate(data);
  }, [values, options, validate, mutate]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    isLoading,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    setValues,
    setErrors,
    setTouched,
  };
}