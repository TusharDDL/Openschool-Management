from typing import List, Dict, Any
from celery import shared_task
from app.core.config import settings
from app.tasks.base import BaseTask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class EmailTemplate:
    @staticmethod
    def render(template_name: str, context: Dict[str, Any]) -> str:
        # In production, load templates from files
        templates = {
            "welcome": """
                <h1>Welcome to {{ school_name }}!</h1>
                <p>Dear {{ name }},</p>
                <p>Your account has been successfully created.</p>
                <p>Your login credentials:</p>
                <ul>
                    <li>Email: {{ email }}</li>
                    <li>Password: {{ password }}</li>
                </ul>
                <p>Please change your password after first login.</p>
            """,
            "reset_password": """
                <h1>Password Reset Request</h1>
                <p>Dear {{ name }},</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{{ reset_link }}">Reset Password</a></p>
                <p>If you didn't request this, please ignore this email.</p>
            """,
            "notification": """
                <h1>{{ title }}</h1>
                <p>Dear {{ name }},</p>
                <p>{{ message }}</p>
            """
        }
        template = Template(templates.get(template_name, ""))
        return template.render(**context)

@shared_task(
    bind=True,
    base=BaseTask,
    name="send_email",
    max_retries=3,
    default_retry_delay=60,  # 1 minute
)
def send_email(
    self,
    to_email: str | List[str],
    subject: str,
    template_name: str,
    context: Dict[str, Any],
    cc: List[str] = None,
    bcc: List[str] = None,
) -> bool:
    try:
        # Convert single email to list
        to_emails = [to_email] if isinstance(to_email, str) else to_email
        cc = cc or []
        bcc = bcc or []

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = ", ".join(to_emails)
        if cc:
            msg["Cc"] = ", ".join(cc)
        if bcc:
            msg["Bcc"] = ", ".join(bcc)

        # Render template
        html_content = EmailTemplate.render(template_name, context)
        msg.attach(MIMEText(html_content, "html"))

        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            
            server.send_message(msg)

        logger.info(
            f"Email sent successfully to {to_emails}",
            extra={
                "subject": subject,
                "template": template_name,
                "recipients": to_emails,
                "cc": cc,
                "bcc": bcc,
            },
        )
        return True

    except Exception as e:
        logger.error(
            f"Failed to send email: {str(e)}",
            extra={
                "subject": subject,
                "template": template_name,
                "recipients": to_emails,
                "cc": cc,
                "bcc": bcc,
                "error": str(e),
            },
        )
        raise self.retry(exc=e)

@shared_task(
    bind=True,
    base=BaseTask,
    name="send_bulk_email",
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
)
def send_bulk_email(
    self,
    recipients: List[Dict[str, Any]],
    subject: str,
    template_name: str,
) -> Dict[str, int]:
    """
    Send bulk emails with personalized content
    
    recipients format:
    [
        {
            "email": "user@example.com",
            "context": {"name": "John", "message": "Hello"}
        }
    ]
    """
    results = {"success": 0, "failed": 0}
    
    for recipient in recipients:
        try:
            send_email.delay(
                to_email=recipient["email"],
                subject=subject,
                template_name=template_name,
                context=recipient["context"],
            )
            results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            logger.error(
                f"Failed to queue email for {recipient['email']}: {str(e)}",
                extra={
                    "recipient": recipient,
                    "subject": subject,
                    "template": template_name,
                    "error": str(e),
                },
            )
    
    return results