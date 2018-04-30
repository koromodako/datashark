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
from core.plugin.plugin import PluginInstance, Plugin
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Examiner(PluginInstance):
    '''Examiner class

    Represents an object able to perform consistency/compliance checks on
    several elements of a container. These elements includes the following:
        * compliance with file format specifications, if there is any
        * consistency of data in terms of security (ex: integrity of records
          of a SQLite database or a Windows registry file)
        * and other things specific to some formats
    '''
    def __init__(self, conf):
        '''Constructs an object

        Arguments:
            conf {Configuration} -- [description]
        '''
        super().__init__(conf)

    def supported_mime_types(self):
        '''Gives a list of MIME types which can be handled by this examiner
        '''
        raise NotImplementedError("Examiner subclasses must implement "
                                  "supported_mime_types() method.")

    def can_examine(self, container):
        '''Checks if examination can be performed

        Checks if underlying examiner instance is able to perform an
        examination of this container.

        Arguments:
            container {Container} -- Container to check for examination
                                     compatibility
        '''
        raise NotImplementedError("Examiner subclasses must implement "
                                  "can_examine() method.")

    async def examine(self, container):
        '''Examine a container

        Performs the examination of the container.

        Arguments:
            container {Container} -- Container to examine
        '''
        raise NotImplementedError("Examiner subclasses must implement "
                                  "examine() method.")
