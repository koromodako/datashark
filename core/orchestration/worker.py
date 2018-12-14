# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: worker.py
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
            LOCAL {str} -- [description]
            REMOTE {str} -- [description]
        '''
        LOCAL = 'local'
        REMOTE = 'remote'

    def __init__(self, num, conf, qin, qout):
        '''Constructs the object
        '''
        self.num = num
        self.conf = conf
        self.qin = qin
        self.qout = qout
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
            2. put (task,result) tuples in self.qout queue for further
               processing
        '''
        raise NotImplementedError("Worker subclasses must implement "
                                  "_perform_task() method.")

    async def do_work(self):
        '''Worker starts consuming tasks asynchronously
        '''
        def debug(msg):
            LGR.debug("Worker n°{}: {}".format(self.num, msg))

        while True:
            debug("waiting for next task.")
            task = await self.qin.get()

            if self.terminated:
                debug("terminated.")
                break

            if task is None:
                debug("no more task to process.")
                break

            if task.category == Task.Category.ABORT:
                debug("aborting.")
                break

            if task.category == Task.Category.EXIT:
                debug("exiting.")
                break

            debug("processing next task: {}".format(task))
            await self._perform_task(task)

            debug("task completed.")
            self.qin.task_done()

        debug("leaving working loop.")

