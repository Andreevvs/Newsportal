from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # импортируем класс получения деталей объекта
from django.views.generic.edit import CreateView
from .models import Post, Category, BaseRegisterForm
from datetime import datetime, date, timedelta
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm,UserForm, CategoryForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save,m2m_changed

class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    queryset = Category.objects.order_by('-id')
    paginate_by = 10
    form_class = CategoryForm

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 12
    form_class = PostForm

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

 # создаём представление, в котором будут детали конкретного отдельного товара
class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'newsdetail.html'  # название шаблона будет product.html
    context_object_name = 'newsdetail'  # название объекта. в нём будет


class NewsSearch(ListView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'newssearch.html'  # название шаблона будет product.html
    context_object_name = 'news'  # название объекта. в нём будет
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('main.add_post',)
    template_name = 'news_create.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')

@login_required
def add_subscribe( request, pk):
    user = request.user
    sid=str(pk)
    #   print('Пользователь' + user.username + 'добавлен в подписчики категории:'+ sid)
    Category.objects.get(pk=pk).subscribers.add(user)
    return redirect('/news/category')


@login_required
def del_subscribe(request, pk):
    user = request.user
    #print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/category')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            subject = f' Hello, {first_name}   {last_name}'
            form.save()
            print(subject)

        send_mail(
            subject=subject,
            message='Спасибо за регистрацию на сайте NewsPortal',
            from_email='VA9979549@yandex.ru',
            recipient_list=[email]
        )

        return HttpResponseRedirect('/news/')

#def notify_subscribers_digest():
#    for category in Category.all():
#        print('Тест'+ category.category)
#   for category in instance.categories.all():
#        news_categories = news_categories + ', ' + category.category
#        recipient_list = ''
#        for user in category.subscribers.all():
#            recipient_list = recipient_list  + user.email + ' ,'
#        subject = f' На сайте NewsPortal в категории {category.category} появилась новая статья - {instance.heder}'
#        print('subject: '+subject)
#        print('message_body: ' + message_body)
#        print('recipient_list: ' + recipient_list)
#    news_categories = ''
#    message_body = f'Ссылка на статью http://127.0.0.1:8000/news/{instance.pk}'
#    for category in instance.categories.all():
#        news_categories = news_categories + ', ' + category.category
#        recipient_list = ''
#        for user in category.subscribers.all():
#            recipient_list = recipient_list  + user.email + ' ,'
#        subject = f' На сайте NewsPortal в категории {category.category} появилась новая статья - {instance.heder}'
#        print('subject: '+subject)
#        print('message_body: ' + message_body)
#        print('recipient_list: ' + recipient_list)
#        # send_mail(
#        #     subject=subject,
#        #     message= message_body
#        #     from_email='V9979549@yandex.ru',
#        #     recipient_list=[recipient_list]
#        # )

#m2m_changed.connect(notify_subscribers_newnews, sender=Post.categories.through)







#class UserDetailView(DetailView):
#    template_name = 'user_detail.html'
#    form_class = UserForm
#    success_url = '/news/'

  #  # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
   # def get_object(self, **kwargs):
  #      id = self.kwargs.get('pk')
  #      return Post.objects.get(pk=id)

