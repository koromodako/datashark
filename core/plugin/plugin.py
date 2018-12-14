# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: plugin.py
#     date: 2018-03-25
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
from slugify import slugify
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Plugin:
    '''Generic Datashark plugin

    Interface for a generic Datashark plugin
    '''

    class Category(Enum):
        '''Plugin's category enumeration
        '''
        EXAMINER = 'examiner'
        DISSECTOR = 'dissector'
        DB_CONNECTOR = 'db_connector'

    def __init__(self, category, instance_cls):
        '''Constructs a new instance

        Arguments:
            category {Plugable.Type} -- Plugin's category
            name {str} -- Plugin's name
        '''
        self.category = category
        self.name = instance_cls.__name__
        self.instance_cls = instance_cls

    def __str__(self):
        return "Plugin(category={},instance_cls={})".format(self.category,
                                                            self.instance_cls)

    def instance(self, conf, **kwargs):
        '''Plugin instance factory

        Datashark framework ensure that this operation is called and is
        the first operation called on a plugin instance.

        1. This method shall import all modules needed to initialize
           self._instance.
        2. This method shall initialize self._instance.

        Arguments:
            conf {Configuration} -- Configuration
        '''
        return self.instance_cls(conf, **kwargs)

class PluginInstance:
    '''[summary]
    '''
    def __init__(self, conf):
        '''Constructs the object

        Arguments:
            conf {Configuration} -- [description]
            name {str} -- [description]
        '''
        self.conf = conf
        self.logger = Logger(Logger.Category.PLUGIN,
                             self.__class__.__name__)
