# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: table.py
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
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================

class Table:
    '''Represents a printable ASCII table
    '''

    def __init__(self, cols=[]):
        '''Constructs the object

        Keyword Arguments:
            cols {list(Column)} -- [description] (default: {[]})
        '''
        self.cols = cols
        self.clen = len(cols)
        self.rows = []
        self.max_width_per_col = [0 for i in range(self.clen)]

    def add_row(self, row):
        '''Add a row

        Arguments:
            row {[type]} -- [description]

        Returns:
            bool -- [description]
        '''
        if len(row) != self.clen:
            LGR.error("incomplete row (row element count and col count "
                      "mismatch) => row ignored.")
            return False

        for i in range(self.clen):

            row[i] = self.cols[i].format(row[i])

            elen = len(row[i])
            if elen > self.max_width_per_col[i]:
                self.max_width_per_col[i] = elen

        self.rows.append(row)
        return True

    def print(self, print_header=True):
        '''Prints the table with or without table's header

        Keyword Arguments:
            print_header {bool} -- [description] (default: {True})
        '''
        rows = self.rows

        if print_header:
            row = []
            for i in range(self.clen):
                name = self.cols[i].name
                nlen = len(name)

                row.append(name)

                if nlen > self.max_width_per_col[i]:
                    self.max_width_per_col[i] = nlen

            rows = [row] + rows

        for row in rows:
            line = ""
            for i in range(self.clen):
                line += self.cols[i].align(row[i], self.max_width_per_col[i])
            print(line)
