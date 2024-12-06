// src/app/(dashboard)/dashboard/communication/page.tsx

'use client'

import React, { ChangeEvent } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { 
  MessageSquare, Bell, Mail, Search 
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'

// TypeScript Types for Translations
type TranslationKeys = {
  compose: string
  announcement: string
  notice: string
  emergency: string
  subject: string
  content: string
  send: string
  cancel: string
  search: string
  recipients: string
  selectRecipients: string
  totalMessages: string
  announcements: string
  notices: string
  messageHistory: string
  allTypes: string
  allCategories: string
  category: string
  priority: string
  highPriority: string
  mediumPriority: string
  lowPriority: string
  noMessages: string
  type: string // Added 'type' key
}

const translations: Record<Language, TranslationKeys> = {
  en: {
    compose: 'Compose Message',
    announcement: 'Announcement',
    notice: 'Notice',
    emergency: 'Emergency',
    subject: 'Subject',
    content: 'Content',
    send: 'Send',
    cancel: 'Cancel',
    search: 'Search messages...',
    recipients: 'Recipients',
    selectRecipients: 'Select Recipients',
    totalMessages: 'Total Messages',
    announcements: 'Announcements',
    notices: 'Notices',
    messageHistory: 'Message History',
    allTypes: 'All Types',
    allCategories: 'All Categories',
    category: 'Category',
    priority: 'Priority',
    highPriority: 'High Priority',
    mediumPriority: 'Medium Priority',
    lowPriority: 'Low Priority',
    noMessages: 'No messages found.',
    type: 'Type', // Added 'type' key
  },
  hi: {
    compose: 'संदेश लिखें',
    announcement: 'घोषणा',
    notice: 'सूचना',
    emergency: 'आपातकालीन',
    subject: 'विषय',
    content: 'संदेश',
    send: 'भेजें',
    cancel: 'रद्द करें',
    search: 'संदेश खोजें...',
    recipients: 'प्राप्तकर्ता',
    selectRecipients: 'प्राप्तकर्ता चुनें',
    totalMessages: 'कुल संदेश',
    announcements: 'घोषणाएं',
    notices: 'सूचनाएं',
    messageHistory: 'संदेश इतिहास',
    allTypes: 'सभी प्रकार',
    allCategories: 'सभी श्रेणियां',
    category: 'श्रेणी',
    priority: 'प्राथमिकता',
    highPriority: 'उच्च प्राथमिकता',
    mediumPriority: 'मध्यम प्राथमिकता',
    lowPriority: 'कम प्राथमिकता',
    noMessages: 'कोई संदेश नहीं मिला।',
    type: 'प्रकार', // Added 'type' key
  },
  bn: {
    compose: 'বার্তা লিখুন',
    announcement: 'ঘোষণা',
    notice: 'বিজ্ঞপ্তি',
    emergency: 'জরুরি',
    subject: 'বিষয়',
    content: 'বার্তা',
    send: 'পাঠান',
    cancel: 'বাতিল',
    search: 'বার্তা খুঁজুন...',
    recipients: 'প্রাপকের',
    selectRecipients: 'প্রাপক নির্বাচন করুন',
    totalMessages: 'মোট বার্তা',
    announcements: 'ঘোষণা',
    notices: 'বিজ্ঞপ্তি',
    messageHistory: 'বার্তা ইতিহাস',
    allTypes: 'সমস্ত ধরণ',
    allCategories: 'সমস্ত বিভাগ',
    category: 'বিভাগ',
    priority: 'অগ্রাধিকার',
    highPriority: 'উচ্চ অগ্রাধিকার',
    mediumPriority: 'মাঝারি অগ্রাধিকার',
    lowPriority: 'নিম্ন অগ্রাধিকার',
    noMessages: 'কোন বার্তা পাওয়া যায়নি।',
    type: 'ধরন', // Added 'type' key
  }
}

type Language = 'en' | 'hi' | 'bn'

interface Message {
  id: string
  subject: string
  content: string
  type: 'announcement' | 'notice' | 'emergency'
  recipients: string[]
  sentAt: string
  sender: string
  status: 'sent' | 'scheduled'
  readBy?: number
  category?: 'academic' | 'administrative' | 'exam' | 'fee' | 'holiday' | 'event'
  priority?: 'high' | 'medium' | 'low'
}

interface MessageFormData {
  subject: string
  content: string
  type: 'announcement' | 'notice' | 'emergency'
  recipients: string // Comma-separated string
  category: 'academic' | 'administrative' | 'exam' | 'fee' | 'holiday' | 'event'
  priority: 'high' | 'medium' | 'low'
}

const INITIAL_MESSAGES: Message[] = [
  {
    id: '1',
    subject: 'Parent-Teacher Meeting (PTM)',
    content: 'वार्षिक पीटीएम अगले शनिवार को निर्धारित है / Annual PTM is scheduled for next Saturday',
    type: 'announcement',
    recipients: ['All Parents'],
    sentAt: '2024-01-15',
    sender: 'Principal',
    status: 'sent',
    readBy: 145,
    category: 'academic',
    priority: 'high'
  },
  {
    id: '2',
    subject: 'Fee Due Reminder / शुल्क बकाया अनुस्मारक',
    content: 'कृपया बकाया शुल्क जमा करें / Please clear pending fees',
    type: 'notice',
    recipients: ['Class 10 Parents'],
    sentAt: '2024-01-16',
    sender: 'Accounts',
    status: 'sent',
    readBy: 42,
    category: 'fee',
    priority: 'medium'
  }
]

const CATEGORIES = [
  { value: 'academic', label: 'Academic/शैक्षणिक/একাডেমিক' },
  { value: 'administrative', label: 'Administrative/प्रशासनिक/প্রশাসনিক' },
  { value: 'exam', label: 'Examination/परीक्षा/পরীক্ষা' },
  { value: 'fee', label: 'Fees/शुल्क/ফি' },
  { value: 'holiday', label: 'Holiday/अवकाश/ছুটি' },
  { value: 'event', label: 'Event/कार्यक्रम/ইভেন্ট' }
]

export default function CommunicationPage() {
  const [messages, setMessages] = React.useState<Message[]>(INITIAL_MESSAGES)
  const [isComposeOpen, setIsComposeOpen] = React.useState(false)
  const [searchTerm, setSearchTerm] = React.useState('')
  const [selectedType, setSelectedType] = React.useState('')
  const [selectedCategory, setSelectedCategory] = React.useState('')
  const [currentLang, setCurrentLang] = React.useState<Language>('en')
  const [formData, setFormData] = React.useState<MessageFormData>({
    subject: '',
    content: '',
    type: 'announcement',
    recipients: '',
    category: 'academic',
    priority: 'medium'
  })
  const { toast } = useToast()

  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSendMessage = async () => {
    try {
      if (!formData.subject || !formData.content || !formData.recipients) {
        toast({
          title: currentLang === 'en' ? "Error" : currentLang === 'hi' ? "त्रुटि" : "ত্রুটি",
          description: currentLang === 'en' ? "Please fill all required fields" 
            : currentLang === 'hi' ? "कृपया सभी आवश्यक फ़ील्ड भरें" 
            : "অনুগ্রহ করে সমস্ত প্রয়োজনীয় ক্ষেত্র পূরণ করুন",
          variant: "destructive"
        })
        return
      }

      const recipientList = formData.recipients.split(',').map(r => r.trim()).filter(r => r !== '')

      const newMessage: Message = {
        id: Date.now().toString(),
        subject: formData.subject,
        content: formData.content,
        type: formData.type,
        recipients: recipientList.length > 0 ? recipientList : ['All'],
        sentAt: new Date().toISOString().split('T')[0],
        sender: 'Admin',
        status: 'sent',
        readBy: 0,
        category: formData.category,
        priority: formData.priority
      }

      setMessages(prev => [newMessage, ...prev])
      setIsComposeOpen(false)
      setFormData({
        subject: '',
        content: '',
        type: 'announcement',
        recipients: '',
        category: 'academic',
        priority: 'medium'
      })

      toast({
        title: currentLang === 'en' ? "Success" : currentLang === 'hi' ? "सफलता" : "সাফল্য",
        description: currentLang === 'en' ? "Message sent successfully" 
          : currentLang === 'hi' ? "संदेश सफलतापूर्वक भेजा गया" 
          : "বার্তা সফলভাবে পাঠানো হয়েছে",
        variant: "default"
      })
    } catch (error) {
      toast({
        title: currentLang === 'en' ? "Error" : currentLang === 'hi' ? "त्रुटि" : "ত্রুটি",
        description: currentLang === 'en' ? "Failed to send message" 
          : currentLang === 'hi' ? "संदेश भेजने में विफल" 
          : "বার্তা পাঠাতে ব্যর্থ",
        variant: "destructive"
      })
    }
  }

  const getMessagePriorityStyle = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredMessages = messages.filter(message => {
    const matchesSearch = 
      message.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
      message.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = selectedType ? message.type === selectedType : true
    const matchesCategory = selectedCategory ? message.category === selectedCategory : true
    return matchesSearch && matchesType && matchesCategory
  })

  const stats = {
    totalMessages: messages.length,
    announcements: messages.filter(m => m.type === 'announcement').length,
    notices: messages.filter(m => m.type === 'notice').length,
    emergency: messages.filter(m => m.type === 'emergency').length
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header Section */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {currentLang === 'en' ? 'Communication' : currentLang === 'hi' ? 'संचार' : 'যোগাযোগ'}
          </h1>
          <p className="text-muted-foreground">
            {currentLang === 'en' ? 'Manage school-wide communications and announcements' 
              : currentLang === 'hi' ? 'स्कूल-व्यापी संचार और घोषणाएं प्रबंधित करें' 
              : 'স্কুল-ব্যাপী যোগাযোগ এবং ঘোষণা পরিচালনা করুন'}
          </p>
        </div>
        <div className="flex gap-4">
          <select
            value={currentLang}
            onChange={(e) => setCurrentLang(e.target.value as Language)}
            className="px-2 py-1 border rounded-md"
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="bn">বাংলা</option>
          </select>
          <Button
            onClick={() => setIsComposeOpen(true)}
            className="flex items-center gap-2"
          >
            <MessageSquare className="h-4 w-4" />
            {translations[currentLang].compose}
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <StatsCard
          title={translations[currentLang].totalMessages}
          value={stats.totalMessages}
          icon={<MessageSquare className="h-4 w-4 text-muted-foreground" />}
        />
        <StatsCard
          title={translations[currentLang].announcements}
          value={stats.announcements}
          icon={<Bell className="h-4 w-4 text-blue-500" />}
        />
        <StatsCard
          title={translations[currentLang].notices}
          value={stats.notices}
          icon={<Mail className="h-4 w-4 text-yellow-500" />}
        />
        <StatsCard
          title={translations[currentLang].emergency}
          value={stats.emergency}
          icon={<Bell className="h-4 w-4 text-red-500" />}
        />
      </div>

      {/* Message List */}
      <Card>
        <CardHeader>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <CardTitle>{translations[currentLang].messageHistory}</CardTitle>
            <div className="flex gap-4">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder={translations[currentLang].search}
                  value={searchTerm}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setSearchTerm(e.target.value)}
                  className="pl-8"
                />
              </div>
              <select
                value={selectedType}
                onChange={(e: ChangeEvent<HTMLSelectElement>) => setSelectedType(e.target.value)}
                className="px-4 py-2 border rounded-md"
              >
                <option value="">{translations[currentLang].allTypes}</option>
                <option value="announcement">{translations[currentLang].announcement}</option>
                <option value="notice">{translations[currentLang].notice}</option>
                <option value="emergency">{translations[currentLang].emergency}</option>
              </select>
              <select
                value={selectedCategory}
                onChange={(e: ChangeEvent<HTMLSelectElement>) => setSelectedCategory(e.target.value)}
                className="px-4 py-2 border rounded-md"
              >
                <option value="">{translations[currentLang].allCategories}</option>
                {CATEGORIES.map(cat => (
                  <option key={cat.value} value={cat.value}>{cat.label}</option>
                ))}
              </select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredMessages.length > 0 ? (
              filteredMessages.map((message) => (
                <MessageCard
                  key={message.id}
                  message={message}
                  currentLang={currentLang}
                  priorityStyle={getMessagePriorityStyle}
                  translations={translations}
                />
              ))
            ) : (
              <p className="text-center text-muted-foreground">
                {translations[currentLang].noMessages}
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Compose Dialog */}
      <ComposeDialog
        isOpen={isComposeOpen}
        onClose={() => setIsComposeOpen(false)}
        formData={formData}
        handleInputChange={handleInputChange}
        handleSendMessage={handleSendMessage}
        currentLang={currentLang}
        translations={translations}
      />
    </div>
  )
}

// Separate components for better organization

const StatsCard = ({ title, value, icon }: { title: string, value: number, icon: React.ReactNode }) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
      <CardTitle className="text-sm font-medium">{title}</CardTitle>
      {icon}
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
    </CardContent>
  </Card>
)

interface MessageCardProps { 
  message: Message
  currentLang: Language
  priorityStyle: (priority: string) => string
  translations: Record<Language, TranslationKeys>
}

const MessageCard = ({ 
  message, 
  currentLang, 
  priorityStyle,
  translations
}: MessageCardProps) => (
  <Card key={message.id} className="p-4">
    <div className="flex justify-between items-start">
      <div>
        <h3 className="font-semibold">{message.subject}</h3>
        <p className="text-sm text-muted-foreground mt-1">
          {message.content}
        </p>
        <div className="flex flex-wrap gap-2 mt-2">
          <span className="text-xs text-muted-foreground">
            {currentLang === 'en' ? 'Sent by' 
              : currentLang === 'hi' ? 'भेजने वाला' 
              : 'পাঠানো হয়েছে দ্বারা'}: {message.sender}
          </span>
          <span className="text-xs text-muted-foreground">
            {currentLang === 'en' ? 'Date' 
              : currentLang === 'hi' ? 'दिनांक' 
              : 'তারিখ'}: {message.sentAt}
          </span>
          {message.readBy !== undefined && (
            <span className="text-xs text-muted-foreground">
              {currentLang === 'en' ? 'Read by' 
                : currentLang === 'hi' ? 'पढ़ा गया' 
                : 'পড়েছেন'}: {message.readBy}
            </span>
          )}
        </div>
      </div>
      <div className="flex flex-col gap-2 items-end">
        <div className="flex gap-2">
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
            message.type === 'emergency' 
              ? 'bg-red-100 text-red-800'
              : message.type === 'announcement'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-gray-100 text-gray-800'
          }`}>
            {translations[currentLang][message.type]}
          </span>
          {message.priority && (
            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${priorityStyle(message.priority)}`}>
              {message.priority.toUpperCase()}
            </span>
          )}
        </div>
        <div className="flex gap-2">
          {message.recipients.map((recipient, index) => (
            <span key={index} className="text-xs text-muted-foreground">
              {recipient}
              {index < message.recipients.length - 1 && ','}
            </span>
          ))}
        </div>
      </div>
    </div>
  </Card>
)

interface ComposeDialogProps {
  isOpen: boolean
  onClose: () => void
  formData: MessageFormData
  handleInputChange: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => void
  handleSendMessage: () => void
  currentLang: Language
  translations: Record<Language, TranslationKeys>
}

const ComposeDialog = ({
  isOpen,
  onClose,
  formData,
  handleInputChange,
  handleSendMessage,
  currentLang,
  translations
}: ComposeDialogProps) => (
  <Dialog open={isOpen} onOpenChange={(open) => { if (!open) onClose() }}>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{translations[currentLang].compose}</DialogTitle>
      </DialogHeader>
      <div className="grid gap-4 py-4">
        <div className="grid gap-2">
          <label htmlFor="subject" className="text-sm font-medium">
            {translations[currentLang].subject}
          </label>
          <Input
            id="subject"
            name="subject"
            placeholder={translations[currentLang].subject}
            value={formData.subject}
            onChange={handleInputChange}
          />
        </div>
        <div className="grid gap-2">
          <label htmlFor="content" className="text-sm font-medium">
            {translations[currentLang].content}
          </label>
          <Textarea
            id="content"
            name="content"
            placeholder={translations[currentLang].content}
            value={formData.content}
            onChange={handleInputChange}
            rows={4}
          />
        </div>
        <div className="grid gap-2">
          <label htmlFor="recipients" className="text-sm font-medium">
            {translations[currentLang].recipients}
          </label>
          <Input
            id="recipients"
            name="recipients"
            placeholder={
              currentLang === 'en' 
                ? "Enter recipients separated by commas" 
                : currentLang === 'hi' 
                ? "प्राप्तकर्ताओं को अल्पविराम से अलग करें" 
                : "কমা দ্বারা আলাদা করে প্রাপকদের লিখুন"
            }
            value={formData.recipients}
            onChange={handleInputChange}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="grid gap-2">
            <label htmlFor="type" className="text-sm font-medium">
              {translations[currentLang].type}
            </label>
            <select
              id="type"
              name="type"
              value={formData.type}
              onChange={handleInputChange}
              className="px-4 py-2 border rounded-md"
            >
              <option value="announcement">{translations[currentLang].announcement}</option>
              <option value="notice">{translations[currentLang].notice}</option>
              <option value="emergency">{translations[currentLang].emergency}</option>
            </select>
          </div>
          <div className="grid gap-2">
            <label htmlFor="category" className="text-sm font-medium">
              {translations[currentLang].category}
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              className="px-4 py-2 border rounded-md"
            >
              {CATEGORIES.map(cat => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="grid gap-2">
          <label htmlFor="priority" className="text-sm font-medium">
            {translations[currentLang].priority}
          </label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleInputChange}
            className="px-4 py-2 border rounded-md"
          >
            <option value="high">{translations[currentLang].highPriority}</option>
            <option value="medium">{translations[currentLang].mediumPriority}</option>
            <option value="low">{translations[currentLang].lowPriority}</option>
          </select>
        </div>
      </div>
      <DialogFooter>
        <Button variant="outline" onClick={onClose}>
          {translations[currentLang].cancel}
        </Button>
        <Button onClick={handleSendMessage}>
          {translations[currentLang].send}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
)
