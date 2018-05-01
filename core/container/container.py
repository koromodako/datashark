# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: container.py
#     date: 2018-04-03
#   author: paul.dautry
#  purpose:
#
#  license:
#    Datashark Forensic framework to process data containers.
#    Copyright (C) 2018 paul.dautry
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
        if not isinstance(parent, UUID):
            raise ValueError("parent must be an instance of uuid.UUID")
        if not isinstance(path, Path):
            raise ValueError("path must be an instance of pathlib.Path")
        if not isinstance(original_path, Path):
            raise ValueError("original_path must be an instance of pathlib.Path")
        if not isinstance(name, str):
            raise ValueError("name must be an instance of str")

        self.tag = Container.Tag.NONE
        self.parent = parent
        self.path = path
        self.original_path = original_path
        self.slug = slugify(name)
        # computed once
        self.uuid = uuid4()
        self.size = None
        guesser = FileTypeGuesser(magic_file=magic_file)
        self.mime_text = guesser.mime_text(self.path)
        self.mime_type = guesser.mime_type(self.path)
        if self.path is not None:
            stat = self.path.stat()
            self.size = stat.st_size

    def __str__(self):
        '''String representation of the object
        '''
        return "Container(uuid={},size={},mime={},path={})".format(self.uuid,
                                                                   self.size,
                                                                   self.mime_type,
                                                                   self.path)

    def _source(self):
        '''Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties of an object.

        Returns:
            {dict} -- [description]
        '''
        return {
            'uuid': self.uuid.urn,
            'parent': self.parent.urn,
            'path': str(self.path),
            'original_path': str(self.original_path),
            'mime_type': self.mime_type,
            'mime_text': self.mime_text,
            'slug': self.slug,
            'size': self.size
        }

    def from_db(self, _source):
        '''Loads a document (dict) which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.

        Arguments:
            _source {dict} -- [description]
        '''
        self.uuid = UUID(_source['uuid'])
        self.parent = UUID(_source['parent'])
        self.path = Path(_source['path'])
        self.original_path = Path(_source['original_path'])
        self.mime_type = _source['mime_type']
        self.mime_text = _source['mime_text']
        self.slug = _source['slug']
        self.size = _source['size']

    def add_tag(self, tag):
        '''Adds given tag which can be a OR-ed combination of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to add
        '''
        self.tag |= tag

    def del_tag(self, tag):
        '''Removes given tag which can be a OR-ed combination of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to remove
        '''
        self.tag ^= tag

    def has_tag(self, tag):
        '''Checks if container has given tag which can be a OR-ed combination
        of tags

        Arguments:
            tag {Container.Tag} -- tag or combination of tags to check
        '''
        return ((self.tag & tag) == tag)

    def bin_file(self, mode=BinFile.OpenMode.READ):
        '''Opens a binary file for the container

        Keyword Arguments:
            mode {BinFile.OpenMode} -- Open mode for underlying binary file
                                       (default: {BinFile.OpenMode.READ})

        Returns:
            [BinFile] -- New instance of binary file
        '''
        return BinFile(self.path, mode)
