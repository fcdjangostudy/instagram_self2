from django.conf.urls import url
from . import views

app_name = 'post'
urlpatterns = [

    url(r'^$', views.post_list, name='post_list'),

    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^create/$', views.post_create, name='post_create'),

    url(r'^(?P<post_pk>\d+)/modify/$', views.post_modify, name='post_modify'),

    url(r'^(?P<post_pk>\d+)/delete/$', views.post_delete, name='post_delete'),

    url(r'^(?P<post_pk>\d+)/comment_create/$', views.comment_create, name='comment_create'),

    # 위쪽의 결과들과 매칭되지 않을 경우
    url(r'^.*/$', views.post_anyway, name='post_anyway'),
]
