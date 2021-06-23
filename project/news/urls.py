from django.urls import path
from .views import PostList, PostDetail, SearchNews, PostCreateView, PostUpdateView, PostDeleteView
from .views import *


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', SearchNews.as_view()),
    path('add', PostCreateView.as_view()),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view()),
    path('subscribe', SubscriberCreateView.as_view(template_name="add_subscriber.html")),
    path('result', SubscriberCreateView.as_view(template_name="result_subscriber.html")),
]