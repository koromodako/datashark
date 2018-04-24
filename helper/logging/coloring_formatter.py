# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: coloring_formatter.py
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
from logging import Formatter
from termcolor import colored
from helper.ms import assert_ms_windows
# =============================================================================
#  GLOBALS
# =============================================================================
COLORED = True
if assert_ms_windows(raise_exc=False):
    COLORED = False
# =============================================================================
#  CLASSES
# =============================================================================
class ColoringFormatter(Formatter):
    '''[summary]

    [description]

    Extends:
        logging.Formatter

    Variables:
        COLORS {dict} -- [description]
    '''
    COLORS = {
        'DEBUG': 'green',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta'
    }

    def __init__(self, fmt=None, datefmt=None, style='%'):
        '''Constructs the object

        Keyword Arguments:
            fmt {[type]} -- [description] (default: {None})
            datefmt {[type]} -- [description] (default: {None})
            style {str} -- [description] (default: {'%'})
        '''
        super(ColoringFormatter, self).__init__(fmt, datefmt, style)

    def format(self, record):
        '''Colorize the log record

        Arguments:
            record {[type]} -- [description]

        Returns:
            [type] -- [description]
        '''
        os = super(ColoringFormatter, self).format(record)
        if COLORED:
            os = colored(os, self.__class__.COLORS[record.levelname])
        return os
