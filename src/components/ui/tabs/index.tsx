// src/components/ui/tabs/index.tsx
'use client';

import * as RadixTabs from '@radix-ui/react-tabs';
import React from 'react';
import './tabs.css'; // Create this CSS file for styling

interface TabsProps extends RadixTabs.TabsProps {}

export const Tabs = RadixTabs.Root;
export const TabsList = RadixTabs.List;
export const TabsTrigger = RadixTabs.Trigger;
export const TabsContent = RadixTabs.Content;
