from mailersend import emails

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMDUyZDMwOGY3NmUyZmY0NDQzMTViYTA4NTE5Y2I5Y2M4YmFlMjU0MWI5Njc1NzRkNjFkOGE2ZTFjOWMyYjQwODUxYzgzZGQ3MDdlYjBmNmQiLCJpYXQiOjE2NjUwNTkyNTMuMDIwMDYxLCJuYmYiOjE2NjUwNTkyNTMuMDIwMDY5LCJleHAiOjQ4MjA3MzI4NTIuOTM0Nywic3ViIjoiNDA4OTAiLCJzY29wZXMiOlsiZW1haWxfZnVsbCIsImRvbWFpbnNfZnVsbCIsImFjdGl2aXR5X2Z1bGwiLCJhbmFseXRpY3NfZnVsbCIsInRva2Vuc19mdWxsIiwid2ViaG9va3NfZnVsbCIsInRlbXBsYXRlc19mdWxsIiwic3VwcHJlc3Npb25zX2Z1bGwiLCJzbXNfZnVsbCIsImVtYWlsX3ZlcmlmaWNhdGlvbl9mdWxsIl19.TtvAGeCBwDZ-eG7KDMS6IJ7dpIfHtm5Shte2nLd4iqZMgpBli3QLJZ4A869qfi-R5WT_mIpzlkLVakADbzFfbZ2g9ddcsRZvUBMFMwadKov3Tc2o3yqgsqprdWBwNaZyYS03hgKd82pc4hu-JhhVWSBz5v1SwG_GkoQ7oIZMnAnjCnXbQYRrYhCsblQ_XHg87FTklv28TvbMHuDfy9ZF5pk0yWGoIyaY8vBIT1Ny2QZodjxE9r91Ba1WkiLF5ZJTGO1E2mKIP-pbMyV_z_Ji9i4bUqgyXS3UK5ASS6pBy1c-yKfRYeYomOi-i2mSyCwJi1GPFTkCfo7dk9FfStkLgIR_6Vfg2U-YaZpUdEsmwA_umRl0gm9blLtZAfPi0GcSeEGsE0RfpH_teFQ9QooFFEqExmg4LkpQLCUMacLSlIkcReTWI9_fqIzDu_NezAu-e4wB30UFBNuO1zEnGJuoDB7anrTLu_6ED3jlkcGwAAA3BDwKgkXRQ-C7ez9B1GD5tLQK9tpWxZBBbye_EjYcK-PQE7lr4NA8Dsb76nFokAy8qYBgGRQyDk333I7ruG0LSHMi2dX-S3a7h7oU37Vy7npKVtzgy5oCwYoSlSj8sRAnwXzq1DU2p5-sPSqugRJ1a3ZYPbVmIWdzdtRB17BrJJ10qHjGlM-Iyxk-R-ZuNdo"

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
            "email": "recipient@email.com",
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
    mailer.set_subject("Hello from {$company}", mail_body)
    mailer.set_template("3vz9dlemoe74kj50", mail_body)
    mailer.set_simple_personalization(variables, mail_body)

    mailer.send(mail_body)