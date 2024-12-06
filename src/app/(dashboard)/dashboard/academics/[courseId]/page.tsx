// src/app/(dashboard)/dashboard/academics/[courseId]/page.tsx
'use client'

import CourseDetails from '@/components/academics/CourseDetails'

export default function CoursePage({ params }: { params: { courseId: string } }) {
  return <CourseDetails courseId={parseInt(params.courseId)} />
}