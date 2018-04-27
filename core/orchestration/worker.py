# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: worker.py
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
from helper.logging.logger import Logger
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, 'worker')
# =============================================================================
#  CLASSES
# =============================================================================
class Worker:
    '''Worker class

    Receives tasks from Orchestrator and perform them until completion or an
    internal exception is raised and returns the result.
    '''
    def __init__(self, num, configuration=None):
        '''Constructs the object
        '''
        self.num = num
        self.tasks = None
        self.configuration = configuration

    async def _perform_tasks(self):
        '''Worker starts performing tasks asynchronously

        Subclasses must override this method.

        This method shall yield (task, result) tuples.
        '''
        raise NotImplementedError("Worker subclasses must implement "
                                  "_perform_tasks() method.")

    async def perform_tasks(self, tasks):
        '''Worker starts performing tasks asynchronously
        '''
        self.tasks = tasks
        async for task, result in self._perform_tasks():
            yield (task, result)
