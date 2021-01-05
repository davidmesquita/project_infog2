from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^api/v1/survivor/$', views.SurvivorCreate.as_view(), name='survivor-create'),
]