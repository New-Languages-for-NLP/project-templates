from pathlib import Path

import typer
from spacy import Vocab
from spacy.training.converters.conllu_to_docs import conllu_sentence_to_doc

MISC_NER_PATTERN = "^((?:name|NE)=)?([BILU])-([A-Z_]+)|O$"


def check(in_dir: Path):
    """Check all .conll files in a directory for errors using spaCy."""

    for file in in_dir.glob("*.conll"):
        # log the file we're working on and open it
        typer.echo(f"Checking {file}")
        input_data = open(file).read()

        # iterate over sentences and attempt to make a Doc from each
        vocab = Vocab()
        for sent in input_data.strip().split("\n\n"):
            lines = sent.strip().split("\n")
            if lines:
                while lines[0].startswith("#"):
                    lines.pop(0)
                    try:
                        conllu_sentence_to_doc(
                            vocab,
                            lines,
                            MISC_NER_PATTERN,
                            merge_subtokens=False,
                            append_morphology=False,
                            ner_map=None,
                        )
                    except Exception as e:
                        typer.secho(f"Error: {e}", fg=typer.colors.RED)
                        typer.echo(f"Sentence:{sent}")


if __name__ == "__main__":
    typer.run(check)
