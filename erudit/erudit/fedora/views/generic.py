# -*- coding: utf-8 -*-

"""
This module defines generic class-based views to use in order to achieve common tasks
that involve Fedora and datastreams.
"""

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from eulfedora.util import RequestFailed
from requests.exceptions import ConnectionError

from ..repository import api


class FedoraFileDatastreamView(SingleObjectMixin, View):
    """
    The FedoraFileDatastreamView CBV can be used to expose Fedora file datastreams
    through Django views.
    """
    cache_timeout = 60  # This is expressed in seconds
    http_method_names = ['get', ]

    # The following attributes should be specified on each subclass
    content_type = None
    datastream_name = None
    fedora_object_class = None

    def dispatch(self, *args, **kwargs):
        return cache_page(self.cache_timeout)(
            super(FedoraFileDatastreamView, self).dispatch)(*args, **kwargs)

    def get(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs.copy()
        self.fedora_object = self.get_fedora_object()
        return self.write_to_response(self.fedora_object)

    def get_fedora_object(self):
        """
        Returns the fedora object whose file content is being displayed
        by the view.

        By default this requires `self.fedora_object_class` to be specified but
        subclasses can override this to return any Fedora digital object.
        """
        if self.fedora_object_class is None:
            raise ImproperlyConfigured(
                '{cls} is missing a Fedora object. Define {cls}.fedora_object_class '
                'or override {cls}.get_fedora_object().'.format(cls=self.__class__.__name__))
        return self.fedora_object_class(api, self._fedora_object_pid)

    def get_fedora_object_pid(self):
        """
        Returns the PID of the fedora object that will be retrieved by the view.

        By default this has the same requires as the
        :meth:`get_object<django:django.views.generic.detail.SingleObjectMixin.get_object>` method
        because the considered object is expected to be an instance of a Fedora Django model,
        which is helpful to retrieve the Fedora PID. But subclasses can override this to control
        the way the Fedora PID is generated.
        """
        try:
            obj = self.get_object()
        except ImproperlyConfigured:
            raise ImproperlyConfigured(
                '{cls} is missing a PID. Define {cls}.model or {cls}.get_object() '
                'if you want the PID to be retrieved from a Fedora-based Django model. '
                'Override {cls}.get_fedora_object_pid() if you want to generate the PID '
                'by yourself.'.format(cls=self.__class__.__name__))
        return obj.pid

    def write_to_response(self, fedora_object):
        """
        Writes the content of the fedora object's datastream to an HttpResponse object
        and return it.
        """
        response = self.get_response_object()
        try:
            content = self.get_datastream_content(fedora_object)
        except (RequestFailed, ConnectionError):
            raise Http404
        self.write_datastream_content(response, content)
        return response

    def get_response_object(self):
        """
        Returns the HttpResponse object that will contain the content of datastream.

        By default this requires `self.content_type` to be specified but
        subclasses can override this to change this. This method can also be overriden
        in order to add extra headers if applicable.
        """
        if self.content_type is None:
            raise ImproperlyConfigured(
                '{cls} is missing a content type. '
                'Define {cls}.content_type.'.format(cls=self.__class__.__name__))
        response = HttpResponse(content_type=self.content_type)
        return response

    def get_datastream_content(self, fedora_object):
        """
        Returns the content of the considered Fedora datastream.

        By default this requires `self.datastream_name` to be specified but
        subclasses can override this to change this.
        """
        if self.datastream_name is None:
            raise ImproperlyConfigured(
                '{cls} is missing a datastream. Define {cls}.datastream_name '
                'or override {cls}.get_datastream_content().'.format(cls=self.__class__.__name__))
        try:
            assert hasattr(fedora_object, self.datastream_name)
            return getattr(fedora_object, self.datastream_name).content
        except (AssertionError, AttributeError):
            raise ImproperlyConfigured(
                'The `{ds}` datastream cannot be retrieved on the {fedoracls} digital object. '
                'Please ensure that a `{ds}` FileDatastream is defined on {fedoracls}.'
                .format(ds=self.datastream_name, fedoracls=self.fedora_object_class.__name__))

    def write_datastream_content(self, response, content):
        """
        Writes the content of the Fedora datastream to the HttpResponse object.
        """
        response.write(content.read() if hasattr(content, 'read') else content)

    @property
    def _fedora_object_pid(self):
        return self.get_fedora_object_pid()
