# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: orchestrator.py
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
from asyncio import PriorityQueue, QueueEmpty, Queue, sleep
from core.hash.hash import Hash
from helper.logging.logger import Logger
from core.orchestration.task import Task
from core.container.container import Container
from core.orchestration.worker_pool import WorkerPool
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class Orchestrator:
    '''Orchestrator class

    Create tasks and hand them over to a pool of instances of Worker.

    It will consume results as they arrive to inject them back into processing
    queue or store them as final results.
    '''
    def __init__(self,
                 conf,
                 hash_db,
                 container_db,
                 whitelist_db,
                 blacklist_db,
                 dissection_db,
                 examination_db):
        '''Constructs the object
        '''
        self.conf = conf

        self.hash_db = hash_db
        self.container_db = container_db
        self.whitelist_db = whitelist_db
        self.blacklist_db = blacklist_db
        self.dissection_db = dissection_db
        self.examination_db = examination_db

        self.qin = PriorityQueue()
        self.qout = Queue()
        self.aborted = False
        self.worker_group = None

    async def _process_hashing_result(self, result):
        '''Treats all hashing result as final results and persist them into
        given database
        '''
        if not isinstance(result.data, Hash):
            raise RuntimeError("result.data must be a Hash instance here!")

        if self.conf.check_black_or_white:

            if self.blacklist_db.retrieve(result.data) is not None:
                result.data.container.add_tag(Container.Tag.BLACKLISTED)

            elif self.whitelist_db.retrieve(result.data) is not None:
                result.data.container.add_tag(Container.Tag.WHITELISTED)

        await self.hash_db.persist(result.data)

    async def _process_dissection_result(self, result):
        '''Treats all dissection result as intermediary results and inject new
        "dissector selection" and "examiner selection" tasks into processing
        queue and persists container
        '''
        if not isinstance(result.data, Dissection):
            raise RuntimeError("result.data must be a Dissection instance here!")

        ds_task = Task(Task.Category.DISSECTOR_SELECTION,
                       self.conf.dissector_selector, result.data.container)

        await self.schedule_tasks([ds_task])

        if self.conf.dissect_and_examine:
            es_task = Task(Task.Category.EXAMINER_SELECTION,
                           self.conf.examiner_selector, result.data.container)

            await self.schedule_tasks([es_task])

        await self.dissection_db.persist(result.data)

    async def _process_examination_result(self, result):
        '''Treats all examination result as final results and persist them into
        given database
        '''
        if not isinstance(result.data, Examination):
            raise RuntimeError("result.data must be an Examination instance here!")

        await self.examination_db.persist(result.data)

    async def _process_examiner_selection_result(self, result):
        '''Adds examination tasks for each selected examiner

        Does nothing if no appropriate examiner was found
        '''
        if not isinstance(result.data, list):
            raise RuntimeError("result.data must be a list instance here!")

        exam_tasks = [Task(Task.Category.EXAMINATION,
                           examiner,
                           result.task.container) for examiner in result.data]

        await self.schedule_tasks(exam_tasks)

    async def _process_dissector_selection_result(self, result):
        '''Adds dissection tasks for each selected dissector

        Does nothing if no appropriate dissector was found
        '''
        if not isinstance(result.data, list):
            raise RuntimeError("result.data must be a list instance here!")

        diss_tasks = [Task(Task.Category.DISSECTION,
                           dissector,
                           result.task.container) for dissector in result.data]

        await self.schedule_tasks(diss_tasks)

    async def _process_result(self, result):
        '''Processes one result depending on task type
        '''
        LGR.debug("Processing one result: {}".format(result))

        task = result.task
        if task.category == Task.Category.HASHING:
            await self._process_hashing_result(result)

        elif task.category == Task.Category.DISSECTION:
            await self._process_dissection_result(result)

        elif task.category == Task.Category.EXAMINATION:
            await self._process_examination_result(result)

        elif task.category == Task.Category.EXAMINER_SELECTION:
            await self._process_examiner_selection_result(result)

        elif task.category == Task.Category.DISSECTOR_SELECTION:
            await self._process_dissector_selection_result(result)

    @property
    def processing(self):
        return (self.worker_group is not None)

    async def abort(self):
        '''Aborts tasks processing
        '''
        LGR.debug("Processing abortion requested.")
        self.aborted = True
        await self.worker_group

    async def schedule_tasks(self, tasks):
        '''Schedules more tasks for processing
        '''
        for task in tasks:
            LGR.debug("Pushing task into processing queue: {}".format(task))
            await self.qin.put(task)

            if not task.container.has_tag(Container.Tag.PERSISTED):
                LGR.debug("Persisting container: {}".format(task.container))
                await self.container_db.persist(task.container)
                task.container.add_tag(Container.Tag.PERSISTED)

    async def process_tasks(self):
        '''Processes all tasks until the input queue is empty or abort()
        is called
        '''
        self.aborted = False
        # create a worker pool
        async with WorkerPool(self.conf, self.qin, self.qout) as pool:
            # start workers
            LGR.debug("Starting workers in the pool.")
            await pool.start()
            # Note:
            #   process results until the queue is empty
            # Warning:
            #   this loop must not contain a blocking function call
            LGR.debug("Entering processing loop.")
            while True:

                if self.qin.empty() and self.qout.empty():
                    # everything has been consumed and no operation remains
                    # send EXIT tasks
                    LGR.debug("Exiting processing loop.")
                    await pool.exit()
                    break

                try:
                    result = self.qout.get_nowait()
                    await self._process_result(result)
                    self.qout.task_done()
                except QueueEmpty as e:
                    await sleep(0.1)

                if self.aborted:
                    LGR.debug("Abort processing loop.")
                    await pool.abort()
                    break

            # wait for workers' group to stop, this is a kind of join
            LGR.debug("Waiting for pool to terminate terminate workers.")
            await pool.join()
