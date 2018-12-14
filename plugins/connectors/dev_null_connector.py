# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: dev_null_connector.py
#     date: 2018-04-28
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
from core.db.connector import DatabaseConnector
# =============================================================================
#  CLASSES
# =============================================================================
class DevNullConnector(DatabaseConnector):
    '''DevNullConnector

    Connects DB to nothing, everything is dropped.

    1. Calling retrieve on this connector raises a RuntimeException,
    2. calling all other methods is a equivalent to a nop.
    '''

    def __init__(self, conf):
        '''Constructs the object
        '''
        super().__init__(conf)

    def __str__(self):
        return str(super())

    async def connect(self):
        '''This is a nop.
        '''
        pass

    async def disconnect(self):
        '''This is a nop.
        '''
        pass

    async def persist(self, objects):
        '''This is a nop.
        '''
        pass

    async def retrieve(self, query):
        '''Calling this method is not allowed.
        '''
        raise RuntimeError("Calling retrieve on a DevNullConnector is "
                           "nonsense.")
