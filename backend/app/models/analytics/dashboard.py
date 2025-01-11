from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum, Text, JSON, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class WidgetType(str, Enum):
    CHART = "CHART"
    TABLE = "TABLE"
    METRIC = "METRIC"
    LIST = "LIST"
    MAP = "MAP"
    CALENDAR = "CALENDAR"
    CUSTOM = "CUSTOM"

class ChartType(str, Enum):
    LINE = "LINE"
    BAR = "BAR"
    PIE = "PIE"
    DONUT = "DONUT"
    AREA = "AREA"
    SCATTER = "SCATTER"
    RADAR = "RADAR"
    HEATMAP = "HEATMAP"
    FUNNEL = "FUNNEL"
    GAUGE = "GAUGE"

class DataSourceType(str, Enum):
    ACADEMIC = "ACADEMIC"
    ATTENDANCE = "ATTENDANCE"
    FINANCIAL = "FINANCIAL"
    STAFF = "STAFF"
    LIBRARY = "LIBRARY"
    TRANSPORT = "TRANSPORT"
    HOSTEL = "HOSTEL"
    CUSTOM = "CUSTOM"

class Dashboard(BaseModel):
    __tablename__ = "dashboards"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_dashboard_code'),
        {'schema': 'analytics'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text)
    layout = Column(JSON)  # Grid layout configuration
    filters = Column(JSON)  # Global dashboard filters
    refresh_interval = Column(Integer)  # In seconds
    is_system = Column(Boolean, default=False)  # System dashboards can't be modified
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON)  # Dashboard-specific settings

    # Relationships
    tenant = relationship("Tenant")
    created_by = relationship("User")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")
    shares = relationship("DashboardShare", back_populates="dashboard", cascade="all, delete-orphan")

class DashboardWidget(BaseModel):
    __tablename__ = "dashboard_widgets"
    __table_args__ = {'schema': 'analytics'}

    dashboard_id = Column(Integer, ForeignKey("analytics.dashboards.id", ondelete="CASCADE"), nullable=False)
    datasource_id = Column(Integer, ForeignKey("analytics.data_sources.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String, nullable=False)
    widget_type = Column(SQLEnum(WidgetType), nullable=False)
    chart_type = Column(SQLEnum(ChartType))  # For chart widgets
    query = Column(Text)  # SQL query or API endpoint
    parameters = Column(JSON)  # Query parameters
    filters = Column(JSON)  # Widget-specific filters
    options = Column(JSON)  # Widget configuration options
    layout = Column(JSON)  # Position and size in grid
    refresh_interval = Column(Integer)  # Override dashboard interval
    is_visible = Column(Boolean, default=True)
    order = Column(Integer, default=0)

    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")
    datasource = relationship("DataSource", back_populates="widgets")

class DataSource(BaseModel):
    __tablename__ = "data_sources"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_datasource_code'),
        {'schema': 'analytics'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text)
    source_type = Column(SQLEnum(DataSourceType), nullable=False)
    connection_details = Column(JSON)  # Database connection or API details
    query_template = Column(Text)  # Base query template
    parameters = Column(JSON)  # Available parameters
    filters = Column(JSON)  # Available filters
    cache_duration = Column(Integer)  # Cache duration in seconds
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    widgets = relationship("DashboardWidget", back_populates="datasource")
    reports = relationship("SavedReport", back_populates="datasource")

class DashboardShare(BaseModel):
    __tablename__ = "dashboard_shares"
    __table_args__ = (
        UniqueConstraint('dashboard_id', 'user_id', name='uq_dashboard_share'),
        {'schema': 'analytics'}
    )

    dashboard_id = Column(Integer, ForeignKey("analytics.dashboards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    
    can_edit = Column(Boolean, default=False)
    can_share = Column(Boolean, default=False)
    expires_at = Column(DateTime)

    # Relationships
    dashboard = relationship("Dashboard", back_populates="shares")
    user = relationship("User")

class SavedReport(BaseModel):
    __tablename__ = "saved_reports"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'code', name='uq_report_code'),
        {'schema': 'analytics'}
    )

    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    datasource_id = Column(Integer, ForeignKey("analytics.data_sources.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text)
    query = Column(Text)
    parameters = Column(JSON)
    filters = Column(JSON)
    columns = Column(JSON)  # Column configurations
    sort_by = Column(JSON)  # Sorting configuration
    format_options = Column(JSON)  # Formatting options
    schedule = Column(JSON)  # Report schedule configuration
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    tenant = relationship("Tenant")
    created_by = relationship("User")
    datasource = relationship("DataSource", back_populates="reports")
    executions = relationship("ReportExecution", back_populates="report", cascade="all, delete-orphan")

class ReportExecution(BaseModel):
    __tablename__ = "report_executions"
    __table_args__ = {'schema': 'analytics'}

    report_id = Column(Integer, ForeignKey("analytics.saved_reports.id", ondelete="CASCADE"), nullable=False)
    executed_by_id = Column(Integer, ForeignKey("public.users.id", ondelete="SET NULL"))
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String, nullable=False)  # Running, Completed, Failed
    parameters = Column(JSON)
    filters = Column(JSON)
    row_count = Column(Integer)
    file_size = Column(Integer)
    file_format = Column(String)
    file_url = Column(String)
    error_message = Column(Text)

    # Relationships
    report = relationship("SavedReport", back_populates="executions")
    executed_by = relationship("User")