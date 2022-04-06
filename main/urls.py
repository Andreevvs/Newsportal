from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreateView,PostUpdateView, PostDeleteView, UserDetailView, BaseRegisterView, upgrade_me, add_subscribe, del_subscribe
from .views import CategoryList
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view()),
    path('add/', PostCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('user/', UserDetailView.as_view(), name='news_detail'),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('signup/', BaseRegisterView.as_view(template_name = 'signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
    path('category/', CategoryList.as_view())
    ]