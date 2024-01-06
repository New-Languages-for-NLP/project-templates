"""Split the corpus into train, dev, and test sets"""


from pathlib import Path
import random

import typer
from spacy.tokens import DocBin
from spacy.util import get_lang_class
from sklearn.model_selection import train_test_split
from wasabi import msg


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
    msg.info(f"Loaded full corpus ({len(all_docs)} documents)")
    msg.info(f"Reserving {split_size:.0%} of the corpus for evaluation")

    # split the docs into train and validation sets
    train_docs, validation_docs = train_test_split(all_docs, test_size=split_size)

    # split the validation docs into dev and test sets
    dev_docs, test_docs = train_test_split(validation_docs, test_size=split_size)

    # save all of the sets to disk
    train_db = DocBin(docs=train_docs)
    train_path = (output_path / "train.spacy").resolve()
    train_db.to_disk(train_path)
    msg.good(f"Generated training set ({len(train_docs)} documents): {train_path}")

    dev_db = DocBin(docs=dev_docs)
    dev_path = (output_path / "dev.spacy").resolve()
    dev_db.to_disk(dev_path)
    msg.good(f"Generated development set ({len(dev_docs)} documents): {dev_path}")

    test_db = DocBin(docs=test_docs)
    test_path = (output_path / "test.spacy").resolve()
    test_db.to_disk(test_path)
    msg.good(f"Generated test set ({len(test_docs)} documents): {test_path}")


if __name__ == "__main__":
    typer.run(split)
