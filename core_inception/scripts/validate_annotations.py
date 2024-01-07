"""Validate that spaCy can parse all .conll and .conllu files in a directory."""

from pathlib import Path

from spacy.training.converters.conllu_to_docs import conllu_to_docs
from spacy.training.converters.conll_ner_to_docs import conll_ner_to_docs
import typer
from wasabi import msg


def check(in_dir: Path):
    # check that the input directory exists
    assert in_dir.is_dir()

    # iterate over all .conll and .conllu files in the directory
    msg.info(f"Validating annotated data")
    conll_files = list(in_dir.glob("*.conll"))
    conllu_files = list(in_dir.glob("*.conllu"))
    for file in conll_files + conllu_files:
        input_data = file.read_text().strip()

        # iterate over sentences and attempt to make a Doc from each
        # if there's an error, print the file, sentence, and the error
        for sent in input_data.split("\n\n"):
            try:
                if file.suffix == ".conll":
                    list(conll_ner_to_docs(sent, no_print=True))
                else:
                    list(conllu_to_docs(sent, no_print=True))
            except Exception as e:
                msg.fail(f"File is not valid: {file.resolve()}")
                msg.fail(f"Error: {e}")
                msg.fail(f"Sentence:")
                print(sent)
                exit(1)

        # if we get here, the file is valid
        msg.good(f"File is valid: {file.resolve()}")


if __name__ == "__main__":
    typer.run(check)
