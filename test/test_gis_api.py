# encoding: utf-8
"""
@author: Michael
@file: test_gis_api.py
@time: 2020/4/23 9:27 AM
@desc:
"""
from unittest import TestCase
from lamina.gis_api import gis_api


class Test(TestCase):
    def test_query_links(self):
        self.fail()

    def test_query_ways(self):
        client = gis_api.app.test_client()
        uri = '/ways?box=121.59930775,31.28129225,121.6212925,31.29743295&zoom=15'
        r = client.get(uri)
        print(r.json)
