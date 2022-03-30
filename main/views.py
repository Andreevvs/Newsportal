from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # импортируем класс получения деталей объекта
from django.views.generic.edit import CreateView
from .models import Post, BaseRegisterForm
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm,UserForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required



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

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

#class UserDetailView(DetailView):
#    template_name = 'user_detail.html'
#    form_class = UserForm
#    success_url = '/news/'

  #  # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
   # def get_object(self, **kwargs):
  #      id = self.kwargs.get('pk')
  #      return Post.objects.get(pk=id)

