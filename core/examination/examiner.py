# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: examiner.py
#     date: 2018-04-24
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

class Examiner(Plugin):
    '''[summary]

    [description]

    Extends:
        Plugin
    '''
    def __init__(self, name):
        '''[summary]

        [description]

        Arguments:
            name {[type]} -- [description]
        '''
        super().__init__(Plugin.Type.EXAMINER, name)

    def supported_mime_types(self):
        '''[summary]

        [description]
        '''
        return self._instance.supported_mime_types()

    def can_examine(self, container):
        '''[summary]

        [description]

        Arguments:
            container {[type]} -- [description]
        '''
        return self._instance.can_examine(container)

    async def examine(self, container):
        '''[summary]

        [description]

        Arguments:
            container {[type]} -- [description]
        '''
        return await self._instance.examine(container)
