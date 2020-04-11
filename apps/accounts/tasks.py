# -*- coding: utf-8 -*-

import time
import logging

from celery import shared_task
from celery.utils.log import get_task_logger


@shared_task
def delay_task():
    logger = get_task_logger(__name__)
    logger.setLevel(logging.DEBUG)
    time.sleep(20)
    logger.info('Delayed Task Finished!!!')

