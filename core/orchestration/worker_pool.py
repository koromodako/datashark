# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: worker_pool.py
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
from asyncio import gather, PriorityQueue, Queue
from helper.logging.logger import Logger
from core.orchestration.task import Task
from core.orchestration.worker import Worker
from core.orchestration.local_worker import LocalWorker
from core.orchestration.remote_worker import RemoteWorker
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class WorkerPool:
    '''WorkerPool class

    Represents a pool of workers.
    '''
    def __init__(self, conf, qin, qout):
        '''Constructs the object

        Arguments:
            category {WorkerPool.Category} -- [description]
            max_workers {int} -- [description]
            qin {asyncio.PriorityQueue} -- [description]
            qout {asyncio.Queue} -- [description]
            configuration {Configuration} -- [description]
        '''
        self.conf = conf
        self.qin = qin
        self.qout = qout
        self.workers = []
        self.workers_coro = None

    async def __aenter__(self):
        '''Context Manager async enter method
        '''
        await self.allocate()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        '''Context Manager async exit method

        Arguments:
            See Context Manager documentation
        '''
        if exc_type:
            LGR.exception("An exception occured within caller with statement.")
        await self.free()

    async def allocate(self):
        '''Allocates workers to be used by the pool
        '''
        if not isinstance(self.qin, PriorityQueue):
            raise RuntimeError("asyncio.PriorityQueue expected here!")

        if not isinstance(self.qout, Queue):
            raise RuntimeError("asyncio.Queue expected here!")

        self.workers = []

        category = self.conf.worker_category
        if category == Worker.Category.LOCAL:
            worker_cls = LocalWorker
        elif category == Worker.Category.REMOTE:
            worker_cls = RemoteWorker
        else:
            ValueError("Configuration value for worker_category does not "
                       "match any known value: {}".format(category))

        for k in range(self.conf.max_workers):

            worker = worker_cls(k,
                                self.conf,
                                self.qin,
                                self.qout)

            await worker.initialize()
            self.workers.append(worker)

    async def free(self):
        '''Frees workers used by the pool
        '''
        for worker in self.workers:
            await worker.terminate()
        self.workers = []

    async def start(self):
        '''Starts workers in the pool
        '''
        LGR.debug("Starting workers...")
        coros = [worker.do_work() for worker in self.workers]
        self.workers_coro = gather(*coros)
        LGR.debug("Workers started.")

    async def exit(self):
        '''Notify workers to exit normally.

        Inject as many EXIT tasks as workers in the pool into processing queue
        to notify them that they have to exit normally.
        '''
        LGR.debug("Injecting EXIT tasks...")
        for _ in self.workers:
            await self.qin.put(Task(Task.Category.EXIT, None, None))
        LGR.debug("EXIT tasks injected.")

    async def abort(self):
        '''Notify workers to abort on next task.

        Inject as many ABORT tasks as workers in the pool into processing queue
        to notify them that they have to exit normally.
        '''
        LGR.debug("Injecting ABORT tasks...")
        for _ in self.workers:
            await self.qin.put(Task(Task.Category.ABORT, None, None))
        LGR.debug("ABORT tasks injected.")

    async def join(self):
        '''Gives worker the order to start consuming tasks
        '''
        LGR.debug("Waiting workers to stop...")
        await self.workers_coro
        LGR.debug("Workers stopped.")
