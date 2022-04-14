from celery import shared_task
import time


@shared_task
def hello():
    print("Hello, fsdfsdfsdf  world!")
    time.sleep(10)
    print("Hello, fsdfsdfsdf  world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def  send_news_update ():
    print ('новые посты за неделю')    #здесь должен быть код  запускаемый по расписанию с рассылкой апдейтов новостей за неделю

@shared_task
def new_news(oid):
    print('новый пост')     #здесь должен быть код запускаемый ппри появлении новой новости