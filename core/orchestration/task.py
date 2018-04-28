# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: task.py
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
from time import time
from enum import Enum
from uuid import uuid4
from core.hash import Hash
from helper.wrapper import lazy
from helper.exception import InvalidPluginTypeException
from helper.logging.logger import Logger
from core.dissection.examiner import Examiner
from core.dissection.dissector import Dissector
from core.plugin.plugin_selector import PluginSelector
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Type.CORE, __name__)
# =============================================================================
#  CLASSES
# =============================================================================
class TaskResult:
    '''Represents a task result
    '''
    def __init__(self, task, data):
        '''Constructs the object

        Arguments:
            task {Task} -- [description]
            data {Typing.Any} -- [description]
        '''
        self.task = task
        self.data = data

class Task:
    '''[summary]

    [description]
    '''
    class Category(Enum):
        '''[summary]

        Variables:
            ABORT {str} -- Tells the worker to end its execution
            HASHING {str} -- Hashing task
            DISSECTION {str} -- Dissection task
            EXAMINATION {str} -- Examination task
        '''
        ABORT = 'abort'
        HASHING = 'hashing'
        DISSECTION = 'dissection'
        EXAMINATION = 'examination'
        EXAMINER_SELECTION = 'examiner_selection'
        DISSECTOR_SELECTION = 'dissector_selection'

    def __init__(self, category, plugin, container):
        '''[summary]

        [description]

        Arguments:
            category {Task.Category} -- [description]
            plugin {Plugin} -- [description]
            container {Container} -- [description]
        '''
        self.uuid = uuid4()
        self.category = category
        self.plugin = plugin
        self.container = container
        self.priority = 0 if category == Task.Category.ABORT else 10
        self.start_time = None
        self.stop_time = None
        self.succeeded = None

    def __str__(self):
        return "Task(uuid={},category={},priority={})".format(self.uuid,
                                                              self.category,
                                                              self.priority)

    @property
    @lazy
    def execution_time(self):
        return self.stop_time - self.start_time

    async def perform_hashing(self):
        if not isinstance(self.plugin, Hash):
            raise InvalidPluginTypeException("Hashing task received an "
                                             "invalid plugin: "
                                             "{}".format(self.plugin))

        ## Note:
        ##    no need to check if this plugin is initialized as it is not
        ##    really a plugin

        return self.plugin.from_container(self.container)

    async def perform_dissection(self):
        '''Generator of Container instances

        Generates containers from given container
        '''
        if not isinstance(self.plugin, Dissector):
            raise InvalidPluginTypeException("Dissection task received an "
                                             "invalid plugin: "
                                             "{}".format(self.plugin))

        if not self.plugin.initialized:
            raise UninitializedPluginException("Uninitialized Dissector given "
                                               "to task.")

        async for container in self.plugin.containers(container):
            yield container

    async def perform_examination(self):
        '''Generator of Examination instances

        Generates containers from given container
        '''
        if not isinstance(self.plugin, Examiner):
            raise InvalidPluginTypeException("Examination task received an "
                                             "invalid plugin: "
                                             "{}".format(self.plugin))

        if not self.plugin.initialized:
            raise UninitializedPluginException("Uninitialized Examiner given "
                                               "to task.")

        return await self.plugin.examine(self.container)

    async def perform_examiner_selection(self):
        if not isinstance(self.plugin, PluginSelector):
            raise InvalidPluginTypeException("Examiner selection task "
                                             "received an invalid plugin: "
                                             "{}".format(self.plugin))

        ## Note:
        ##    no need to check if this plugin is initialized as it is not
        ##    really a plugin

        return self.plugin.select_examiners_for(self.container)

    async def perform_dissector_selection(self):
        if not isinstance(self.plugin, PluginSelector):
            raise InvalidPluginTypeException("Dissector selection task "
                                             "received an invalid plugin: "
                                             "{}".format(self.plugin))

        ## Note:
        ##    no need to check if this plugin is initialized as it is not
        ##    really a plugin

        return self.plugin.select_dissectors_for(self.container)

    async def perform(self):
        '''Generator of results

        Generates results from underlying computation task
        '''
        try:

            self.start_time = time()

            if self.category == Task.Category.HASHING:
                yield TaskResult(self, await self.perform_hashing())

            elif self.category == Task.Category.DISSECTION:
                async for container in self.perform_dissection():
                    yield TaskResult(self, container)

            elif self.category == Task.Category.EXAMINATION:
                yield TaskResult(self, await self.perform_examination())

            elif self.category == Task.Category.EXAMINER_SELECTION:
                yield TaskResult(self, await self.perform_examiner_selection())

            elif self.category == Task.Category.DISSECTOR_SELECTION:
                yield TaskResult(self, await self.perform_dissector_selection())

            self.succeeded = True

        except Exception as e:
            LGR.exception("An exception occured while performing a task. "
                          "Details below.")
            self.succeeded = False

        finally:
            self.stop_time = time()
