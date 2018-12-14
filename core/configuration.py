# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: configuration.py
#     date: 2018-04-03
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
from munch import Munch
from pathlib import Path
from ruamel.yaml import safe_load, safe_dump
from helper.wrapper import lazy
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Configuration(Munch):
    '''Represents a configuration set which can be saved to disk.
    '''
    @classmethod
    def load(cls, path):
        '''Loads a configuration from the disk

        Returns:
            Configuration or None -- [description]
        '''
        if path is None:
            # try multiple path in the following order
            paths = [
                Path().joinpath('datashark.yml'),
                Path.home().joinpath('datashark.yml'),
                Path('/etc/datashark/datashark.yml')
            ]
            for p in paths:
                if p.is_file():
                    path = p

        if path is None:
            # return an empty config
            return cls.fromDict({})

        try:

            with path.open('r') as f:
                conf = safe_load(f)
                conf = cls.fromDict(conf)
                conf.path = path
            return conf

        except Exception as e:
            LGR.exception("An exception occured while loading a configuration "
                          "from a YAML file. Details below.")
            return None

    def save(self):
        '''Writes the configuration to the disk

        [description]

        Returns:
            bool -- True if succeeds, False otherwise
        '''
        if 'path' not in self.keys():
            LGR.error("You must give a valid path to your configuration before"
                      " using save() method.")
            return False

        try:
            with self.path.open('w') as f:
                safe_dump(f, self.toDict())
            return True
        except Exception as e:
            LGR.exception("An exception occured while saving a configuration "
                          "to a YAML file. Details below.")
            return False

    def save_as(self, path):
        '''[summary]

        Arguments:
            path {[type]} -- [description]

        Returns:
            bool -- True if succeeds, False otherwise
        '''
        self.path = path
        return self.save()
