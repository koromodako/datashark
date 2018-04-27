# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: workspace.py
#     date: 2018-04-27
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
from uuid import uuid4
from pathlib import Path
from slugify import slugify
from datetime import datetime
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, 'workspace')
# =============================================================================
#  CLASSES
# =============================================================================
class Workspace:
    '''Represents a Datashark workspace
    '''

    def __init__(self, name, log_dir, tmp_dir, dat_dir):
        '''Constructs an object

        Arguments:
            log_dir {Path} -- [description]
            tmp_dir {Path} -- [description]
            dat_dir {Path} -- [description]
        '''
        self.name = name
        self.slug = slugify(name)
        self.uuid = uuid4()
        self.timestamp = datetime.now().isoformat()
        self.log_dir = log_dir if isinstance(log_dir, Path) else Path(log_dir)
        self.tmp_dir = tmp_dir if isinstance(tmp_dir, Path) else Path(tmp_dir)
        self.dat_dir = dat_dir if isinstance(dat_dir, Path) else Path(dat_dir)
