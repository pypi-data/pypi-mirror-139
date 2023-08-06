"""A set of convenience functions to search in fields"""
import re
from typing import Generator

from unidecode import unidecode
from tinydb import database

from . import model


def creator_name(corpusdb: database.TinyDB,
                 pattern: str) -> Generator[model.Book, None, None]:
    """Return a list of document based on creator's name. It completely
    ignores accents and case."""
    for document in iter(corpusdb):
        if any(re.search(unidecode(pattern),
                        unidecode(creator['name']),
                        flags=re.IGNORECASE)
               for creator in document['creator']):
            yield model.Book(**document)

def index(corpusdb: database.TinyDB,
          pattern: str) -> Generator[model.Book, None, None]:
    """Return a list of document based on document index."""
    for document in iter(corpusdb):
        if re.search(pattern, document['index']):
            yield model.Book(**document)


def title(corpusdb: database.TinyDB,
          pattern: str) -> Generator[model.Book, None, None]:
    """Return a list of documents based on name. It completely
    ignores accents and case"""
    for document in iter(corpusdb):
        if re.search(unidecode(pattern),
                     unidecode(document['title']),
                     flags=re.IGNORECASE):
            yield model.Book(**document)
