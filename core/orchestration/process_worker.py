# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: process_worker.py
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
from core.orchestration.worker import Worker
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class ProcessWorker(Worker):
    '''ProcessWorker class

    Represents a worker executing locally in a separate process
    '''
        async def initialize(self):
        '''Performs initialization of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to False
            2. return True on success, False otherwise
        '''
        self.terminated = False
        return True

    async def terminate(self):
        '''Performs cleanup of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to True
            2. return True on success, False otherwise
        '''
        self.terminated = True
        return True

    async def _perform_task(self, task):
        '''Performs task asynchronously

        Subclasses must override this method.

        This method shall:
            1. perform actual task work
            2. put (task,result) tuples in self.tq_out queue for further
               processing
        '''
        async for result in task.perform():
            await self.tq_out.put(result)
