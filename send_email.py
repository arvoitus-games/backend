from mailersend import emails
import os

api_key = os.environ.get("MAILERSEND_API_KEY")

EMAIL_CONFIRMATION_TEMPLATE = "3vz9dlemoe74kj50"
EMAIL_CONFIRMATION_SUBJECT = "Email Confirmation"

PASSWORD_RECOVERY_TEMPLATE = "z3m5jgro68dgdpyo"
PASSWORD_RECOVERY_SUBJECT = "Password Recovery"

def send_confirmation_email(email, name, url, type="EMAIL_VERIFICATION"):
    mailer = emails.NewEmail(api_key)

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "Arvoitus",
        "email": "noreply@arvoitus.games",
    }

    recipients = [
        {
            "name": name,
            "email": email,
        }
    ]

    variables = [
        {
            "email": email,
            "substitutions": [
                {
                    "var": "username",
                    "value": name
                },
                {
                    "var": "account.name",
                    "value": "Arvoitus"
                },
                {
                    "var": "support_email",
                    "value": "alexey@arvoitus.games"
                },
                {
                    "var": "url",
                    "value": url
                }
            ]
        }
    ]

    subject = EMAIL_CONFIRMATION_SUBJECT
    if type == "PASSWORD_RECOVERY": subject = PASSWORD_RECOVERY_SUBJECT

    template = EMAIL_CONFIRMATION_TEMPLATE
    if type == "PASSWORD_RECOVERY": subject = PASSWORD_RECOVERY_TEMPLATE

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_template(template, mail_body)
    mailer.set_simple_personalization(variables, mail_body)

    mailer.send(mail_body)