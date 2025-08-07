from spacy.tokens import Span
from spacy.language import Language

def is_location(span: Span, nlp: Language) -> bool:
    doc = nlp(span.text)
    return any(ent.label_ in {"GPE", "LOC"} for ent in doc.ents)
