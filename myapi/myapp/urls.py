from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^v1/survivor/$', views.SurvivorCreate.as_view(), name='survivor-create'),
    url(r'^v1/survivor/(?P<pk_sur_1>[^/]+)/trade-items/(?P<pk_sur_2>[^/]+)$', views.TradeItems.as_view(), name='trade_items'),
]