"""Split the corpus into train, dev, and test sets"""


import typer
from pathlib import Path
import random

from spacy.tokens import DocBin
from spacy.util import get_lang_class
from sklearn.model_selection import train_test_split


def split(input_path: Path, output_path: Path, split_size: float, lang: str):
    # make sure corpus file and output dir exist
    assert input_path.is_file()
    assert output_path.is_dir()

    # load custom language model for its vocab
    lang = get_lang_class(lang)
    nlp = lang()

    # load all the docs from the input file and shuffle them
    all_docs = list(DocBin().from_disk(input_path).get_docs(nlp.vocab))
    random.shuffle(all_docs)

    # split the docs into train and validation sets
    train_docs, validation_docs = train_test_split(all_docs, test_size=split_size)

    # split the validation docs into dev and test sets
    dev_docs, test_docs = train_test_split(validation_docs, test_size=split_size)

    # save all of the sets to disk
    train_db = DocBin(docs=train_docs)
    train_db.to_disk(output_path / "train.spacy")
    typer.echo(f"Wrote 'train.spacy' ({len(train_docs)} docs)")

    dev_db = DocBin(docs=dev_docs)
    dev_db.to_disk(output_path / "dev.spacy")
    typer.echo(f"Wrote 'dev.spacy' ({len(dev_docs)} docs)")

    test_db = DocBin(docs=test_docs)
    test_db.to_disk(output_path / "test.spacy")
    typer.echo(f"Wrote 'test.spacy' ({len(test_docs)} docs)")


if __name__ == "__main__":
    typer.run(split)
