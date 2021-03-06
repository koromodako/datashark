# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: logger.py
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
from sys import stderr
from enum import Enum
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO, ERROR
from logging.handlers import RotatingFileHandler
from helper.logging.coloring_formatter import ColoringFormatter
# =============================================================================
#  CLASSES
# =============================================================================
class Logger:
    '''Wrapper around logging.Logger hiding underlying logger interface and
    adding useful things
    '''
    class Category(Enum):
        '''Logger's category enumeration

        Variables:
            CORE {str} -- [description]
            PLUGIN {str} -- [description]
        '''
        CORE = 'core'
        PLUGIN = 'plugin'

    ROOT_LOGGER = getLogger('datashark')
    OPT_DEBUG = True
    OPT_SILENT = False
    LOGFILE_FMT = '(%(asctime)s)[%(levelname)s]{%(process)d:%(name)s} - %(message)s'
    CONSOLE_FMT = '[%(levelname)s]{%(process)d:%(name)s} - %(message)s'

    @staticmethod
    def configure(log_dir,
                  debug=True,
                  silent=False,
                  logfile_fmt=None,
                  console_fmt=None):

        Logger.OPT_DEBUG = debug
        Logger.OPT_SILENT = silent
        Logger.LOGFILE_FMT = logfile_fmt or Logger.LOGFILE_FMT
        Logger.CONSOLE_FMT = console_fmt or Logger.CONSOLE_FMT

        Logger.ROOT_LOGGER.setLevel(DEBUG)

        log_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

        error_hdlr = RotatingFileHandler(str(log_dir.joinpath('datashark.error.log')),
                                         maxBytes=10*1024*1024,
                                         backupCount=5)
        error_hdlr.setFormatter(Formatter(fmt=Logger.LOGFILE_FMT))
        error_hdlr.setLevel(ERROR)
        Logger.ROOT_LOGGER.addHandler(error_hdlr)

        info_hdlr = RotatingFileHandler(str(log_dir.joinpath('datashark.info.log')),
                                        maxBytes=10*1024*1024,
                                        backupCount=5)
        info_hdlr.setFormatter(Formatter(fmt=Logger.LOGFILE_FMT))
        info_hdlr.setLevel(DEBUG if Logger.OPT_DEBUG else INFO)
        Logger.ROOT_LOGGER.addHandler(info_hdlr)

        if not Logger.OPT_SILENT:
            console_hdlr = StreamHandler(stream=stderr)
            console_hdlr.setFormatter(ColoringFormatter(fmt=Logger.CONSOLE_FMT))
            Logger.ROOT_LOGGER.addHandler(console_hdlr)

    def __init__(self, category, name):
        '''[summary]

        [description]

        Arguments:
            category {[type]} -- [description]
            name {[type]} -- [description]
        '''
        if '.' in name:
            name = name.split('.')[-1]

        if name == '__main__':
            self.name = 'datashark.{}'.format(name)
        else:
            self.name = 'datashark.{}.{}'.format(category, name)
        self._logger = getLogger(self.name)

    def debug(self, msg, *args, **kwargs):
        '''cf. logging.Logger.debug
        '''
        if Logger.OPT_DEBUG:
            self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        '''cf. logging.Logger.info
        '''
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        '''cf. logging.Logger.warning
        '''
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        '''cf. logging.Logger.error
        '''
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        '''cf. logging.Logger.critical
        '''
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        '''cf. logging.Logger.exception
        '''
        self._logger.exception(msg, *args, **kwargs)

    def todo(self, task, no_raise=False):
        '''Display a TODO message raises NotImplementedError depending on
        no_raise argument value.

        Arguments:
            task {str} -- [description]

        Keyword Arguments:
            no_raise {bool} -- [description] (default: {False})
        '''
        msg = "not implemented. Contribute! TODO: {}".format(task)

        if no_raise:
            self._logger.warning(msg)
        else:
            raise NotImplementedError(msg)
