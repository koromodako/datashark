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
from concurrent.futures import ProcessPoolExecutor
from helper.logging.logger import Logger
from core.orchestration.process_worker import ProcessWorker
from core.orchestration.cluster_worker import ClusterWorker
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, 'worker_pool')
# =============================================================================
#  CLASSES
# =============================================================================
class WorkerPool:
    '''WorkerPool class

    Represents a pool of workers.
    '''
    class Type(Enum):
        '''WorkerPool's types enumeration

        Variables:
            CLUSTER {str} -- [description]
            PROCESS {str} -- [description]
        '''
        CLUSTER = 'cluster'
        PROCESS = 'process'

    def __init__(self, type, max_workers, tpq_in, tq_out, configuration):
        '''Constructs the object

        Arguments:
            type {WorkerPool.Type} -- [description]
            max_workers {int} -- [description]
            tpq_in {asyncio.PriorityQueue} -- [description]
            tq_out {asyncio.Queue} -- [description]
            configuration {Configuration} -- [description]
        '''
        self.type = type
        self.max_workers = max_workers
        self.tpq_in = tpq_in
        self.tq_out = tq_out
        self.workers = []
        self.executor = ProcessPoolExecutor(max_workers=max_workers)
        self.configuration = configuration

    async def allocate(self):
        '''Allocates workers to be used by the pool
        '''
        if not isinstance(self.tpq_in, PriorityQueue):
            raise RuntimeError("asyncio.PriorityQueue expected here!")

        if not isinstance(self.tq_out, Queue):
            raise RuntimeError("asyncio.Queue expected here!")

        self.workers = []

        if self.type == WorkerPool.Type.PROCESS:
            worker_cls = ProcessWorker
        elif self.type == WorkerPool.Type.CLUSTER:
            worker_cls = ClusterWorker

        for k in range(self.size):

            worker = worker_cls(k,
                                self.tpq_in,
                                self.tq_out,
                                self.configuration)

            await worker.initialize()
            self.workers.append(worker)

    async def free(self):
        '''Frees workers used by the pool
        '''
        for worker in self.workers:
            await worker.terminate()
        self.workers = []

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

    def __enter__(self):
        '''Context Manager enter method
        '''
        raise RuntimeError("You must use 'async with' statement with the "
                           "worker pool.")

    def __exit__(self,  exc_type, exc_value, traceback):
        '''Context Manager exit method
        '''
        raise RuntimeError("You must use 'async with' statement with the "
                           "worker pool.")

    async def abort(self):
        '''Notify workers to finish currrent task and abort on the next one.

        Inject abort tasks into IN Priority Queue to notify workers that they
        must abort execution.
        '''
        for worker in self.workers:
            self.tpq_in.put((0, Task(Task.Category.ABORT, None, None)))

    async def perform_tasks(self):
        '''Gives worker the order to start consuming tasks
        '''
        LGR.debug("Starting workers...")
        workers_group = gather([worker.do_work() for worker in self.workers])
        LGR.debug("Done starting workers.")
        return workers_group
