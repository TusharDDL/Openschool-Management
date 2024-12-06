// src/types/layout.ts
import { type ElementType } from 'react'

export interface SidebarItem {
  icon: ElementType
  label: string
  href: string
}

export interface NavbarProps {
  onMenuClick: () => void
}