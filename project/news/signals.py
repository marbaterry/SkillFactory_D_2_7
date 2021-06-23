from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, User, CategorySubscriber, Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        emails = []
        new_sub = instance
        title = instance.title
        body = instance.content[:50]
        subject = f'Добавлена новая статья {title}'
        i = instance.category_id
        category = Category.objects.all()
        for list in category:
            if list == i:
                print(list)
                subscribers = list.subscriber.all()
                print(subscribers)
                # emails = []
                for subs in subscribers:
                    email = subs.email
                    emails.append(email)
        html_content = render_to_string(
            'post_subscribe.html',
            {
                'new_sub': new_sub,
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=body,  # это то же, что и message
            from_email='big.gray.city@yandex.ru',
            to=emails,  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()