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
        reg.register_entry(test_callback, 'error', 'entry is invalid')
        self.assertEqual(reg.errors, {'error': 'entry is invalid'})
        self.assertEqual(reg.entry_validators, {'error': test_callback})

    def test_already_registered(self):
        reg = ValidatorRegister()
        reg.register_entry(test_callback, 'error', 'entry is invalid')
        with self.assertRaises(ValueError):
            reg.register_entry(test_callback, 'error', 'entry is broken')
