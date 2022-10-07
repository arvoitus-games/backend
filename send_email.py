from mailersend import emails
import os

api_key = os.environ.get("MAILERSEND_API_KEY")

def send_confirmation_email(email, name, url):
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
                    "value": "alexey.nikolaev@aaltoes.com"
                },
                {
                    "var": "url",
                    "value": url
                }
            ]
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("Arvoitus: Email Confirmation", mail_body)
    mailer.set_template("3vz9dlemoe74kj50", mail_body)
    mailer.set_simple_personalization(variables, mail_body)

    mailer.send(mail_body)