from django.core.mail import EmailMessage

import pytest

from contact import forms, models
from contact.tests.conftest import department_instance, message_instance


@pytest.mark.django_db
class TestContactForm:
    """
    Tests for the contact form
    """

    def test_form_save(self, message_instance, department_instance):
        """
        Test the form saves correctly on submission
        """

        data = {
            "name": "Test User",
            "email_address": "test@example.com",
            "department": department_instance.pk,
            "message": "`Test message",
        }

        form = forms.ContactForm(data=data)
        form.process(ip_address="0.0.0.0")

        assert form.is_valid()
        assert (
            models.Message.objects.filter(email_address=data["email_address"])[0].name
            == "Test User"
        )

    def test_email_send(self, mocker, message_instance):
        """
        Test the admin email notification gets sent
        """

        send_mock = mocker.Mock()
        mocker.patch.object(
            EmailMessage, "send", send_mock,
        )
        form = forms.ContactForm(instance=message_instance)

        form.instance.send_email()
        send_mock.assert_called_once()
