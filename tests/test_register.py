"""
Test validator register
"""
import unittest

from polint import ValidatorRegister


def test_callback(dummy):
    """Does nothing, used for ValidationRegister"""
    raise NotImplementedError


class TestValidatorRegister(unittest.TestCase):
    """
    Test `ValidatorRegister`.
    """
    def test_empty_register(self):
        reg = ValidatorRegister()
        self.assertEqual(reg.errors, {})
        self.assertEqual(reg.entry_validators, {})

    def test_register(self):
        reg = ValidatorRegister()
        reg.register_entry(test_callback, 'entry', 'entry is invalid')
        reg.register_file(test_callback, 'file', 'entry is invalid')

        self.assertEqual(reg.errors, {'entry': 'entry is invalid', 'file': 'entry is invalid'})
        self.assertEqual(reg.entry_validators, {'entry': test_callback})
        self.assertEqual(reg.file_validators, {'file': test_callback})

    def test_already_registered(self):
        reg = ValidatorRegister()
        reg.register_entry(test_callback, 'entry', 'entry is invalid')
        reg.register_file(test_callback, 'file', 'file is invalid')

        with self.assertRaises(ValueError):
            reg.register_entry(test_callback, 'entry', 'it is broken')
        with self.assertRaises(ValueError):
            reg.register_entry(test_callback, 'file', 'it is broken')
        with self.assertRaises(ValueError):
            reg.register_file(test_callback, 'entry', 'it is broken')
        with self.assertRaises(ValueError):
            reg.register_file(test_callback, 'file', 'it is broken')
