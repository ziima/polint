"""
Test command calls.
"""
import os
import unittest

from polint import main

try:
    # Python 2
    from cStringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


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

    def test_ignore_unknown(self):
        # Ignore unknown error
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'invalid.po'), '--ignore', 'unknown'], output=output)
        self.assertEqual(context.exception.code, 1)
        self.assertIn('invalid.po:13: [fuzzy] translation is fuzzy\n', output.getvalue())
        self.assertIn('invalid.po:13: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:17: [obsolete] entry is obsolete\n', output.getvalue())
        self.assertIn('invalid.po:17: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:20: [untranslated] translation is missing\n', output.getvalue())
        self.assertIn('invalid.po:23: [location] entry contains location\n', output.getvalue())

    def test_ignore_untranslated(self):
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'invalid.po'), '--ignore', 'untranslated'],
                 output=output)
        self.assertEqual(context.exception.code, 1)
        self.assertIn('invalid.po:13: [fuzzy] translation is fuzzy\n', output.getvalue())
        self.assertIn('invalid.po:17: [obsolete] entry is obsolete\n', output.getvalue())
        self.assertNotIn(': [untranslated] ', output.getvalue())

    def test_ignore_multiple(self):
        # Ignore multiple errors
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            main([os.path.join(os.path.dirname(__file__), 'data', 'invalid.po'), '--ignore', 'untranslated,location'],
                 output=output)
        self.assertEqual(context.exception.code, 1)
        self.assertIn('invalid.po:13: [fuzzy] translation is fuzzy\n', output.getvalue())
        self.assertIn('invalid.po:17: [obsolete] entry is obsolete\n', output.getvalue())
        self.assertNotIn(': [untranslated] ', output.getvalue())
        self.assertNotIn(': [location] ', output.getvalue())

    def test_ignore_all(self):
        # Ignore multiple errors
        output = StringIO()
        with self.assertRaises(SystemExit) as context:
            cmd = [os.path.join(os.path.dirname(__file__), 'data', 'invalid.po'), '--ignore',
                   'untranslated,location,fuzzy,obsolete']
            main(cmd, output=output)
        self.assertEqual(context.exception.code, 0)
