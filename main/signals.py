from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, PostCategory
from django.core.mail import send_mail

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers_newnews(sender, instance,  **kwargs):
    news_categories = ''
    message_body = f'Ссылка на статью http://127.0.0.1:8000/news/{instance.pk}'
    for category in instance.categories.all():
        news_categories = news_categories + ', ' + category.category
        recipient_list = ''
        n = 0
        for user in category.subscribers.all():
            if n == 0:
                recipient_list = recipient_list  + user.email  # Надо убрать запятую если адресат 1
                n +=1
            else:
                recipient_list = recipient_list +' ,'+ user.email
        subject = f' На сайте NewsPortal в категории {category.category} появилась новая статья - {instance.heder}'
       #print('subject: '+subject)
       # print('message_body: ' + message_body)
       # print('recipient_list: ' + recipient_list)
       # send_mail(
       #     subject=subject,
       #     message=message_body,
       #     from_email = 'VA9979549@yandex.ru',
       #     recipient_list = [recipient_list],
       #     )

#m2m_changed.connect(notify_subscribers_newnews, sender=Post.categories.through)