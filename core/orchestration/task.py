# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     file: task.py
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
from time import time
from enum import Enum
from uuid import uuid4
from core.hash.hash import Hash
from helper.exception import InvalidPluginTypeException
from helper.logging.logger import Logger
from core.container.container import Container
from core.dissection.dissector import Dissector
from core.examination.examiner import Examiner
from core.plugin.plugin_selector import PluginSelector
# =============================================================================
#  GLOBALS
# =============================================================================
LGR = Logger(Logger.Category.CORE, __name__)
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

    def __str__(self):
        return "TaskResult(task={},data={})".format(self.task, self.data)

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
        EXIT = 'exit'
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
        self.priority = self._set_priority()
        self.start_time = None
        self.stop_time = None
        self.succeeded = None

    def __str__(self):
        return "Task(uuid={},category={},priority={},container={})".format(self.uuid,
                                                                           self.category,
                                                                           self.priority,
                                                                           self.container)

    def __lt__(self, other):
        '''Comparison operator is defined on priority: lowest priority first
        '''
        return (self.priority < other.priority)

    @property
    def execution_time(self):
        '''[summary]
        '''
        return self.stop_time - self.start_time

    def _set_priority(self):
        '''[summary]
        '''
        priority = 1

        if self.category == Task.Category.EXIT:
            priority = 2
        elif self.category == Task.Category.ABORT:
            priority = 0

        return priority

    def _perform_hashing(self):
        '''[summary]
        '''
        ## Note:
        ##    no need to check plugin as it is not really a plugin
        LGR.info("Hash computation begins for {}".format(self.container))
        return Hash(self.container)

    def _perform_dissection(self):
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

        LGR.info("Dissection begins for {}".format(self.container))
        return self.plugin.dissect(self.container)

    def _perform_examination(self):
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

        LGR.info("Examination begins for {}".format(self.container))
        return self.plugin.examine(self.container)

    def _perform_examiner_selection(self):
        '''[summary]
        '''
        ## Note:
        ##    no need to check if this plugin is initialized as it is not
        ##    really a plugin
        LGR.info("Examiner selection begins for {}".format(self.container))
        return PluginSelector.select_examiners_for(self.container)

    def _perform_dissector_selection(self):
        '''[summary]
        '''
        ## Note:
        ##    no need to check if this plugin is initialized as it is not
        ##    really a plugin
        LGR.info("Dissector selection begins for {}".format(self.container))
        return PluginSelector.select_dissectors_for(self.container)

    def perform(self):
        '''Generator of results

        Generates results from underlying computation task
        '''
        try:

            self.start_time = time()

            if self.category == Task.Category.HASHING:
                yield TaskResult(self, self._perform_hashing())

            elif self.category == Task.Category.DISSECTION:
                for container in self._perform_dissection():
                    yield TaskResult(self, container)

            elif self.category == Task.Category.EXAMINATION:
                yield TaskResult(self, self._perform_examination())

            elif self.category == Task.Category.EXAMINER_SELECTION:

                if self.container.has_tag(Container.Tag.BLACKLISTED|Container.Tag.WHITELISTED):
                    yield TaskResult(self, None)

                yield TaskResult(self, self._perform_examiner_selection())

            elif self.category == Task.Category.DISSECTOR_SELECTION:

                if self.container.has_tag(Container.Tag.BLACKLISTED|Container.Tag.WHITELISTED):
                    yield TaskResult(self, None)

                yield TaskResult(self, self._perform_dissector_selection())

            self.succeeded = True

        except Exception as e:
            LGR.exception("An exception occured while performing a task. "
                          "Details below.")
            self.succeeded = False

        finally:
            self.stop_time = time()
