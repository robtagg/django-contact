import pytest

from contact import models


@pytest.fixture
def department_instance():
    return models.Department.objects.create(label="Test department", recipients="test@example.com")


@pytest.fixture
def message_instance(department_instance):
    return models.Message.objects.create(
        name="Test User",
        email_address="test@example.com",
        department=department_instance,
        ip_address="0.0.0.0",
    )
