# pylint: skip-file
import unittest

from fastapi import Depends
from fastapi import Request
from fastapi.testclient import TestClient

from unimatrix.ext import webapi


EVENT_DTO = {
    'message': {
        'attributes': {
            'apiVersion': 'v1',
            'kind': 'TestEvent',
            'spec': {
                'foo': 'bar'
            }
        },
        'messageId': '3830828261466574',
        'message_id': '3830828261466574',
        'publishTime': '2022-01-12T13:26:29.661Z',
        'publish_time': '2022-01-12T13:26:29.661Z'
    },
    'subscription': 'projects/unimatrixinfra/subscriptions/eventarc-europe-west4-molano-api-listener-fb812acb-sub-328'
}


class GoogleListenerTestCase(unittest.TestCase):
    url = '/google.cloud.pubsub.topic.v1.messagePublished'
    event = EVENT_DTO

    class listener_class(webapi.WebhookListener):
        handles = [
            "*.TestEvent"
        ]

        async def handle(self, request: Request, foo=Depends(lambda: 1)):
            print(self, foo)

    def setUp(self):
        self.app = webapi.application_factory(
            'listener',
            allowed_hosts=['*'],
            handlers=[self.listener_class, self.listener_class]
        )
        self.client = TestClient(self.app)

    def test_message_is_accepted(self):
        response = self.client.post(self.url, json=self.event)
        self.assertEqual(response.status_code, 202, response.text)
