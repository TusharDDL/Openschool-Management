from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class BookCategory(str, Enum):
    TEXTBOOK = "TEXTBOOK"
    REFERENCE = "REFERENCE"
    FICTION = "FICTION"
    NON_FICTION = "NON_FICTION"
    MAGAZINE = "MAGAZINE"
    JOURNAL = "JOURNAL"
    OTHER = "OTHER"

class BookStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"
    RESERVED = "RESERVED"
    LOST = "LOST"
    DAMAGED = "DAMAGED"
    UNDER_REPAIR = "UNDER_REPAIR"
    WRITTEN_OFF = "WRITTEN_OFF"

class Book(BaseModel):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'isbn', name='uq_book_isbn'),
        {'schema': 'library'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String)
    edition = Column(String)
    publication_year = Column(Integer)
    category = Column(SQLEnum(BookCategory), nullable=False)
    subject = Column(String)
    description = Column(Text)
    price = Column(Float)
    location = Column(String)  # Physical location in library
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    is_reference = Column(Boolean, default=False)  # Reference books can't be issued
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    copies = relationship("BookCopy", back_populates="book", cascade="all, delete-orphan")

class BookCopy(BaseModel):
    __tablename__ = "book_copies"
    __table_args__ = (
        UniqueConstraint('book_id', 'accession_number', name='uq_book_copy'),
        {'schema': 'library'}
    )

    book_id = Column(Integer, ForeignKey("library.books.id", ondelete="CASCADE"), nullable=False)
    
    accession_number = Column(String, nullable=False)  # Unique identifier for each copy
    status = Column(SQLEnum(BookStatus), nullable=False, default=BookStatus.AVAILABLE)
    condition = Column(String)  # Good, Fair, Poor, etc.
    procurement_date = Column(Date)
    procurement_price = Column(Float)
    remarks = Column(Text)

    # Relationships
    book = relationship("Book", back_populates="copies")
    issues = relationship("BookIssue", back_populates="book_copy", cascade="all, delete-orphan")

class BookIssue(BaseModel):
    __tablename__ = "book_issues"
    __table_args__ = {'schema': 'library'}

    book_copy_id = Column(Integer, ForeignKey("library.book_copies.id", ondelete="CASCADE"), nullable=False)
    issued_to_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    issued_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    fine_amount = Column(Float, default=0.0)
    fine_paid = Column(Boolean, default=False)
    fine_payment_date = Column(Date)
    remarks = Column(Text)

    # Relationships
    book_copy = relationship("BookCopy", back_populates="issues")
    issued_to = relationship("User", foreign_keys=[issued_to_id])
    issued_by = relationship("User", foreign_keys=[issued_by_id])

class LibrarySettings(BaseModel):
    __tablename__ = "library_settings"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'school_id', name='uq_library_settings'),
        {'schema': 'library'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"), nullable=False)
    
    max_books_per_student = Column(Integer, nullable=False, default=2)
    max_books_per_teacher = Column(Integer, nullable=False, default=5)
    issue_duration_days = Column(Integer, nullable=False, default=14)
    fine_per_day = Column(Float, nullable=False, default=1.0)
    allow_renewals = Column(Boolean, default=True)
    max_renewals = Column(Integer, default=1)
    reservation_duration_days = Column(Integer, default=2)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")