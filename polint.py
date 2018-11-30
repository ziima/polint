"""
Validate gettext PO files.

Usage: polint.py [options] <path>...
       polint.py -h | --help
       polint.py --version

Positional arguments:
  path                  PO file or directory to be linted

Options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --show-msg            print the message for each error
  -i, --ignore=IGNORE   skip errors (e.g. untranslated,location)
"""
import fnmatch
import os
import sys
from collections import OrderedDict

import polib
from docopt import docopt

__version__ = '0.4'


################################################################################
# Validators register
class ValidatorRegister(object):
    """Validators register."""

    def __init__(self):
        """Initialize the register. Take no parameters."""
        # Dictionary of (code, description) pairs
        self._errors = OrderedDict()
        # Dictionary of (code, callback) pairs
        self._validators = OrderedDict()

    @property
    def errors(self):
        """Return dictionary of (error_code, error_description) pairs."""
        return self._errors.copy()

    @property
    def validators(self):
        """Return dictionary of (error_code, callback) pairs."""
        return self._validators.copy()

    def register(self, callback, error_code, error_description):
        """Register validator.

        @param callback: Function which performs validation.
        @type callback: function
        @param error_code: Error code which will be reported if validation fails.
        @type error_code: text
        @param error_description: Error description which will be reported if validation fails.
        @type error_description: text
        @raises ValueError: If `error_code` is already registered.
        """
        if error_code in self._validators:
            raise ValueError('Validator for %s is already registered.' % error_code)
        self._errors[error_code] = error_description
        self._validators[error_code] = callback


REGISTER = ValidatorRegister()


################################################################################
# Linter
class Status(object):
    """Linting process status.

    @ivar entry: Currently processed entry.
    @ivar previous: Previously processed entry.
    """

    def __init__(self):
        """Initialize the register. Take no parameters."""
        self.entry = None
        self.previous = None

    def step(self, entry):
        """Move to the next entry.

        @param entry: The next entry.
        """
        self.previous = self.entry
        self.entry = entry


class Linter(object):
    """Linter performs the actual validation of the PO files.

    If opens the pofile and runs all registered validators on each entry.

    @ivar errors: Dictionary of (entry, errors) pairs found in validation
    @type errors: {POEntry: [text, text, ...], ...}
    """

    def __init__(self, pofile, exclude=None, register=REGISTER):
        """Initialize Linter.

        @param pofile: Filename or a file to be validated
        @type pofile: text or file
        @param exclude: Set of validators to exclude
        @type exclude: Set of strings
        @param register: Validator register to be used
        @type register: ValidatorRegister
        """
        self.pofile = pofile
        self.register = register
        self.exclude = exclude or set()
        self.errors = OrderedDict()

    def run_validators(self):
        """Run the checks."""
        validators = tuple((code, v) for code, v in self.register.validators.items() if code not in self.exclude)
        status = Status()
        for entry in polib.pofile(self.pofile):
            status.step(entry)
            for code, callback in validators:
                if not callback(status):
                    entry_errors = self.errors.setdefault(status.entry, [])
                    entry_errors.append(code)


################################################################################
# Validators
#
# All validators has to expect POEntry as their first argument and return whether the validation passed.
def fuzzy_validator(status):
    """Check if current entry is fuzzy."""
    return 'fuzzy' not in status.entry.flags


REGISTER.register(fuzzy_validator, 'fuzzy', 'translation is fuzzy')


def obsolete_validator(status):
    """Check if current entry is obsolete."""
    return not status.entry.obsolete


REGISTER.register(obsolete_validator, 'obsolete', 'entry is obsolete')


def untranslated_validator(status):
    """Check if current entry is translated."""
    return status.entry.translated()


REGISTER.register(untranslated_validator, 'untranslated', 'translation is missing')


def no_location_validator(status):
    """Check if current entry has no location data."""
    return not status.entry.occurrences


REGISTER.register(no_location_validator, 'location', 'entry contains location')


def sort_validator(status):
    """Check if the entry is properly sorted."""
    if status.previous is None:
        # First entry is always correctly sorted.
        return True
    if status.previous.msgid == status.entry.msgid:
        previous_msgctx = status.previous.msgctxt or ''
        entry_msgctxt = status.entry.msgctxt or ''
        return previous_msgctx < entry_msgctxt
    else:
        return status.previous.msgid < status.entry.msgid


REGISTER.register(sort_validator, 'unsorted', 'entry is not sorted')


################################################################################
# Polint command
MSG_FORMAT = '%(filename)s:%(line)s: [%(error)s] %(description)s\n'


def get_files(paths):
    """Return only paths to files to be linted.

    @param paths: List of files or directories to be linted.
    """
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for filename in fnmatch.filter(files, '*.po'):
                    yield os.path.join(root, filename)
        else:
            yield path


def main(args=None, output=sys.stdout):
    """Run the polint.

    @param args: Command line arguments. Mainly for tests.
    @param output: Standard output file object. Mainly for tests.
    """
    options = docopt(__doc__, args, version=__version__)

    exit_code = 0
    if options.get('--ignore'):
        exclude = {i for i in options['--ignore'].split(',')}
    else:
        exclude = None
    for filename in get_files(options['<path>']):
        linter = Linter(filename, exclude=exclude)
        linter.run_validators()
        if linter.errors:
            exit_code = 1
        error_defs = REGISTER.errors
        for entry, errors in linter.errors.items():
            for error in errors:
                msg_data = {'filename': filename, 'line': entry.linenum, 'error': error,
                            'description': error_defs[error]}
                output.write(MSG_FORMAT % msg_data)
            if options['--show-msg']:
                output.write(str(entry))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
