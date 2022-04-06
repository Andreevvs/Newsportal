from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Post, Category
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['category']  # не забываем включить галочку в поля иначе она не будет показываться на странице!

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'type', 'categories', 'heder','text']  # не забываем включить галочку в поля иначе она не будет показываться на странице!

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user