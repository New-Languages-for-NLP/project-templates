import spacy
from spacy.language import Language
from spacy.lang.en import EnglishDefaults


@spacy.registry.languages("zxx")
class NewLanguage(Language):
    """Placeholder language class representing your new language."""

    lang = "zxx"
    Defaults = EnglishDefaults


__all__ = ["NewLanguage"]
