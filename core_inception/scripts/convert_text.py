"""Convert plaintext to spaCy binary format for pretraining"""

import typer
from pathlib import Path

from spacy.tokens import DocBin
from spacy.util import get_lang_class


def convert(input_path: Path, output_path: Path, lang: str):
    # make sure the input and output directories exist
    assert input_path.is_dir()
    assert output_path.is_dir()

    # load custom language model for its vocab
    lang = get_lang_class(lang)
    nlp = lang()

    # convert all of the input .txt files to docs
    db = DocBin()
    for text_file in input_path.glob("*.txt"):
        doc = nlp.make_doc(text_file.read_text())
        db.add(doc)

    # save the DocBin to disk
    db.to_disk(output_path / "pretrain.spacy")
    typer.echo(f"Wrote 'pretrain.spacy' ({len(db)} docs)")


if __name__ == "__main__":
    typer.run(convert)
