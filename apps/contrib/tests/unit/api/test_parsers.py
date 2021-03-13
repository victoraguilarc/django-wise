# -*- coding: utf-8 -*-

import io

from apps.contrib.api.parsers import PlainTextParser


class PlainTextParserTests:
    content = 'whatever_plain_text'

    def test_parse(self):
        parser = PlainTextParser()
        stream = io.StringIO(self.content)
        parsed_data = parser.parse(stream)
        assert isinstance(parsed_data, str)
        assert parsed_data == self.content
