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
from asyncio import PriorityQueue, Queue
from helper.logging.logger import Logger
from core.orchestration.task import Task
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
    def __init__(self, conf):
        '''Constructs the object
        '''
        self.conf = conf
        self.tq_out = Queue()
        self.tpq_in = PriorityQueue()
        self.aborted = False
        self.worker_group = None

    async def _process_hashing_result(self, result):
        '''Treats all hashing result as final results and persist them into
        given database
        '''
        if not isinstance(result.data, Hash):
            raise RuntimeError("result.data must be a Hash instance here!")

        self.conf.hash_db.persist(result.data)

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

        self.conf.dissection_db.persist(result.data)

    async def _process_examination_result(self, result):
        '''Treats all examination result as final results and persist them into
        given database
        '''
        if not isinstance(result.data, Examination):
            raise RuntimeError("result.data must be an Examination instance here!")

        self.conf.examination_db.persist(result.data)

    async def _process_examiner_selection_result(self, result):
        '''Adds examination tasks for each selected examiner

        Does nothing if no appropriate examiner was found
        '''
        if not isinstance(result.data, list):
            raise RuntimeError("result.data must be a list instance here!")

        await self.schedule_tasks([Task(Task.Category.EXAMINATION,
                                        examiner,
                                        result.task.container) for examiner in result.data])

    async def _process_dissector_selection_result(self, result):
        '''Adds dissection tasks for each selected dissector

        Does nothing if no appropriate dissector was found
        '''
        if not isinstance(result.data, list):
            raise RuntimeError("result.data must be a list instance here!")

        await self.schedule_tasks([Task(Task.Category.DISSECTION,
                                        dissector,
                                        result.task.container) for dissector in result.data])

    async def _process_result(self, task, result):
        '''Processes one result depending on task type
        '''
        LGR.debug("Processing one result from {}".fromat(task))

        if task.category == Task.Category.HASHING:
            await self._process_hashing_result(task, result)

        elif task.category == Task.Category.DISSECTION:
            await self._process_dissection_result(task, result)

        elif task.category == Task.Category.EXAMINATION:
            await self._process_examination_result(task, result)

        elif task.category == Task.Category.EXAMINER_SELECTION:
            await self._process_examiner_selection_result(task, result)

        elif task.category == Task.Category.DISSECTOR_SELECTION:
            await self._process_dissector_selection_result(task, result)

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
            LGR.debug("Pushing {} into processing queue.".format(task))
            await self.tpq_in.put(task)

    async def process_tasks(self):
        '''Processes all tasks until the input queue is empty or abort()
        is called
        '''
        self.aborted = False
        # create a worker pool
        async with WorkerPool(self.tpq_in, self.tq_out, self.conf) as pool:
            # start workers
            self.worker_group = await pool.perform_tasks()
            # process results till the queue is empty
            while True:
                LGR.debug("Waiting for a result to come...")
                result = await self.tq_out.get()

                if result is None:
                    LGR.debug("Result is None, breaking out of result loop")
                    break

                await self._process_result(result)

                self.tq_out.task_done()

                if self.aborted:
                    LGR.debug("Abort processing.")
                    await pool.abort()
            # wait for workers' group to stop
            await self.worker_group
            self.worker_group = None
