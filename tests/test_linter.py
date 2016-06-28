"""
Test Linter
"""
import unittest
import os

from polib import POEntry
from polint import ValidatorRegister, Linter


def invalidator(dummy):
    """Validator which never passes"""
    return False


class TestLinter(unittest.TestCase):
    """
    Test `Linter` class
    """
    def test_empty_file(self):
        reg = ValidatorRegister()
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'empty.po'), reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_no_validators(self):
        reg = ValidatorRegister()
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_run_validators(self):
        reg = ValidatorRegister()
        reg.register(invalidator, 'error', 'entry in invalid')
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), reg)

        linter.run_validators()

        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertEqual(linter.errors, {entry: ['error']})


class TestRunValidators(unittest.TestCase):
    """
    Test `Linter.run_validators` class with default register
    """
    def test_empty(self):
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'empty.po'))

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_header_only(self):
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'header_only.po'))

        linter.run_validators()

        self.assertEqual(linter.errors, {})

    def test_simple_valid(self):
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'))

        linter.run_validators()

        self.assertEqual(linter.errors, {})
