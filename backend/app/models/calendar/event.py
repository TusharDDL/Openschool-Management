from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from app.models.base import BaseModel

class EventType(str, Enum):
    ACADEMIC = "ACADEMIC"  # Classes, exams, etc.
    ADMINISTRATIVE = "ADMINISTRATIVE"  # Meetings, reviews, etc.
    CULTURAL = "CULTURAL"  # Celebrations, performances
    SPORTS = "SPORTS"  # Sports events, competitions
    HOLIDAY = "HOLIDAY"  # School holidays
    EXAM = "EXAM"  # Examinations
    ASSIGNMENT = "ASSIGNMENT"  # Assignment deadlines
    MEETING = "MEETING"  # Parent meetings, staff meetings
    OTHER = "OTHER"

class RecurrenceType(str, Enum):
    NONE = "NONE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    CUSTOM = "CUSTOM"

class EventStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    POSTPONED = "POSTPONED"

class Calendar(BaseModel):
    __tablename__ = "calendars"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'name', name='uq_calendar_name'),
        {'schema': 'calendar'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    school_id = Column(Integer, ForeignKey("public.schools.id", ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    color = Column(String)  # Hex color code
    is_primary = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON)  # Calendar-specific settings

    # Relationships
    tenant = relationship("Tenant")
    school = relationship("School")
    owner = relationship("User")
    events = relationship("Event", back_populates="calendar", cascade="all, delete-orphan")
    subscriptions = relationship("CalendarSubscription", back_populates="calendar", cascade="all, delete-orphan")

class Event(BaseModel):
    __tablename__ = "events"
    __table_args__ = {'schema': 'calendar'}

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    calendar_id = Column(Integer, ForeignKey("calendar.calendars.id", ondelete="CASCADE"), nullable=False)
    creator_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(SQLEnum(EventType), nullable=False)
    status = Column(SQLEnum(EventStatus), nullable=False, default=EventStatus.SCHEDULED)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    all_day = Column(Boolean, default=False)
    location = Column(String)
    virtual_meeting_link = Column(String)
    recurrence_type = Column(SQLEnum(RecurrenceType), default=RecurrenceType.NONE)
    recurrence_pattern = Column(JSON)  # For custom recurrence rules
    color = Column(String)  # Override calendar color
    is_public = Column(Boolean, default=True)
    requires_registration = Column(Boolean, default=False)
    max_participants = Column(Integer)
    reminder_before = Column(Integer)  # Minutes before event
    metadata = Column(JSON)  # Additional event data
    parent_event_id = Column(Integer, ForeignKey("calendar.events.id", ondelete="CASCADE"))  # For recurring events

    # Relationships
    tenant = relationship("Tenant")
    calendar = relationship("Calendar", back_populates="events")
    creator = relationship("User", foreign_keys=[creator_id])
    attendees = relationship("EventAttendee", back_populates="event", cascade="all, delete-orphan")
    resources = relationship("EventResource", back_populates="event", cascade="all, delete-orphan")
    attachments = relationship("EventAttachment", back_populates="event", cascade="all, delete-orphan")
    recurring_events = relationship("Event", backref=backref("parent_event", remote_side=[id]))

class EventAttendee(BaseModel):
    __tablename__ = "event_attendees"
    __table_args__ = (
        UniqueConstraint('event_id', 'user_id', name='uq_event_attendee'),
        {'schema': 'calendar'}
    )

    event_id = Column(Integer, ForeignKey("calendar.events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    response_status = Column(String)  # ACCEPTED, DECLINED, TENTATIVE, PENDING
    response_time = Column(DateTime)
    response_comment = Column(Text)
    is_organizer = Column(Boolean, default=False)
    is_optional = Column(Boolean, default=False)
    notification_sent = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)

    # Relationships
    event = relationship("Event", back_populates="attendees")
    user = relationship("User")

class EventResource(BaseModel):
    __tablename__ = "event_resources"
    __table_args__ = (
        UniqueConstraint('event_id', 'resource_id', name='uq_event_resource'),
        {'schema': 'calendar'}
    )

    event_id = Column(Integer, ForeignKey("calendar.events.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resource.resources.id", ondelete="CASCADE"), nullable=False)
    
    quantity = Column(Integer, default=1)
    notes = Column(Text)
    is_confirmed = Column(Boolean, default=False)

    # Relationships
    event = relationship("Event", back_populates="resources")
    resource = relationship("Resource")

class EventAttachment(BaseModel):
    __tablename__ = "event_attachments"
    __table_args__ = {'schema': 'calendar'}

    event_id = Column(Integer, ForeignKey("calendar.events.id", ondelete="CASCADE"), nullable=False)
    uploaded_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)

    # Relationships
    event = relationship("Event", back_populates="attachments")
    uploaded_by = relationship("User")

class CalendarSubscription(BaseModel):
    __tablename__ = "calendar_subscriptions"
    __table_args__ = (
        UniqueConstraint('calendar_id', 'user_id', name='uq_calendar_subscription'),
        {'schema': 'calendar'}
    )

    calendar_id = Column(Integer, ForeignKey("calendar.calendars.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    role = Column(String, nullable=False)  # OWNER, EDITOR, VIEWER
    color_override = Column(String)  # Personal color preference
    notification_preferences = Column(JSON)
    is_hidden = Column(Boolean, default=False)
    default_reminder = Column(Integer)  # Minutes before event

    # Relationships
    calendar = relationship("Calendar", back_populates="subscriptions")
    user = relationship("User")