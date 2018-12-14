# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: container.py
#     date: 2018-04-03
#   author: koromodako
#  purpose:
#
#  license:
#    Datashark Forensic framework to process data containers.
#    Copyright (C) 2018 koromodako
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# =============================================================================
#  IMPORTS
# =============================================================================
from enum import Flag
from uuid import UUID, uuid4
from pathlib import Path
from slugify import slugify
from core.db.object import DBObject
from helper.bin_file import BinFile
from helper.logging.logger import Logger
from core.container.file_type_guesser import FileTypeGuesser
# =============================================================================
#  CLASSES
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Container(DBObject):
    '''[summary]

    [description]
    '''
    INDEX = 'container'
    FIELDS = [
        ('uuid', DBObject.DataType.STRING),
        ('parent', DBObject.DataType.STRING),
        ('path', DBObject.DataType.STRING),
        ('original_path', DBObject.DataType.STRING),
        ('mime_type', DBObject.DataType.STRING),
        ('mime_text', DBObject.DataType.STRING),
        ('slug', DBObject.DataType.STRING),
        ('size', DBObject.DataType.INT),
    ]
    PRIMARY = 'uuid'

    class Tag(Flag):
        '''Tag flag values
        '''
        NONE        = 0x00
        PERSISTED   = 0x01
        WHITELISTED = 0x02
        BLACKLISTED = 0x04

    def __init__(self,
                 name='',
                 path=Path(),
                 parent=UUID(int=0),
                 original_path=Path(),
                 magic_file=None):
        '''[summary]

        [description]

        Keyword Arguments:
            parent {UUID} -- [description] (default: {None})
            path {Path} -- [description] (default: {None})
            original_path {Path} -- [description] (default: {None})
            name {str} -- [description] (default: {None})
            magic_file {str} -- [description] (default: {None})
        '''
        super().__init__()
        if not isinstance(parent, UUID):
            raise ValueError("parent must be an instance of uuid.UUID")
        if not isinstance(path, Path):
            raise ValueError("path must be an instance of pathlib.Path")
        if not isinstance(original_path, Path):
            raise ValueError("original_path must be an instance of pathlib.Path")
        if not isinstance(name, str):
            raise ValueError("name must be an instance of str")

        self._tag = Container.Tag.NONE
        self._parent = parent
        self._path = path
        self._original_path = original_path
        self._slug = slugify(name)
        # computed once
        self._uuid = uuid4()
        self._size = None
        guesser = FileTypeGuesser(magic_file=magic_file)
        self._mime_text = guesser.mime_text(self._path)
        self._mime_type = guesser.mime_type(self._path)
        if self._path is not None:
            stat = self._path.stat()
            self._size = stat.st_size

    def __str__(self):
        '''String representation of the object
        '''
        return "Container(uuid={},size={},mime={},path={})".format(self._uuid,
                                                                   self._size,
                                                                   self._mime_type,
                                                                   self._path)

    @property
    def tag(self):
        return self._tag

    @property
    def parent(self):
        return self._parent

    @property
    def path(self):
        return self._path

    @property
    def original_path(self):
        return self._original_path

    @property
    def slug(self):
        return self._slug

    @property
    def uuid(self):
        return self._uuid

    @property
    def size(self):
        return self._size

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def mime_text(self):
        return self._mime_text

    def _source(self):
        '''Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties of an object.

        Returns:
            {dict} -- [description]
        '''
        return {
            'uuid': self._uuid.urn,
            'parent': self._parent.urn,
            'path': str(self._path),
            'original_path': str(self._original_path),
            'mime_type': self._mime_type,
            'mime_text': self._mime_text,
            'slug': self._slug,
            'size': self._size
        }

    def from_db(self, _source):
        '''Loads a document (dict) which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.

        Arguments:
            _source {dict} -- [description]
        '''
        self._uuid = UUID(_source['uuid'])
        self._parent = UUID(_source['parent'])
        self._path = Path(_source['path'])
        self._original_path = Path(_source['original_path'])
        self._mime_type = _source['mime_type']
        self._mime_text = _source['mime_text']
        self._slug = _source['slug']
        self._size = _source['size']

    def add_tag(self, tag):
        '''Adds given tag which can be a OR-ed combination of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to add
        '''
        self._tag |= tag

    def del_tag(self, tag):
        '''Removes given tag which can be a OR-ed combination of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to remove
        '''
        self._tag ^= tag

    def has_tag(self, tag):
        '''Checks if container has given tag which can be a OR-ed combination
        of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to check
        '''
        return ((self._tag & tag) == tag)

    def bin_file(self):
        '''Opens a read-only binary file for the container

        Returns:
            [BinFile] -- New instance of binary file
        '''
        return BinFile(self._path, BinFile.OpenMode.READ)
