# Change log for utf8-locale, the UTF-8-compatible locale detector

0.3.0
-----

- BREAKING: The Rust implementation does not make the individual
  functions visible by default in the top-level namespace;
  the new builder interface is preferred.

- IMPORTANT: Add a new object-oriented interface for the Python and Rust
  implementations: configure a `Utf8Detect` or `LanguagesDetect` object,
  and invoke their `.detect()` method instead of invoking the individual
  functions.

- Fix the functional test's behavior if the u8loc executable does not
  advertise the query-preferred feature.
- Add a C implementation: a `libutf8_locale` library and a `u8loc`
  executable built using CMake.
- Add the `tests/full.sh` development helper tool that rebuilds all
  the implementations and runs their respective tests.
- Add `*.c`, `*.h`, and `*.1` file definitions to the EditorConfig file.

- Python:
  - drop the `b0` suffix from the `black` tool versioned dependencies;
    the `black` tool is no longer in beta since version 22
  - move the languages test data to the `tests/data.json` definitions, too
  - add an object-oriented builder interface

- Rust:
  - add an object-oriented builder interface
  - add the beginnings of a unit test suite using the JSON test definitions
  - use the `lazy_static` crate to only compile regular expressions once
  - import struct names directly as a more idiomatic style

0.2.0
-----

- IMPORTANT: the "C" language is now appended to the end of the list
  returned by the `get_preferred_languages()` function if it is not
  already there!

- Add the `get_utf8_vars()` function returning an environment-like
  dictionary that only contains the variables that need to be set,
  i.e. `LC_ALL` and `LANGUAGE`.
- Add the `u8loc` command-line tool to the Python implementation.
- Add the `u8loc.1` manual page.
- Bring the Python build infrastructure somewhat more up to date.
- Add the `tests/functional.py` functional testing tool.
- Require Python 3.7 for dataclasses support.
- Add an EditorConfig definitions file.
- Push the Python implementation into a `python/` source subdirectory.
- Add a Rust implementation.

0.1.1
-----

- Ignore locales with weird names instead of erroring out.
- Ignore the type of a `subprocess.check_output()` mock in the test suite.
- Add a manifest file for the source distribution.

0.1.0
-----

- First public release.
