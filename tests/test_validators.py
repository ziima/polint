"""
Tests for individual validators.
"""
import unittest

from polib import POEntry

from polint import fuzzy_validator, no_location_validator, obsolete_validator, untranslated_validator


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


class TestObsoleteValidator(unittest.TestCase):
    """
    Test `obsolete_validator`.
    """
    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertTrue(obsolete_validator(entry))

    def test_fail(self):
        entry = POEntry(msgid="Source", msgstr="Translation", obsolete=True)
        self.assertFalse(obsolete_validator(entry))


class TestUntranslatedValidator(unittest.TestCase):
    """
    Test `untranslated_validator`.
    """
    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertTrue(untranslated_validator(entry))

    def test_fail_missing(self):
        entry = POEntry(msgid="Source", msgstr="")
        self.assertFalse(untranslated_validator(entry))

    def test_fail_fuzzy(self):
        # Fuzzy translations are considered untranslated
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['fuzzy'])
        self.assertFalse(untranslated_validator(entry))

    def test_fail_obsolete(self):
        # Obsolete translations are considered untranslated
        entry = POEntry(msgid="Source", msgstr="Translation", obsolete=True)
        self.assertFalse(untranslated_validator(entry))


class TestNoLocationValidator(unittest.TestCase):
    """
    Test `no_location_validator`.
    """
    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertTrue(no_location_validator(entry))

    def test_fail(self):
        entry = POEntry(msgid="Source", msgstr="Translation", occurrences=[('source.py', 1)])
        self.assertFalse(no_location_validator(entry))
