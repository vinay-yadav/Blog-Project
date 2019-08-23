"""Try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from .views import (
    home_page,
    about_page,
    contact_page,
    example_page,
)
from blog.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('about/', about_page),
    path('contact/', contact_page),
    path('example/', example_page),
    # path('blog/<int:blog_id>/', blog_post_details_page),            # using id for dynamic url
    # re_path(r'^blog/(?P<blog_id>\w+)/$', blog_post_details_page),   # same as above just with regex
    # path('blog/<str:slug>/', blog_post_detail_view),                  # using slug for dynamic url
    # # re_path(r'^blog/(?P<slug>\w+)/$', blog_post_details_page),
    # path('blog/', blog_post_list_view),
    path('blog-new/', blog_post_create_view),
    # path('blog/<str:slug>/edit/', blog_post_update_view),
    # path('blog/<str:slug>/delete/', blog_post_delete_view),
    path('blog/', include('blog.urls'))
]
