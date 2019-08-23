from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path('blog/<int:blog_id>/', blog_post_details_page),            # using id for dynamic url
    # re_path(r'^blog/(?P<blog_id>\w+)/$', blog_post_details_page),   # same as above just with regex
    path('<str:slug>/', blog_post_detail_view),                  # using slug for dynamic url
    # re_path(r'^blog/(?P<slug>\w+)/$', blog_post_details_page),
    path('', blog_post_list_view),
    path('<str:slug>/edit/', blog_post_update_view),
    path('<str:slug>/delete/', blog_post_delete_view),
]
