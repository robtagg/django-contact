from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from . import forms


def index(request):
    """
    Main contact message view
    """
    form = forms.ContactForm(data=request.POST or None)

    if form.is_valid():
        form.process(ip_address=request.META["REMOTE_ADDR"])
        return redirect(
            reverse_lazy(getattr(settings, "CONTACT_SUCCESS_URL", "contact:index")) + "?thanks"
        )
    return render(
        request, "contact/contact.html", {"form": form, "thanks": "thanks" in request.GET}
    )
