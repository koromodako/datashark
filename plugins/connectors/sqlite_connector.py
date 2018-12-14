# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: sqlite_connector.py
#     date: 2018-04-30
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
from pathlib import Path
from aiosqlite3 import connect
from core.db.object import DBObject
from core.db.connector import DatabaseConnector
# =============================================================================
#  CLASSES
# =============================================================================
class SQLiteConnector(DatabaseConnector):
    '''SQLiteConnector

    Connects to a SQLite database
    '''
    TYPE_MAPPING = {
        DBObject.DataType.INT: 'INTEGER',
        DBObject.DataType.BOOL: 'INTEGER',
        DBObject.DataType.BYTES: 'BLOB',
        DBObject.DataType.FLOAT: 'REAL',
        DBObject.DataType.STRING: 'TEXT'
    }

    def __init__(self, conf, read_only):
        '''Constructs the object
        '''
        super().__init__(conf, read_only)
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
            self.logger.warning("called on an opened connection!")
            return False

        try:
            Path(self.conf.path).parent.joinpath('perm-test.ds').touch()
        except Exception as e:
            self.logger.error("cannot write {} due to invalid permissions!".format(
                              self.conf.path))
            return False

        uri = 'file:{}'.format(self.conf.path)
        if self.read_only:
            uri += '?mode=ro'

        self.conn = await connect(uri, uri=True)
        return True

    async def disconnect(self):
        '''Closes underlying connection
        '''
        if not self._is_connected():
            self.logger.warning("called on a closed connection!")
            return

        await self.conn.close()
        self.conn = None

    async def _table_exists(self, obj):
        '''Checks if table exists
        '''
        query = "SELECT * FROM sqlite_master "
        query += "WHERE name='{}' ".format(obj['_meta']['index'])
        query += "AND type='table';"

        self.logger.debug("Querying database: {}".format(query))
        async with self.conn.cursor() as cursor:
            await cursor.execute(query)
            r = await cursor.fetchall()

        return (len(r) != 0)

    async def _create_table(self, obj):
        '''Creates the table if it does not exist
        '''
        query = "CREATE TABLE IF NOT EXISTS {}(".format(obj['_meta']['index'])
        for name, data_type in obj['_meta']['fields']:
            query += "{} {}, ".format(name,
                                      SQLiteConnector.TYPE_MAPPING[data_type])
        query = query[:-2] + ");"

        self.logger.debug("Querying database: {}".format(query))
        async with self.conn.cursor() as cursor:
            await cursor.execute(query)

    async def _insert_one(self, obj):
        '''Inserts a single object into the database

        Notes:
            it might be interesting to optimize the execution inserting
            multiple records in a single call
        '''
        query = "INSERT INTO {} VALUES (".format(obj['_meta']['index'])
        for _, value in obj['_source'].items():
            query += "'{}', ".format(value)
        query = query[:-2] + ");"

        self.logger.debug("Querying database: {}".format(query))
        async with self.conn.cursor() as cursor:
            await cursor.execute(query)

    async def persist(self, objects):
        '''Inserts a DBObject into underlying database creating a table if
        needed

        Notes:
            it might be interesting to optimize the execution inserting
            multiple records in a single call
        '''
        if not self._is_connected():
            self.logger.warning("persist() called on a closed connection!")
            return False

        for obj in objects:
            if not await self._table_exists(obj):
                await self._create_table(obj)
            await self._insert_one(obj)

        await self.conn.commit()

    async def retrieve(self, query):
        '''Retrieves an object from the database using given query
        '''
        if not self._is_connected():
            self.logger.warning("retrieve() called on a closed connection!")
            return False
        self.logger.todo("implement SQLiteConnector.retrieve) method.")
