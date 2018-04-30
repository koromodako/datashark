# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: sqlite_connector.py
#     date: 2018-04-30
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
from sqlite3 import connect
from core.db.connector import DatabaseConnector
# =============================================================================
#  CLASSES
# =============================================================================
class SQLiteConnector(DatabaseConnector):
    '''SQLiteConnector

    Connects to a SQLite database
    '''
    def __init__(self, conf):
        '''Constructs the object
        '''
        super().__init__(conf)
        self.conn = None

    def __str__(self):
        '''String representation of the object
        '''
        return str(super())

    def _is_connected(self):
        '''Returns true if underlying connection is opened, False otherwise
        '''
        return (self.conn is not None)

    async def connect(self):
        '''Opens underlying connection
        '''
        if self._is_connected():
            LGR.warning("connect() called on an opened connection!")
            return False

        self.conn = connect(self.conf.path)
        return True

    async def disconnect(self):
        '''Closes underlying connection
        '''
        if not self._is_connected():
            LGR.warning("disconnect() called on a closed connection!")
            return

        self.conn.close()
        self.conn = None

    async def persist(self, objects):
        '''[summary]

        [description]
        '''
        if not self._is_connected():
            LGR.warning("persist() called on a closed connection!")
            return False
        self.logger.todo("implement SQLiteConnector.persist() method.")

    async def retrieve(self, query):
        '''[summary]

        [description]
        '''
        if not self._is_connected():
            LGR.warning("retrieve() called on a closed connection!")
            return False
        self.logger.todo("implement SQLiteConnector.retrieve) method.")

    async def delete(self, query):
        '''[summary]

        [description]
        '''
        if not self._is_connected():
            LGR.warning("delete() called on a closed connection!")
            return False
        self.logger.todo("implement SQLiteConnector.delete() method.")
