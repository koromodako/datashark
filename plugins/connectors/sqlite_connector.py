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
        super().__init__(conf, 'sqlite')

    def __str__(self):
        return str(super())

    async def connect(self):
        '''[summary]

        [description]
        '''
        self.logger.todo("implement SQLiteConnector.connect() method.")

    async def disconnect(self):
        '''[summary]

        [description]
        '''
        self.logger.todo("implement SQLiteConnector.disconnect() method.")

    async def persist(self, objects):
        '''[summary]

        [description]
        '''
        self.logger.todo("implement SQLiteConnector.persist() method.")

    async def retrieve(self, query):
        '''[summary]

        [description]
        '''
        self.logger.todo("implement SQLiteConnector.retrieve) method.")

    async def delete(self, query):
        '''[summary]

        [description]
        '''
        self.logger.todo("implement SQLiteConnector.delete() method.")
