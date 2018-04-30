# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: bin_file.py
#     date: 2018-04-23
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
from io import SEEK_SET
from enum import Enum
from pathlib import Path
from helper.memory_map import MemoryMap
from helper.logging.logger import Logger
from helper.formatting.formatter import Formatter
# =============================================================================
#  GLOBALS / CONFIG
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class BinFile:
    '''Represents a regular file accessible in binary mode only
    '''

    class OpenMode(Enum):
        '''BinFile's open modes enumeration
        '''
        READ = 'r'
        WRITE = 'w'
        CREATE = 'x'
        APPEND = 'a'

    @staticmethod
    def exists(path):
        '''Test if given path exists and is a regular file

        Arguments:
            path {Path} -- path of the file to test

        Returns:
            bool -- True if the file exists and is a regular file, False
                    otherwise
        '''
        return path.is_file()

    def __init__(self, path, mode=OpenMode.READ):
        '''Constructs an object

        Arguments:
            path {[type]} -- [description]
            mode {[type]} -- [description]
        '''
        self.fp = None
        self.path = path if isinstance(path, Path) else Path(path)
        self.mode = BinFile.OpenMode(mode)
        self.dirname = path.parent
        self.basename = path.name
        self.rlvpath = path.resolve()

    def __enter__(self):
        '''Context manager __enter__ to enable the use of "with" statement

        Returns:
            BinFile -- Instance of binary file
        '''
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Context manager __exit__ to enable the use of "with" statement

        Arguments:
            exc_type {[type]} -- [description]
            exc_value {[type]} -- [description]
            traceback {[type]} -- [description]
        '''
        if exc_type:
            LGR.exception("An exception occured within caller with statement.")
        self.close()

    def is_valid(self):
        '''
        '''
        return (self.fp is not None)

    def open(self):
        '''[summary]

        Returns:
            bool -- [description]
        '''
        if self.fp is not None:
            LGR.warning("File is already opened: {}".format(self))
            return False

        try:
            self.fp = self.path.open(self.mode+'b')
        except Exception as e:
            LGR.exception("File open operation failed: {}".format(self))
            self.fp = None
            return False

        return True

    def close(self):
        '''[summary]

        Returns:
            bool -- [description]
        '''
        if self.fp is None:
            LGR.warning("File is already closed: {}".format(self))
            return False

        self.fp.close()
        self.fp = None
        return True

    def stat(self):
        '''[summary]

        Returns:
            [type] -- [description]
        '''
        return self.path.stat()

    def size(self):
        '''[summary]

        Returns:
            [type] -- [description]
        '''
        return self.stat().st_size

    def seek(self, offset, whence=SEEK_SET):
        '''[summary]

        Arguments:
            offset {[type]} -- [description]

        Keyword Arguments:
            whence {[type]} -- [description] (default: {io.SEEK_SET})

        Returns:
            [type] -- [description]
        '''
        return self.fp.seek(offset, whence)

    def read_text(self, size=-1, seek=None, encoding='utf-8'):
        '''[summary]

        Keyword Arguments:
            size {number} -- [description] (default: {-1})
            seek {[type]} -- [description] (default: {None})
            encoding {str} -- [description] (default: {'utf-8'})

        Returns:
            [type] -- [description]
        '''
        return self.read(n, seek).decode(encoding)

    def read(self, size=-1, seek=None):
        '''[summary]

        Keyword Arguments:
            size {number} -- [description] (default: {-1})
            seek {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        '''
        if isinstance(seek, int):
            self.seek(seek)
        return self.fp.read(size)

    def readinto(self, b):
        '''[summary]

        Arguments:
            b {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        return self.fp.readinto(b)

    def write_text(self, text, encoding='utf-8'):
        '''[summary]

        Arguments:
            text {[type]} -- [description]

        Keyword Arguments:
            encoding {str} -- [description] (default: {'utf-8'})

        Returns:
            [type] -- [description]
        '''
        return self.fp.write(text.encode(encoding))

    def write(self, data):
        '''[summary]

        Arguments:
            data {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        return self.fp.write(data)

    def flush(self):
        '''Flushes file buffers to disk

        Note:
            Disk cache might still buffer this data
        '''
        self.fp.flush()

    def mmap(self, start, size, unit=1):
        '''[summary]

        Arguments:
            start {int} -- Start offset (in units)
            size {int} -- Size to map from start (in units)

        Keyword Arguments:
            unit int -- Number of bytes in a single unit (default: {1})

        Returns:
            MemoryMap -- returns a memory map
        '''
        return MemoryMap(self, start, size, unit)

    def dump(self, size=-1, seek=None):
        '''Prints an hexdump of `size` bytes from `seek` offset.

        Usage:
            bf = BinFile()
            print(bf.dump(size=512,seek=512))

        Keyword Arguments:
            size {int} -- Size of the dump (in bytes) (default: {-1})
            seek {int or None} -- Start offset of the dump (in bytes)
                                  (default: {None})

        Returns:
            str -- Printable hexdump
        '''
        return Formatter.hexdump(self.read(size, seek))
