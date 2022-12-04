# from django.conf.urls import url  # 现在必须替换为以下
from django.urls import re_path as url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home$', views.home),
    url(r'^forecast$', views.forecast),
    url(r'^recommend$', views.recommend),
    url(r'^visualization$', views.visualization)
]
