# -*- coding: utf-8 -*-

from collections import OrderedDict


class Currency(object):
    TYPES = OrderedDict([
       ('vnd', u'Đồng'),

    ])

    @classmethod
    def lookup(cls, currency_code):
        """
        Return the full currency name.

        :param currency_code: Currency abbreviation
        :type currency_code: str
        :return: str
        """
        return Currency.TYPES[currency_code]
