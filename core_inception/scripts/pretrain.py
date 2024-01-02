
"""Load inception conllu data and convert to spaCy binary format (DocBin)"""
import srsly
import typer
import warnings
from pathlib import Path
import subprocess

import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans, get_lang_class


def pretrain(raw_text_folder:str, lang:str):

    lang = get_lang_class(lang)
    nlp = lang()
    #TODO handle only txt files? what of other formats
    texts = [t.read_text() for t in Path(raw_text_folder).iterdir() if t.suffix == ".txt"]
    docbin = DocBin()
    [docbin.add(nlp(text)) for text in texts]
    save_path = Path.cwd() / 'corpus' / 'converted' / 'raw_text.spacy'
    docbin.to_disk(save_path)


if __name__ == "__main__":
    typer.run(pretrain)
