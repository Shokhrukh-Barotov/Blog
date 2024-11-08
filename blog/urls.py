from django.urls import path
from .views import PostListView, post_detail, post_share, BlogCreateView, post_comment

app_name = 'blog'
urlpatterns = [
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    # path('<int:post_id>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('', PostListView.as_view(), name='post_list'),
    # path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         post_detail,
         name='post_detail'),

]
