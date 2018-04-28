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
from enum import Enum
from asyncio import get_event_loop
from helper.logging.logger import Logger
from core.orchestration.task import Task
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Worker:
    '''Worker class

    Receives tasks from Orchestrator and perform them until completion or an
    internal exception is raised and returns the result.
    '''
    class Category(Enum):
        '''Worker's category enumeration

        Variables:
            CLUSTER {str} -- [description]
            PROCESS {str} -- [description]
        '''
        CLUSTER = 'cluster'
        PROCESS = 'process'

    def __init__(self, num, tpq_in, tq_out, executor, configuration):
        '''Constructs the object
        '''
        self.num = num
        self.tpq_in = tpq_in
        self.tq_out = tq_out
        self.executor = executor
        self.configuration = configuration
        self.terminated = None

    async def initialize(self):
        '''Performs initialization of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to False
            2. return True on success, False otherwise
        '''
        raise NotImplementedError("Worker subclasses must implement "
                                  "initialize() method.")

    async def terminate(self):
        '''Performs cleanup of the worker if needed

        Subclasses must override this method.

        This method shall:
            1. set self.terminated to True
            2. return True on success, False otherwise
        '''
        raise NotImplementedError("Worker subclasses must implement "
                                  "terminate() method.")

    async def _perform_task(self, task):
        '''Performs task asynchronously

        Subclasses must override this method.

        This method shall:
            1. perform actual task work
            2. put (task,result) tuples in self.tq_out queue for further
               processing
        '''
        raise NotImplementedError("Worker subclasses must implement "
                                  "_perform_task() method.")

    async def do_work(self):
        '''Worker starts consuming tasks asynchronously
        '''
        LGR.debug("Worker n°{}: entering working loop...".format(self.num))
        while True:
            task = await self.tpq_in.get()

            if self.terminated:
                LGR.debug("Worker n°{}: terminated.".format(self.num))
                break

            if task is None:
                LGR.debug("Worker n°{}: no more task to process.".format(self.num))
                break

            if task.category == Task.Category.ABORT:
                LGR.debug("Worker n°{}: aborting.".format(self.num))
                break

            loop = get_event_loop()
            await loop.run_in_executor(self.executor, self._perform_task, task)

            LGR.debug("Worker n°{}: task completed.".format(self.num))
            self.tpq_in.task_done()

        LGR.debug("Worker n°{}: leaving working loop.".format(self.num))

