from django import forms
from django.conf import settings

from . import models


class ContactForm(forms.ModelForm):
    """
    Form to create a new contact message
    """

    class Meta:
        model = models.Message
        fields = ["name", "email_address", "department", "message"]

    def process(self, ip_address):
        """
        Process the contact form
        """
        obj = self.save()
        obj.ip_address = ip_address

        # send out the admin notification email
        if getattr(settings, "CONTACT_SEND_EMAIL", True):
            obj.send_email()

        return obj
