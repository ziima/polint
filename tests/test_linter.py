"""Test Linter."""
import os
import unittest

from mock import sentinel
from polib import POEntry

from polint import Linter, Status, ValidatorRegister


def invalidator(dummy):
    """Return failure in every case."""
    return False


class TestStatus(unittest.TestCase):
    """Test `Status` class."""

    def test_new(self):
        status = Status()
        self.assertIsNone(status.entry)
        self.assertIsNone(status.previous)

    def test_first_step(self):
        status = Status()
        status.step(sentinel.first)

        self.assertEqual(status.entry, sentinel.first)
        self.assertIsNone(status.previous)

    def test_next_step(self):
        status = Status()
        status.step(sentinel.first)
        status.step(sentinel.second)

        self.assertEqual(status.entry, sentinel.second)
        self.assertEqual(status.previous, sentinel.first)


class TestLinter(unittest.TestCase):
    """Test `Linter` class."""

    def test_empty_file(self):
        reg = ValidatorRegister()
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'empty.po'), register=reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_no_validators(self):
        reg = ValidatorRegister()
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), register=reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_run_validators(self):
        reg = ValidatorRegister()
        reg.register(invalidator, 'error', 'entry in invalid')
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), register=reg)

        linter.run_validators()

        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertEqual(linter.errors, {entry: ['error']})

    def test_exclude(self):
        reg = ValidatorRegister()
        reg.register(invalidator, 'error', 'entry in invalid')
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), exclude={'error'},
                        register=reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})
