# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: memory_map.py
#     date: 2018-04-23
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
from helper.formatting.formatter import Formatter
# =============================================================================
#  GLOBALS / CONFIG
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================

class MemoryMap:
    '''Memory map class

    Represents a memory map of N units mapped from a BinFile.
    '''
    def __init__(self, bf, start, size, unit=1):
        '''Constructs the object.

        If you want a memory map of sectors (512 bytes), just use unit=512.

        Arguments:
            bf {BinFile} -- underlying BinFile
            start {int} -- Offset within the BinFile (in units)
            size {[type]} -- Size of the map (in units)

        Keyword Arguments:
            unit {int} -- Size of a unit in bytes (default: {1})
        '''
        super(MemoryMap, self).__init__()
        self._bf = bf
        self.start = start
        self.size = size
        self.unit = unit
        self.type = type

    def read_one(self, idx):
        '''Reads one unit from the memory map

        Arguments:
            idx {int} -- Index of the unit to read, 0-based.

        Returns:
            bytes -- A buffer having a size of at most <unit>.
        '''
        if idx >= self.size:
            LGR.warn("reading after end of map => None returned.")
            return None

        return self._bf.read(self.unit,
                             self.unit * (self.start + idx))

    def read_many(self, indices):
        '''Reads many, possible not contiguous, units from the memory map

        Arguments:
            indices {list(int)} -- List of indices

        Yields:
            bytes -- [description]
        '''
        for idx in indices:
            yield self.read_one(idx)

    def read_all(self):
        '''Reads all the memory map.

        Be careful not to load to many data in memory.

        Returns:
            bytes -- Full memory map data
        '''
        return self._bf.read(self.unit * self.size,
                             self.unit * self.start)

    def __str__(self):
        '''String representation of the object
        '''
        unit = Formatter.format_size(self.unit)
        return 'MemoryMap(start={},size={},unit={})'.format(self.start,
                                                            self.size,
                                                            unit)

