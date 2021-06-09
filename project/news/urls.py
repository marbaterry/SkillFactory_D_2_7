from django.urls import path
from .views import PostList, PostDetail, SearchNews, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', SearchNews.as_view()),
    path('add', PostCreateView.as_view()),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view()),
]