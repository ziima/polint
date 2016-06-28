"""
Tests for individual validators.
"""
import unittest

from polib import POEntry
from polint import fuzzy_validator


class TestFuzzyValidator(unittest.TestCase):
    """
    Test `fuzzy_validator`.
    """
    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertTrue(fuzzy_validator(entry))

    def test_fail_fuzzy(self):
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['fuzzy'])
        self.assertFalse(fuzzy_validator(entry))

    def test_fail_multiple_flags(self):
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['another', 'fuzzy', 'flag'])
        self.assertFalse(fuzzy_validator(entry))
