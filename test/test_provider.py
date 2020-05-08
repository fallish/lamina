# encoding: utf-8
"""
@author: Michael
@file: test_provider.py
@time: 2020/4/20 11:24 PM
@desc:
"""
from unittest import TestCase

from lamina.provider import TianDiTu, GaoDe


class TestLayerType(TestCase):
    def test_or(self):
        self.assertEqual(TianDiTu.Normal, TianDiTu.NormalMap | TianDiTu.NormalAnnotation)

    def test_in(self):
        self.assertTrue(TianDiTu.NormalMap in TianDiTu.Normal)
        self.assertTrue(TianDiTu.NormalAnnotation in TianDiTu.Normal)

        self.assertTrue(TianDiTu.SatelliteMap in TianDiTu.Satellite)
        self.assertFalse(GaoDe.SatelliteMap in TianDiTu.Satellite)
