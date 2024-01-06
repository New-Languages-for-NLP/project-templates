This directory contains the language module exported from Cadet.

The language module needs to be installable via `pip`, so it must include (at a minimum) a `setup.py` file and a `__init__.py` file. The `setup.py` file uses spaCy's entry points to register the language with spaCy.

**Replace the contents of this directory with your own language module**, renaming the directories labeled `zxx` to your ISO-639 language code. Then, **change the value of the `lang` variable in `project.yml`** to your language code.
