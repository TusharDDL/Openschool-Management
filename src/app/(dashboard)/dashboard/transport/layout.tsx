// src/app/(dashboard)/dashboard/transport/layout.tsx

'use client'

import React from 'react'
import { TransportProvider } from '@/contexts/TransportContext'

interface TransportLayoutProps {
  children: React.ReactNode
}

export default function TransportLayout({ children }: TransportLayoutProps) {
  return (
    <TransportProvider>
      {children}
    </TransportProvider>
  )
}
