This directory contains annotated data exported from INCEpTION.

Data for most linguistic layers is stored in the [CoNLL-U format](https://universaldependencies.org/format.html), with one token per line and blank lines separating sentences. Each annotated text is stored in a single file with the `.conllu` extension, by convention.

Because CoNLL-U does not support named entity annotation without a custom extension, named entity annotations are stored in the simpler [IOB format](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)). Each annotated text is stored in a single file with the `.conll` extension, similar to [CoNLL-2002 data](https://aclanthology.org/W02-2024.pdf).

When the data is converted into spaCy's binary format, any `.conllu` and `.conll` files with the same base name will be joined together into a single collection of documents. For example, `my_text.conllu` and `my_text.conll` will be joined together into a single collection of documents named `my_text`. **If the filenames differ, the data will be treated as separate documents, which will impact your model's accuracy.**

The included examples are annotated data from Project Gutenberg; see the README in the [text](../text) directory for more information. This data was annotated automatically and is not intended to be used for training a real model.
