# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: database.py
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
from core.db.object import DBObject
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Database:
    '''[summary]

    [description]
    '''
    def __init__(self, connector):
        '''[summary]

        [description]

        Arguments:
            connector {DatabaseConnector} -- [description]
        '''
        self.connector = connector
        self.connected = False

    async def init(self):
        '''[summary]

        [description]
        '''
        self.connected = await self.connector.connect()
        return self.connected

    async def term(self):
        '''[summary]

        [description]
        '''
        await self.connector.disconnect()
        self.connected = False

    async def persist(self, objs):
        '''Persists one or more objects

        See DatabaseConnector.persist() for details
        '''
        if not isinstance(objs, list):
            objs = [objs]

        objects = []
        for obj in objs:
            if isinstance(obj, DBObject):
                objects.append(obj.to_db())
            else:
                raise ValueError("Database can only persists subclasses of "
                                 "DBObject instances.")

        return await self.connector.persist(objects)

    async def retrieve(self, query):
        '''Retrieves one or more objects

        See DatabaseConnector.retrieve() for details
        '''
        return await self.connector.retrieve(query)

    async def delete(self, query):
        '''Deletes one or more objects

        See DatabaseConnector.delete() for details
        '''
        return await self.connector.delete(query)
