from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Notice

import datetime

from celery import shared_task


@shared_task
def weekly_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    notices = Notice.objects.filter(dateCreation__gte=last_week)
    html_content = render_to_string(
        'notices/daily_notice.html',
        {
            'link': settings.SITE_URL,
            'notices': notices,
        }
    )
    recipients = User.objects.values_list('email', flat=True)
    for recipient in recipients:
        msg = EmailMultiAlternatives(
            subject=f'New notices per week',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
