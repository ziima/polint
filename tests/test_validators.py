"""Tests for individual validators."""
import unittest

from polib import POEntry

from polint import (Status, fuzzy_validator, no_location_validator, obsolete_validator, sort_validator,
                    untranslated_validator)


class TestFuzzyValidator(unittest.TestCase):
    """Test `fuzzy_validator`."""

    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        status = Status()
        status.step(entry)
        self.assertTrue(fuzzy_validator(status))

    def test_fail_fuzzy(self):
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['fuzzy'])
        status = Status()
        status.step(entry)
        self.assertFalse(fuzzy_validator(status))

    def test_fail_multiple_flags(self):
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['another', 'fuzzy', 'flag'])
        status = Status()
        status.step(entry)
        self.assertFalse(fuzzy_validator(status))


class TestObsoleteValidator(unittest.TestCase):
    """Test `obsolete_validator`."""

    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        status = Status()
        status.step(entry)
        self.assertTrue(obsolete_validator(status))

    def test_fail(self):
        entry = POEntry(msgid="Source", msgstr="Translation", obsolete=True)
        status = Status()
        status.step(entry)
        self.assertFalse(obsolete_validator(status))


class TestUntranslatedValidator(unittest.TestCase):
    """Test `untranslated_validator`."""

    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        status = Status()
        status.step(entry)
        self.assertTrue(untranslated_validator(status))

    def test_fail_missing(self):
        entry = POEntry(msgid="Source", msgstr="")
        status = Status()
        status.step(entry)
        self.assertFalse(untranslated_validator(status))

    def test_fail_fuzzy(self):
        # Fuzzy translations are considered untranslated
        entry = POEntry(msgid="Source", msgstr="Translation", flags=['fuzzy'])
        status = Status()
        status.step(entry)
        self.assertFalse(untranslated_validator(status))

    def test_fail_obsolete(self):
        # Obsolete translations are considered untranslated
        entry = POEntry(msgid="Source", msgstr="Translation", obsolete=True)
        status = Status()
        status.step(entry)
        self.assertFalse(untranslated_validator(status))


class TestNoLocationValidator(unittest.TestCase):
    """Test `no_location_validator`."""

    def test_pass(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        status = Status()
        status.step(entry)
        self.assertTrue(no_location_validator(status))

    def test_fail(self):
        entry = POEntry(msgid="Source", msgstr="Translation", occurrences=[('source.py', 1)])
        status = Status()
        status.step(entry)
        self.assertFalse(no_location_validator(status))


class TestSortValidator(unittest.TestCase):
    """Test `sort_validator`."""

    def test_first_entry(self):
        entry = POEntry(msgid="Source", msgstr="Translation")
        status = Status()
        status.step(entry)
        self.assertTrue(sort_validator(status))

    def test_sorted(self):
        first = POEntry(msgid="First", msgstr="Translation")
        second = POEntry(msgid="Second", msgstr="Translation")
        status = Status()
        status.step(first)
        status.step(second)
        self.assertTrue(sort_validator(status))

    def test_unsorted(self):
        first = POEntry(msgid="Second", msgstr="Translation")
        second = POEntry(msgid="First", msgstr="Translation")
        status = Status()
        status.step(first)
        status.step(second)
        self.assertFalse(sort_validator(status))

    def test_msgctxt_none(self):
        first = POEntry(msgid="First", msgstr="Translation")
        second = POEntry(msgid="First", msgstr="Trans.", msgctxt="abbrev.")
        status = Status()
        status.step(first)
        status.step(second)
        self.assertTrue(sort_validator(status))

    def test_msgctxt_both(self):
        first = POEntry(msgid="First", msgstr="Trans.", msgctxt="abbrev.")
        second = POEntry(msgid="First", msgstr="Translation", msgctxt="long")
        status = Status()
        status.step(first)
        status.step(second)
        self.assertTrue(sort_validator(status))
