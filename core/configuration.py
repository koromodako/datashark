# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: configuration.py
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
from munch import munchify
from ruamel.yaml import safe_load, safe_dump
from helper.wrapper import lazy
# =============================================================================
#  CLASSES
# =============================================================================
class Configuration:
    """[summary]

    [description]

    Extends:
        Munch
    """
    def __init__(self, path):
        """[summary]

        Arguments:
            path {Path} -- [description]
        """
        self.path = path
        self._conf = None

    @property
    @lazy
    def conf(self):
        """[summary]

        [description]

        Decorators:
            lazy

        Returns:
            [type] -- [description]
        """
        return munchify(self._conf)

    def load(self):
        """[summary]

        [description]

        Returns:
            bool -- [description]
        """
        try:
            with self.path.open() as f:
                self._conf = safe_load(f)
            return True
        except Exception as e:
            return False

    def save(self):
        """[summary]

        [description]

        Returns:
            bool -- [description]
        """
        try:
            with self.path.open() as f:
                safe_dump(f, self._conf)
            return True
        except Exception as e:
            return False
