# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
    url(r'^$', views.SearchResultsView.as_view(), name='results'),
    url(r'^avancee/$', views.AdvancedSearchView.as_view(), name='advanced_search'),
    url(r'^api/eruditdocuments/', views.EruditDocumentListAPIView.as_view(),
        name='eruditdocument_api_list'),

    url(_(r'^sauvegardes/ajout/$'), views.SavedSearchAddView.as_view(), name='add_search'),
    url(_(r'^sauvegardes/suppression/(?P<uuid>[\w-]+)/$'),
        views.SavedSearchRemoveView.as_view(), name='remove_search'),
]
