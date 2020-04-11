# -*- coding: utf-8 -*-

import json
import boto3

from environ import environ

env = environ.Env()


class SNS:

    SNS_VEHICLE_STATE_TOPIC = env('SNS_VEHICLE_STATE_TOPIC', default=None)

    @classmethod
    def publish_vehicle_state(cls, vehicle_profile):
        cls.publish_message(
            topic=cls.SNS_VEHICLE_STATE_TOPIC,
            message={
                'label': vehicle_profile.label,
                'state': vehicle_profile.state,
            }
        )

    @classmethod
    def publish_message(cls, topic, message):
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=topic,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json',
        )
