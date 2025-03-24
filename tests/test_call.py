"""Test command calls."""

import os
import unittest
from io import StringIO

from polint import get_files, main


class TestGetFiles(unittest.TestCase):
    """Test `get_files` function."""

    def test_single_file(self):
        single_file = os.path.join(os.path.dirname(__file__), 'data', 'empty.po')
        files = get_files([single_file])
        self.assertEqual(list(files), [single_file])

    def test_directory(self):
        dirname = os.path.join(os.path.dirname(__file__), 'data')
        files = get_files([dirname])
        self.assertCountEqual(
            list(files),
            [os.path.join(dirname, f) for f in ('empty.po', 'header_only.po', 'invalid.po', 'simple_valid.po')])

    def test_directory_filter(self):
        # Test `get_files` returns only gettext files when run on `tests` directory, i.e. it ignores .py files.
        dirname = os.path.dirname(__file__)
        files = get_files([dirname])
        self.assertCountEqual(
            list(files),
            [os.path.join(dirname, 'data', f) for f in ('empty.po', 'header_only.po', 'invalid.po', 'simple_valid.po')])


class TestMain(unittest.TestCase):
    """Test `main` function."""

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
        location_output = 'invalid.po:23: [unsorted] entry is not sorted\n' \
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
                   'untranslated,location,fuzzy,obsolete,unsorted']
            main(cmd, output=output)
        self.assertEqual(context.exception.code, 0)
