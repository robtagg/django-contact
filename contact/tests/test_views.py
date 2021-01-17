from django.urls import resolve, reverse

import pytest
from pytest_django.asserts import assertTemplateUsed

from contact import forms, models, views

from . import conftest


@pytest.mark.django_db
class TestContactView:
    """
    Test case for the form views
    """

    def test_index_view_url(self):
        """
        Tests the index url points to the correct view
        """

        path = reverse("contact:index")
        assert path == f"/contact/"
        assert "contact:index" == resolve(path).view_name

    def test_index_template(self, client):
        """
        Test the response for the form view
        """

        response = client.get((reverse("contact:index")))
        assert response.status_code == 200
        assertTemplateUsed(response, "contact/contact.html")

    def test_index_context(self, client):
        """
        Tests the index view context contains the form
        """

        response = client.get((reverse("contact:index")))
        assert "form" in response.context
        assert "thanks" in response.context
        assert response.context["thanks"] == False

    def test_form_submission(self, client, department_instance):
        """
        Tests a successfull form submission
        """

        post_data = {
            "name": "Test User",
            "email_address": "test2@example.com",
            "department": department_instance.pk,
            "message": "`Test message",
        }

        response = client.post((reverse("contact:index")), data=post_data)

        assert response.status_code == 302
        assert models.Message.objects.filter(email_address="test2@example.com").exists()

    def test_form_thanks(self, client):
        """
        Tests the thanks key in request.get after submission
        """

        response = client.get((reverse("contact:index") + "?thanks"))
        assert response.context["thanks"] == True
