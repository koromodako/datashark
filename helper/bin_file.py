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
from pathlib import Path
from core.helper.memory_map import MemoryMap
from core.helper.logging.logger import Logger
from core.helper.formatting.formatter import Formatter
# =============================================================================
#  GLOBALS / CONFIG
# =============================================================================
LGR = Logger(Logger.Type.CORE, 'bin_file')
# =============================================================================
#  CLASSES
# =============================================================================
class BinFile(object):

    @staticmethod
    def exists(path):
        '''[summary]

        Arguments:
            path {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        return path.is_file()

    def __init__(self, path, mode):
        '''[summary]

        Arguments:
            path {[type]} -- [description]
            mode {[type]} -- [description]
        '''
        self.fp = None
        self.path = path if isinstance(path, Path) else Path(path)
        self.mode = mode
        self.dirname = path.parent
        self.basename = path.name
        self.rlvpath = path.resolve()

    def __enter__(self):
        '''[summary]

        Returns:
            [type] -- [description]
        '''
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''[summary]

        Arguments:
            exc_type {[type]} -- [description]
            exc_value {[type]} -- [description]
            traceback {[type]} -- [description]
        '''
        if exc_type:
            LGR.exception('an exception occured within caller with statement.')
        self.close()

    def is_valid(self):
        '''[summary]
        '''
        return (self.fp is not None)

    def open(self):
        '''[summary]

        Returns:
            bool -- [description]
        '''
        if self.fp is not None:
            LGR.warning("file is already opened.")
            return False

        try:
            self.fp = self.path.open(self.mode+'b')
        except Exception as e:
            LGR.exception("file open operation failed.")
            self.fp = None
            return False

        return True

    def close(self):
        '''[summary]

        Returns:
            bool -- [description]
        '''
        if self.fp is None:
            LGR.warning("file is already closed.")
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

    def seek(self, offset, whence=io.SEEK_SET):
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
        '''[summary]
        '''
        self.fp.flush()

    def mmap(self, start, size, unit=1):
        '''[summary]

        Arguments:
            start {[type]} -- [description]
            size {[type]} -- [description]

        Keyword Arguments:
            unit {number} -- [description] (default: {1})

        Returns:
            [type] -- [description]
        '''
        return MemoryMap(self, start, size, unit)

    def dump(self, size=-1, seek=None):
        '''[summary]

        Keyword Arguments:
            size {number} -- [description] (default: {-1})
            seek {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        '''
        return Formatter.hexdump(self.read(size, seek))