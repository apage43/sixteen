# -*- coding: utf-8 -*-

import unittest
from sixteen.parser import AssemblyParser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = AssemblyParser()
        self.parse = self.parser.parse

    def assertParses(self, given, expected):
        self.assertEquals(self.parse(given), expected)

    def test_parse_registers(self):
        self.assertParses("A", (0x00, None))
        self.assertParses("B", (0x01, None))
        self.assertParses("Y", (0x04, None))
        self.assertParses("J", (0x07, None))

    def test_parse_register_pointers(self):
        self.assertParses("[A]", (0x08, None))
        self.assertParses("[B]", (0x09, None))
        self.assertParses("[Y]", (0x0c, None))
        self.assertParses("[J]", (0x0f, None))

    def test_parse_next_word_plus_registers(self):
        self.assertParses("[0x0000 + A]", (0x10, 0x0000)) 
        self.assertParses("[0x0300 + B]", (0x11, 0x0300)) 
        self.assertParses("[0xffff + I]", (0x16, 0xffff)) 
        self.assertParses("[0x03f0 + J]", (0x17, 0x03f0)) 