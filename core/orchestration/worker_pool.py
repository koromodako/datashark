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
from asyncio import ensure_future
from helper.logging.logger import Logger
from core.orchestration.thread_worker import ThreadWorker
from core.orchestration.process_worker import ProcessWorker
from core.orchestration.cluster_worker import ClusterWorker
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, 'worker_pool')
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def consume(worker, tasks):
    results = {}

    async for task, result in worker.perform_tasks(tasks):

        if task.uuid not in results:
            results[task.uuid] = {'task': task, 'results': []}

        result[task.uuid]['results'].append(result)

    return results
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
            THREAD {str} -- [description]
            CLUSTER {str} -- [description]
            PROCESS {str} -- [description]
        '''
        THREAD = 'thread'
        CLUSTER = 'cluster'
        PROCESS = 'process'

    def __init__(self, type, size, configuration):
        '''[summary]

        [description]

        Arguments:
            type {[type]} -- [description]
            size {[type]} -- [description]
            configuration {[type]} -- [description]
        '''
        self.type = type
        self.size = size
        self.workers = []
        self.configuration = configuration

    def allocate(self):
        '''[summary]

        [description]
        '''
        self.workers = []

        if self.type == WorkerPool.Type.THREAD:
            worker_cls = ThreadWorker
        elif self.type == WorkerPool.Type.PROCESS:
            worker_cls = ProcessWorker
        elif self.type == WorkerPool.Type.CLUSTER:
            worker_cls = ClusterWorker

        for k in range(self.size):
            worker = worker_cls(k, self.configuration[k])
            worker.initialize()
            self.workers.append(worker)

    def free(self):
        '''[summary]

        [description]
        '''
        for worker in self.workers:
            if worker.is_running():
                worker.cancel()
            worker.terminate()
        self.workers = []

    def __enter__(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [description]
        '''
        self.allocate()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        '''[summary]

        [description]

        Arguments:
            exc_type {[type]} -- [description]
            exc_value {[type]} -- [description]
            traceback {[type]} -- [description]
        '''
        if exc_type:
            LGR.exception("An exception occured within caller with statement.")
        self.free()

    async def perform_tasks(self, task_queue):
        '''[summary]

        [description]
        '''
        while True:
            task = task_queue.get()

            if task is None:
                break

            worker = self.workers[self.available_worker.pop()]
            coro = ensure_future(consume(worker, [task]))



def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = queue.Queue()
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
