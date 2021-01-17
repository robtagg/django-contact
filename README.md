# Django Contact

A simple contact app that includes departments with support for multiple recipients.


## Settings

The following settings can be set:

| Setting                       | Description                                               | Default     |
| :-------------                | :----------:                                              | -----------: |
| DEFAULT_FROM_EMAIL            | Set to the email from address.                            |
| CONTACT_EMAIL_SUBJECT         | Sets the email subject.                                   | New contact message
| CONTACT_EMAIL_TEMPLATE        | Sets the template to use for the admin email notification | contact/email/email_notification.txt
| CONTACT_SEND_EMAIL            | Toggles the admin email notification send                 | True
