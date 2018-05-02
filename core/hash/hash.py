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
from core.db.object import DBObject
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Hash(DBObject):
    '''Represents a hash result of a container

    Stores multiple hash values for a single container.
    '''
    INDEX = 'hash'
    FIELDS = [
        ('md5', DBObject.DataType.STRING),
        ('sha1', DBObject.DataType.STRING),
        ('sha_256', DBObject.DataType.STRING),
        ('sha3_256', DBObject.DataType.STRING),
        ('container_uuid', DBObject.DataType.STRING)
    ]
    PRIMARY = 'container_uuid'

    HASHES = ['MD5', 'SHA1', 'SHA-256', 'SHA3-256']

    def __init__(self, container=None):
        super().__init__()
        self._md5 = None
        self._sha1 = None
        self._sha_256 = None
        self._sha3_256 = None
        self._container = container
        self._container_uuid = container.uuid
        self._compute_hashes()

    @property
    def md5(self):
        return self._md5

    @property
    def sha1(self):
        return self._sha1

    @property
    def sha_256(self):
        return self._sha_256

    @property
    def sha3_256(self):
        return self._sha3_256

    @property
    def container_uuid(self):
        return self._container_uuid

    def _compute_hashes(self):
        result = Crypto.multihash(Hash.HASHES, self._container)
        (self._md5, self._sha1, self._sha_256, self._sha3_256) = result

    def _source(self):
        '''Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties of an object.

        Returns:
            {dict} -- [description]
        '''
        return {
            'md5': self._md5,
            'sha1': self._sha1,
            'sha_256': self._sha_256,
            'sha3_256': self._sha3_256,
            'container_uuid': self._container._source()['uuid']
        }

    def from_db(self, _source):
        '''Loads a document (dict) which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.

        Arguments:
            doc {dict} -- [description]
        '''
        self._md5 = _source['md5']
        self._sha1 = _source['sha1']
        self._sha_256 = _source['sha_256']
        self._sha3_256 = _source['sha3_256']
        self._container_uuid = UUID(_source['container_uuid'])
