# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: registry.py
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
from core.plugin.plugin import Plugin
from helper.logging.logger import Logger
from helper.formatting.formatter import Formatter
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Registry:
    '''[summary]

    [description]
    '''
    def __init__(self):
        '''Constructs the object
        '''
        super(Registry, self).__init__()
        self._plugins = {}

    def print_list(self):
        '''Prints a human readable list of plugins
        '''
        print("Loaded plugins: ", end='')
        Formatter.pretty_print(self._plugins, 1)

    def register(self, category, instance_cls):
        '''Registers a plugin

        Arguments:
            plugin {Plugin} -- Plugin instance to be registered
        '''
        plugin = Plugin(category, instance_cls)

        if plugin.category not in self._plugins:
            self._plugins[plugin.category] = {}

        # register an instance of the plugin
        self._plugins[plugin.category][plugin.name] = plugin

    def plugins(self, category):
        '''[summary]

        [description]

        Arguments:
            category {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        return self._plugins.get(category).items()

    def instanciate(self, category, name, conf):
        '''Returns a plugin instance

        Arguments:
            category {Plugin.Category} -- [description]
            name {str} -- [description]

        Returns:
            Plugin or None -- [description]
        '''
        plugin = self._plugins.get(category, {}).get(name)

        if plugin is None:
            LGR.error("Failed to find a plugin matching given constraints: "
                      "(category={},name={})".format(category, name))
            return None

        return plugin.instance(conf)
