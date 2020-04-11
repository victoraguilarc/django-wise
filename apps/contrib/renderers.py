# -*- coding: utf-8 -*-

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder


class SafeJSONEncoder(JSONEncoder):
    """Process the object encode/decode to JSON safely."""

    def encode(self, instance):
        """Override JSONEncoder.encode method.

        It because it has hacks for performance that make things more complicated.
        """
        chunks = self.iterencode(instance, True)  # noqa: WPS425
        return ''.join(chunks)

    def iterencode(self, instance, _one_shot=False):  # noqa: D102
        chunks = super().iterencode(instance, _one_shot)
        for chunk in chunks:
            chunk = chunk.replace('&', '\\u0026')
            chunk = chunk.replace('<', '\\u003c')
            chunk = chunk.replace('>', '\\u003e')
            yield chunk


class SafeJSONRenderer(JSONRenderer):  # noqa: D101
    encoder_class = SafeJSONEncoder
