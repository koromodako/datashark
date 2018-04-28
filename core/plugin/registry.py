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
        '''[summary]

        [description]

        Arguments:
            arg {[type]} -- [description]
        '''
        super(Registry, self).__init__()
        self._plugins = {}

    def register(self, category, instance_cls):
        '''Registers a plugin

        Arguments:
            plugin {Plugin} -- Plugin instance to be registered
        '''
        plugin = Plugin(category, instance_cls)

        if Plugin.Category not in self._plugins:
            self._plugins[plugin.category] = {}

        # register an instance of the plugin
        self._plugins[plugin.category][plugin.name] = plugin

    def plugins(self, type=None, name=None):
        '''[summary]

        Arguments:
            type {Plugin.Category} -- [description]

        Returns:
            dict or None -- [description]
        '''
        if type is None:
            return self._plugins

        plugins = self._plugins.get(type)

        if name is None:
            return plugins

        if plugins is None:
            return None

        return plugins.get(name)

    def plugin_instance(self, type, name, conf):
        '''Returns a plugin

        Arguments:
            type {Plugin.Category} -- [description]
            name {str} -- [description]

        Returns:
            Plugin or None -- [description]
        '''
        plugin = self._plugins.get(type, {}).get(name)

        if plugin is None:
            return None

        return plugin.instance(conf)
