# -*- coding: utf-8 -*-

from django.conf.urls import include
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),

    url(_(r'^compte/'), include('apps.public.auth.urls', namespace='auth')),
    url(_(r'^compte/actions/'), include(
        'apps.public.account_actions.urls', namespace='account_actions')),
    url(_(r'^notices/'), include('apps.public.citations.urls', namespace='citations')),
    url(_(r'^recherche/'), include('apps.public.search.urls', namespace='search')),
    url(_(r'^theses/'), include('apps.public.thesis.urls', namespace='thesis')),

    # The journal URLs are at the end of the list because some of them are catchalls.
    url(r'^', include('apps.public.journal.urls', namespace='journal')),
]
