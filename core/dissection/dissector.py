# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: dissector.py
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
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================

class Dissector(Plugin):
    '''Dissector

    Represents a dissector, i.e. an object able to extract containers from a
    parent container. This object will use one to several parsers to extract
    all "sub-containers" contained by given container.
    '''
    def __init__(self, name):
        '''Constructs an object

        Arguments:
            name {str} -- Dissector unique name
        '''
        super().__init__(Plugin.Type.DISSECTOR, name)

    def supported_mime_types(self):
        '''Gives a list of MIME types which can be handled by this dissector
        '''
        return self._instance.supported_mime_types()

    def can_dissect(self, container):
        '''Checks if dissection can be performed

        Checks if underlying dissector instance is able to perform a dissection
        of this container.

        Arguments:
            container {Container} -- Container to check for dissection
                                     compatibility
        '''
        return self._instance.can_dissect(container)

    async def containers(self, container):
        '''Extract containers from given container

        Performs the dissection of the container.

        Arguments:
            container {Container} -- Container to dissect
        '''
        async for container in self._instance.containers(container):
            yield container
