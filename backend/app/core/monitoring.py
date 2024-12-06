import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from prometheus_client import Counter, Histogram, generate_latest
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

DB_QUERY_LATENCY = Histogram(
    'db_query_duration_seconds',
    'Database query latency',
    ['operation', 'table']
)

CACHE_HITS = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

class RequestResponseMiddleware:
    async def __call__(
        self,
        request: Request,
        call_next: Any
    ) -> Response:
        start_time = datetime.utcnow()
        
        # Extract request details
        method = request.method
        url = request.url.path
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        
        # Remove sensitive data
        if headers.get("authorization"):
            headers["authorization"] = "[REDACTED]"
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            # Update metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=url,
                status=response.status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=method,
                endpoint=url
            ).observe(duration)
            
            # Log request details
            log_data = {
                "timestamp": start_time.isoformat(),
                "method": method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration": duration,
                "headers": headers,
                "query_params": query_params,
                "client_ip": request.client.host,
                "school_id": getattr(request.state, "school_id", None)
            }
            
            logger.info(f"Request processed: {json.dumps(log_data)}")
            
            return response
            
        except Exception as e:
            # Log error details
            error_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "method": method,
                "url": str(request.url),
                "error": str(e),
                "headers": headers,
                "query_params": query_params,
                "client_ip": request.client.host,
                "school_id": getattr(request.state, "school_id", None)
            }
            
            logger.error(f"Request failed: {json.dumps(error_data)}")
            raise

def setup_monitoring(app: Any) -> None:
    """Set up monitoring for the application"""
    
    # Configure OpenTelemetry
    trace.set_tracer_provider(TracerProvider())
    otlp_exporter = OTLPSpanExporter(endpoint=settings.OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument()
    
    # Instrument Redis
    RedisInstrumentor().instrument()
    
    # Add middleware
    app.middleware("http")(RequestResponseMiddleware())
    
    # Add metrics endpoint
    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type="text/plain"
        )

class QueryLogger:
    """Log and track database queries"""
    
    def log_query(
        self,
        operation: str,
        table: str,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        duration: Optional[float] = None
    ) -> None:
        # Update metrics
        if duration:
            DB_QUERY_LATENCY.labels(
                operation=operation,
                table=table
            ).observe(duration)
        
        # Log query details
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "table": table,
            "query": query,
            "params": params,
            "duration": duration
        }
        
        logger.info(f"Database query: {json.dumps(log_data)}")

class CacheLogger:
    """Log and track cache operations"""
    
    def log_operation(
        self,
        operation: str,
        key: str,
        hit: bool,
        duration: Optional[float] = None
    ) -> None:
        # Update metrics
        if hit:
            CACHE_HITS.labels(cache_type="redis").inc()
        else:
            CACHE_MISSES.labels(cache_type="redis").inc()
        
        # Log operation details
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "key": key,
            "hit": hit,
            "duration": duration
        }
        
        logger.info(f"Cache operation: {json.dumps(log_data)}")

query_logger = QueryLogger()
cache_logger = CacheLogger()