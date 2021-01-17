from django.core import mail
from django.test import override_settings

import pytest

from contact.models import Department, Message

from . import conftest


@pytest.mark.django_db
class TestDepartment:
    """
    Tests the department model
    """

    def test_string_repr(self, department_instance):
        """
        Tests the string representation for a department
        """

        obj = department_instance
        assert str(obj) == "Test department"

    def test_save_method(self, department_instance):
        """
        Tests that the save method strips spaces from recipients field
        """

        obj = department_instance
        obj.recipients = "test@example.com,  test2@example.com"
        obj.save()
        assert obj.recipients == "test@example.com,test2@example.com"

    def test_email_recipients(self, department_instance):
        """
        Test that the email_recipients property returns a list
        """

        obj = department_instance
        assert isinstance(obj.email_recipients, list)


@pytest.mark.django_db
class TestMessage:
    """
    Tests the message model
    """

    def test_str(self, message_instance):
        """
        Tests the string representation for a message
        """

        obj = message_instance
        assert str(obj) == "Message from Test User"

    @override_settings(CONTACT_EMAIL_SUBJECT="New contact message")
    def test_email_is_sent(self, mocker, message_instance):
        """
        Tests that an email is sent when calling send_email
        """

        message_instance.send_email()
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "New contact message"
