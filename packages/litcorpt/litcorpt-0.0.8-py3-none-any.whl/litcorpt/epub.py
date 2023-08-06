"""Functions to read epub and convert to litcorpt Book model"""

from typing import Dict, List, Generator, Iterator
from pathlib import Path

import ebooklib
from ebooklib import epub

from bs4 import BeautifulSoup as bs

from . import model


def epub_metadata_field_get(epub_handler: ebooklib.epub.EpubBook,
                            field_name: str) -> List[str]:
    """Retrieve a DC epub metadata and filter it"""
    field_value = epub_handler.get_metadata('DC', field_name)
    values = [entry[0]
              for entry in field_value
              if entry[0] is not None]

    # Convert html to text in description
    if field_name == 'description':
        values = list(map(lambda x: bs(x, 'html.parser').text.strip(), values))

    return values


def epub_metadata(epub_handler: ebooklib.epub.EpubBook) -> Dict:
    """Return a dictionary with epub metadata"""
    metadata_fields = ['identifier', 'title', 'language', 'creator',
                       'description', 'subject',
                       # Often trash data, just ignore
                       # 'format',
                       # 'relation',
                       # 'source',
                       # 'type',
                       # 'contributor',
                       # 'date',
                       ]

    metadata: Dict = {}
    for field_name in metadata_fields:
        field_value = epub_metadata_field_get(epub_handler, field_name)
        if field_value:
            metadata[field_name] = field_value

    return metadata


def epub_metadata_filter_identifier(identifier: List[str]) -> List[str]:
    """Filter identifier field"""
    identifier_filtered = []

    invalid_matches = [ 'urn', 'uuid', 'AWP', 'awp', '{' ]

    for ident in identifier:
        if not 10 < len(ident) < 23:
            continue

        if any(match in ident for match in invalid_matches):
            continue

        identifier_filtered.append(ident)

    return identifier_filtered


def epub_metadata_filter_language(language: List[str]) -> List[str]:
    """Filter language field"""
    language_filtered = []
    for lang in language:
        if lang.lower() == 'pt-br':
            lang = 'pt_BR'
        language_filtered.append(lang)

    return language_filtered


def epub_metadata_filter_creator(creator: List[str]) -> List[Dict]:
    """Filter creator field"""
    creator_filtered: List[str] = []
    for creat in creator:
        if creat.count(',') == 1:
            # We have a SURNANE, Name
            creat = ' '.join(list(map(lambda x: x.strip(), creat.split(',')))[::-1])
            creator_filtered.append(creat.strip())
        elif creator.count(',') > 1:
            # We proably have a list of authors separated by 'commas'.
            creat_list = creat.split(',')
            for creat_slice in creat_list:
                creator_filtered.append(creat_slice.strip())
        else:
            # We have a Name Surname
            creator_filtered.append(creat.strip())

    creator_dict: List[Dict] = []
    for creat in creator_filtered:
        creat_dict = {'role': 'author'}

        name = creat.split()
        if len(name) == 1:
            creat_dict['lastname'] = name[0]
        elif len(name) > 1:
            creat_dict['lastname'] = name[-1]
            creat_dict['firstname'] = ' '.join(name[:-1])

        creator_dict.append(creat_dict)

    return creator_dict


def epub_metadata_to_book(metadata: Dict, index: str) -> model.Book:
    """Return Book metadata from ePub"""
    local_metadata = metadata.copy()

    local_metadata['index'] = index

    if 'identifier' in metadata and metadata['identifier']:
        local_metadata['identifier'] = epub_metadata_filter_identifier(local_metadata['identifier'])

    if not local_metadata['identifier']:
        del local_metadata['identifier']

    if 'language' in metadata and metadata['language']:
        local_metadata['language'] = epub_metadata_filter_language(local_metadata['language'])

    if 'creator' in metadata and metadata['creator']:
        local_metadata['creator'] = epub_metadata_filter_creator(local_metadata['creator'])

    book = model.Book(**local_metadata)

    return book


def epub_contents_text(epub_items: Iterator[ebooklib.epub.EpubHtml]) -> str:
    """Convert a epub content to text"""
    book_contents: List[str] = []
    book_contents = [bs(epub_item.get_body_content(), "html.parser").text
                     for epub_item in epub_items]

    contents: str = "".join(book_contents)
    return contents


def epub_filter_bodymatter(epub_items: Iterator[ebooklib.epub.EpubHtml],
                          ) -> Generator[ebooklib.epub.EpubHtml, None, None]:
    """Filter some epub content"""
    # Remove some useless epub content.
    for epub_item in epub_items:
        if "odin" in epub_item.get_name().lower():
            continue
        if "copyright" in epub_item.get_name().lower():
            continue
        if "toc" in epub_item.get_name().lower():
            continue
        if "also" in epub_item.get_name().lower():
            continue

        yield epub_item


def epub_filter_text(epub_items: Iterator[ebooklib.epub.EpubItem],
                    ) -> Generator[ebooklib.epub.EpubHtml, None, None]:
    """Filter out all non text content from epub"""
    for epub_item in epub_items:
        if epub_item.get_type() == ebooklib.ITEM_DOCUMENT:
            yield epub_item


def get_epub_items(epub_handler: ebooklib.epub.EpubBook,
                  ) -> Generator[ebooklib.epub.EpubItem, None, None]:
    """Generator for epub items in epub"""
    for epub_item in epub_handler.get_items():
        yield epub_item


def read(path: Path, index: str) -> model.Book:
    """Receive a epub file path and convert to Book Model indexed by index.
    Index will be used to uniquely identify the book in database, also as a directory
    name when writing to disk.
    """
    epub_handler: ebooklib.epub.EpubBook = epub.read_epub(path)
    epub_contents: Iterator[ebooklib.epub.EpubItem] = get_epub_items(epub_handler)
    epub_contents = epub_filter_text(epub_contents)
    epub_contents = epub_filter_bodymatter(epub_contents)
    epub_text: str = epub_contents_text(epub_contents)
    metadata: Dict = epub_metadata(epub_handler)
    metadata['contents'] = epub_text
    book = epub_metadata_to_book(metadata, index)

    return book
