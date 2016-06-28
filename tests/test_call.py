"""
Test command calls.
"""
import unittest
import os
from cStringIO import StringIO

from polint import main


class TestMain(unittest.TestCase):
    """
    Test `main` function
    """
    def test_empty(self):
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'empty.po')])
        self.assertEqual(context.exception.code, 0)

    def test_header_only(self):
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'header_only.po')])
        self.assertEqual(context.exception.code, 0)

    def test_simple_valid(self):
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po')])
        self.assertEqual(context.exception.code, 0)

    def test_multiple_valid_files(self):
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'simple_valid.po'),
                  os.path.join(os.path.dirname(__file__), 'data', 'header_only.po')])
        self.assertEqual(context.exception.code, 0)

    def test_invalid(self):
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'invalid.po')], output=output)
        self.assertEqual(context.exception.code, 1)
        self.assertIn('invalid.po:13: [fuzzy] translation is fuzzy\n', output.getvalue())
        self.assertIn('invalid.po:13: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:17: [obsolete] entry is obsolete\n', output.getvalue())
        self.assertIn('invalid.po:17: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:20: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:23: [location] entry contains location\n', output.getvalue())

    def test_show_msg(self):
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'invalid.po'), '--show-msg'], output=output)
        self.assertEqual(context.exception.code, 1)
        location_output = 'invalid.po:23: [location] entry contains location\n' \
                          '#: source.file:42\n' \
                          'msgid "Location"\n' \
                          'msgstr "Location"\n'
        self.assertIn(location_output, output.getvalue())
