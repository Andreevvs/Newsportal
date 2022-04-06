import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Post, Category
from datetime import datetime, date, timedelta
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    for category in Category.objects.all():
        new_posts = Post.objects.filter(categories=category)
        posts_last_week = new_posts.filter(time_in__gte=date.today() - timedelta(days=14))
        post_list = ''
        for post in posts_last_week:
            recipient_list = ''
            post_list = post_list + f'{post.heder}: Ссылка на статью http://127.0.0.1:8000/news/{post.pk}, '
            n = 0
            for user in category.subscribers.all():
                if n == 0:
                    recipient_list = recipient_list + user.email  # Надо убрать , запятую если адресат 1
                    n += 1
                else:
                    recipient_list = recipient_list + ' ,' + user.email
        subject = f' На сайте NewsPortal в категории {category.category} за 2 недели появились новые статьи'
        message_body = 'Новые статьи:' + post_list
        print('subject: ' + subject)
        print('message_body: ' + message_body)
        print('recipient_list: ' + recipient_list)
        send_mail(
                  subject=subject,
                  message='Спасибо за регистрацию на сайте NewsPortal',
                from_email='VA9979549@yandex.ru',
                recipient_list=[recipient_list]
            )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/2"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")