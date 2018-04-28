# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: win.py
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
from os import name
from helper.exception import LinuxSpecificFeatureException
from helper.exception import MSWindowsSpecificFeatureException
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, __name__)
WINDOWS = (name == 'nt')
# =============================================================================
#  FUNCTIONS
# =============================================================================
def assert_ms_windows(raise_exc=True, invert=False):
    if invert and WINDOWS and raise_exc:
        raise LinuxSpecificFeatureException("This feature can only be used on "
                                            "Linux.")

    if not WINDOWS and raise_exc:
        raise MSWindowsSpecificFeatureException("This feature can only be "
                                                "used on Windows.")

    assertion_result = (not WINDOWS) if invert else WINDOWS
    LGR.debug('assert_ms_windows(): {}'.format(assertion_result))
    return assertion_result
