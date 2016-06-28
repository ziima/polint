"""
polint - Linter for gettext PO files
"""
import argparse
import sys
from collections import OrderedDict

import polib


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
        self._validators = OrderedDict()

    @property
    def errors(self):
        """
        Dictionary of (error_code, error_description) pairs.
        """
        return self._errors.copy()

    @property
    def validators(self):
        """
        Dictionary of (error_code, callback) pairs.
        """
        return self._validators.copy()

    def register(self, callback, error_code, error_description):
        """
        Registers validator.

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
class Linter(object):
    """
    Linter performs the actual validation of the PO files

    If opens the pofile and runs all registered validators on each entry.

    @ivar errors: Dictionary of (entry, errors) pairs found in validation
    @type errors: {POEntry: [text, text, ...], ...}
    """
    def __init__(self, pofile, register=REGISTER):
        """
        Initializes Linter

        @param pofile: Filename or a file to be validated
        @type pofile: text or file
        @param register: Validator register to be used
        @type register: ValidatorRegister
        """
        self.pofile = pofile
        self.register = register
        self.errors = OrderedDict()

    def run_validators(self):
        """
        Runs the checks
        """
        for entry in polib.pofile(self.pofile):
            for code, callback in self.register.validators.iteritems():
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
REGISTER.register(fuzzy_validator, 'fuzzy', 'translation is fuzzy')


def obsolete_validator(entry):
    """Checks if entry is obsolete"""
    return not entry.obsolete
REGISTER.register(obsolete_validator, 'obsolete', 'entry is obsolete')


def untranslated_validator(entry):
    """Checks if entry is translated"""
    return entry.translated()
REGISTER.register(untranslated_validator, 'untranslated', 'translation is missing')


def no_location_validator(entry):
    """Checks if entry has no location data"""
    return not entry.occurrences
REGISTER.register(no_location_validator, 'location', 'entry contains location')


################################################################################
# Polint command
def get_parser():
    parser = argparse.ArgumentParser(description="Validates PO files")
    parser.add_argument('filenames', metavar='file', nargs='+', help='PO file to be linted')
    parser.add_argument('--show-msg', action="store_true", help="Print the message for each error")
    return parser


MSG_FORMAT = '%(filename)s:%(line)s: [%(error)s] %(description)s\n'


def main(args=None, output=sys.stdout):
    parser = get_parser()
    options = parser.parse_args(args)

    exit_code = 0
    for filename in options.filenames:
        linter = Linter(filename)
        linter.run_validators()
        if linter.errors:
            exit_code = 1
        error_defs = REGISTER.errors
        for entry, errors in linter.errors.iteritems():
            for error in errors:
                msg_data = {'filename': filename, 'line': entry.linenum, 'error': error,
                            'description': error_defs[error]}
                output.write(MSG_FORMAT % msg_data)
            if options.show_msg:
                output.write(str(entry))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
