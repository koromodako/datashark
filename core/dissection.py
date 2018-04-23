# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: dissection.py
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
from uuid import UUID, uuid4
from pathlib import Path
from slugify import slugify
from core.db.object import DatabaseObject
# =============================================================================
#  CLASSES
# =============================================================================
class Dissection(DatabaseObject):
    """[summary]

    [description]
    """
    def __init__(self,
                 parent=None,
                 path=None,
                 original_path=None,
                 name=None):
        super(Dissection, self).__init__()
        self.parent = parent
        self.path = path
        self.original_path = original_path
        self.slug = slugify(name)
        # computed once
        self.uuid = uuid4()
        self.size = None
        if self.path is not None:
            stat = self.path.stat()
            self.size = stat.st_size

    def from_db(self, doc):
        """Loads a document (dict) which is returned by any DatabaseConnector

        Loads all persistent properties of an object from a dict.

        Arguments:
            doc {dict} -- [description]
        """
        self.parent =
        self.path =
        self.original_path =
        self.slug =
        self.uuid = UUID()
        self.stat =

    def to_db(self):
        """Creates a document (dict) which can be used by any DatabaseConnector

        Creates a dict which contains all persistent properties of an object.

        Returns:
            {dict} -- [description]
        """
        raise NotImplementedError("DatabaseObject subclasses must implement "
                                  "to_db() method.")


