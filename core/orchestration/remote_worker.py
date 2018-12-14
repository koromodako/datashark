# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: remote_worker.py
#     date: 2018-04-27
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
from helper.logging.logger import Logger
from core.orchestration.worker import Worker
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class RemoteWorker(Worker):
    '''RemoteWorker class

    Represents a worker distributed on a cluster of servers
    '''
    async def initialize(self):
        '''Performs initialization of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to False
            2. return True on success, False otherwise
        '''
        LGR.todo("implement RemoteWorker.initialize()!")

    async def terminate(self):
        '''Performs cleanup of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to True
            2. return True on success, False otherwise
        '''
        LGR.todo("implement RemoteWorker.terminate()!")

    async def _perform_task(self, task):
        '''Performs task asynchronously

        Subclasses must override this method.

        This method shall:
            1. perform actual task work
            2. put (task,result) tuples in self.qout queue for further
               processing
        '''
        LGR.todo("implement RemoteWorker._perform_task()!")
