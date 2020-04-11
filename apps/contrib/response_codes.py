# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

# >> Providers

OPS_SERVER_UNAVAILABLE = {
    'code': 'ops.ServerUnavailable',
    'detail': _('Ops Server is unavailable.'),
}

INVALID_OPS_SERVER_REQUEST = {
    'code': 'ops.InvalidRequest',
    'detail': _('Ops Server invalid request.'),
}

SYNC_USER_ERROR = {
    'code': 'ops.SyncUserError',
    'detail': _('Sync User error.'),
}
SYNC_BASE_ERROR = {
    'code': 'ops.SyncBaseError',
    'detail': _('Sync Base error.'),
}

CORE_SERVER_UNAVAILABLE = {
    'code': 'core.ServerUnavailable',
    'detail': _('Core Server is unavailable.'),
}

MAP_SERVER_UNAVAILABLE = {
    'code': 'maps.ServerUnavailable',
    'detail': _('Maps Server is unavailable.'),
}

# >> SNS

NOT_SNS_REQUEST = {
    'code': 'ops.NotSNSRequests',
    'detail': _('This resource is forbidden for not SNS requests.'),
}

METHOD_NOT_ALLOWED = {
    'code': 'sns.MethodNotAllowed',
    'detail': _('This method is not allowed for SNS requests'),
}

INVALID_SNS_SIGNATURE = {
    'code': 'ops.InvalidSNSSignature',
    'detail': _('Invalid SNS Signature.'),
}

SNS_ENDPOINT_SUBSCRIBE_FAILED = {
    'code': 'ops.SNSEndpointSubscribeFailed',
    'detail': _('SNS endpoint subscribe failed.'),
}

SNS_ENDPOINT_SUBSCRIBE_CONFIRMED = {
    'code': 'ops.SNSEndpointSubscribeConfirmed',
    'detail': _('SNS endpoint subscribe confirmed.'),
}
