# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SubscriptionInformationUpdateView.as_view(), name='update'),
]
