# -*- coding: utf-8 -*-

import io
from apps.contrib.api.parsers import PlainTextParser, SNSJsonParser


class PlainTextParserTests:
    content = 'whatever_plain_text'

    def test_parse(self):
        parser = PlainTextParser()
        stream = io.StringIO(self.content)
        parsed_data = parser.parse(stream)
        assert isinstance(parsed_data, str)
        assert parsed_data == self.content


class SNSJsonParserTests:
    content = '{"status": "OK", "items": [0,1,2]}'

    def test_parse(self):
        parser = SNSJsonParser()
        stream = io.StringIO(self.content)
        parsed_data = parser.parse(stream)
        assert isinstance(parsed_data, dict)
        assert {'status', 'items'} <= set(parsed_data.keys())
        assert isinstance(parsed_data['items'], list)

    def test_parse_invalid_json(self):
        parser = SNSJsonParser()
        stream = io.StringIO('invalid_json')
        parsed_data = parser.parse(stream)
        assert isinstance(parsed_data, str)
        assert parsed_data == ''

