
from django.conf.urls import url

from apps.users.views import UsernameCountView, MobileCountView
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),  # 注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', UsernameCountView.as_view(), name = 'count'),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view(), name='count_mobile')
]