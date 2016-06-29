# polint - Linter for gettext PO files #

[![Build Status](https://travis-ci.org/ziima/polint.svg?branch=master)](https://travis-ci.org/ziima/polint)

`polint` is a tool which validates PO files against defined convensions

## Usage ##
```
polint.py [options] file [file ...]
```
To print complete usage use `--help` option.


## Errors ##
 * `fuzzy` - Translation is fuzzy
 * `obsolete` - Entry is obsolete
 * `untranslated` - Translation is missing. That includes `fuzzy` or `obsolete`.
 * `location` - Entry contains location data
