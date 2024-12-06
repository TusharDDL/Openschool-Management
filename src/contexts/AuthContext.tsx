'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/services/api';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: number;
  email: string;
  name?: string;
  role: 'super_admin' | 'school_admin' | 'teacher' | 'student';
  tenant_id: number;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
      }
      setUser(null);
      router.push('/login');
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        if (token) {
          const decoded = jwtDecode<User>(token);
          const currentTime = Date.now() / 1000;
          if ((decoded as any).exp && (decoded as any).exp < currentTime) {
            await logout();
            return;
          }
          setUser(decoded);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        await logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const getDashboardPath = (role: string): string => {
    const rolePathMap: Record<string, string> = {
      super_admin: '/dashboard/admin',
      school_admin: '/dashboard/school',
      teacher: '/dashboard/teacher',
      student: '/dashboard/student',
    };
    return rolePathMap[role] || '/dashboard';
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      const { access_token } = response;
      
      if (!access_token) {
        throw new Error('No access token received');
      }

      localStorage.setItem('token', access_token);
      const decoded = jwtDecode<User>(access_token);
      setUser(decoded);
      
      const dashboardPath = getDashboardPath(decoded.role);
      router.push(dashboardPath);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}