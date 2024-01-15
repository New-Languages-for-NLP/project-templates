# Project Assets

## Annotations (`/annotations`)

This directory contains annotated data exported from INCEpTION.

Data for most linguistic layers is stored in the [CoNLL-U format](https://universaldependencies.org/format.html), with one token per line and blank lines separating sentences. Each annotated text is stored in a single file with the `.conllu` extension.

If you have named entity annotations and wish to combine them with your other syntactic annotations, you can additionally export the [CoNLL-2002 NER format](https://www.clips.uantwerpen.be/conll2002/ner/) for each file. These files will have the `.conll` extension. After export, you can use the `merge_annotations` script to add the NER annotations to the `MISC` column of your CoNLL-U files, for example:

```bash
python scripts/merge_annotations.py annotations/my_text.conllu annotations/my_text.conll > merged.conllu
```

For more information, try:

```bash
python scripts/merge_annotations.py --help
```

The included examples are annotated data from Project Gutenberg; see section on the [text](../text) directory below for more information. This example data was annotated automatically and is not intended to be used for training a real model.

## Language Module (`/lang`)

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

## Raw Text (`/text`)

This directory contains two example texts from Project Gutenberg:

- _A Muramasa blade: A story of feudalism in old Japan_ by Louis Wertheimber (1887) - [muramasa.txt](muramasa.txt)
- _The Vanguard of Venus_ by Landell Bartlett (1944) - [vanguard.txt](vanguard.txt)

For the license governing the use of these texts, see [LICENSE](LICENSE).

You can use plain text (`.txt`) files like this to pre-train your language model.

**Replace these texts with ones from your target language.**

Make sure to replace the [LICENSE](LICENSE) file with one that applies to your texts, or cite the source of your texts in your project description.
