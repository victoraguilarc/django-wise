# -*- coding: utf-8 -*-
#
# A S Y N C  T A S K S
#
Q_CLUSTER = {
    'retry': 180,
    'name': 'queue-cluster',
    'workers': 2,
    'timeout': 180,
    'django_redis': 'default',
    'save_limit': 5000,
}
