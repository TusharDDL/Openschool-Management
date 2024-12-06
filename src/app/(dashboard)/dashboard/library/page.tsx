'use client'

import React, { useState } from 'react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BookOpen, Search, PlusCircle, Edit2, Trash2 } from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { toast } from '@/hooks/use-toast'
import { Label } from '@/components/ui/label'

interface Book {
  id: string
  title: string
  author: string
  isbn: string
  category: string
  status: 'available' | 'issued' | 'lost'
  dueDate?: string
  issuedTo?: string
  addedDate: string
}

const CATEGORIES = [
  { value: 'Textbook', label: 'Textbook' },
  { value: 'Fiction', label: 'Fiction' },
  { value: 'Non-Fiction', label: 'Non-Fiction' },
  { value: 'Reference', label: 'Reference' },
  { value: 'Magazine', label: 'Magazine' },
  { value: 'Other', label: 'Other' }
]

const INITIAL_BOOKS: Book[] = [
  {
    id: "1",
    title: "Mathematics Grade 10",
    author: "John Smith",
    isbn: "9781234567890",
    category: "Textbook",
    status: "available",
    addedDate: "2024-01-01"
  },
  {
    id: "2",
    title: "Physics Fundamentals",
    author: "Sarah Johnson",
    isbn: "9789876543210",
    category: "Textbook",
    status: "issued",
    dueDate: "2024-02-01",
    issuedTo: "Alex Brown",
    addedDate: "2024-01-01"
  }
]

export default function LibraryPage() {
  const [books, setBooks] = useState<Book[]>(INITIAL_BOOKS)
  const [searchTerm, setSearchTerm] = useState('')
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [selectedBook, setSelectedBook] = useState<Book | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    isbn: '',
    category: 'Textbook'
  })

  const resetFormData = () => {
    setFormData({
      title: '',
      author: '',
      isbn: '',
      category: 'Textbook'
    })
  }

  const handleAddBook = () => {
    if (!formData.title || !formData.author || !formData.isbn) {
      toast({
        title: "Error",
        description: "Please fill in all required fields",
        variant: "destructive",
      })
      return
    }

    const newBook: Book = {
      id: Date.now().toString(),
      ...formData,
      status: 'available',
      addedDate: new Date().toISOString().split('T')[0]
    }

    setBooks(prev => [...prev, newBook])
    setIsAddDialogOpen(false)
    resetFormData()
    toast({
      title: "Success",
      description: "Book added successfully",
    })
  }

  const handleEditInit = (book: Book) => {
    setSelectedBook(book)
    setFormData({
      title: book.title,
      author: book.author,
      isbn: book.isbn,
      category: book.category
    })
    setIsEditDialogOpen(true)
  }

  const handleEditBook = () => {
    if (!selectedBook) return

    if (!formData.title || !formData.author || !formData.isbn) {
      toast({
        title: "Error",
        description: "Please fill in all required fields",
        variant: "destructive",
      })
      return
    }

    const updatedBooks = books.map(book => 
      book.id === selectedBook.id 
        ? { ...book, ...formData }
        : book
    )

    setBooks(updatedBooks)
    setIsEditDialogOpen(false)
    setSelectedBook(null)
    resetFormData()
    toast({
      title: "Success",
      description: "Book updated successfully",
    })
  }

  const handleDeleteBook = (id: string) => {
    if (window.confirm('Are you sure you want to delete this book?')) {
      setBooks(prev => prev.filter(book => book.id !== id))
      toast({
        title: "Success",
        description: "Book deleted successfully",
      })
    }
  }

  const handleIssueReturn = (book: Book) => {
    if (book.status === 'available') {
      const studentName = prompt('Enter student name:')
      if (!studentName) return

      const dueDate = new Date()
      dueDate.setDate(dueDate.getDate() + 14)

      const updatedBooks = books.map(b =>
        b.id === book.id
          ? {
              ...b,
              status: 'issued' as const,
              issuedTo: studentName,
              dueDate: dueDate.toISOString().split('T')[0]
            }
          : b
      )
      setBooks(updatedBooks)
      toast({
        title: "Success",
        description: `Book issued to ${studentName}`,
      })
    } else {
      const updatedBooks = books.map(b =>
        b.id === book.id
          ? {
              ...b,
              status: 'available' as const,
              issuedTo: undefined,
              dueDate: undefined
            }
          : b
      )
      setBooks(updatedBooks)
      toast({
        title: "Success",
        description: "Book returned successfully",
      })
    }
  }

  const filteredBooks = books.filter(book =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
    book.isbn.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="flex flex-col gap-5 p-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Library Management</h2>
          <p className="text-muted-foreground">
            Manage and track your library inventory
          </p>
        </div>
        <Button onClick={() => setIsAddDialogOpen(true)}>
          <PlusCircle className="mr-2 h-4 w-4" /> Add Book
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="p-4">
          <div className="flex items-center gap-4">
            <BookOpen className="h-6 w-6" />
            <div>
              <p className="text-sm font-medium text-muted-foreground">Total Books</p>
              <p className="text-2xl font-bold">{books.length}</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-4">
            <BookOpen className="h-6 w-6 text-green-500" />
            <div>
              <p className="text-sm font-medium text-muted-foreground">Available</p>
              <p className="text-2xl font-bold">
                {books.filter(b => b.status === 'available').length}
              </p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-4">
            <BookOpen className="h-6 w-6 text-yellow-500" />
            <div>
              <p className="text-sm font-medium text-muted-foreground">Issued</p>
              <p className="text-2xl font-bold">
                {books.filter(b => b.status === 'issued').length}
              </p>
            </div>
          </div>
        </Card>
      </div>

      <div className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search books..."
            className="pl-8"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="h-12 px-4 text-left align-middle font-medium">Title</th>
                <th className="h-12 px-4 text-left align-middle font-medium">Author</th>
                <th className="h-12 px-4 text-left align-middle font-medium">ISBN</th>
                <th className="h-12 px-4 text-left align-middle font-medium">Category</th>
                <th className="h-12 px-4 text-left align-middle font-medium">Status</th>
                <th className="h-12 px-4 text-left align-middle font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredBooks.map((book) => (
                <tr key={book.id} className="border-b">
                  <td className="p-4 align-middle">{book.title}</td>
                  <td className="p-4 align-middle">{book.author}</td>
                  <td className="p-4 align-middle">{book.isbn}</td>
                  <td className="p-4 align-middle">{book.category}</td>
                  <td className="p-4 align-middle">
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        book.status === 'available'
                          ? 'bg-green-100 text-green-800'
                          : book.status === 'issued'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {book.status}
                    </span>
                  </td>
                  <td className="p-4 align-middle">
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleIssueReturn(book)}
                      >
                        {book.status === 'available' ? 'Issue' : 'Return'}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEditInit(book)}
                      >
                        <Edit2 className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteBook(book.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Book</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                placeholder="Enter book title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="author">Author</Label>
              <Input
                id="author"
                placeholder="Enter author name"
                value={formData.author}
                onChange={(e) => setFormData(prev => ({ ...prev, author: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="isbn">ISBN</Label>
              <Input
                id="isbn"
                placeholder="Enter ISBN"
                value={formData.isbn}
                onChange={(e) => setFormData(prev => ({ ...prev, isbn: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="category">Category</Label>
              <Select 
                value={formData.category}
                onValueChange={(value) => setFormData(prev => ({ ...prev, category: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORIES.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAddBook}>Add Book</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Book</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="edit-title">Title</Label>
              <Input
                id="edit-title"
                placeholder="Enter book title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-author">Author</Label>
              <Input
                id="edit-author"
                placeholder="Enter author name"
                value={formData.author}
                onChange={(e) => setFormData(prev => ({ ...prev, author: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-isbn">ISBN</Label>
              <Input
                id="edit-isbn"
                placeholder="Enter ISBN"
                value={formData.isbn}
                onChange={(e) => setFormData(prev => ({ ...prev, isbn: e.target.value }))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-category">Category</Label>
              <Select
                value={formData.category}
                onValueChange={(value) => setFormData(prev => ({ ...prev, category: value }))}
                >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {CATEGORIES.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      {category.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleEditBook}>Save Changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}