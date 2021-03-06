# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from base.viewmixins import LoginRequiredMixin
from base.viewmixins import MenuItemMixin

from ..viewmixins import OrganisationScopePermissionRequiredMixin

from .forms import SubscriptionInformationForm


class SubscriptionInformationUpdateView(
        LoginRequiredMixin, OrganisationScopePermissionRequiredMixin, MenuItemMixin, FormView):
    form_class = SubscriptionInformationForm
    menu_library = 'subscription_information'
    permission_required = 'subscription.manage_organisation_subscription_information'
    template_name = 'userspace/library/subscription_information/update.html'

    def get_form_kwargs(self):
        kwargs = super(SubscriptionInformationUpdateView, self).get_form_kwargs()
        kwargs.update({'organisation': self.current_organisation})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SubscriptionInformationUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, _("Les informations de l'abonnement ont été mises à jour avec succès"))
        return reverse(
            'userspace:library:subscription_information:update',
            args=(self.current_organisation.pk, ))
