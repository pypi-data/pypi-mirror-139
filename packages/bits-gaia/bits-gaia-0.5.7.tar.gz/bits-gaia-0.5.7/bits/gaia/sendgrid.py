# -*- coding: utf-8 -*-
"""SendGrid class for Gaia."""
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Attachment
from sendgrid.helpers.mail import ClickTracking
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import ContentId
from sendgrid.helpers.mail import Disposition
from sendgrid.helpers.mail import FileContent
from sendgrid.helpers.mail import FileName
from sendgrid.helpers.mail import FileType
from sendgrid.helpers.mail import From
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import MimeType
from sendgrid.helpers.mail import SendAt
from sendgrid.helpers.mail import Subject
from sendgrid.helpers.mail import To
from sendgrid.helpers.mail import TrackingSettings
# from sendgrid.helpers.mail import Email
# from sendgrid.helpers.mail import SendGridException


class SendGrid:
    """SendGrid class."""

    def __init__(self, api_key):
        """Initialize a class instance."""
        self.api_key = api_key
        self.client = SendGridAPIClient(api_key=api_key)

    @classmethod
    def add_pdf_attachment(
            cls,
            message,
            data,
            disposition="inline",
            domain="broadinstitute.org",
            file_name="file.pdf",
            file_type="application/pdf",
    ):
        """Add a PDF attachment to a message."""
        attachment = Attachment()
        attachment.content_id = ContentId(f"<{file_name}@{domain}>")
        attachment.disposition = Disposition(disposition)
        attachment.file_content = FileContent(base64.b64encode(data).decode())
        attachment.file_name = FileName(file_name)
        attachment.file_type = FileType(file_type)
        message.attachment = attachment
        return message

    # pylint: disable=too-many-arguments
    @classmethod
    def create_email_message(
            cls,
            from_email_address,
            from_email_name,
            to_email_addresses,
            subject,
            html_content=None,
            plain_text_content=None,
            send_at=None,
    ):
        """Return a Mail object that can be sent with Sendgrid."""
        message = Mail()

        # create the From address
        message.from_email = From(from_email_address, from_email_name)

        # create a list of To email address(es)
        to_emails = []
        for email in to_email_addresses:
            to_emails.append(To(email=email))
        message.to = to_emails

        # create Subject of the message
        message.subject = Subject(subject)

        # check the content
        if not html_content and not plain_text_content:
            raise ValueError("At least one of 'html_content' or 'plain_text_content' is required.")

        # create the content
        if html_content:
            message.content = Content(MimeType.html, html_content)
        if plain_text_content:
            message.plain_text_content = Content(MimeType.text, plain_text_content)

        # check send_at
        if send_at:
            message.send_at = SendAt(send_at)

        return message

    def disable_click_tracking(self, message):
        """Disable click tracking for a message."""
        tracking_settings = TrackingSettings()
        tracking_settings.click_tracking = ClickTracking(False, False)
        message.tracking_settings = tracking_settings
        return message

    def send_email_message(self, message):
        """Send an email message using Sendgrid."""
        try:
            response = self.client.send(message)
        except Exception as sendgrid_error:
            print(f"ERROR: Failed sending Sendgrid email: {sendgrid_error}")
            return None

        return response

    # def send_text_email(self, from_email, to_emails, subject, content):
    #     """Send a text email with sendgrid."""
    #     message = Mail(
    #         from_email=Email(from_email),
    #         to_emails=To(to_emails),
    #         subject=subject,
    #         plain_text_content=Content("text/plain", content),
    #     )
    #     return self.client.mail.send.post(request_body=message.get())
