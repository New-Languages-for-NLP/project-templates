import re
from pathlib import Path

import typer
from wasabi import msg
from spacy.morphology import Morphology


def merge(
    base_doc_path: Path = typer.Argument(help="Path to the base CoNLL-U file"),
    ner_doc_path: Path = typer.Argument(help="Path to the NER CoNLL-2002 file"),
    cleanup: bool = typer.Option(
        default=False, help="Delete the NER doc after merging"
    ),
):
    """
    Merge entities from a CoNLL-2002 file into a CoNLL-U file.

    IOB-format tags will be inserted into the MISC column of the base doc, e.g.
    "NE=B-PERSON" for a token that is the beginning of a PERSON entity.

    This format is automatically recognized by spacy's `convert` command, so
    the merged file will produce a spacy `Doc` with both syntactic and semantic
    annotations (i.e. `doc.ents`).
    """
    # make sure the input directory exists
    if not base_doc_path.is_file():
        msg.fail(f"File not found: {base_doc_path.resolve()}")
    if not ner_doc_path.is_file():
        msg.fail(f"File not found: {ner_doc_path.resolve()}")

    # load the file contents
    base_doc = base_doc_path.read_text("utf8").strip()
    ner_doc = ner_doc_path.read_text("utf8").strip()

    # split the file contents into sentences
    base_sentences = base_doc.split("\n\n")
    ner_sentences = ner_doc.split("\n\n")
    if len(base_sentences) != len(ner_sentences):
        msg.fail(
            f"Number of sentences in base and NER docs do not match: "
            f"{len(base_sentences)} != {len(ner_sentences)}"
        )

    # merge the sentences
    output_sentences = []
    for base_sent, ner_sent in zip(base_sentences, ner_sentences):
        base_lines = base_sent.split("\n")
        ner_lines = ner_sent.split("\n")
        output_lines = []
        i = 0
        # skip comment lines in the base doc
        for base_line in base_lines:
            if base_line.startswith("#"):
                output_lines.append(base_line)
            else:
                ner_line = ner_lines[i]
                base_token = base_line.split("\t")
                ner_token = re.split(r"\s+", ner_line)
                misc = Morphology.feats_to_dict(base_token[9])

                # if the final column in the NER doc is not "O", add it to the
                # MISC of the base doc as "NE", e.g. "NE=B-PER"
                if len(ner_token) > 1 and not ner_token[-1].startswith("O"):
                    misc["NE"] = ner_token[-1]
                    base_token[9] = Morphology.dict_to_feats(misc)

                output_lines.append("\t".join(base_token))
                i += 1
        output_sentences.append("\n".join(output_lines))

    # join the sentences back together
    output_str = "\n\n".join(output_sentences)

    # write to stdout
    typer.echo(output_str)

    # if cleanup is True, remove the NER doc
    if cleanup:
        ner_doc_path.unlink()


if __name__ == "__main__":
    typer.run(merge)
