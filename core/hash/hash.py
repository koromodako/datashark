# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: hash.py
#     date: 2018-04-27
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
from helper.crypto import Crypto
from core.db.object import DatabaseObject
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Hash(DatabaseObject):
    '''Represents a hash result of a container

    Stores multiple hash values for a single container.
    '''
    INDEX = 'hash'
    FIELDS = [
        ('md5', DatabaseObject.FieldType.STRING),
        ('sha1', DatabaseObject.FieldType.STRING),
        ('sha_256', DatabaseObject.FieldType.STRING),
        ('sha3_256', DatabaseObject.FieldType.STRING),
    ]

    def __init__(self, container=None):
        self.md5 = None
        self.sha1 = None
        self.sha_256 = None
        self.sha3_256 = None
        self.container = container
        self._compute_hashes()

    def _compute_hashes(self, container):
        hash_names = ['MD5', 'SHA1', 'SHA-256', 'SHA3-256']
        result = Crypto.multihash(hash_names, self.container)
        (self.md5, self.sha1, self.sha_256, self.sha3_256) = result

    def _source(self):
        '''Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties of an object.

        Returns:
            {dict} -- [description]
        '''
        return {
            'md5': self.md5,
            'sha1': self.sha1,
            'sha_256': self.sha_256,
            'sha3_256': self.sha3_256,
            'container': self.container._source()
        }

    def from_db(self, _source):
        '''Loads a document (dict) which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.

        Arguments:
            doc {dict} -- [description]
        '''
        self.md5 = _source['md5']
        self.sha1 = _source['sha1']
        self.sha_256 = _source['sha_256']
        self.sha3_256 = _source['sha3_256']
