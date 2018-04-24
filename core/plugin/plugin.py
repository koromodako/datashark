# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plugin.py
#     date: 2018-03-25
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
from enum import Enum
from slugify import slugify
from helper.logging.logger import Logger
# =============================================================================
#  CLASSES
# =============================================================================
class Plugin:
    '''Generic Datashark plugin

    Interface for a generic Datashark plugin
    '''

    class Type(Enum):
        '''Describe the type of plugin

        Extends:
            Enum
        '''
        DRIVER = 'driver'
        PARSER = 'parser'
        EXAMINER = 'examiner'
        DISSECTION = 'dissection'
        DB_CONNECTOR = 'db_connector'

    def __init__(self, type, name):
        '''Constructs a new instance

        Arguments:
            type {Plugable.Type} -- Plugin's type
            name {str} -- Plugin's name
        '''
        super(Plugable, self).__init__()
        self.type = type
        self.name = name
        self.slug = slugify(name)
        self.logger = Logger(Logger.Type.PLUGIN, '{}.{}'.format(type, slug))
        self._instance = None

    def __str__(self):
        return "Plugin(type={},name={},slug={})".format(self.type,
                                                        self.name,
                                                        self.slug)

    async def init(self, gconf, pconf):
        '''Initializes the plugin

        Datashark framework ensure that this operation is called and is
        the first operation called on a plugin instance.

        1. This method shall import all modules needed to initialize
           self.instance.
        2. This method shall initialize self.instance.

        Arguments:
            gconf {dict} -- Global configuration
            pconf {dict} -- Plugin-specific configuration
        '''
        raise NotImplementedError("Plugin subclasses must implement init()")

    async def term(self):
        '''Terminates the plugin

        Datashark framework ensure that this operation is called and is
        the last operation called on a plugin instance.

        1. This method shall perform all cleaning operations relative to
           self.instance.
        '''
        raise NotImplementedError("Plugin subclasses must implement term()")
