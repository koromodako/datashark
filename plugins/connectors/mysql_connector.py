# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: mysql_connector.py
#     date: 2018-05-01
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
from aiomysql import create_pool
from core.db.connector import DatabaseConnector
# =============================================================================
#  CLASSES
# =============================================================================
class MySQLConnector(DatabaseConnector):
    '''MySQLConnector

    Connects to a MySQL database
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
            self.logger.warning("connect() called on an opened connection!")
            return False
        self.logger.todo("implement MySQLConnector.connect() method.")

    async def disconnect(self):
        '''Closes underlying connection
        '''
        if not self._is_connected():
            self.logger.warning("disconnect() called on a closed connection!")
            return
        self.logger.todo("implement MySQLConnector.disconnect() method.")

    async def persist(self, objects):
        '''[summary]

        [description]
        '''
        if not self._is_connected():
            self.logger.warning("persist() called on a closed connection!")
            return False
        self.logger.todo("implement MySQLConnector.persist() method.")

    async def retrieve(self, query):
        '''[summary]

        [description]
        '''
        if not self._is_connected():
            self.logger.warning("retrieve() called on a closed connection!")
            return False
        self.logger.todo("implement MySQLConnector.retrieve) method.")
