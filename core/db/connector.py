# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: database_connector.py
#     date: 2018-04-02
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
from core.plugin.plugin import Plugin
# =============================================================================
#  CLASSES
# =============================================================================
class DatabaseConnector(Plugin):
    '''DatabaseConnector class

    Represents a generic connection with a database. It defines an interface.
    '''
    def __init__(self, name):
        '''[summary]

        [description]

        Arguments:
            name {[type]} -- [description]
        '''
        super().__init__(Plugin.Type.DB_CONNECTOR, name)

    def __str__(self):
        return "DatabaseConnector(name={})".format(self.name)

    async def connect(self):
        '''[summary]

        [description]

        Returns:
            {bool} - True if conection succeeded, False otherwise
        '''
        return await self._instance.connect()

    async def disconnect(self):
        '''Disconnects the program from database closing all underlying
        sessions if any.

        [description]
        '''
        return await self._instance.disconnect()

    async def persist(self, objects):
        '''[summary]

        [description]

        Arguments:
            objects {DatabaseObject} -- Dict or list of dicts representing
                                        object(s) to be created or updated an
                                        object.
        Returns:
            {bool} - True if persitence succeeded, False otherwise
        '''
        return await self._instance.persit(objects)

    async def retrieve(self, query):
        '''[summary]

        [description]

        Arguments:
            query {dict} -- Dict representation of a query which can be
                            interpreted by the underlying database connector
                            subclass to retrieve an object.
        Returns:
            {list} - list of dicts being retrieved objects
        '''
        return await self._instance.retrieve(query)

    async def delete(self, query):
        '''[summary]

        [description]

        Arguments:
            query {dict} -- Dict representation of a query which can be
                            interpreted by the underlying database connector
                            subclass to delete one or more objects.
        Returns:
            {int} - Number of objects deleted.
        '''
        return await self._instance.delete(query)
