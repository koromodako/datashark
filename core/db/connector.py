# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: database_connector.py
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
from core.plugin.plugin import PluginInstance, Plugin
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class DatabaseConnector(PluginInstance):
    '''DatabaseConnector class

    Represents a generic connection with a database. It defines an interface.
    '''
    def __init__(self, conf, read_only):
        '''Constructs the object

        Arguments:
            conf {Configuration} -- [description]
        '''
        super().__init__(conf)
        self.read_only = read_only

    def __str__(self):
        '''String representation of the object
        '''
        return "DatabaseConnector(name={})".format(self.name)

    async def connect(self):
        '''Connects the program to the database
        '''
        raise NotImplementedError("DatabaseConnector subclasses must implement"
                                  " connect() method.")

    async def disconnect(self):
        '''Disconnects the program from database closing all underlying
        sessions if any.
        '''
        raise NotImplementedError("DatabaseConnector subclasses must implement"
                                  " disconnect() method.")

    async def persist(self, objects):
        '''Persists an object into the database

        Arguments:
            objects {DBObject} -- Dict or list of dicts representing
                                        object(s) to be created or updated an
                                        object.
        Returns:
            {bool} - True if persitence succeeded, False otherwise
        '''
        raise NotImplementedError("DatabaseConnector subclasses must implement"
                                  " persist() method.")

    async def retrieve(self, query):
        '''Retrieves an object from the database

        Arguments:
            query {dict} -- Dict representation of a query which can be
                            interpreted by the underlying database connector
                            subclass to retrieve an object.
        Returns:
            {list} - list of dicts being retrieved objects
        '''
        raise NotImplementedError("DatabaseConnector subclasses must implement"
                                  " retrieve() method.")

