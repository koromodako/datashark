# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: column.py
#     date: 2018-04-24
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
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================

class Column:
    '''Column definition for printable ASCII table
    '''

    class Alignment(Enum):
        '''Column's content alignment enumeration

        Variables:
            LEFT {int} -- [description]
            RIGHT {int} -- [description]
            CENTERED {int} -- [description]
        '''
        LEFT = 0
        RIGHT = 1
        CENTERED = 2

    def __init__(self, name=None, alignment=Alignment.LEFT, fmtr=None):
        '''Constructs the object

        Keyword Arguments:
            name {str} -- [description] (default: {None})
            alignment {Column.Alignment} -- [description] (default: {Alignment.LEFT})
            fmtr {function} -- [description] (default: {None})
        '''
        self.name = name
        if not isinstance(alignment, Column.Alignment):
            LGR.error("programmatical error: align argument must be an "
                      "instance of Column.Alignment.")
        self.alignment = alignment
        self.fmtr = fmtr

    def format(self, value):
        '''Returns value formatted using given fmtr or str()

        Arguments:
            value {Typing.Any} -- Value to be converted to its string
                                  representation

        Returns:
            str -- String representation of input value
        '''
        if self.fmtr is not None:
            value = self.fmtr(value)

        if not isinstance(value, str):
            value = str(value)

        return value

    def align(self, value, max_width):
        '''Add appropriate padding to respect alignment

        Arguments:
            value {str} -- Input string to be aligned
            max_width {int} -- Max width of the column

        Returns:
            str -- Aligned version of input value
        '''
        vlen = len(value)
        miss = (max_width - vlen + 2)

        if self.alignment == Column.Alignment.LEFT:
            value += miss * BS

        elif self.alignment == Column.Alignment.RIGHT:
            value = miss * BS + value

        elif self.alignment == Column.Alignment.CENTERED:
            value = (miss // 2) * BS + value + (miss // 2) * BS
            value += BS if (miss % 2) == 1 else ''

        else:
            LGR.error("invalid alignment value => defaulting to "
                      "Column.Alignment.NONE.")

        return value
