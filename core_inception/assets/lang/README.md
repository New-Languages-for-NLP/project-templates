This directory contains the language module exported from Cadet.

The language module needs to be installable via `pip`, so it must include (at a minimum) a `setup.py` file and a `__init__.py` file. The `setup.py` file uses spaCy's entry points to register the language with spaCy.

The module should have a directory structure like this:
```
lang
├── zxx
│   ├── setup.py
│   ├── zxx
│   │   ├── __init__.py
│   │   └── [any other files in the module]
```

**Replace the contents of this directory with your own language module**, renaming the directories labeled `zxx` to your [ISO-639 language code](https://www.loc.gov/standards/iso639-2/php/code_list.php). Then:
- change the value of the `lang` variable in `project.yml` to your language code
- change the value of `[nlp.lang]` in `configs/config.cfg` to your language code

When you run `spacy project run install-language`, spaCy will install your language module as a Python package, and register it with spaCy.
