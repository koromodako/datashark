# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: object.py
#     date: 2018-04-02
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
from enum import Enum
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class DBObject:
    '''[summary]

    [description]
    '''
    EXPECTED_CONSTANTS = [
        'INDEX',
        'FIELDS',
        'PRIMARY'
    ]

    class DataType(Enum):
        '''DataType's type enumeration

        Variables:
            INT {str} -- [description]
            BOOL {str} -- [description]
            BYTES {str} -- [description]
            FLOAT {str} -- [description]
            STRING {str} -- [description]
        '''
        INT = 'int'
        BOOL = 'bool'
        BYTES = 'bytes'
        FLOAT = 'float'
        STRING = 'string'

    def _source(self):
        '''Creates dict which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties mapped with
        the appropriate field name

        All keys in the dict which are not declared in FIELDS class constant
        will not be persisted by DatabaseConnector subclasses.
        '''
        raise NotImplementedError("DBObject subclasses must implement "
                                  "_source() method.")

    def from_db(self, _source):
        '''Loads a dict which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.
        '''
        raise NotImplementedError("DBObject subclasses must implement "
                                  "from_db() method.")

    def to_db(self):
        '''Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties and metadata
        associated with an object.

        DBObject subclasses must define:
            + INDEX:    object name to be used as index/table name
            + FIELDS:   object fields in source with associated DBObject.DataType
            + PRIMARY:  object primary field (unique key)
        '''
        for constant in DBObject.EXPECTED_CONSTANTS:
            if not constant in dir(self):
                raise ValueError("DBObject must define the following class "
                                 "constants: {}".format(DBObject.EXPECTED_CONSTANTS))

        return {
            '_meta': {
                'index': self.INDEX,
                'fields': self.FIELDS,
                'primary': self.PRIMARY
            },
            '_source': self._source()
        }
