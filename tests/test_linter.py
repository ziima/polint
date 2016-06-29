"""
Test Linter
"""
import os
import unittest

from polib import POEntry

from polint import Linter, ValidatorRegister


def invalidator(dummy):
    """Validator which never passes"""
    return False


class TestLinter(unittest.TestCase):
    """
    Test `Linter` class
    """
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
        reg.register_entry(invalidator, 'error', 'entry in invalid')
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), register=reg)

        linter.run_validators()

        entry = POEntry(msgid="Source", msgstr="Translation")
        self.assertEqual(linter.errors, {entry: ['error']})

    def test_exclude(self):
        reg = ValidatorRegister()
        reg.register_entry(invalidator, 'error', 'entry in invalid')
        linter = Linter(os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'), exclude={'error'},
                        register=reg)

        linter.run_validators()

        self.assertEqual(linter.errors, {})
