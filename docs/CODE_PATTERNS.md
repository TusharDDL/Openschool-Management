# School Management System - Code Patterns and Best Practices

## Table of Contents
1. [Frontend Patterns](#frontend-patterns)
2. [Backend Patterns](#backend-patterns)
3. [State Management](#state-management)
4. [Form Handling](#form-handling)
5. [API Integration](#api-integration)
6. [Error Handling](#error-handling)
7. [Testing Patterns](#testing-patterns)

## Frontend Patterns

### Component Organization

1. **Page Components** (`src/app/**/page.tsx`)
```typescript
// Always use TypeScript and proper typing
export default function DashboardPage() {
  // 1. Hooks at the top
  const { data, loading } = useQuery(...);
  
  // 2. Derived state and callbacks
  const filteredData = useMemo(...);
  
  // 3. Effects
  useEffect(...);
  
  // 4. Render methods
  const renderContent = () => {...};
  
  // 5. Return JSX
  return (
    <Layout>
      {renderContent()}
    </Layout>
  );
}
```

2. **Reusable Components** (`src/components/*`)
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  // Use utility function for class names
  const className = cn(
    'button-base',
    variantStyles[variant],
    sizeStyles[size]
  );
  
  return <button className={className}>{children}</button>;
}
```

### Custom Hooks Usage

1. **API Hooks** (`src/hooks/useApi.ts`)
```typescript
// In components
const { data, loading, error, execute } = useApi(
  studentAPI.getAssignments,
  {
    onSuccess: (data) => {
      toast.success('Assignments loaded');
    },
  }
);
```

2. **Form Hooks** (`src/hooks/useForm.ts`)
```typescript
// In form components
const form = useForm({
  initialValues,
  validate,
  onSubmit: async (values) => {
    await submitData(values);
  },
});
```

## Backend Patterns

### API Route Organization

1. **Route Structure**
```python
# backend/app/api/v1/endpoints/students.py

@router.get("/{student_id}")
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Validate permissions
    # 2. Get data
    # 3. Return response
```

2. **Dependency Injection**
```python
# backend/app/api/deps.py

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Validate token and return user
```

## State Management

1. **Context Usage**
```typescript
// src/providers/auth-provider.tsx
export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Provide auth state and methods
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Usage in components
const { user, login, logout } = useAuth();
```

2. **Local State Management**
```typescript
// Use local state for component-specific data
const [isOpen, setIsOpen] = useState(false);

// Use context for shared state
const { user } = useAuth();

// Use query hooks for server state
const { data } = useQuery('students', fetchStudents);
```

## Form Handling

1. **Form Validation**
```typescript
const validate = (values: FormValues) => {
  const errors: Partial<Record<keyof FormValues, string>> = {};
  
  if (!values.email) {
    errors.email = 'Required';
  } else if (!isValidEmail(values.email)) {
    errors.email = 'Invalid email';
  }
  
  return errors;
};
```

2. **Form Submission**
```typescript
const handleSubmit = async (values: FormValues) => {
  try {
    await submitForm(values);
    toast.success('Form submitted successfully');
  } catch (error) {
    toast.error(getErrorMessage(error));
  }
};
```

## API Integration

1. **API Service Structure**
```typescript
// src/services/api.ts
export const studentAPI = {
  getAll: () => api.get('/students'),
  getById: (id: string) => api.get(\`/students/\${id}\`),
  create: (data: CreateStudentDto) => api.post('/students', data),
  update: (id: string, data: UpdateStudentDto) => api.put(\`/students/\${id}\`, data),
  delete: (id: string) => api.delete(\`/students/\${id}\`),
};
```

2. **Error Handling**
```typescript
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      auth.logout();
    }
    return Promise.reject(error);
  }
);
```

## Error Handling

1. **Frontend Error Boundaries**
```typescript
export class ErrorBoundary extends React.Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorDisplay error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

2. **Backend Error Handling**
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## Testing Patterns

1. **Component Tests**
```typescript
describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(onClick).toHaveBeenCalled();
  });
});
```

2. **API Tests**
```python
def test_create_user(client: TestClient, db: Session):
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Best Practices

1. **Code Organization**
   - Keep components small and focused
   - Use TypeScript for better type safety
   - Follow the Single Responsibility Principle

2. **Performance**
   - Use React.memo for expensive components
   - Implement proper pagination
   - Use proper caching strategies

3. **Security**
   - Validate all inputs
   - Implement proper authentication
   - Use CSRF protection
   - Sanitize data

4. **Accessibility**
   - Use semantic HTML
   - Implement proper ARIA attributes
   - Ensure keyboard navigation works

5. **Documentation**
   - Document complex logic
   - Add JSDoc comments for functions
   - Keep README files updated