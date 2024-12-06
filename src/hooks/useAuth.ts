import { useContext, useCallback } from 'react';
import { AuthContext } from '@/contexts/AuthContext';
import { useRouter } from 'next/router';
import { toast } from 'react-toastify';

export function useAuth() {
  const context = useContext(AuthContext);
  const router = useRouter();

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  const { user, login, logout, loading } = context;

  const handleLogin = useCallback(async (email: string, password: string) => {
    try {
      await login(email, password);
      toast.success('Successfully logged in!');
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Login failed');
      throw error;
    }
  }, [login]);

  const handleLogout = useCallback(async () => {
    try {
      await logout();
      router.push('/auth/login');
      toast.success('Successfully logged out!');
    } catch (error) {
      toast.error('Logout failed');
      throw error;
    }
  }, [logout, router]);

  const isAuthenticated = !!user;
  const isAdmin = user?.role === 'super_admin';
  const isSchoolAdmin = user?.role === 'school_admin';
  const isTeacher = user?.role === 'teacher';
  const isStudent = user?.role === 'student';

  return {
    user,
    loading,
    isAuthenticated,
    isAdmin,
    isSchoolAdmin,
    isTeacher,
    isStudent,
    login: handleLogin,
    logout: handleLogout,
  };
}