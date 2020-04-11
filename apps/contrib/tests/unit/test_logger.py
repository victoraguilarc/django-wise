# -*- coding: utf-8 -*-

from apps.contrib.logging import Logger


class LoggerTests:

    message = 'ANYTHING'

    def test_debug(self):
        assert Logger.debug(self.message) is None

    def test_info(self):
        assert Logger.info(self.message) is None

    def test_error(self):
        assert Logger.error(self.message) is None

    def test_warning(self):
        assert Logger.warning(self.message) is None
