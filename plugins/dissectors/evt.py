# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: evt.py
#     date: 2018-05-13
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
from core.dissection.dissector import Dissector
# =============================================================================
#  CLASSES
# =============================================================================
class EVTDissector(Dissector):
    '''EVTDissector
    '''
    def __init__(self, conf):
        '''Constructs an object

        Arguments:
            conf {Configuration} -- [description]
        '''
        super().__init__(conf)

    def supported_mime_types(self):
        '''Gives a list of MIME types which can be handled by this dissector
        '''
        self.logger.todo("implement EVTDissector.supported_mime_types() method.")

    def can_dissect(self, container):
        '''Checks if dissection can be performed

        Checks if underlying dissector instance is able to perform a dissection
        of this container.

        Arguments:
            container {Container} -- Container to check for dissection
                                     compatibility
        '''
        self.logger.todo("implement EVTDissector.can_dissect() method.")

    def containers(self, container):
        '''Extract containers from given container

        Performs the dissection of the container.

        Arguments:
            container {Container} -- Container to dissect
        '''
        self.logger.todo("implement EVTDissector.containers() method.")
