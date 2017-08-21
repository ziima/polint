"""
polint - Linter for gettext PO files
"""
import argparse
import sys
from collections import OrderedDict

import polib


__version__ = '0.1'


################################################################################
# Validators register
class ValidatorRegister(object):
    """
    Register of validators
    """
    def __init__(self):
        # Dictionary of (code, description) pairs
        self._errors = OrderedDict()
        # Dictionary of (code, callback) pairs
        self._entry_validators = OrderedDict()

    @property
    def errors(self):
        """
        Returns registered errors.

        @return: Dictionary of (error_code, error_description) pairs.
        """
        return self._errors.copy()

    @property
    def entry_validators(self):
        """
        Returns registered entry validators.

        @return: Dictionary of (error_code, callback) pairs.
        """
        return self._entry_validators.copy()

    def register_entry(self, callback, error_code, error_description):
        """
        Registers entry validator.

        Callback must match signature (POEntry entry).

        @param callback: Function which performs validation.
        @type callback: function
        @param error_code: Error code which will be reported if validation fails.
        @type error_code: text
        @param error_description: Error description which will be reported if validation fails.
        @type error_description: text
        @raises ValueError: If `error_code` is already registered.
        """
        if error_code in self._errors:
            raise ValueError('Validator for %s is already registered.' % error_code)
        self._errors[error_code] = error_description
        self._entry_validators[error_code] = callback


REGISTER = ValidatorRegister()


################################################################################
# Linter
class Linter(object):
    """
    Linter performs the actual validation of the PO files

    If opens the pofile and runs all registered validators on each entry.

    @ivar errors: Dictionary of (entry, errors) pairs found in validation
    @type errors: {POEntry: [text, text, ...], ...}
    """
    def __init__(self, pofile, exclude=None, register=REGISTER):
        """
        Initializes Linter

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
        """
        Runs the checks
        """
        entry_validators = tuple((code, v) for code, v in self.register.entry_validators.items()
                                 if code not in self.exclude)
        for entry in polib.pofile(self.pofile):
            for code, callback in entry_validators:
                if not callback(entry):
                    entry_errors = self.errors.setdefault(entry, [])
                    entry_errors.append(code)


################################################################################
# Validators
#
# All validators has to expect POEntry as their first argument and return whether the validation passed.
def fuzzy_validator(entry):
    """Checks if entry is fuzzy"""
    return 'fuzzy' not in entry.flags
REGISTER.register_entry(fuzzy_validator, 'fuzzy', 'translation is fuzzy')


def obsolete_validator(entry):
    """Checks if entry is obsolete"""
    return not entry.obsolete
REGISTER.register_entry(obsolete_validator, 'obsolete', 'entry is obsolete')


def untranslated_validator(entry):
    """Checks if entry is translated"""
    return entry.translated()
REGISTER.register_entry(untranslated_validator, 'untranslated', 'translation is missing')


def no_location_validator(entry):
    """Checks if entry has no location data"""
    return not entry.occurrences
REGISTER.register_entry(no_location_validator, 'location', 'entry contains location')


################################################################################
# Polint command
def get_parser():
    parser = argparse.ArgumentParser(description="Validates PO files")
    parser.add_argument('filenames', metavar='file', nargs='+', help='PO file to be linted')
    parser.add_argument('--show-msg', action="store_true", help="Print the message for each error")
    parser.add_argument('--ignore', default='', help="skip errors (e.g. untranslated,location)")
    return parser


MSG_FORMAT = '%(filename)s:%(line)s: [%(error)s] %(description)s\n'


def main(args=None, output=sys.stdout):
    parser = get_parser()
    options = parser.parse_args(args)

    exit_code = 0
    exclude = {i for i in options.ignore.split(',')}
    for filename in options.filenames:
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
            if options.show_msg:
                output.write(str(entry))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
