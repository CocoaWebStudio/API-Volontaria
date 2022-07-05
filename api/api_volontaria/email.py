import sys
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings

from api_volontaria.apps.log_management.models import EmailLog

class EmailAPI:
    def send_template_email(self, to_email, subject, template, context):
        try:
            htmlTemplate = template + '.html'
            textTemplate = template + '.txt'
            message = render_to_string(textTemplate, context)
            html_message = render_to_string(htmlTemplate, context)
            from_email = 'info@pureconnexion.org'

            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently = False,
                html_message = html_message
            )
            print("sended")

            EmailLog.add(
                user_email=[to_email],
                type_email=template,
                nb_email_sent='sended',
            )
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print( "<p>Email Error: %s</p>" % e )
