import base64


def generate_sns_subscription(subscribe_url='http://sns.server'):
    return {
        'Type': 'SubscriptionConfirmation',
        'MessageId': '165545c9-2a5c-472c-8df2-7ff2be2b3b1b',
        'Token': '2336412f37f...',
        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:MyTopic',
        'Message': '....',
        'SubscribeURL': subscribe_url,
        'Timestamp': '2012-04-26T20:45:04.751Z',
        'SignatureVersion': '1',
        'Signature': 'test_signature',
        'SigningCertURL': 'https://sns.server/certificate.pem'
    }


def generate_sns_notification(signature='test_signature', signing_cert_url='https://sns.server/certificate.pem'):
    return {
        'Type': 'Notification',
        'MessageId': '22b80b92-fdea-4c2c-8f9d-bdfb0c7bf324',
        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:MyTopic',
        'Subject': 'My First Message',
        'Message': 'Hello world!',
        'Timestamp': '2012-05-02T00:54:06.655Z',
        'SignatureVersion': '1',
        'Signature': base64.b64encode('base64 encoded string'.encode()).decode(),
        'SigningCertURL': signing_cert_url,
        'UnsubscribeURL': 'https://sns.server/unsubscribe'
    }
