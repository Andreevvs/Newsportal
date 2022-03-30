from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from main.models import *
user1 = User.objects.create_user('Иванов')
user2 = User.objects.create_user('Петров')
Author.objects.create(user=user1)
Author.objects.create(user=user2)

Category.objects.create(category='Политика')
Category.objects.create(category='Экономика')
Category.objects.create(category='Развлечения')
Category.objects.create(category='Искусство')

author1 = Author.objects.get(pk=1)
author2 = Author.objects.get(pk=2)
Post.objects.create(heder='статья 1',author=author1,type = 0)
Post.objects.create(heder='статья 2',author=author2, type = 0)
Post.objects.create(heder='новость 1',author=author2, type = 1)

cat1 = Category.objects.get(pk=1)
cat2 = Category.objects.get(pk=2)
cat3 = Category.objects.get(pk=3)
cat4 = Category.objects.get(pk=4)

post1 = Post.objects.get(heder="статья 1")
post2 = Post.objects.get(heder="статья 2")
post3 = Post.objects.get(heder="новость 1")

post1.categories.add(cat1)
post1.categories.add(cat2)
post2.categories.add(cat3)
post3.categories.add(cat4)

Comment.objects.create(author=author1, post=post1, text= 'Comment1')
Comment.objects.create(author=author1, post=post2, text= 'Comment2')
Comment.objects.create(author=author2, post=post3, text= 'Comment3')
Comment.objects.create(author=author2, post=post3, text= 'Comment4')

Comment.objects.get(pk=1).like()
Comment.objects.get(pk=1).like()
Comment.objects.get(pk=3).like()

post1.like()
post1.like()
post1.like()
post2.like()
post1.dislike()




a = Author.objects.order_by('-rate')[:1]

for i in a:
    i.rate
    i.user.username


author1.rate

post1.rate


postRate = self.post_set.aggregate(postRating=Sum('rate'))
pRate = 0
pRate += postRate.get('postRating')
commentRate = self.comment_set.aggregate(commentRating=Sum('rate'))
cRate = 1
cRate =cRate + commentRate.get('commentRating')

self.rate = pRate*3+cRate