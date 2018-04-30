# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: file_type_guesser.py
#     date: 2018-04-03
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
from magic import Magic
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class FileTypeGuesser:
    '''Guess file MIME type from content using a magic file'''
    def __init__(self, magic_file=None):
        '''[summary]

        [description]

        Keyword Arguments:
            magic_file {str} -- Magic database to use (default: {None})
        '''
        self.magic_file = magic_file

    def mime_text(self, path):
        '''Returns a textual description of the MIME type.

        Arguments:
            path {Path} -- Path of the file to analyze
        '''
        if not path.is_file():
            return None

        magic = Magic(magic_file=self.magic_file)
        return magic.from_file(str(path))

    def mime_type(self, path):
        '''Returns a MIME description of the MIME type.

        Arguments:
            path {Path} -- Path of the file to analyze
        '''
        if not path.is_file():
            return None

        magic = Magic(magic_file=self.magic_file, mime=True)
        return magic.from_file(str(path))

