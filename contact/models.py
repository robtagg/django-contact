from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone


class Department(models.Model):
    """
    Stores a department object in the database
    """

    label = models.CharField(max_length=255)
    recipients = models.CharField(
        max_length=255, help_text="Seperate multiple addresses with a comma"
    )

    def __str__(self):
        return self.label

    @property
    def email_recipients(self):
        """
        Returns the recipients as a list
        """
        return self.recipients.split(",")

    def save(self, *args, **kwargs):
        # clean spaces from the recipients field
        self.recipients = self.recipients.replace(" ", "")
        super().save(*args, **kwargs)


class Message(models.Model):
    """
    Stores a contact message object in the database
    """

    name = models.CharField(max_length=255)
    email_address = models.EmailField()
    message = models.TextField()
    department = models.ForeignKey(
        to="contact.Department", related_name="messages", on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name}"

    def send_email(self):
        """
        Send an email to the admins, notifying of the new contact message
        """
        return EmailMultiAlternatives(
            subject=getattr(settings, "CONTACT_EMAIL_SUBJECT", "New contact message"),
            body=render_to_string(
                getattr(
                    settings, "CONTACT_EMAIL_TEMPLATE", "contact/email/email_notification.txt"
                ),
                context={"obj": self},
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.department.email_recipients,
        ).send()
