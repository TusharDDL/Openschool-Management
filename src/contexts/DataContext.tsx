import React, { createContext, useContext, useReducer, useCallback } from 'react';
import { useQuery } from '@/hooks/useQuery';

// Types
interface DataState {
  users: any[];
  schools: any[];
  students: any[];
  teachers: any[];
  courses: any[];
  loading: boolean;
  error: Error | null;
}

type DataAction =
  | { type: 'SET_DATA'; payload: { key: keyof DataState; data: any[] } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: Error | null }
  | { type: 'UPDATE_ITEM'; payload: { key: keyof DataState; id: string; data: any } }
  | { type: 'DELETE_ITEM'; payload: { key: keyof DataState; id: string } }
  | { type: 'ADD_ITEM'; payload: { key: keyof DataState; data: any } };

// Initial state
const initialState: DataState = {
  users: [],
  schools: [],
  students: [],
  teachers: [],
  courses: [],
  loading: false,
  error: null,
};

// Context
const DataContext = createContext<{
  state: DataState;
  dispatch: React.Dispatch<DataAction>;
  refreshData: (key: keyof DataState) => Promise<void>;
} | undefined>(undefined);

// Reducer
function dataReducer(state: DataState, action: DataAction): DataState {
  switch (action.type) {
    case 'SET_DATA':
      return {
        ...state,
        [action.payload.key]: action.payload.data,
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'UPDATE_ITEM':
      return {
        ...state,
        [action.payload.key]: state[action.payload.key].map((item: any) =>
          item.id === action.payload.id ? { ...item, ...action.payload.data } : item
        ),
      };
    case 'DELETE_ITEM':
      return {
        ...state,
        [action.payload.key]: state[action.payload.key].filter(
          (item: any) => item.id !== action.payload.id
        ),
      };
    case 'ADD_ITEM':
      return {
        ...state,
        [action.payload.key]: [...state[action.payload.key], action.payload.data],
      };
    default:
      return state;
  }
}

// Provider
export function DataProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(dataReducer, initialState);

  const refreshData = useCallback(async (key: keyof DataState) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const { data } = await useQuery(`/api/v1/${key}`);
      dispatch({ type: 'SET_DATA', payload: { key, data } });
      dispatch({ type: 'SET_ERROR', payload: null });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error as Error });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, []);

  return (
    <DataContext.Provider value={{ state, dispatch, refreshData }}>
      {children}
    </DataContext.Provider>
  );
}

// Hook
export function useData() {
  const context = useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
}

// Utility hooks
export function useUsers() {
  const { state, dispatch, refreshData } = useData();
  return {
    users: state.users,
    loading: state.loading,
    error: state.error,
    refreshUsers: () => refreshData('users'),
    updateUser: (id: string, data: any) =>
      dispatch({ type: 'UPDATE_ITEM', payload: { key: 'users', id, data } }),
    deleteUser: (id: string) =>
      dispatch({ type: 'DELETE_ITEM', payload: { key: 'users', id } }),
    addUser: (data: any) =>
      dispatch({ type: 'ADD_ITEM', payload: { key: 'users', data } }),
  };
}

export function useSchools() {
  const { state, dispatch, refreshData } = useData();
  return {
    schools: state.schools,
    loading: state.loading,
    error: state.error,
    refreshSchools: () => refreshData('schools'),
    updateSchool: (id: string, data: any) =>
      dispatch({ type: 'UPDATE_ITEM', payload: { key: 'schools', id, data } }),
    deleteSchool: (id: string) =>
      dispatch({ type: 'DELETE_ITEM', payload: { key: 'schools', id } }),
    addSchool: (data: any) =>
      dispatch({ type: 'ADD_ITEM', payload: { key: 'schools', data } }),
  };
}

export function useStudents() {
  const { state, dispatch, refreshData } = useData();
  return {
    students: state.students,
    loading: state.loading,
    error: state.error,
    refreshStudents: () => refreshData('students'),
    updateStudent: (id: string, data: any) =>
      dispatch({ type: 'UPDATE_ITEM', payload: { key: 'students', id, data } }),
    deleteStudent: (id: string) =>
      dispatch({ type: 'DELETE_ITEM', payload: { key: 'students', id } }),
    addStudent: (data: any) =>
      dispatch({ type: 'ADD_ITEM', payload: { key: 'students', data } }),
  };
}

export function useTeachers() {
  const { state, dispatch, refreshData } = useData();
  return {
    teachers: state.teachers,
    loading: state.loading,
    error: state.error,
    refreshTeachers: () => refreshData('teachers'),
    updateTeacher: (id: string, data: any) =>
      dispatch({ type: 'UPDATE_ITEM', payload: { key: 'teachers', id, data } }),
    deleteTeacher: (id: string) =>
      dispatch({ type: 'DELETE_ITEM', payload: { key: 'teachers', id } }),
    addTeacher: (data: any) =>
      dispatch({ type: 'ADD_ITEM', payload: { key: 'teachers', data } }),
  };
}

export function useCourses() {
  const { state, dispatch, refreshData } = useData();
  return {
    courses: state.courses,
    loading: state.loading,
    error: state.error,
    refreshCourses: () => refreshData('courses'),
    updateCourse: (id: string, data: any) =>
      dispatch({ type: 'UPDATE_ITEM', payload: { key: 'courses', id, data } }),
    deleteCourse: (id: string) =>
      dispatch({ type: 'DELETE_ITEM', payload: { key: 'courses', id } }),
    addCourse: (data: any) =>
      dispatch({ type: 'ADD_ITEM', payload: { key: 'courses', data } }),
  };
}