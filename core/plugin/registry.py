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

    def register(self, plugin):
        '''Registers a plugin

        Arguments:
            plugin {Plugin} -- Plugin instance to be registered
        '''
        if plugin.type not in self._plugins:
            self._plugins[plugin.type] = {}
        self._plugins[plugin.type][plugin.slug] = plugin

    def plugins(self, type=None):
        '''[summary]

        Arguments:
            type {Plugin.Type} -- [description]

        Returns:
            dict or None -- [description]
        '''
        if not type:
            return self._plugins
        return self._plugins.get(type)

    def plugin(self, type, slug):
        '''Returns a plugin

        Arguments:
            type {Plugin.Type} -- [description]
            slug {str} -- [description]

        Returns:
            Plugin or None -- [description]
        '''
        return self._plugins.get(type, {}).get(slug)
