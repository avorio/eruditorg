# -*- coding: utf-8 -*-

from django.conf import settings


def common_settings(request):
    """ Passing custom CONSTANT in Settings into RequestContext. """
    COMMON_CONTEXT = {
        'MAILCHIMP_UUID': settings.MAILCHIMP_UUID,
        'MAILCHIMP_ACTION_URL': settings.MAILCHIMP_ACTION_URL,
    }

    try:
        # set EXTRA_CONTEXT in local settings
        COMMON_CONTEXT.update(settings.EXTRA_CONTEXT)
    except:
        pass

    if settings.DEBUG:
        COMMON_CONTEXT.update({
            "WEBPACK_DEV_SERVER_URL": getattr(settings, 'WEBPACK_DEV_SERVER_URL', ''),
        })

    return COMMON_CONTEXT
