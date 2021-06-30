from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import time
import datetime
import pytz



@shared_task
def send_email(subject, body, emails, html_content):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,  # это то же, что и message
        # from_email='big.gray.city@yandex.ru',
        from_email='marbaterrys@yandex.ru',
        to=emails,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_mailing():
    now = datetime.datetime.now()
    last = now - datetime.timedelta(days=7)
    now = pytz.utc.localize(now)
    last = pytz.utc.localize(last)

    for u in User.objects.all():
        if len(u.category_set.all()) > 0:
            emails = []
            emails.append(u.email)
            list_of_posts = Post.objects.filter(date__range=(last, now),
                                                category_id__in=u.category_set.all())
            title_string = ','.join([str(i) for i in list_of_posts])
            subject = f'Новые статьи за неделю {title_string}'
            body = ''
            html_content = render_to_string(
                'post_subscribe_weekly.html',
                {
                    'list_of_posts': list_of_posts,
                }
            )
            send_email.delay(subject, body, emails, html_content)


